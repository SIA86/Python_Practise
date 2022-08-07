import csv
from peewee import *

db = SqliteDatabase(database='stocks', pragmas={'journal_mode': 'wal'})


class Stock(Model):
    name = CharField()
    price = FloatField()
    change = CharField()
    volume = CharField()

    class Meta:
        database = db

def main():

    db.connect()
    db.create_tables([Stock])

    with open ("currency.csv") as f:
        order = ['name', 'price', 'change', 'volume']
        reader = csv.DictReader(f, fieldnames=order)

        stocks = list(reader)

        for row in stocks:
            stock = Stock(name= row['name'], price = row['price'], change= row['change'], volume= ['volume'])
            stock.save()
            


if __name__ == "__main__":
    main()