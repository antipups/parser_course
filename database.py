# from cx_Oracle import Connection
from config import *
from enum import Enum
from typing import Tuple, Dict, List
from pymysql import Connection


class Table(Enum):
    courses = 'courses'
    currencies = 'currencies'


def conver_to_string(course: List[Course], id_: str):
    return (f'("{id_}", "' + '", "'.join(str(cell) for cell in row) + '")' for row in course)


class Database:

    def __init__(self):
        self._connect = Connection(host='localhost',
                                   user='root',
                                   password='root',
                                   db='work_curses')

        self._cursor = self._connect.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connect.close()

    def commit(self, queries=None):
        if isinstance(queries, str):
            queries = (queries, )
        for query in queries:
            self._cursor.execute(query=query)
        self._connect.commit()

    def truncate_all(self):
        query = (f'TRUNCATE TABLE {table.name}' for table in Table)
        self.commit(query)

    def add_new_currency(self, data: Dict[str, List[Course]]):
        title, courses = data.popitem()
        queries = ['INSERT INTO `currencies` (title)'
                   f'VALUES ("{title}")',
                   'INSERT INTO `courses` (`id`, `date`, `amount_foreign_value`, `amount_ruble_value`) '
                   'VALUES ' + ', '.join(conver_to_string(course=courses,
                                                          id_=title))]
        self.commit(queries=queries)



if __name__ == '__main__':
    # with Database() as db:
    #     db.truncate_all()
    # sex = tuple(conver_to_string([Course(1, 2, 3), Course(1, 2, 3)])))
    # print(tuple(conver_to_string([Course(1, 2, 3), Course(1, 2, 3)])))
    pass