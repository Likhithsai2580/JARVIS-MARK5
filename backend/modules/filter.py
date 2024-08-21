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
        python_code = matches[0].strip()
        return python_code
    else:
        return None