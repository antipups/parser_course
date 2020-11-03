from typing import Iterator, Match, List, Generator, Tuple
import re
from config import *


def get_rows(html_code: str) -> Tuple[Match[str]]:
    """
        Возвращает итератор со всеми рядами (tr)
    :param html_code:
    :return:
    """
    return tuple(re.finditer(pattern=r'<tr((?!/tr).)*',
                             string=html_code,
                             flags=re.DOTALL))[2:]


def get_cells(row_code: str) -> Course:
    """
        Возвращает именованный кортеж значениями курса за определенное число
    :param row_code: tr из html
    :return:
    """
    return Course(*re.findall(pattern=r'\d[^<]*',
                              string=row_code))


def cut_course(html_code: str) -> List[Course]:
    result_list = []
    for row in get_rows(html_code=html_code):
        result_list.append(get_cells(row.group()))
    return result_list

