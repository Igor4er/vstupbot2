from vb2.common.db import results, coeficients, users
from vb2.common.dto import Results, Coeficients


async def update_results(message, data):
    """Method for saving user examine results"""

    uuid = message.from_user.id
    result = await results.get_by_id(uuid=uuid)
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
    await results.update_or_create(Results(**row))


async def exam_calculation(query):
    uuid = query.data.replace("CALC ", "")
    id = query['from']['id']
    user = await users.get_by_id(id)
    marks = await results.get_by_id(id)
    print(uuid)
    # params = [lambda Coeficients: uuid == Coeficients.speciality]
    params = [lambda Coeficients: uuid in Coeficients.speciality]
    coefs = await coeficients.filter(params)

    if marks.subject_name == "HISTORY":
        third_coef = coefs[0].history
    elif marks.subject_name == "FOREIGN":
        third_coef = coefs[0].foreign
    elif marks.subject_name == "PHYSICS":
        third_coef = coefs[0].physics
    elif marks.subject_name == "BIO":
        third_coef = coefs[0].biology
    elif marks.subject_name == "CHEMISTRY":
        third_coef = coefs[0].chemistry

    # coefs
    ua = coefs[0].ukrainian
    math = coefs[0].math
    sum = ua + math + third_coef

    result = (marks.ua * ua + marks.math * math + marks.third_subject * third_coef) / sum
    return result