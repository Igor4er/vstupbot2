from vb2.settings import settings
import requests
import json
from vb2.common.dto import *

AUTH_HEADERS = {"apikey": settings.DB_KEY, "Authorization": f"Bearer {settings.DB_KEY}"}
PREFER_MINIMAL_RETURN = {"Prefer": "return=minimal"}
TYPE_JSON = {"Content-Type": "application/json"}


def insert_category_into_base(category: str):
    r = requests.post(
        f"{settings.DB_URL}/categories",
        json={"name": category},
        headers={
            "apikey": settings.DB_KEY,
            "Authorization": f"Bearer {settings.DB_KEY}",
            "Content-Type": "application/json",
            # "Prefer": "return=minimal",
        },
    )
    if not r.ok:
        print(r.status_code)
        print(r.content)


class DbTable:
    def __init__(self, dto):
        self.Dto = dto
        self.name = dto.__name__.lower()

    async def get_by_id(self, uuid: str):
        req = requests.get(
            f"{settings.DB_URL}/{self.name}",
            params={"uuid": f"eq.{uuid}"},
            headers=dict(AUTH_HEADERS),  # dict(AUTH_HEADERS, **PREFER_MINIMAL_RETURN)
        )
        if req.ok:
            ans = json.loads(req.content.decode("utf-8"))
            if len(ans) == 1:
                return self.Dto(**ans[0])
        return None

    def all(self) -> list | None:
        req = requests.get(
            f"{settings.DB_URL}/{self.name}",
            params={"select": "*"},
            headers=dict(AUTH_HEADERS),  # dict(AUTH_HEADERS, **PREFER_MINIMAL_RETURN)
        )
        if req.ok:
            alls = []
            ans = json.loads(req.content.decode("utf-8"))
            for an in ans:
                alls.append(self.Dto(**an))
            return alls
        else:
            return None

    async def insert_row(self, row):
        """
        Вставляє рядок в базу.
        :param row: Любий dto з vb2.common.dto
        :return: Чи успішно всталено рядок
        """
        if not isinstance(row, self.Dto):
            raise TypeError(f"row is not {self.Dto.__name__} dto")
        # row.zero()
        req = requests.post(
            f"{settings.DB_URL}/{self.name}",
            json=row.model_dump(exclude=("uuid", "created_at")),
            headers=dict(AUTH_HEADERS, **TYPE_JSON, **PREFER_MINIMAL_RETURN),
        )
        if req.ok:
            return True
        return req.status_code

    async def update_row(self, row):
        """
        Оновлює ряок в базі.
        :param row: Любий dto з vb2.common.dto
        :return: Чи успішно оновлено рядок
        """
        if not isinstance(row, self.Dto):
            raise TypeError(f"row is not {self.Dto.__name__} dto")
        req = requests.patch(
            f"{settings.DB_URL}/{self.name}",
            params={"uuid": f"eq.{row.uuid}"},
            json=row.model_dump(),
            headers=dict(AUTH_HEADERS, **TYPE_JSON, **PREFER_MINIMAL_RETURN),
        )
        if req.ok:
            return True
        return req.status_code

    async def update_or_create(self, row):
        if not isinstance(row, self.Dto):
            raise TypeError(f"row is not {self.Dto.__name__} dto")
        if await self.get_by_id(row.uuid) is not None:
            return await self.update_row(row)
        else:
            return await self.insert_row(row)

    async def get_or_create(self, row):
        if not isinstance(row, self.Dto):
            raise TypeError(f"row is not {self.Dto.__name__} dto")
        gbi = await self.get_by_id(row)
        if gbi is not None:
            return gbi
        else:
            return await self.insert_row(row)

    async def filter(self, filters: list) -> list:
        """
        Фільтрує всі записи в бд по списку фльтрів.
        :param filters: Список lambda функцій, якій приймають dto, і вертають bool
        :return: То що відфільтрувалось по фільрам
        """
        dtos = self.all()
        for ft in filters:
            dtos = list(filter(ft, dtos))
        return dtos


categories = DbTable(dto=Categories)
coeficients = DbTable(dto=Coeficients)
specialities = DbTable(dto=Specialities)
users = DbTable(dto=Users)
results = DbTable(dto=Results)
