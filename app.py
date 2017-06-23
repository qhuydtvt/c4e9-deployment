"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
import mlab
from mongoengine import *
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

app.config["IMG_PATH"] = os.path.join(app.root_path, "static", "img")

# 1: Connect
mlab.connect()

# 2: Add data
class Item(Document):
    image = StringField()
    title = StringField()
    price = FloatField()

#item1 = Item(image="http://lpjp-dunebuggysrl.netdna-ssl.com/media/catalog/product/LCI/Bc/B4/swCYODnJGzU4cfprkDL-ifgzM1NNMNZY832oUV97ImRzIjoic21hbGxfaW1hZ2UiLCJmIjoiXC9DXC9GXC9JXC9MXC9QXC9EXC8wXC8wXC8yXC8yXC85XC81XC9DRklMUEQwMDIyOTUwX05SMDAwMl8xMDAuanBnIiwiZmEiOjEsImZmIjoxLCJmaCI6NjAxLCJmcSI6OTAsImZ0IjoxLCJmdyI6NDEwfQ~~.jpg",
             # title="Slip in",
             # price=813)
#
# item1.save()
#

###
# Routing for your application.
###

@app.route("/")
def index():
    return render_template("index.html", items=Item.objects())


@app.route("/add-lingerie", methods=["GET", "POST"])
def add_lingerie():
    if request.method == "GET": # Client asking for FORM
        return render_template("add_item.html")
    elif request.method == "POST": # Client submitting FORM
        # 1. Get data from FORM (Title, Image, Price)
        # Validate input
        form = request.form
        title = form["title"]
        price = form["price"]

        image = request.files["image"]
        filename = secure_filename(image.filename) # make image name machine-friendly
        save_location = os.path.join(app.config["IMG_PATH"], filename)

        image.save(save_location)

        # if not isinstance(price, float):
        #     return redirect(url_for("add_lingerie"))
        #
        # # 2. Create data (database)
        item = Item(
            title=title,
            image="/images/{0}".format(filename),
            price=price)

        item.save()

        # # 3. Redirect

        return redirect(url_for("index"))


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route("/images/<image_name>")
def image(image_name):
    # file not found
    # send_from_directory(app.config["IMG_PATH"], ".png")
    return send_from_directory(app.config["IMG_PATH"], image_name)


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=False)
