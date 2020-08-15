from flask import Flask, render_template, jsonify, redirect
from splinter import Browser
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = PyMongo(app)
# conn="mongodb://localhost:27017"
# client=pymongo.MongoClient(conn)
# db=client.mars_app
# collection=db.mars
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    print(mars)
    return render_template("index.html", mars=mars)
    

@app.route("/scrape")
def scrape():
    mars_info = scrape_mars.scrape()
    mongo.db.mars.update({}, mars_info, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)




