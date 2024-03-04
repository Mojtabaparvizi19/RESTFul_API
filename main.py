from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from random import *

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=True)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random", methods=["GET"])
def get_random_cafe():
    results = db.session.execute(db.Select(Cafe)).scalars().all()
    random_cafe = choice(results)

    information = {
        random_cafe.name: {
            "can_take_calls": random_cafe.can_take_calls,
            "coffee_price": random_cafe.coffee_price,
            "has_sockets": random_cafe.has_sockets,
            "has_toilet": random_cafe.has_toilet,
            "has_wifi": random_cafe.has_wifi,
            "id": random_cafe.id,
            "img_url": random_cafe.img_url,
            "location": random_cafe.location,
            "map_url": random_cafe.map_url,
            "seats": random_cafe.seats
        }
    }
    return jsonify(information)


@app.route("/all")
def get_all_cafe():
    # list_of_cafe = []
    # results = db.session.execute(db.Select(Cafe)).scalars().all()
    # for item in results:
    #     list_of_cafe.append(item.to_dict())
    # return jsonify(list_of_cafe)
    information = {}
    results = db.session.execute(db.Select(Cafe)).scalars().all()
    for item in results:
        information[item.name] = {
            "can_take_calls": item.can_take_calls,
            "coffee_price": item.coffee_price,
            "has_sockets": item.has_sockets,
            "has_toilet": item.has_toilet,
            "has_wifi": item.has_wifi,
            "id": item.id,
            "img_url": item.img_url,
            "location": item.location,
            "map_url": item.map_url,
            "seats": item.seats
        }
    return jsonify(information)


@app.route("/search")
def search():
    location_query = request.args.get("loc")
    cafe = db.session.execute(db.Select(Cafe).where(Cafe.location == location_query)).scalars().all()
    if len(cafe) != 0:
        dictionary = {}
        for item in cafe:
            dictionary[item.name] = {
                "can_take_calls": item.can_take_calls,
                "coffee_price": item.coffee_price,
                "has_sockets": item.has_sockets,
                "has_toilet": item.has_toilet,
                "has_wifi": item.has_wifi,
                "id": item.id,
                "img_url": item.img_url,
                "location": item.location,
                "map_url": item.map_url,
                "seats": item.seats
            }
        return jsonify(dictionary)

    else:

        return jsonify(error={f"Not Found": f"Sorry, We don't have a cafe at {location_query} location"}), 404



# HTTP GET - Read Record



# HTTP POST - Create Record
@app.route("/add",methods=["POST"])
def add():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify({"response": {"success": "The cafe  was 'added'.!"}})


@app.route("/update_price/<int:cafe_id>", methods=["PATCH", "POST"])
def update_price(cafe_id):
    new_price = request.args.get("price")
    all_cafe = db.session.execute(db.Select(Cafe)).scalars().all()
    all_id = [cafe.id for cafe in all_cafe]
    if cafe_id in all_id:
        cafe = db.get_or_404(Cafe, cafe_id)
        print(cafe.name)
        cafe.coffee_price = new_price
        db.session.commit()
        response = {
            "success": "The price has been Updated! :D"
        }
        return jsonify(response)
    else:
        print("failed")
        error = {
            "error ": "no cafe was found"
        }
        return jsonify(error), 404


@app.route("/remove/<int:cafe_id>", methods=["DELETE", "POST"])
def remove_cafe(cafe_id):
    API_key = request.args.get("api-key")
    if API_key == "mojtabaparvizi19":
        all_cafe = db.session.execute(db.Select(Cafe)).scalars().all()
        all_id = [cafe.id for cafe in all_cafe]
        if cafe_id in all_id:
            cafe_to_remove = db.get_or_404(Cafe, cafe_id)
            db.session.delete(cafe_to_remove)
            db.session.commit()
            response = {
                "success": "The cafe has been removed"
            }
            return jsonify(response), 200
        else:
            print("Failed! Id doesnt exist")
            error = {
                "failed": f"{cafe_id} does not exist"
            }
            return jsonify(error), 404
    else:
        response = {
            "failed!": "Not a valid APi"
        }
        return jsonify(response), 403


if __name__ == '__main__':
    app.run(debug=True)
