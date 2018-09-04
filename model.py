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


class Bill(BaseModel):
    value = IntegerField()
    user = ForeignKeyField(User, backref='donations')


