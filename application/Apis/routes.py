from flask import Blueprint,redirect,flash,render_template,url_for,request,jsonify
from application.models import Users,Reservation,ReservationSchema,Devices,DeviceSchema,UserSchema
from application.Main.forms import BookDeviceForm
from application import db
import os
from sqlalchemy import text
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
apis  = Blueprint('apis', __name__,template_folder='templates',static_folder='../static',url_prefix="/apis")


@apis.route('/get_reservations')
@login_required
def Index():
    id = request.args.get('id')
    orders_query = text("SELECT * FROM reservation  LEFT JOIN devices on devices.device_id=reservation.device_id where client_id="+str(id))
    order_execute = db.engine.execute(orders_query)
    reservation_schema = ReservationSchema(many=True)
    orders = reservation_schema.dump(order_execute)
    return jsonify({
        "reservations":orders
    })


@apis.route('/get_all_devices',methods=['GET'])
def Device():
    
    device = Devices.query.all()
    device_schema = DeviceSchema(many=True)
    devices = device_schema.dump(device)
    return jsonify({
        "devices":devices
    })

@apis.route('/get_all_orders')
def AllOrders():
    orders_query = text("SELECT * FROM reservation LEFT JOIN users on users.id=client_id LEFT JOIN devices on devices.device_id=reservation.device_id")
    order_execute = db.engine.execute(orders_query)
    orders_schema = ReservationSchema(many=True)

    orders = orders_schema.dump(order_execute)
    return jsonify({
        "orders":orders
    })


        

@apis.route('/get_all_users')
def GetAllUsers():
    user_query = Users.query.filter_by(is_admin=0).all()
    users_schema = UserSchema(many=True)
    users = users_schema.dump(user_query)

    return jsonify({
        "users":users
    })



@apis.route("/get_your_booked_orders")
def GetYourBookedOrders():
    user_id = request.args.get("user_id")
    orders_query = text("SELECT * FROM reservation  LEFT JOIN devices on devices.device_id=reservation.device_id where client_id="+str(user_id))
    order_execute = db.engine.execute(orders_query)
    reservation_schema = ReservationSchema(many=True)
    orders = reservation_schema.dump(order_execute)

    return jsonify({
        "orders":orders
    })
