import os
import datetime
from peewee import Model, CharField, IntegerField, DateField, DateTimeField, FloatField, ForeignKeyField
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///my_database.db'))


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(max_length=255, unique=True)
    move_in = DateTimeField()
    move_out = DateTimeField()
    #move_out = DateTimeField(default=datetime.datetime.now)
    password = CharField(max_length=255, null=True)
    acct_balance = FloatField()

    def __init__(self, username, move_in, move_out, password, acct_balance):
        self.username = username    
        self.move_in = move_in
        self.move_out = move_out
        self.password = password
        self.acct_balance = acct_balance

    def __repr__(self):
        return f"User {self.username}, Password: {self.password}"
#    days_billed = IntegerField(move_out - move_in)


class Bill(BaseModel):
    name = CharField(max_length=255, unique=True)
    amount = FloatField()
    first_day = DateTimeField()
    last_day = DateTimeField()
    paid_on = DateTimeField(null=True)
    paid_by = ForeignKeyField(User, backref='all', null=True)

    def __init__(self, name, amount, first_day, last_day, paid_on, paid_by):
        self.name = name
        self.amount = amount
        self.first_day = first_day
        self.last_day = last_day
        self.paid_on = paid_on
        self.paid_by = paid_by

    def cost_per_day(self):
        days = len(daterange(self.first_day, self.last_day))
        return amount / days



#    user = ForeignKeyField(User, backref='bills')
