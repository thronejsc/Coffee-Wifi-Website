from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, URL
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=True)
    img_url: Mapped[str] = mapped_column(String(500), nullable=True)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    open_time: Mapped[str] = mapped_column(String(10), nullable=True)
    closing_time: Mapped[str] = mapped_column(String(10), nullable=True)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    wifi_rating: Mapped[str] = mapped_column(String(1), nullable=False)
    outlet_rating: Mapped[str] = mapped_column(String(1), nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(10), nullable=True)
    coffee_rating: Mapped[str] = mapped_column(String(10), nullable=True)
    cafe_desc: Mapped[str] = mapped_column(String(1000), nullable=True)


with app.app_context():
    db.create_all()


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField('Map URL', validators=[URL()])
    img_url = StringField('Image URL')
    location = StringField('Cafe location', description='ex. City or Country', validators=[DataRequired()])
    seats = StringField('Number of seats', description='ex. (10, 10-15, 20+ )', validators=[DataRequired()])
    open_time = StringField('Open time', description="ex. 11AM/1:30PM", validators=[DataRequired()])
    closing_time = StringField('Closing time', description="ex. 11AM/1:30PM", validators=[DataRequired()])
    can_take_calls = BooleanField('Can Take Calls')
    has_toilet = BooleanField('Has Toilet/Restroom')
    coffee_price = StringField('Coffee price', description='Estimate or minimum price', validators=[DataRequired()])
    coffee_rating = SelectField(label="Coffee Rating",
                                choices=[('1', '☕️'), ('2', '☕️☕️'), ('3', '☕️☕️☕️'), ('4', '☕️☕️☕️☕️'),
                                         ('5', '☕️☕️☕️☕️☕️')],
                                validators=[DataRequired()])
    wifi_rating = SelectField(label="WiFi Rating",
                              choices=[('1', '💪'), ('2', '💪💪'), ('3', '💪💪💪'), ('4', '💪💪💪💪'), ('5', '💪💪💪💪💪'),
                                       ('0', '✘')],
                              validators=[DataRequired()])
    outlet_rating = SelectField(label="Outlet Rating",
                                choices=[('1', '🔌'), ('2', '🔌🔌'), ('3', '🔌🔌🔌'), ('4', '🔌🔌🔌🔌'), ('5', '🔌🔌🔌🔌🔌'),
                                         ('0', '✘')],
                                validators=[DataRequired()])
    cafe_desc = TextAreaField(label='Cafe Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


# TODO: Make a form for reviews for a cafe


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cafe/<cafe_name>")
def cafe(cafe_name):
    cafe_name = cafe_name.replace('-', ' ')
    requested_cafe = db.session.execute(db.select(Cafe).where(Cafe.name == cafe_name)).scalar()
    wifi_rating = int(requested_cafe.wifi_rating) if requested_cafe.wifi_rating else 0
    outlet_rating = int(requested_cafe.outlet_rating) if requested_cafe.outlet_rating else 0
    coffee_rating = int(requested_cafe.coffee_rating)
    print(wifi_rating)
    print(type(wifi_rating))
    return render_template("cafe.html", cafe_name=cafe_name, wifi_rating=wifi_rating, outlet_rating=outlet_rating, coffee_rating=coffee_rating, cafe=requested_cafe)


@app.route('/all-cafes-json')
def all_cafe_json():
    cafes = []
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()

    if all_cafes:
        for cafe in all_cafes:
            cafe_json = {
                "id": cafe.id,
                "name": cafe.name,
                "map_url": cafe.map_url,
                "location": cafe.location,
                "seats": cafe.seats,
                "has_toilet": cafe.has_toilet,
                "has_wifi": cafe.has_wifi,
                "has_sockets": cafe.has_sockets,
                "can_take_calls": cafe.can_take_calls,
                "coffee_price": cafe.coffee_price
            }
            cafes.append(cafe_json)

        return jsonify(cafes)
    else:
        not_found = {
            "error": {
                "Not Found": "There are no cafes in the database"
            }
        }
        return not_found


@app.route('/all')
def all_cafes():
    # column_names = Cafe.__table__.columns.keys()
    column_names = ['Name', 'Location', 'Map URL', 'Seats', 'WiFi Connection', 'Toilet', 'Sockets Availability', 'Can take calls', 'Coffee Rating']
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    modified_cafes = []
    for cafe in all_cafes:
        modified_cafe = {
            "name": cafe.name,
            "map_url": cafe.map_url,
            "location": cafe.location,
            "seats": cafe.seats,
            "has_toilet": "Yes" if cafe.has_toilet else "No",
            "wifi_rating": cafe.wifi_rating,
            "outlet_rating": cafe.outlet_rating,
            "can_take_calls": "Yes" if cafe.can_take_calls else "No",
            "coffee_rating": cafe.coffee_rating
        }
        modified_cafes.append(modified_cafe)

    return render_template("all_cafes.html", column_names=column_names, cafes=modified_cafes)


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            open_time=form.open_time.data,
            closing_time=form.closing_time.data,
            seats=form.seats.data,
            has_toilet=form.has_toilet.data,
            wifi_rating=form.wifi_rating.data,
            outlet_rating=form.outlet_rating.data,
            can_take_calls=form.can_take_calls.data,
            coffee_price=form.coffee_price.data,
            coffee_rating=form.coffee_rating.data,
            cafe_desc=form.cafe_desc.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("all_cafes"))
    return render_template('add.html', form=form)






if __name__ == '__main__':
    app.run(debug=True)