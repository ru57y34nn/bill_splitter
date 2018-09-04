import os

from peewee import Model, CharField, IntegerField, DateField, ForeignKeyField
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///my_database.db'))


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(max_length=255, unique=True)
    move_in = DateField()
    move_out = DateField()
    days_billed = move_out - move_in


class Bill(BaseModel):
    name = CharField(max_length=255, unique=True)
    amount = IntegerField()
    start_date = DateField()
    end_date = DateField()
#    user = ForeignKeyField(User, backref='bills')


