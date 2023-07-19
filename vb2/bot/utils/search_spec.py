from vb2.common.db import specialities


async def search_by_code(params):
    list_of_spec = await specialities.filter(params)
    found = []
    for spec in list_of_spec:
        found.append(spec)
    return found


async def search_by_word(message):
    specs = specialities.all()
    found = []
    words = message.text.lower().split()
    for spec in specs:
        common_words = 0
        total_words = len(words)
        name = spec.name.lower()
        for word in words:
            if word in name:
                common_words += 1
        percents = common_words/total_words
        if percents >= 0.51:
            found.append(spec)
    return found