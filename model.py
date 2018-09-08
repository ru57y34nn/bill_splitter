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
    password = CharField(max_length=255, null=True)
#    days_billed = IntegerField(move_out - move_in)


class Bill(BaseModel):
    name = CharField(max_length=255, unique=True)
    amount = IntegerField()
    first_day = DateField()
    last_day = DateField()
    paid_by = ForeignKeyField(User, null=True)
#    user = ForeignKeyField(User, backref='bills')
