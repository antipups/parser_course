from cx_Oracle import Connection
from config import *
from enum import Enum
from typing import Tuple, Dict, List
# from pymysql import Connection


class Table(Enum):
    """
        Класс для констант названий таблиц
    """
    courses = 'courses'
    currencies = 'currencies'


def conver_to_string(course: List[Course], id_: str):
    """
        Конвертация списка курсов в одну строку для инсерта в бд
    :param course:
    :param id_:
    :return:
    """
    return (f'("{id_}", "' + '", "'.join(str(cell) for cell in row) + '")' for row in course)


class Database:
    """
        Класс для работы с базой данных, он "прокладка" между программой и БД
    """
    def __init__(self):
        """
            Конструктор класса, тут подключаемся к БД
        """
        with open('config.txt', 'r') as f:
            clear_string = lambda line: line[:-1] if '\n' in line else line
            HOST, PASSWORD, USER, DB = tuple(clear_string(line) for line in f.readlines()[:4])
        self._connect = Connection(host=HOST,
                                   user=USER,
                                   password=PASSWORD,
                                   db=DB)

        self._cursor = self._connect.cursor()

    def __enter__(self):
        """
            Создаем метод для работы с базой данных через with as
        :return:
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
            Также метод для работы с with as
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self._connect.close()

    def commit(self, queries=None):
        """
            Сохранение изменений в базе, с попутным приминением запросов если их передали
        :param queries:
        :return:
        """
        if isinstance(queries, str):    # если запрос один (т.к. цикл пройдется посимвольно мы создаем кортеж и кладем в него запрос)
            queries = (queries, )
        for query in queries:
            self._cursor.execute(query=query)
        self._connect.commit()

    def truncate_all(self):
        """
            Чистим бд перед очередным парсингом
        :return:
        """
        query = (f'TRUNCATE TABLE {table.name}' for table in Table)
        self.commit(query)

    def add_new_currency(self, data: Dict[str, List[Course]]):
        """
            Добавление в бд записи
        :param data: словарь имеющий структуру КЛЮЧ : СПИСОК КУРСОВ ЗА ВСЁ ВРЕМЯ
        :return:
        """
        title, courses = data.popitem()
        queries = ['INSERT INTO `currencies` (title)'
                   f'VALUES ("{title}")',
                   'INSERT INTO `courses` (`id`, `date`, `amount_foreign_value`, `amount_ruble_value`) '
                   'VALUES ' + ', '.join(conver_to_string(course=courses,
                                                          id_=title))]
        self.commit(queries=queries)

    def get_course(self, date: str) -> List[tuple]:
        """
            Получение курса по определенной дате
        :param date:
        :return:
        """
        query = 'SELECT `id`,' \
                '       `amount_foreign_value`, ' \
                '       `amount_ruble_value` ' \
                f'FROM `{Table.courses.name}` ' \
                f'WHERE `date` = "{date}"'
        self._cursor.execute(query)
        return self._cursor.fetchall()

    def get_cross_course(self, date: str) -> Tuple[tuple]:
        """
            Получение всех курсов по каждой валюте к рублю, после, сравнение их между собой
        :param date:
        :return:
        """
        query = 'SELECT CONCAT(new_courses.id, /* выводим название сравниваемой валюты */' \
                '              " - ", ' \
                '              courses.id,  /* выводим название второй сравниваемой валюты */' \
                '              ": 1 к ", ' \
                '              CAST(REPLACE(amount_ruble_value, ",", ".") AS float) / CAST(amount_foreign_value AS float) / course_to_ruble2)  /* получаем цену одной валюты за рублю и после делим вторую валюту на это значение*/' \
                f'FROM `{Table.courses.name}` ' \
                f'INNER JOIN (SELECT id, CAST(REPLACE(amount_ruble_value, ",", ".") AS float) / CAST(amount_foreign_value AS float) AS course_to_ruble2 FROM courses WHERE date = "{date}") AS new_courses /* подключаем с помощью крестового соединения (каждый к каждому)*/' \
                f'WHERE `date` = "{date}" AND course_to_ruble2 != CAST(REPLACE(amount_ruble_value, ",", ".") AS float) / CAST(amount_foreign_value AS float) /* отбираем нужную дату и удаляем курсы 1 к 1*/'
        self._cursor.execute(query)
        return self._cursor.fetchall()


if __name__ == '__main__':
    # with Database() as db:
    #     db.truncate_all()
    # sex = tuple(conver_to_string([Course(1, 2, 3), Course(1, 2, 3)])))
    # print(tuple(conver_to_string([Course(1, 2, 3), Course(1, 2, 3)])))
    pass