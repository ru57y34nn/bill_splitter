import os

from peewee import Model, CharField, IntegerField, DateField, ForeignKeyField
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///my_database.db'))


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(max_length=255, unique=True)
#    move_in = DateField()
#    move_out = DateField()
#    days_billed = move_out - move_in


class Bill(BaseModel):
    name = CharField(max_length=255, unique=True)
    amount = IntegerField()
#    start_date = DateField()
#    end_date = DateField()
#    user = ForeignKeyField(User, backref='bills')
'''
Afunction should take in each user and get users move_in and move_out date
and make a list of dates from first to last day.  It should then get the total from each bill
and divide that by the total days in the billing period to get a cost per day for the bill.
For each day in the billing period, it should loop through each persons list of days
and get a total n for that day that is then uses to divide that days cost per day by.
'''

