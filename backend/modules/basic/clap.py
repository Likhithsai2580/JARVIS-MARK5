import sounddevice as sd
import numpy as np
import torch
import torchaudio
import torchaudio.transforms as T
from torch import nn
from torchvision.transforms import Resize

class AudioClassifier(nn.Module):
    def __init__(self):
        super(AudioClassifier, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.fc1 = nn.Linear(32 * 64 * 64, 128)
        self.fc2 = nn.Linear(128, 2)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, 32 * 64 * 64)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

class ClapDetector:
    def __init__(self, model_path: str, threshold: float = 0.5):
        self.model = self.load_model(model_path)
        self.threshold = threshold

    def load_model(self, model_path: str) -> nn.Module:
        model = AudioClassifier()
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        model.eval()
        return model

    def transform_audio(self, audio_data: np.ndarray, sample_rate: int, n_mels: int = 128, n_fft: int = 400, hop_length: int = 200) -> torch.Tensor:
        waveform = torch.from_numpy(audio_data).float()
        mel_spectrogram = T.MelSpectrogram(
            sample_rate=sample_rate,
            n_fft=n_fft,
            win_length=n_fft,
            hop_length=hop_length,
            n_mels=n_mels,
        )(waveform)
        mel_spectrogram = Resize((256, 256))(mel_spectrogram)
        normalized_spec = (mel_spectrogram - mel_spectrogram.mean()) / mel_spectrogram.std()
        return normalized_spec.unsqueeze(0)

    def detect_clap(self, indata, frames, time, status):
        audio_data = indata[:, 0]
        sample_rate = 44100
        spec = self.transform_audio(audio_data, sample_rate)
        output = self.model(spec)
        _, predicted = torch.max(output.data, 1)
        if predicted.item() == 1:
            print("Clap detected!")
            return True
        return False

    def listen_for_claps(self):
        with sd.InputStream(callback=self.detect_clap):
            sd.sleep(1000)

def main_clap_exe():
    model_path = "path_to_your_model.pth"
    clap_detector = ClapDetector(model_path)
    print("waiting for clap")
    while True:
        if clap_detector.listen_for_claps():
            return True
