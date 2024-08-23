import json
from dotenv import load_dotenv
from os import environ
load_dotenv()

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ['how', 'what', 'who', 'where', 'when', 'why', 'which', 'whose', 'whom', 'can you', "what's", "where's", "how's"]
    if any((word + ' ' in new_query for word in question_words)):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + '?'
            return new_query.capitalize()
        new_query += '?'
        return new_query.capitalize()
    if query_words[-1][-1] in ['.', '?', '!']:
        new_query = new_query[:-1] + '.'
        return new_query.capitalize()
    new_query += '.'
    return new_query.capitalize()

def LoadMessages():
    with open('ChatLog.json', 'r') as f:
        messages = json.load(f)
        return messages
        return messages

def GuiMessagesConverter(messages: list[dict[str, str]]):
    temp = []
    Assistantname = environ['AssistantName']
    Username = environ['NickName']
    for message in messages:
        if message['role'] == 'assistant':
            temp.append(f"""<span class = "Assistant">{Assistantname}</span> : {message['content']}""")
            temp.append('[*end*]')
        elif message['role'] == 'user':
            temp.append(f"""<span class = "User">{Username}</span> : {message['content']}""")
        else:
            temp.append(f"""<span class = "User">{Username}</span> : {message['content']}""")
    return temp