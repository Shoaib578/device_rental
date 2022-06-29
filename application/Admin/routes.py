from flask import Blueprint,redirect,flash,render_template,url_for,request
from application.models import Users,Reservation,Devices,ReservationSchema
from application.Admin.forms import AddDeviceForm
from application import db
import os
import requests
import json
from sqlalchemy import text
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
admin  = Blueprint('admin', __name__,template_folder='templates',static_folder='../static')


@admin.route('/admin')
@login_required
def Index():
    if current_user.is_authenticated:
        if current_user.is_admin == 0:
            return redirect(url_for("main.Index"))
    api = requests.get("http://127.0.0.1:5000/apis/get_all_users")    
    data= api.text    
    parse = json.loads(data)
    return render_template('admin/index.html',users=parse["users"])


@admin.route('/admin/orders')
@login_required
def Orders():
    if current_user.is_authenticated:
        if current_user.is_admin == 0:
            return redirect(url_for("main.Index"))
    
    api = requests.get('http://127.0.0.1:5000/apis/get_all_orders')
    data= api.text
    parse =json.loads(data)
    
    print(parse)
    return render_template('admin/orders.html',orders=parse['orders'])

@admin.route('/admin/accept_order/<int:id>',methods=["GET","POST"])
@login_required
def AcceptOrder(id):
    if current_user.is_authenticated:
        if current_user.is_admin == 0:
            return redirect(url_for("main.Index"))

    order = Reservation.query.filter_by(reserve_id=id).first()
    order.status = 'accepted'
    db.session.commit()
    flash("Accepted Successfully")
    return redirect(url_for("admin.Orders"))



@admin.route('/admin/complete_order/<int:id>',methods=["GET","POST"])
@login_required
def CompleteOrder(id):
    if current_user.is_authenticated:
        if current_user.is_admin == 0:
            return redirect(url_for("main.Index"))

    order = Reservation.query.filter_by(reserve_id=id).first()
    order.status = 'completed'
    db.session.commit()
    flash("Completed Successfully")
    return redirect(url_for("admin.Orders"))


@admin.route('/admin/delete_order/<int:id>',methods=["GET","POST"])
@login_required
def DeleteOrder(id):
    if current_user.is_authenticated:
        if current_user.is_admin == 0:
            return redirect(url_for("main.Index"))

    order = Reservation.query.filter_by(reserve_id=id).first()
    db.session.delete(order)
    db.session.commit()
    flash("Deleted Successfully")
    return redirect(url_for("admin.Orders"))



@admin.route('/admin/devices',methods=['GET','POST'])
@login_required
def Device():
    if current_user.is_authenticated:
        if current_user.is_admin == 0:
            return redirect(url_for("main.Index"))
    
    form = AddDeviceForm()
    if request.method == 'POST' and form.validate():
        device = Devices(DeviceName=form.DeviceName.data,Manufacture=form.Manufacture.data,ProductType=form.ProductType.data,OS=form.OS.data)
        db.session.add(device)
        db.session.commit()
        flash("Device Added Successfully")
        return redirect(url_for('admin.Device'))

    api = requests.get("http://127.0.0.1:5000/apis/get_all_devices")
    data= api.text
    parse = json.loads(data)
    return render_template('admin/devices.html',form=form,devices=parse['devices'])




@admin.route('/admin/delete_device/<int:id>',methods=["GET","POST"])
@login_required
def DeleteDevice(id):
    if current_user.is_authenticated:
        if current_user.is_admin == 0:
            return redirect(url_for("main.Index"))

    device = Devices.query.filter_by(device_id=id).first()
    db.session.delete(device)
    db.session.commit()
    flash("Deleted Successfully")
    return redirect(url_for("admin.Device"))



@admin.route('/admin/delete_user/<int:id>',methods=["GET","POST"])
@login_required
def DeleteUser(id):
    if current_user.is_authenticated:
        if current_user.is_admin == 0:
            return redirect(url_for("main.Index"))

    user = Users.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    flash("Deleted Successfully")
    return redirect(url_for("admin.Index"))


@admin.route('/admin_logout',methods=["GET","POST"])
@login_required
def Logout():
    if current_user.is_authenticated:
        if current_user.is_admin == 0:
            return redirect(url_for("main.Index"))
    logout_user()
    return redirect(url_for("auth.Login"))