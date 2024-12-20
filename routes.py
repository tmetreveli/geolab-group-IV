from forms import AddProductForm, RegisterForm, LoginForm
import os
from flask import Flask, render_template, redirect, request, flash
from extensions import app
from models import Dog, User
from extensions import db
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/add", methods=["GET", "POST"])
@login_required
def addproduct():
    form = AddProductForm()
    if form.validate_on_submit():
        file = request.files['name']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        colour = form.colour.data
        mood = form.mood.data
        # dog = {"name": file.filename, "colour": colour, "mood": mood, "id": len(dogs)}
        dog = Dog(name=file.filename, colour=colour, mood=mood)
        db.session.add(dog)
        db.session.commit()
        # dogs.append(dog)

        return redirect("/show_products")
    return render_template("add_product.html", form=form)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):

    selected_dog = Dog.query.get(id)
    form = AddProductForm(name=selected_dog.name, colour=selected_dog.colour, mood=selected_dog.mood)

    print(selected_dog)
    if form.validate_on_submit():
        file = request.files['name']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        selected_dog.name = file.filename
        # print(selected_dog.name)
        selected_dog.mood = form.mood.data
        selected_dog.colour = form.colour.data
        db.session.commit()

        return redirect("/show_products")
    return render_template("add_product.html", form=form)

@app.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete(id):
    selected_dog = Dog.query.get(id)
    db.session.delete(selected_dog)
    db.session.commit()
    return redirect("/show_products")

# @app.route('/about_me')
# def greeting():
#     return "About me!"
#
# @app.route('/hello/<name>')
# def hello(name):
#     return f'hello {name}'

@app.route('/')
def show_products():
    dogs = Dog.query.all()
    # print(dogs)
    return render_template("index.html", dogs=dogs)

@app.route('/show_details/<int:dog_id>')
@login_required
def show_details(dog_id):
    selected_dog = Dog.query.get_or_404(dog_id)

    return render_template('details.html', dog=selected_dog)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.name.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("You successfully registered")
        return redirect("/")

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        print(user)
        if user and check_password_hash(user.password, form.password.data):
            flash("you logged in successfully")
            login_user(user)
            return redirect("/")
    return render_template("login.html", form=form)

@app.route("/logout", methods = ["GET", "POST"])
def logout():
    logout_user()
    flash("You logged out")
    return redirect("/")

# CRUD - create retrieve update delete