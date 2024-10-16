import re

def filter_python(txt):
    pattern = r"```python(.*?)```"
    matches = re.findall(pattern, txt, re.DOTALL)

    if matches:
        python_code = matches[0].strip()
        return python_code
    else:
        return None

def filter_json(txt):
    pattern = r"```json(.*?)```"
    matches = re.findall(pattern, txt, re.DOTALL)

    if matches:
        json_code = matches[0].strip()
        return json_code
    else:
        return None

def filter_code(txt, language):
    pattern = rf"```{language}(.*?)```"
    matches = re.findall(pattern, txt, re.DOTALL)

    if matches:
        code = matches[0].strip()
        return code
    else:
        return None

def filter_markdown(txt):
    pattern = r"```markdown(.*?)```"
    matches = re.findall(pattern, txt, re.DOTALL)

    if matches:
        markdown_code = matches[0].strip()
        return markdown_code
    else:
        return None

def filter_html(txt):
    pattern = r"```html(.*?)```"
    matches = re.findall(pattern, txt, re.DOTALL)

    if matches:
        html_code = matches[0].strip()
        return html_code
    else:
        return None

def filter_code_blocks(txt):
    pattern = r"```(.*?)```"
    matches = re.findall(pattern, txt, re.DOTALL)

    if matches:
        code_blocks = [match.strip() for match in matches]
        return code_blocks
    else:
        return None
