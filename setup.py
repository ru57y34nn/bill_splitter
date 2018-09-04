import random

from model import db, User, Bill 

db.connect()

# This line will allow you "upgrade" an existing database by
# dropping all existing tables from it.
db.drop_tables([User, Bill])

db.create_tables([User, Bill])

rusty = User(name="Rusty")
rusty.save()

bob = User(name="Bob")
bob.save()

charlie = User(name="Charlie")
charlie.save()

users = [rusty, bob, charlie]

#for x in range(30):
#    Donation(donor=random.choice(donors), value=random.randint(100, 10000)).save()

