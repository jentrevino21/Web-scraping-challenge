from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient
import scrape_mars

app = Flask(__name__)


myclient = MongoClient("mongodb://localhost:27017")
mars_databse = myclient["mars_databse"]

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_databse"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_db = mongo.db.mars.find_one() # mars_data = mongo.data base name. collection
    return render_template("index.html", mars_data = mars_db) #Variable to pass = mars_data

@app.route("/scrape")
def scraper():
    mars_info = mongo.db.mars #Current collection
    mars_data = scrape_mars.scrapper() #calls the scrape function
    mars_info.update({}, mars_data, upsert=True) #update any current listing {} with the new listing data.
    return redirect("/", code=302) #instead of returning a html or render, we are returning a "/" to direct to main page. code = 302 --> redirect.


if __name__ == "__main__":
    app.run(debug=True)