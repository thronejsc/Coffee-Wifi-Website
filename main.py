from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
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
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)
# TODO: Add reviews and cafe desc


with app.app_context():
    db.create_all()


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe location', validators=[URL()])
    open_time = StringField('Open time', description="ex. 11AM/1:30PM", validators=[DataRequired()])
    closing_time = StringField('Closing time', description="ex. 11AM/1:30PM", validators=[DataRequired()])
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
    submit = SubmitField('Submit')

# TODO: Make a form for reviews for a cafe


@app.route("/")
def home():
    return render_template("index.html")


# When user wants to see a specific cafe
# @app.route("/cafe/<int:cafe_id>", methods=["GET"])
# def show_post(cafe_id):
#     requested_cafe = db.get_or_404(Cafe, cafe_id)
#
#     return render_template("cafe.html", post=requested_cafe)


if __name__ == '__main__':
    app.run(debug=True)