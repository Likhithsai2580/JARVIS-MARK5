# JARVIS-MARK5 Extension API

This document provides a detailed reference for the Extension API used in JARVIS-MARK5. Developers can use this API to create new extensions that seamlessly integrate with the JARVIS-MARK5 system.

## Table of Contents

1. [Extension Base Class](#extension-base-class)
2. [Lifecycle Methods](#lifecycle-methods)
3. [Utility Methods](#utility-methods)
4. [Event Handling](#event-handling)
5. [Configuration Management](#configuration-management)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)

## Extension Base Class

All extensions should inherit from the `Extension` base class:

```python
from jarvis.core import Extension

class MyExtension(Extension):
    def __init__(self, config):
        super().__init__(config)
        # Your initialization code here
```

## Lifecycle Methods

### `__init__(self, config)`

The constructor for your extension. Use this to set up any initial state or resources.

- `config`: A dictionary containing the configuration for your extension.

### `initialize()`

Called when the extension is first loaded. Use this for any one-time setup operations.

```python
def initialize(self):
    # Perform setup operations
    pass
```

### `shutdown()`

Called when JARVIS-MARK5 is shutting down. Use this to clean up resources.

```python
def shutdown(self):
    # Perform cleanup operations
    pass
```

## Utility Methods

### `send_message(self, message)`

Send a message back to the user.

- `message`: The text of the message to send.

```python
self.send_message("Hello from MyExtension!")
```

### `get_config(self)`

Retrieve the configuration for your extension.

```python
config = self.get_config()
api_key = config.get('api_key', '')
```

### `log(self, level, message)`

Log a message at the specified level.

- `level`: The log level (e.g., 'INFO', 'WARNING', 'ERROR')
- `message`: The message to log

```python
self.log('INFO', 'MyExtension initialized successfully')
```

## Event Handling

### `on_message(self, message)`

Called for every message processed by JARVIS-MARK5.

- `message`: A dictionary containing message details.

```python
def on_message(self, message):
    if 'hello' in message['text'].lower():
        self.send_message("Hello! I'm MyExtension.")
```

### `on_command(self, command, args)`

Called when a specific command for your extension is invoked.

- `command`: The name of the command.
- `args`: A list of arguments passed to the command.

```python
def on_command(self, command, args):
    if command == 'mycommand':
        self.handle_my_command(args)
```

## Configuration Management

Extensions can define their configuration schema in the `config.json` file:

```json
{
  "name": "MyExtension",
  "version": "1.0.0",
  "description": "An example extension",
  "commands": [
    {
      "name": "mycommand",
      "description": "Performs a custom action"
    }
  ],
  "settings": {
    "api_key": {
      "type": "string",
      "description": "API key for external service",
      "required": true
    },
    "max_retries": {
      "type": "integer",
      "description": "Maximum number of retries",
      "default": 3
    }
  }
}
```

Access configuration values in your code:

```python
api_key = self.get_config().get('api_key')
max_retries = self.get_config().get('max_retries', 3)
```

## Error Handling

Use Python's exception handling to manage errors in your extension:

```python
try:
    # Your code here
except Exception as e:
    self.log('ERROR', f"An error occurred: {str(e)}")
    self.send_message("I'm sorry, but an error occurred while processing your request.")
```

## Best Practices

1. **Modularity**: Keep your extension focused on a specific functionality.
2. **Error Handling**: Implement proper error handling to prevent crashes.
3. **Configuration**: Use the `config.json` file for any configurable options.
4. **Documentation**: Provide clear documentation for your extension's usage and commands.
5. **Resource Management**: Properly initialize and clean up resources in `initialize()` and `shutdown()`.
6. **Asynchronous Operations**: For long-running tasks, consider using asynchronous programming to avoid blocking the main thread.
7. **Testing**: Write unit tests for your extension to ensure reliability.
8. **Versioning**: Use semantic versioning for your extension releases.

## Example Extension

Here's a simple example that puts it all together:

```python
from jarvis.core import Extension
import requests

class WeatherExtension(Extension):
    def __init__(self, config):
        super().__init__(config)
        self.api_key = self.get_config().get('api_key')
        self.base_url = "https://api.weatherservice.com/v1"

    def initialize(self):
        self.log('INFO', 'WeatherExtension initialized')

    def on_command(self, command, args):
        if command == 'weather':
            if len(args) == 0:
                self.send_message("Please provide a city name.")
            else:
                self.get_weather(args[0])

    def get_weather(self, city):
        try:
            response = requests.get(f"{self.base_url}/weather", params={
                'q': city,
                'appid': self.api_key
            })
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            self.send_message(f"The weather in {city} is {description} with a temperature of {temp}°C.")
        except Exception as e:
            self.log('ERROR', f"Error fetching weather: {str(e)}")
            self.send_message("Sorry, I couldn't fetch the weather information at this time.")

    def shutdown(self):
        self.log('INFO', 'WeatherExtension shutting down')

def initialize(config):
    return WeatherExtension(config)
```

This example demonstrates how to create a weather extension that responds to a 'weather' command, fetches data from an external API, and sends the result back to the user.
