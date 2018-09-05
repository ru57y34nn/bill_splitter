import os
import base64
from flask import Flask, render_template, request, redirect, url_for, session
from peewee import fn
from model import Bill, User

app = Flask(__name__)
# app.secret_key = b'\xf1A\x88f\x1a@6\x1d\xa2\xc8J\xfc\x9e\x9c1\x86p\x04\xc1\xc7\xc7\x03\xfd\xbd'
# app.secret_key = os.environ.get('SECRET_KEY').encode()


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/bills/')
def all():
    bills = Bill.select()
    return render_template('bills.jinja2', bills=bills)


@app.route('/users/')
def users():
    all_users = User.select()
    return render_template('users.jinja2', all_users=all_users)


@app.route('/createuser/', methods=['GET', 'POST'])
def createuser():
    if request.method == 'POST':
        user_name = request.form['name']
        movein_day = request.form['first_day']
        moveout_day = request.form['last_day']
        new_user = User(username=user_name, move_in=movein_day, move_out=moveout_day)
        new_user.save()
        return redirect(url_for('users'))
    return render_template('createuser.jinja2')


@app.route('/createbill/', methods=['GET', 'POST'])
def createbill():
    if request.method == 'POST':
        bill_name = request.form['name']
        bill_amt = int(request.form['amount'])
        bill_start = request.form['first_day']
        bill_end = request.form['last_day']
        new_bill = Bill(name=bill_name, amount=bill_amt, first_day=bill_start, last_day=bill_end)
        new_bill.save()
        return redirect(url_for('all'))

    return render_template('createbill.jinja2')


@app.route('/report/')
def report():
    bills = Bill.select(Bill.amount)
    total = 0
    for bill in bills:
        total += bill.amount
    bills_total = total
    return render_template('report.jinja2', bills_total=bills_total)


# function for a view to display each persons totals goes here
'''
Afunction should take in each user and get users move_in and move_out date
and make a list of dates from first to last day.  It should then get the total from each bill
and divide that by the total days in the billing period to get a cost per day for the bill.
For each day in the billing period, it should loop through each persons list of days
and get a total n for that day that is then uses to divide that days cost per day by.
'''



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port, debug=True)
