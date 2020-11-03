from my_parser import parse, monotonic
from database import Database


if __name__ == '__main__':
    start = monotonic()
    with Database() as db:
        db.truncate_all()
        for currency in parse():
            db.add_new_currency(currency)
    print('Ready', monotonic() - start)
