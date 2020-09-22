import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)


app.config["MONGO_DBNAME"] = 'myfirstdb'
app.config["MONGO_URI"] = 'mongodb+srv://Sebson1990:ZJREXjhCSSPZOp66@cluster0.g4vuv.mongodb.net/myfirstdb?ssl=true&ssl_cert_reqs=CERT_NONE'
mongo = PyMongo(app)

@app.route('/')
@app.route('/get_reviews')
def get_reviews():
    return render_template("reviews.html",Reviews=mongo.db.Reviews.find())

@app.route('/add_review')
def add_review():
    return render_template("addreview.html")

@app.route('/company_list')
def company_list():
    return render_template("companylist.html")

@app.route('/company_profile')
def company_profile():
    return render_template("companyprofile.html")

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=(os.environ.get('PORT')),
        debug=True)
