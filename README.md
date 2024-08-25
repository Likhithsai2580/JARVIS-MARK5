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
- [Advanced Features](#advanced-features)
- [Performance Optimization](#performance-optimization)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [Frequently Asked Questions](#frequently-asked-questions)
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
- Real-time data analysis and visualization capabilities
- Integration with popular productivity tools and APIs

## Installation

1. Ensure you have Python 3.8+ installed on your system.

2. Clone the repository:
   ```bash
   git clone https://github.com/Likhithsai2580/JARVIS-MARK5.git
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

6. (Optional) Install additional dependencies for specific features:
   ```bash
   pip install -r requirements-extra.txt
   ```

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

### Database Configuration

JARVIS-MARK5 uses a PostgreSQL database to store conversation history and other relevant data. This allows for persistent storage and retrieval of information across sessions.

#### PostgreSQL Setup

1. Ensure you have PostgreSQL installed on your system.
2. Create a new database named `memory_agent`.
3. Set up a user with the following credentials:
   - Username: `admin`
   - Password: `admin`
4. Make sure the PostgreSQL server is running on `localhost` and port `5432`.

You can customize these settings by modifying the `DB_PARAMS` dictionary in `backend/modules/llms.py` or by setting the following environment variables:
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`

#### Why PostgreSQL?

PostgreSQL is used in JARVIS-MARK5 for several reasons:
1. **Persistent Storage**: It allows the system to maintain conversation history and other data across multiple sessions.
2. **Efficient Querying**: PostgreSQL's powerful querying capabilities enable quick retrieval of relevant information.
3. **Scalability**: As the amount of data grows, PostgreSQL can handle large datasets efficiently.
4. **Data Integrity**: PostgreSQL ensures data consistency and provides ACID compliance.

#### How It Works

1. When JARVIS-MARK5 starts, it establishes a connection to the PostgreSQL database.
2. Each conversation (user input and AI response) is stored in the `conversations` table.
3. The system can retrieve past conversations to provide context for new queries.
4. The database is also used to store embeddings for efficient semantic search capabilities.

By using a database, JARVIS-MARK5 can learn from past interactions and provide more contextually relevant responses over time.

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

       def process_command(self, command):
           # Implement your extension's command processing logic
           pass

   def setup(jarvis):
       config = jarvis.load_config('my-new-extension/config.json')
       jarvis.register_extension(MyNewExtension(config))
   ```

4. In `config.json`, define any configuration options for your extension:
   ```json
   {
     "name": "My New Extension",
     "version": "1.0.0",
     "description": "A brief description of your extension",
     "options": {
       "option1": "default_value",
       "option2": 42
     }
   }
   ```

5. Document your extension in the `README.md` file, including its purpose, usage, and any dependencies.

6. Add your extension to the main JARVIS-MARK5 `config.json` file as described in the "Adding Existing Extensions" section.

7. Test your extension thoroughly and consider submitting it to the JARVIS-MARK5 extensions repository for others to use.

## Advanced Features

### Natural Language Understanding

JARVIS-MARK5 employs advanced natural language understanding (NLU) techniques to interpret user queries and commands more accurately. This includes:

- Intent recognition
- Entity extraction
- Sentiment analysis
- Context-aware interpretation

To fine-tune the NLU capabilities for your specific use case, you can modify the `nlu_config.json` file in the `config` directory.

### Custom Skill Development

You can create custom skills for JARVIS-MARK5 to extend its capabilities:

1. Create a new Python file in the `skills` directory (e.g., `my_custom_skill.py`).
2. Define your skill class, inheriting from the base `Skill` class:

   ```python
   from jarvis.core import Skill

   class MyCustomSkill(Skill):
       def __init__(self):
           super().__init__("my_custom_skill")

       def execute(self, params):
           # Implement your skill logic here
           pass
   ```

3. Register your skill in the `skills_registry.py` file.

### API Integration

JARVIS-MARK5 supports integration with various external APIs. To add a new API:

1. Create an API wrapper in the `api_wrappers` directory.
2. Add the API configuration to the `config.json` file.
3. Use the API in your modules or skills as needed.

## Performance Optimization

To ensure optimal performance of JARVIS-MARK5:

1. **Caching**: Implement caching mechanisms for frequently accessed data or API responses.
2. **Asynchronous Processing**: Use asynchronous programming techniques for I/O-bound operations.
3. **Database Indexing**: Optimize database queries by creating appropriate indexes.
4. **Load Balancing**: For high-traffic deployments, consider implementing load balancing across multiple instances.

## Security Considerations

When deploying JARVIS-MARK5, keep the following security best practices in mind:

1. **API Key Management**: Use environment variables or a secure key management system to store sensitive API keys.
2. **Input Validation**: Implement thorough input validation to prevent injection attacks.
3. **Rate Limiting**: Apply rate limiting to prevent abuse of the system.
4. **Regular Updates**: Keep all dependencies up-to-date to address potential vulnerabilities.
5. **Encryption**: Use HTTPS for all network communications and encrypt sensitive data at rest.

## Troubleshooting

If you encounter any issues while using JARVIS-MARK5, please check the following:

1. Ensure all dependencies are correctly installed.
2. Verify that your configuration files are set up properly.
3. Check the logs for any error messages.

Common Issues:

1. **API Connection Errors**: Verify API keys and network connectivity.
2. **Module Import Errors**: Ensure all required dependencies are installed.
3. **Performance Issues**: Check system resources and optimize database queries.

For more detailed troubleshooting, refer to the [Troubleshooting Guide](docs/troubleshooting.md).

## Contributing

We welcome contributions to JARVIS-MARK5! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear, descriptive messages.
4. Push your changes to your fork.
5. Submit a pull request to the main repository.

Please ensure your code adheres to our coding standards and include tests for new features.

### Code Style

We follow the PEP 8 style guide for Python code. Please ensure your contributions adhere to this standard. You can use tools like `flake8` or `black` to automatically format your code.

### Testing

When submitting a pull request, make sure to include appropriate unit tests for your changes. Run the existing test suite to ensure your changes don't break any existing functionality:

```bash
pytest tests/
```

## Roadmap

Future plans for JARVIS-MARK5 include:

- Enhanced multi-language support
- Integration with more IoT devices and smart home platforms
- Advanced data analytics and machine learning capabilities
- Improved voice recognition and synthesis
- Expanded plugin ecosystem

We welcome community input on prioritizing these features. Please use the GitHub issues to suggest and discuss future enhancements.

## Frequently Asked Questions

1. **Q: Can JARVIS-MARK5 run offline?**
   A: Yes, with local LLM support enabled, many features can work offline. However, some functionalities may require an internet connection.

2. **Q: How do I update JARVIS-MARK5?**
   A: Pull the latest changes from the repository and run `pip install -r requirements.txt` to update dependencies.

3. **Q: Is JARVIS-MARK5 compatible with Windows/macOS/Linux?**
   A: Yes, JARVIS-MARK5 is designed to be cross-platform compatible. However, some features may require additional setup on specific operating systems.


## License

JARVIS-MARK5 is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

We would like to thank the contributors and maintainers of the open-source projects that JARVIS-MARK5 relies on, including:

- Perplexica (AI-powered search engine)
- OpenAI (Large Language Models)
- Groq (API for querying knowledge graphs)
- Anthropic (AI-powered search engine)
- PyTorch (Deep learning framework)
- Transformers (Library for transformer models)
- PyGitHub (Python library for GitHub API)

We are grateful for their hard work and dedication, which has made JARVIS-MARK5 possible.

---

We hope you enjoy using JARVIS-MARK5! For any questions, issues, or suggestions, please don't hesitate to open an issue on our GitHub repository or join our community Discord server.

Happy coding with JARVIS-MARK5! 🚀🤖
