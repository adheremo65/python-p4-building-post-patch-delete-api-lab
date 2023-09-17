#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
# with app.app_context():
#     BakedGood.query.delete()
#     Bakery.query.delete()
#     db.session.commit()

# @app.route('/')
# def home():
#     return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

# @app.route('/bakeries')
# def bakeries():

#     bakeries = Bakery.query.all()
#     bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

#     response = make_response(
#         bakeries_serialized,
#         200
#     )
#     return response

# @app.route('/bakeries/<int:id>')
# def bakery_by_id(id):

#     bakery = Bakery.query.filter_by(id=id).first()
#     bakery_serialized = bakery.to_dict()

#     response = make_response(
#         bakery_serialized,
#         200
#     )
#     return response

# @app.route('/baked_goods/by_price')
# def baked_goods_by_price():
#     baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
#     baked_goods_by_price_serialized = [
#         bg.to_dict() for bg in baked_goods_by_price
#     ]
    
#     response = make_response(
#         baked_goods_by_price_serialized,
#         200
#     )
#     return response

# @app.route('/baked_goods/most_expensive')
# def most_expensive_baked_good():
#     most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
#     most_expensive_serialized = most_expensive.to_dict()

#     response = make_response(
#         most_expensive_serialized,
#         200
#     )
#     return response
@app.route("/baked_goods",methods = ["GET","POST"])
def baked_goods():
    
    bakee_goods = BakedGood.query.all()
    if request.method == "POST":
        new_baked_goods = BakedGood(
            name = request.form.get("name"),
            price = request.form.get("price"),
            created_at = request.form.get("created_at"),
            updated_at = request.form.get("updated_at")
        )
    db.session.add(new_baked_goods)
    db.session.commit()
    new_bakeed_dict = new_baked_goods.to_dict()
    response = make_response(new_bakeed_dict,201)
    return response


@app.route("/bakeries/<int:id>", methods = ["GET","POST","DELETE","PATCH"])
def bakerie(id):
    get_bakeries = Bakery.query.filter(Bakery.id == id).first()
    if request.method == "PATCH":
        for attr in request.form:
            setattr(get_bakeries, attr, request.form[attr])
        db.session.add(get_bakeries)
        db.session.commit()
    bakeries_dict = get_bakeries.to_dict()
    response = make_response(bakeries_dict, 200)
    return response


@app.route("/baked_goods/<int:id>", methods = ["DELETE","PATCH"])
def deleted(id):
    baked_delted = BakedGood.query.filter_by(id == id).first()
    if baked_delted:
        request.method == "DELETE"
        db.session.delete(baked_delted)
        db.session.commit()
    res_body = {
        
        "message": "record successfully deleted"
    }
    response = make_response(jsonify(res_body), 200)
    return response
    




        
      



if __name__ == '__main__':
    app.run(port=5555, debug=True)
