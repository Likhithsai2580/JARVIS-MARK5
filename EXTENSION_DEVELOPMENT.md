# JARVIS-MARK5 Extension Development Guide

This guide will walk you through the process of developing extensions for JARVIS-MARK5. Extensions allow you to add new functionalities to the system, enhancing its capabilities and customizing it to your needs.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Extension Structure](#extension-structure)
3. [Developing Your Extension](#developing-your-extension)
4. [Testing Your Extension](#testing-your-extension)
5. [Packaging and Distribution](#packaging-and-distribution)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

## Getting Started

Before you begin, ensure you have:

1. JARVIS-MARK5 installed and running on your system
2. Python 3.8 or higher
3. Basic understanding of Python programming
4. Familiarity with the JARVIS-MARK5 [Extension API](EXTENSION_API.md)

## Extension Structure

A typical JARVIS-MARK5 extension has the following structure:

```
my_extension/
├── __init__.py
├── config.json
├── README.md
├── requirements.txt
└── test_my_extension.py
```

- `__init__.py`: Main Python file containing your extension code
- `config.json`: Configuration file for your extension
- `README.md`: Documentation for your extension
- `requirements.txt`: List of Python dependencies
- `test_my_extension.py`: Unit tests for your extension

## Developing Your Extension

### Step 1: Create the Extension Directory

```bash
mkdir extensions/my_extension
cd extensions/my_extension
```

### Step 2: Create the `__init__.py` File

This is where your main extension code will reside:

```python
from jarvis.core import Extension

class MyExtension(Extension):
    def __init__(self, config):
        super().__init__(config)
        # Initialize your extension here

    def on_message(self, message):
        # Handle incoming messages
        pass

    def on_command(self, command, args):
        # Handle specific commands
        if command == 'mycommand':
            self.send_message(f"Executing mycommand with args: {args}")

# This function is required to initialize your extension
def initialize(config):
    return MyExtension(config)
```

### Step 3: Create the `config.json` File

Define your extension's configuration:

```json
{
  "name": "My Extension",
  "version": "1.0.0",
  "description": "A brief description of what your extension does",
  "commands": [
    {
      "name": "mycommand",
      "description": "Description of what this command does"
    }
  ],
  "settings": {
    "some_option": {
      "type": "string",
      "description": "Description of this option",
      "default": "default_value"
    }
  }
}
```

### Step 4: Write Your README.md

Provide clear documentation for your extension:

```markdown
# My Extension

Brief description of what your extension does.

## Installation

Instructions on how to install your extension.

## Usage

Examples of how to use your extension.

## Configuration

Explanation of configuration options.

## Commands

List and describe the commands provided by your extension.
```

### Step 5: Create requirements.txt

List any additional Python packages your extension needs:

```
requests==2.26.0
```

## Testing Your Extension

Create a `test_my_extension.py` file for unit tests:

```python
import unittest
from unittest.mock import MagicMock
from . import MyExtension

class TestMyExtension(unittest.TestCase):
    def setUp(self):
        config = {'some_option': 'test_value'}
        self.extension = MyExtension(config)

    def test_on_command(self):
        self.extension.send_message = MagicMock()
        self.extension.on_command('mycommand', ['arg1', 'arg2'])
        self.extension.send_message.assert_called_once_with(
            "Executing mycommand with args: ['arg1', 'arg2']"
        )

if __name__ == '__main__':
    unittest.main()
```

Run your tests:

```bash
python -m unittest test_my_extension.py
```

## Packaging and Distribution

1. Ensure your extension works correctly within JARVIS-MARK5.
2. Create a GitHub repository for your extension.
3. Tag a release with a semantic version number.
4. Update the JARVIS-MARK5 extension registry (if applicable).

## Best Practices

1. **Follow PEP 8**: Adhere to Python style guidelines.
2. **Error Handling**: Implement proper error handling and logging.
3. **Documentation**: Provide clear, comprehensive documentation.
4. **Testing**: Write unit tests for all major functionalities.
5. **Configuration**: Use `config.json` for all configurable options.
6. **Versioning**: Use semantic versioning for releases.
7. **Resource Management**: Properly initialize and clean up resources.
8. **Asynchronous Operations**: Use async programming for long-running tasks.

## Troubleshooting

Common issues and their solutions:

1. **Extension not loading**: 
   - Check if the extension is properly added to JARVIS-MARK5's configuration.
   - Ensure all dependencies are installed.

2. **Commands not recognized**: 
   - Verify that commands are correctly defined in `config.json`.
   - Check if the `on_command` method is properly implemented.

3. **Configuration not working**: 
   - Ensure `config.json` is properly formatted.
   - Verify that you're accessing configuration values correctly in your code.

4. **Errors during execution**: 
   - Check the JARVIS-MARK5 log files for error messages.
   - Use try-except blocks to catch and handle exceptions.

For more complex issues, open an issue on the GitHub repository.

---

Remember to refer to the [Extension API Documentation](EXTENSION_API.md) for detailed information on available methods and interfaces. Happy developing!
