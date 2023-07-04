import os
import json


def change_dir(dir, rep):
    """ Method for switching directory for reading and writing files """
    # gives the path of directory
    path = os.path.realpath(__file__)
    directory = os.path.dirname(path)

    # replaces folder name of util to text
    directory = directory.replace(dir, rep)
    os.chdir(directory)


def add_user(query):
    """ It's kludge for storing user data in json while DB isn't ready"""
    change_dir('utils', 'user')
    path = "users.json"
    with open(path, "w", encoding='utf-8') as file:
        user = query['from']
        row = {f"{user['id']}": {
            "first_name": user['first_name'],
            "last_name": user['last_name'],
            "username": user['username'],
            "language": query.data
        }}
        json.dump(row, file, ensure_ascii=False)


def load_user(message):
    """ It's kludge for storing user data in json while DB isn't ready"""
    change_dir('utils', 'user')
    path = "users.json"
    with open(path, encoding='utf-8') as file:
        users = json.load(file)
        return users[str(message.from_user.id)]["language"]


def load_text(message):
    try:
        language = load_user(message)
    except:
        language = "ua"
    change_dir('utils', 'text')
    path = f"text_{language}.json" # Multi-language support
    with open(path, encoding='utf-8') as file:
        return json.load(file)
