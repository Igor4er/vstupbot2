import os
import json
from datetime import datetime
from vb2.common.db import users, results
from vb2.common.dto import Users, Results


def change_dir(dir, rep):
    """ Method for switching directory for reading and writing files """
    # gives the path of directory
    path = os.path.realpath(__file__)
    directory = os.path.dirname(path)

    # replaces folder name of util to text
    directory = directory.replace(dir, rep)
    os.chdir(directory)


async def add_user(query):
    """DB is here now!!!"""
    user = query['from']
    row = {
        "uuid": user['id'],
        "first_name": user['first_name'],
        "last_name": user['last_name'],
        "username": user['username'],
        "language": query.data
    }
    await users.update_or_create(Users(**row))


async def update_results(message, data):
    """DB is here now!!!"""
    uuid = message.from_user.id
    message = message.text
    subject = data.get('subject')
    row = {
        "uuid": uuid,
        "user": uuid,
    }
    if subject == "UA":
        row.update({"ua": int(message)})
    elif subject == "MATH":
        row.update({"math": int(message)})
    else:
        row.update({"third_subject": int(message),
                    "subject_name": subject})

    await results.update_or_create(Results(**row))


async def load_user(message):
    """"HI, DB!"""
    uuid = message.from_user.id
    user: Users = await users.get_by_id(uuid=uuid)
    if user is not None:
        return user.language
    return None


async def load_text(message):
    try:
        language = await load_user(message)
    except Exception as e:
        print(e)
        language = "ua"
    change_dir('utils', 'text')
    if language is None:
        path = "text_ua.json"
    else:
        path = f"text_{language}.json" # Multi-language support
    with open(path, encoding='utf-8') as file:
        return json.load(file)
