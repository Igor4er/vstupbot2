from vb2.common.db import insert_category_into_base
from tqdm import tqdm


def list_specs() -> list:
    with open("speclist.txt", "r") as f:
        specs = []
        for line in f.readlines():
            if not line[0].isdigit():
                if len(line) > 5:
                    specs.append(line.replace("\n", ""))
        return specs


def create_specs():
    spec_list = list_specs()
    for spec in tqdm(spec_list):
        insert_category_into_base(spec)


if __name__ == "__main__":
    create_specs()
