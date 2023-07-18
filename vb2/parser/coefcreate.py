import asyncio
from vb2.common.dto import Specialities
from vb2.common.db import categories, specialities


def link_specs_to_categories() -> dict:
    key = None
    linked = {}
    with open("speclist.txt", "r") as f:
        for fline in f.readlines():
            line = fline.strip()
            if line != "" and line is not None:
                if not line[0].isdigit():
                    key = line
                else:
                    if linked.get(key, None) is None:
                        linked[key] = []
                    linked[key].append(line)
    return linked


async def category_uuid_by_name(name: str) -> str:
    cat = await categories.filter([lambda category: category.name == name])
    if len(cat) > 0:
        return cat[0].uuid


async def main():
    linked_specs = link_specs_to_categories()
    linked_cats = linked_specs.keys()
    for linked_cat in linked_cats:
        cat_uuid = await category_uuid_by_name(linked_cat)
        for spec in linked_specs[linked_cat]:
            codebuf = ""
            namebuf = ""
            wc = True
            for sym in spec:
                if sym.isalpha() and sym.isupper():
                    wc = False
                if wc:
                    codebuf += sym
                else:
                    namebuf += sym
            code = codebuf.strip()
            name = namebuf.strip()

            j = {"code": code, "name": name, "category": cat_uuid}

            await specialities.update_or_create(Specialities(**j))


if __name__ == "__main__":
    asyncio.run(main())
