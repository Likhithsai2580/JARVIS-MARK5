# JARVIS-MARK5

JARVIS-MARK5 is an advanced AI-powered assistant that combines various modules and functionalities to provide a comprehensive user experience. It's designed to be extensible, powerful, and user-friendly.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Modules](#modules)
  - [Perplexica](#perplexica)
  - [PowerPoint Generator](#powerpoint-generator)
  - [GitHub Integration](#github-integration)
  - [Local LLM Support](#local-llm-support)
  - [Multi-modal Interactions](#multi-modal-interactions)
- [Extending JARVIS-MARK5](#extending-jarvis-mark5)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- AI-powered search engine (Perplexica) for intelligent information retrieval
- Automated PowerPoint generation based on user prompts
- Comprehensive GitHub integration for seamless development workflows
- Local Large Language Model support for enhanced privacy and offline capabilities
- Multi-modal interactions supporting text, speech, and image inputs/outputs
- Extensible architecture allowing easy addition of new modules and functionalities
- Advanced natural language processing for complex query understanding
- Customizable user interface for personalized experiences

## Installation

1. Ensure you have Python 3.8+ installed on your system.

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/JARVIS-MARK5.git
   cd JARVIS-MARK5
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the configuration files as described in the [Configuration](#configuration) section.

## Configuration

### Main Configuration

Create a `config.json` file in the `config` directory with the following structure:

```json
{
    "OBJ_DETECTION_URL": "http://your-object-detection-service.com/api",
    "OCR_LINK": "http://your-ocr-service.com/api",
    "DEFAULT_LLM": "gpt-3.5-turbo",
    "USE_LOCAL_LLM": false,
    "LOCAL_LLM_URL": "http://localhost:8000",
    "ENABLE_SPEECH": true,
    "ENABLE_IMAGE_PROCESSING": true
}
```

Adjust the values according to your setup and preferences.

### API Keys

Create a `config.py` file in the root directory and add your API keys:

```python
groq_api = "your-groq-api-key"
openai_api = "your-openai-api-key"
github_token = "your-github-personal-access-token"
```

### Perplexica Configuration

For the Perplexica module, rename `sample.config.toml` to `config.toml` in the `backend/AI/Perplexica` directory and fill in the necessary fields:

```toml
[GENERAL]
PORT = 8888
SIMILARITY_MEASURE = "cosine"

[API_KEYS]
OPENAI = "your_openai_api_key"
GROQ = "your_groq_api_key"
ANTHROPIC = "your_anthropic_api_key"

[API_ENDPOINTS]
SEARXNG = "http://localhost:8080"
OLLAMA = "http://localhost:11434"
```

## Usage

To start JARVIS-MARK5:

1. Ensure all configurations are set up correctly.
2. Activate your virtual environment if not already active.
3. Run the main application:
   ```bash
   python jarvis.py
   ```

### Basic Commands

- To perform a search: "Search for [query]"
- To generate a PowerPoint: "Create a presentation about [topic]"
- To use GitHub features: "Clone repository [repo_name]" or "Create a new repository named [name]"
- To switch between text and voice input: "Enable voice input" or "Disable voice input"

## Modules

### Perplexica

Perplexica is an AI-powered search engine integrated into JARVIS-MARK5. It provides advanced search capabilities and can be used as a standalone application.

Key features:
- Semantic search using embeddings
- Integration with multiple search backends
- Customizable ranking algorithms

For more information on Perplexica, refer to the [Perplexica README](backend/AI/Perplexica/README.md).

### PowerPoint Generator

JARVIS-MARK5 includes a PowerPoint generation module that can create presentations based on user prompts.

Key features:
- Automatic content generation and structuring
- Customizable templates and styles
- Integration with image generation APIs for visuals

For more information on the PowerPoint generator, refer to the [PowerPointer README](backend/modules/Powerpointer/README.md).

### GitHub Integration

JARVIS-MARK5 provides various GitHub-related functionalities, including:

- Searching repositories
- Cloning repositories
- Uploading projects to GitHub
- Creating repositories
- Retrieving commits and issues

This integration allows for seamless development workflows directly from the JARVIS-MARK5 interface.

For more details on GitHub integration, refer to the [GitHub configuration file](extensions/config_all.json).

### Local LLM Support

JARVIS-MARK5 can be configured to use local Large Language Models for enhanced privacy and offline capabilities. This feature allows users to run language models on their own hardware, reducing reliance on external APIs.

To enable local LLM support:
1. Set up a local LLM server (e.g., using [LocalAI](https://github.com/go-skynet/LocalAI))
2. Update the `config.json` file with:
   ```json
   "USE_LOCAL_LLM": true,
   "LOCAL_LLM_URL": "http://localhost:8000"
   ```

### Multi-modal Interactions

JARVIS-MARK5 supports various input and output modalities:

- Text: Traditional text-based interactions
- Speech: Voice input and text-to-speech output
- Image: Image analysis and generation capabilities

To enable or disable specific modalities, adjust the settings in `config.json`.

## Extending JARVIS-MARK5

JARVIS-MARK5 is designed to be easily extensible. This section covers how to add existing extensions and develop new ones.

### Adding Existing Extensions

To add an existing extension to JARVIS-MARK5:

1. Navigate to the `extensions` directory:
   ```bash
   cd extensions
   ```

2. Clone or download the extension repository:
   ```bash
   git clone https://github.com/username/jarvis-extension-name.git
   ```

3. Install any required dependencies:
   ```bash
   pip install -r jarvis-extension-name/requirements.txt
   ```

4. Add the extension to the `config.json` file in the root directory:
   ```json
   {
     "extensions": [
       // ... other extensions ...
       "jarvis-extension-name"
     ]
   }
   ```

5. Restart JARVIS-MARK5 for the changes to take effect.

### Developing New Extensions

To develop a new extension for JARVIS-MARK5:

1. Create a new directory for your extension in the `extensions` folder:
   ```bash
   mkdir extensions/my-new-extension
   cd extensions/my-new-extension
   ```

2. Create the following files in your extension directory:
   - `__init__.py`: Main entry point for your extension
   - `config.json`: Configuration file for your extension
   - `README.md`: Documentation for your extension

3. In `__init__.py`, define your extension class:
   ```python
   from jarvis.core import Extension

   class MyNewExtension(Extension):
       def __init__(self, config):
           super().__init__(config)
           # Initialize your extension here

- Perplexica (AI-powered search engine)
- OpenAI (Large Language Models)
- Groq (API for querying knowledge graphs)
- Anthropic (AI-powered search engine)
- PyTorch (Deep learning framework)
- Transformers (Library for transformer models)
- PyGitHub (Python library for GitHub API)

We would like to thank the contributors and maintainers of these projects for their hard work and dedication.

## Troubleshooting

If you encounter any issues while using JARVIS-MARK5, please check the following:

1. Ensure all dependencies are correctly installed.
2. Verify that your configuration files are set up properly.
3. Check the logs for any error messages.

If you still face problems, please open an issue on our GitHub repository with a detailed description of the problem and steps to reproduce it.

## Contributing

We welcome contributions to JARVIS-MARK5! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear, descriptive messages.
4. Push your changes to your fork.
5. Submit a pull request to the main repository.

Please ensure your code adheres to our coding standards and include tests for new features.

## License

JARVIS-MARK5 is released under the MIT License. See the [LICENSE](LICENSE) file for details.