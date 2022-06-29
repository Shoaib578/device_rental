from flask import Blueprint,redirect,flash,render_template,url_for,request
from application.models import Users,Reservation,ReservationSchema,Devices
from application.Main.forms import BookDeviceForm
from application import db
import os
import json
import requests

from sqlalchemy import text
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
main  = Blueprint('main', __name__,template_folder='templates',static_folder='../static')


@main.route('/')
@login_required
def Index():

    if current_user.is_authenticated:
        if current_user.is_admin == 1:
            return redirect(url_for("admin.Index"))
    
   
    api = requests.get("http://127.0.0.1:5000/apis/get_your_booked_orders?user_id="+str(current_user.id))
    data = api.text
    parse = json.loads(data)
    
    
    

    return render_template('main/index.html',orders=parse['orders'])


@main.route('/devices',methods=['GET','POST'])
@login_required
def Device():
    if current_user.is_authenticated:
        if current_user.is_admin == 1:
            return redirect(url_for("admin.Index"))
    
    
    
    devices = requests.get('http://127.0.0.1:5000/apis/get_all_devices')
    data= devices.text
    parse = json.loads(data)
    return render_template('main/devices.html',devices=parse['devices'])


@main.route('/book_device/<int:device_id>',methods=['GET','POST'])
@login_required
def BookDevice(device_id):
    if current_user.is_authenticated:
        if current_user.is_admin == 1:
            return redirect(url_for("admin.Index"))
    
    form = BookDeviceForm()
    if request.method == 'POST' and form.validate():
        
        order = Reservation(client_id=current_user.id,device_id=device_id,reserve_date=form.ReserveDate.data,pickup_date=form.PickupDate.data,return_date=form.ReturnDate.data,reason=form.Reason.data,status='pending')
        db.session.add(order)
        db.session.commit()
        flash("You Have Booked a Device Successfully")
        return redirect(url_for("main.Device"))
    return render_template('main/book_device.html',form=form,device_id=device_id)

@main.route('/logout',methods=["GET","POST"])
@login_required
def Logout():
    if current_user.is_authenticated:
        if current_user.is_admin == 1:
            return redirect(url_for("admin.Index"))
    logout_user()
    return redirect(url_for("auth.Login"))