import os
# import base64
from flask import Flask, render_template, request, redirect, url_for, session
# from peewee import fn
from model import Bill, User
import datetime
from datetime import date, datetime
from dateutil.rrule import rrule, DAILY
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
# app.secret_key = b'\xf1A\x88f\x1a@6\x1d\xa2\xc8J\xfc\x9e\x9c1\x86p\x04\xc1\xc7\xc7\x03\xfd\xbd'
app.secret_key = os.environ.get('SECRET_KEY').encode()


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.select().where(User.username == request.form['name']).get()

        if user and pbkdf2_sha256.verify(request.form['password'], user.password):
            session['username'] = request.form['name']
            return redirect(url_for('users'))

        return render_template('login.jinja2', error="Incorrect username or password.")

    else:
        return render_template('login.jinja2')


@app.route('/bills/')
def all():
    bills = Bill.select()
#    bill_dict = dict()
    for bill in bills:
        # bill_name = bill.name
        bill.amount = "${:0.2f}".format(bill.amount)
        bill.paid_on = bill.paid_on
        bill.paid_by = str(bill.paid_by)
#        bill_start = bill.first_day
#        bill_end = bill.last_day
    return render_template('bills.jinja2', bills=bills)


@app.route('/users/')
def users():
    all_users = User.select()
    return render_template('users.jinja2', all_users=all_users)


@app.route('/createuser/', methods=['GET', 'POST'])
def createuser():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        user_name = request.form['name']
        movein_day = request.form['first_day']
        moveout_day = request.form['last_day']
        new_user = User(username=user_name,
                        move_in=movein_day,
                        move_out=moveout_day)
        new_user.save()
        return redirect(url_for('users'))
    return render_template('createuser.jinja2')


@app.route('/createbill/', methods=['GET', 'POST'])
def createbill():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        bill_name = request.form['name']
        bill_amt = int(request.form['amount'])
        bill_start = request.form['first_day']
        bill_end = request.form['last_day']
        new_bill = Bill(name=bill_name,
                        amount=bill_amt,
                        first_day=bill_start,
                        last_day=bill_end)
        new_bill.save()
        return redirect(url_for('all'))

    return render_template('createbill.jinja2')


def daterange(start_date, end_date):
    days = []
    for dt in rrule(DAILY, dtstart=start_date, until=end_date):
        days.append(dt.strftime("%Y-%m-%d"))
    return days


def make_date(start_date, end_date):
    day1 = datetime.strptime(str(start_date), "%Y-%m-%d").date()
    day2 = datetime.strptime(str(end_date), "%Y-%m-%d").date()
    return day1, day2


def breakdown():
    bills = Bill.select()
    users = User.select()
    bill_cpd = dict()
    for bill in bills:
        billday1, billday2 = make_date(bill.first_day, bill.last_day)
        bill_days = daterange(billday1, billday2)
        cpd = bill.amount / float(len(bill_days))
        costsperday = dict()
        for day in bill_days:
            n = 0
            for user in users:
                userday1, userday2 = make_date(user.move_in, user.move_out)
                user_days = daterange(userday1, userday2)
                if day in user_days:
                    n += 1
            costperday = cpd / float(n)
            costsperday[day] = costperday
        bill_cpd[str(bill.name)] = costsperday
    return bill_cpd


def total_users():
    users = User.select()
    bill_cpd = breakdown()
    users_totals = dict()
    for user in users:
        username = str(user.username)
        users_totals[username] = ''
        userday1, userday2 = make_date(user.move_in, user.move_out)
        user_days = daterange(userday1, userday2)
        # user_totals = list()
        user_totals = dict()
        for key, value in bill_cpd.items():
            bill_name = key
            bill_total = 0
            for key, value in bill_cpd[bill_name].items():
                if key in user_days:
                    bill_total += value
            user_totals[bill_name] = bill_total
        users_totals[username] = user_totals
        users_final = dict()
        for key, value in users_totals.items():
            username = key
            usertotal = 0
            for key, value in users_totals[username].items():
                usertotal += value
            usertotal = "${:0.2f}".format(usertotal)
            users_final[username] = usertotal
    return users_totals, users_final


def who_owes_who():
    '''
    for bill in bills:
        for users != bill.paid_by:
            user_bill_totals = total_users()[0]
            for key, value in user_bill_totals[user]:
                if key == bill:
                    user owes bill.paid_by value
    '''
    pass


@app.route('/report/')
def report():
    bills = Bill.select(Bill.amount)
    users = User.select()
    total = 0
    for bill in bills:
        total += bill.amount
    bills_total = total
    bills_total = "${:0.2f}".format(bills_total)
    user_bill_totals = total_users()[0]
    user_totals = total_users()[1]
    for key, value in user_totals.items():
        for user in users:
            if user.username == key:
                user.amt_owed = value
    return render_template('report.jinja2', bills_total=bills_total, users=users,
                           user_bill_totals=user_bill_totals)


@app.route('/paidby/', methods=['GET', 'POST'])
def paidby():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        payer_name = request.form['username']
        bill_name = request.form['billname']
#        find_bill = Bill.select().where(Bill.name == bill_name).get()
        find_user = User.select().where(User.username == payer_name)

        if find_user.exists():
            Bill.update(paid_on=datetime.now(), paid_by=find_user.get())\
                .where(Bill.name == bill_name).execute()
            return redirect(url_for('all'))
        else:
            return render_template('paidby.jinja2', error="User does not exist.")
    else:
        return render_template('paidby.jinja2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port, debug=True)
