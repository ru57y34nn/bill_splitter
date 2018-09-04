import os
import base64
from flask import Flask, render_template, request, redirect, url_for, session
from peewee import fn
from model import Donation, Donor

app = Flask(__name__)
# app.secret_key = b'\xf1A\x88f\x1a@6\x1d\xa2\xc8J\xfc\x9e\x9c1\x86p\x04\xc1\xc7\xc7\x03\xfd\xbd'
app.secret_key = os.environ.get('SECRET_KEY').encode()


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/bills/')
def all():
    bills = Bill.select()
    return render_template('bills.jinja2', bills=bills)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        bill_name = request.form['name']
        bill_amt = int(request.form['amount'])
#        find_bill = Bill.select().where(Bill.name == bill_name)

#        if find_donor.exists():
#            Donation(donor=find_donor.get(), value=donation_amt).save()
#            return redirect(url_for('all'))
#        else:
        new_bill = Bill(name=bill_name, amount=bill_amt)
        new_bill.save()
#        Donation(donor=new_donor, value=donation_amt).save()
        return redirect(url_for('all'))

    return render_template('create.jinja2')

"""
@app.route('/report')
def report():
    donations = Donation.select(
        Donation.donor, fn.Count(Donation.value).alias('count'),
        fn.Sum(Donation.value).alias('total'),
        fn.Avg(Donation.value).alias('average')).group_by(Donation.donor)
    return render_template('report.jinja2', donations=donations)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port, debug=True)
'''