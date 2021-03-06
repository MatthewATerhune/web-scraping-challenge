#app.py
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find record of data from the mongo database
    mars_data= mongo.db.collection.find_one()

    return render_template("index.html", mars_data=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()

    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)