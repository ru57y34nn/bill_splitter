#import random
from model import db, User, Bill 
from passlib.hash import pbkdf2_sha256

db.connect()

# This line will allow you "upgrade" an existing database by
# dropping all existing tables from it.
db.drop_tables([User, Bill])

db.create_tables([User, Bill])

rent = Bill(name="Rent", amount=1600, first_day="2018-01-01", last_day="2018-01-31")
rent.save()

electricity = Bill(name="Electricity", amount=100, first_day="2018-01-05", last_day="2018-02-04")
electricity.save()

dennis = User(username="Dennis", move_in="2018-01-01", move_out="2018-01-31",
              password=pbkdf2_sha256.hash("password"))
dennis.save()

mac = User(username="Mac", move_in="2018-01-05", move_out="2018-02-15",
		   password=pbkdf2_sha256.hash("drowssap"))
mac.save()

# charlie = User(username="Charlie", move_in="2018/01/01", move_out="2018/01/25")
# charlie.save()

users = [dennis, mac]



#User(name="admin", password=pbkdf2_sha256.hash("password")).save()

#for x in range(30):
#    Donation(donor=random.choice(donors), value=random.randint(100, 10000)).save()

