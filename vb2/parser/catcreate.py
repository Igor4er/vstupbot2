import asyncio
from bs4 import BeautifulSoup
import requests
from vb2.common.db import specialities, coeficients
from vb2.common.dto import Coeficients
from tqdm import tqdm


async def spec_uuid_by_code(code: str) -> str:
    spec = await specialities.filter([lambda speciality: speciality.code == code])
    if len(spec) > 0:
        return spec[0].uuid


def get_studspravka_site_bs4() -> BeautifulSoup:
    req = requests.get(
        "https://studspravka.com.ua/zno/spetsialnosti-i-predmeti-zno-dlia-vstupu",
        headers={
            "Host": "studspravka.com.ua",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept": "*/*",
        },
    )
    if req.ok:
        return BeautifulSoup(req.content, features="html.parser")
    else:
        raise IndexError("Не вдалось завантажити студсправку")


def get_studspravka_table_from_bs4(soup: BeautifulSoup):
    table = soup.find("table", class_="table table-bordered").find("tbody")
    if table is None:
        raise IndexError("Таблицю не знайдено")
    return table


async def get_rows_from_table(table) -> list[Coeficients]:
    trs = table.find_all("tr")
    coefs = []
    for tr in tqdm(trs, desc="Парсинг студсправки"):
        tds = tr.find_all("td")
        spec = tds[0].text
        codebuf = ""
        for sym in spec:
            if not sym.isalpha():
                codebuf += sym
        code = codebuf.strip()
        spec_uuid = await spec_uuid_by_code(code)
        ukrainian = float(tds[1].text.replace(",", ".").replace(",", "."))
        math = float(tds[2].text.replace(",", "."))
        history = float(tds[3].text.replace(",", "."))
        foreign = float(tds[4].text.replace(",", "."))
        biology = float(tds[5].text.replace(",", "."))
        physics = float(tds[6].text.replace(",", "."))
        chemestry = float(tds[7].text.replace(",", "."))

        try:
            coef = Coeficients(
                speciality=spec_uuid,
                math=math,
                ukrainian=ukrainian,
                history=history,
                foreign=foreign,
                biology=biology,
                physics=physics,
                chemestry=chemestry,
            )
            coefs.append(coef)
        except Exception:
            pass
    return coefs


async def main():
    ss_bs4 = get_studspravka_site_bs4()
    ss_table = get_studspravka_table_from_bs4(ss_bs4)
    coeficients_ = await get_rows_from_table(ss_table)
    for coef in tqdm(coeficients_, desc="Створення записів в БД"):
        await coeficients.update_or_create(coef)


if __name__ == "__main__":
    asyncio.run(main())
