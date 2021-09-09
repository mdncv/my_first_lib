from __future__ import annotations

import asyncio
import sys
from typing import Iterable

import aiohttp


def transpose(matrix: Iterable[Iterable[int]]) -> list[Iterable[int]]:
    """Транспонирование матрицу."""
    return list(zip(*matrix))


def matrix_counterclockwise(matrix: list[Iterable[int]]) -> list[int]:
    """
    "Разворачивает" матрицу против часовой стрелки.
    """
    new_list = []
    matrix = transpose(matrix)  # возможность обходить по часовой стрелке
    while matrix:
        first_row, *matrix = matrix  # "срезается" верхняя строка матрицы
        new_list.extend(first_row)
        matrix = transpose(
            matrix
        )  # оставшаяся часть матрицы транспонируется
        matrix.reverse()  # и отображается
    return new_list


def form_matrix(content: str) -> list[Iterable[int]]:
    """Создает матрицу из полученного текста."""
    matrix = []
    for line in content.splitlines():
        line = line.strip('+-\n| ')
        if not line:
            continue
        new_list = [
            *map(int, line.split("|"))
        ]  # разделение по символам "|"
        matrix.append(new_list)
    return matrix


async def get_matrix(url: str) -> list[int]:
    """Получает матрицу из переданной ссылки."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                status, data = resp.status, await resp.text()
                if 200 <= status < 300:
                    return matrix_counterclockwise(form_matrix(data))
                print(
                    f"Server returned non 2xx status - {status}:\n{data}",
                    file=sys.stderr,
                )
    except asyncio.TimeoutError:
        print("timeout occurred", file=sys.stderr)
    except aiohttp.ClientError:
        import traceback

        traceback.print_exc(file=sys.stderr)
    exit(1)


if __name__ == "__main__":
    SOURCE_URL = "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"
    TRAVERSAL = [
        10,
        50,
        90,
        130,
        140,
        150,
        160,
        120,
        80,
        40,
        30,
        20,
        60,
        100,
        110,
        70,
    ]


    def test_get_matrix():
        got = asyncio.run(get_matrix(SOURCE_URL))
        assert got == TRAVERSAL, f"{got} != {TRAVERSAL}"


    test_get_matrix()
