from vb2.common.db import results
from vb2.common.dto import Results


async def update_results(message, data):
    """DB is here now!!!"""

    uuid = message.from_user.id
    result = await results.get_by_id(uuid=uuid)
    print(result)
    message = message.text
    subject = data.get("subject")
    row = {
        "uuid": uuid,
        "user": uuid,
    }
    if result is not None:
        row.update(
            {
                "ua": result.ua,
                "math": result.math,
                "third_subject": result.third_subject,
                "subject_name": result.subject_name,
            }
        )
    if subject == "UA":
        row.update({"ua": int(message)})
    elif subject == "MATH":
        row.update({"math": int(message)})
    else:
        row.update({"third_subject": int(message), "subject_name": subject})
    print(row)
    await results.update_or_create(Results(**row))
