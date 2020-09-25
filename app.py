import os
from flask import (Flask, flash, render_template, redirect, request, url_for, flash)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import AddReviewForm

app = Flask(__name__)

if os.path.exists("env.py"):
    import env

app.config["MONGO_DBNAME"] = os.environ.get('MONGO_DBNAME')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)
app.secret_key = os.environ.get("SECRET_KEY")

#home page:

@app.route('/')
@app.route('/get_reviews')
def get_reviews():
    return render_template("reviews.html",Reviews=mongo.db.Reviews.find(), agencies=mongo.db.Agencies.find())

#company list:

@app.route('/get_companies')
def get_companies():
    return render_template("companylist.html", agencies=mongo.db.Agencies.find())

#adding new reviews:

#@app.route('/add_review', methods=["GET", "POST"])
#def add_review():
#    f = AddReviewForm()
#    if f.validate_on_submit():
#        review = {
#            "review_title": f.review_title.data,
#            "review_content": f.review_content.data,
#            "agency_name": request.form.get("agency_name")
#        }
#        mongo.db.Reviews.insert_one(review)
#        flash("Review Successfully Added")
#        return redirect(url_for("get_reviews"))
#
#    companies = mongo.db.Agencies.find().sort("agency_name", 1)
#    return render_template("addreview.html", companies=companies, form=f)

@app.route('/add_review', methods=["GET", "POST"])
def add_review():
    if request.method == "POST": 
        review = {
            "review_title": request.form.get("review_title"),
            "review_content": request.form.get("review_content"),
            "agency_name": request.form.get("agency_name"),
        }
        mongo.db.Reviews.insert_one(review)
        flash("Review Successfully Added")
        return redirect(url_for("get_reviews"))

    companies = mongo.db.Agencies.find().sort("agency_name", 1)
    return render_template("addreview.html", companies=companies)

#editing reviews:

@app.route("/edit_review/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    if request.method == 'POST':
        submit = {
            "agency_name": request.form.get("agency_name"),
            "review_title": request.form.get("review_title"),
            "review_content": request.form.get("review_content")
        }
        mongo.db.Reviews.update({"_id": ObjectId(review_id)}, submit)
        flash("Review Successfully Updated")

    review= mongo.db.Reviews.find_one({"_id": ObjectId(review_id)})
    companies = mongo.db.Agencies.find().sort("agency_name", 1)
    return render_template("editreview.html", review=review, companies=companies)

#deleting reviews:

@app.route("/remove_review/<review_id>")
def remove_review(review_id):
    review = mongo.db.Reviews.delete_one({"_id": ObjectId(review_id)})

    flash("Review deleted successfully")
    return redirect('get_reviews')
    
#adding new companies:

@app.route('/add_company', methods=["POST"])
def add_company():
    if request.method == "POST": 
        company = {
            "company_name": request.form.get("company_name"),
            "company_location": request.form.get("company_location"),
        }
        mongo.db.Reviews.insert_one(company)
        flash("Company Successfully Added")


#company list:

@app.route('/company_list')
def company_list():
    return render_template("companylist.html")

#company profile page:

@app.route('/company_profile')
def company_profile():
    return render_template("companyprofile.html", Reviews=mongo.db.Reviews.find())



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=(os.environ.get('PORT')),
        debug=True)
