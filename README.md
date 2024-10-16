# JARVIS-MARK5

JARVIS-MARK5 is an advanced AI-powered assistant designed to combine multiple modules and functionalities for a comprehensive and versatile user experience. Inspired by Iron Man's JARVIS, this AI assistant integrates powerful tools such as GPT-4, Groq, and other LLMs, with features spanning automation, intelligent search, and multi-modal interactions. JARVIS-MARK5 is built with scalability in mind and can be extended and customized easily, making it ideal for developers, researchers, and enthusiasts who want to push the boundaries of AI-driven assistants.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
  - [Main Configuration](#main-configuration)
  - [API Keys](#api-keys)
  - [Perplexica Configuration](#perplexica-configuration)
  - [Database Configuration](#database-configuration)
- [Usage](#usage)
  - [Basic Commands](#basic-commands)
  - [Module Commands](#module-commands)
- [Modules](#modules)
  - [Perplexica](#perplexica)
  - [PowerPoint Generator](#powerpoint-generator)
  - [GitHub Integration](#github-integration)
  - [Multi-modal Interactions](#multi-modal-interactions)
- [Extending JARVIS-MARK5](#extending-jarvis-mark5)
  - [Adding Existing Extensions](#adding-existing-extensions)
  - [Developing New Extensions](#developing-new-extensions)
- [Advanced Features](#advanced-features)
  - [Natural Language Understanding](#natural-language-understanding)
  - [Real-time Data Analysis](#real-time-data-analysis)
  - [Task Automation](#task-automation)
- [Performance Optimization](#performance-optimization)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
  - [Code Style](#code-style)
  - [Testing](#testing)
- [Roadmap](#roadmap)
- [FAQ](#frequently-asked-questions)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

JARVIS-MARK5 offers a wide range of features:

- **AI-powered Search Engine**: The Perplexica module, integrated with GPT-4 and Groq, for intelligent and context-aware information retrieval.
- **Automated PowerPoint Generator**: Generates presentations based on natural language input.
- **GitHub Integration**: Seamless integration for interacting with GitHub repositories (cloning, creating, committing, etc.).
- **Multi-modal Interactions**: Supports text, speech, and image-based interactions.
- **Extensible Architecture**: Easily add new modules or modify existing ones to suit your needs.
- **Natural Language Processing (NLP)**: Advanced capabilities to understand and process complex user queries.
- **Real-time Data Analysis & Visualization**: Analyze data and generate real-time insights and visual representations.
- **Customizable UI**: Personalize the user interface to suit individual preferences and workflows.
- **Voice Recognition and Text-to-Speech**: Switch between voice and text input/output seamlessly.
- **Cross-platform Compatibility**: Runs on Windows, macOS, and Linux.
- **IoT and API Integration**: Integrate with third-party APIs and smart devices.
- **Enhanced Classification Algorithm**: More sophisticated logic for classification tasks.
- **Optimized Tools**: Improved performance and efficiency of existing tools.
- **New Features**: Additional functionalities to enhance user experience.

## Installation

To install JARVIS-MARK5, follow these steps:

1. **Ensure Python 3.8+ is installed**:
   Make sure that you have the correct version of Python installed by running:
   ```bash
   python --version
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/Likhithsai2580/JARVIS-MARK5.git
   cd JARVIS-MARK5
   ```

3. **Create and activate a virtual environment**:
   On Linux/macOS:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure settings**: Set up your configuration files as described in the [Configuration](#configuration) section below.

6. **(Optional) Install additional features**:
   To install extra dependencies for specific modules, run:
   ```bash
   pip install -r requirements-extra.txt
   ```

---

## Configuration

### Main Configuration

The core configuration file for JARVIS-MARK5 is `config.json`, located in the `config` directory. This file contains basic settings and can be customized based on your requirements.

Here is an example `config.json` structure:
```json
{
    "OCR_LINK": "http://your-ocr-service.com/api",
    "GROQ_API": "YOUR_GROQ_API_KEY"
}
```

Update the `OCR_LINK` with the appropriate OCR service and provide your Groq API key.

### API Keys

Many of JARVIS-MARK5’s functionalities require API keys, such as for OpenAI and Groq. Ensure that you have signed up for these services and obtained API keys. You will then need to include them in the respective configuration files, as described in the section for each module.

### Perplexica Configuration

The Perplexica module is the AI-powered search engine within JARVIS-MARK5. To configure Perplexica:

1. Rename `sample.config.toml` to `config.toml` in `backend/AI/Perplexica`.
2. Edit the file to include your API keys and preferences:

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

### Database Configuration

JARVIS-MARK5 uses PostgreSQL to store conversation history and other data persistently. 

#### PostgreSQL Setup

1. **Install PostgreSQL**: Make sure PostgreSQL is installed and running.
2. **Create a database**: 
   ```bash
   createdb memory_agent
   ```
3. **Set up credentials**:
   - Username: `admin`
   - Password: `admin`
   
   Adjust the database credentials in the `DB_PARAMS` in `backend/modules/llms.py` or set the environment variables:
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_HOST`
   - `DB_PORT`

---

## Usage

Once everything is installed and configured, you can start JARVIS-MARK5 by running the following command:

```bash
python jarvis.py
```

### Basic Commands

- **Search**: `Search for [query]`
- **Generate PowerPoint**: `Create a presentation about [topic]`
- **GitHub Command**: `Clone repository [repo_name]` or `Create repository named [name]`
- **Voice Input/Output**: `Enable voice input` or `Disable voice input`

### Module Commands

Each module in JARVIS-MARK5 has its own set of commands. For example, to use the Perplexica search engine, you can simply input a natural language query, and the module will return relevant results.

---

## Modules

### Perplexica

The **Perplexica** module acts as an intelligent search engine that uses embeddings and similarity measures to retrieve relevant information.

- **Key Features**:
  - Semantic search using transformer-based embeddings.
  - Multiple search backend integration (SearxNG, Ollama, etc.).
  - Customizable ranking algorithms.

For more details, see the [Perplexica README](backend/AI/Perplexica/README.md).

### PowerPoint Generator

This module allows users to generate entire PowerPoint presentations from a simple prompt.

- **Key Features**:
  - Automatic slide generation with customizable templates.
  - Integration with image generation APIs for slide visuals.

### GitHub Integration

With built-in GitHub integration, JARVIS-MARK5 allows you to manage your repositories directly from the interface.

- **Key Features**:
  - Clone, create, and manage repositories.
  - Retrieve commits and issues.
  - Push and pull changes seamlessly.

For configuration details, check the [GitHub integration guide](extensions/config_all.json).

### Multi-modal Interactions

JARVIS-MARK5 supports multiple forms of input and output, allowing users to interact with it through:
- **Text-based** queries and responses.
- **Voice-based** interactions.
- **Image analysis** and generation.

You can configure or switch between these modalities in the `config.json` file.

---

## Extending JARVIS-MARK5

### Adding Existing Extensions

To install an existing extension:

1. Navigate to the `extensions` directory.
2. Clone the desired extension repository.
3. Install its dependencies.
4. Add the extension to the `config.json` file.

### Developing New Extensions

If you want to build your own extension, follow these steps:
1. Create a new directory for your extension.
2. Define your extension in the `__init__.py` file.
3. Include the necessary configuration in `config.json`.
4. Document your extension’s API endpoints (if applicable).

For a detailed tutorial, see the [Extensions Developer Guide](docs/extensions_guide.md).

---

## Advanced Features

### Natural Language Understanding

JARVIS-MARK5 incorporates advanced NLU to accurately interpret user commands and questions. The NLP pipeline leverages pre-trained models from GPT-4 and other LLMs.

### Real-time Data Analysis

Leverage JARVIS-MARK5's data analysis capabilities to analyze and visualize real-time data, powered by Python libraries such as Pandas, NumPy, and Matplotlib.

### Task Automation

Automate repetitive tasks, such as setting reminders, managing calendars, or generating reports, using JARVIS-MARK5’s task scheduling system.

---

## Performance Optimization

To improve performance, consider:

- Using GPU acceleration for AI-based tasks.
- Caching frequently used data.
- Limiting unnecessary API calls by fine-tuning request frequency.

---

## Security Considerations

Ensure security by:

- Securing your API keys in environment variables.
- Enabling SSL for all external API calls.
- Limiting access to sensitive data via authentication mechanisms.

---

## Troubleshooting

If you encounter issues, consult the [Troubleshooting Guide](docs/troubleshooting.md), which covers common problems and solutions such as:

- **API errors**
- **Missing dependencies**
- **Database connection issues**

---

## Contributing

### Code Style

Follow PEP-8 guidelines for Python code. Make sure to lint your code before committing.

### Testing

Run tests using `pytest`. Include unit tests for any new modules or features.

---

## Roadmap

Future plans for JARVIS-MARK5 include:

- **Mobile App Integration**
- **Enhanced Multi-modal Interaction**
- **Support for additional LLMs**
- **IoT device automation**

---

## Frequently Asked Questions

1. **Can I use JARVIS-MARK5 offline?**  
   Yes, certain functionalities can work offline, but most AI-driven modules require an internet connection.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.

---

## Acknowledgements

Special thanks to all contributors and developers who helped build and improve JARVIS-MARK5.
