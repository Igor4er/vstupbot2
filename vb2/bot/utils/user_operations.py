import os
import json
from vb2.common.db import users
from vb2.common.dto import Users


def change_dir(dir, rep):
    """Method for switching directory for reading and writing files"""
    # gives the path of directory
    path = os.path.realpath(__file__)
    directory = os.path.dirname(path)

    # replaces folder name of util to text
    directory = directory.replace(dir, rep)
    os.chdir(directory)


async def add_user(query):
    """DB is here now!!!"""
    user = query["from"]
    try:
        language = query.data
    except Exception as e:
        print(e)
        language = "ua"
    row = {
        "uuid": user["id"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "username": user["username"],
        "language": language,
    }
    print(row)
    await users.update_or_create(Users(**row))


async def load_user(message):
    """ "HI, DB!"""
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
    change_dir("utils", "text")
    if language is None:
        path = "text_ua.json"
    else:
        path = f"text_{language}.json"  # Multi-language support
    with open(path, encoding="utf-8") as file:
        return json.load(file)
