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
def get_reviews(agency_id):
    company = mongo.db.Agencies.find_one({"_id": ObjectId(agency_id)})
    return render_template("reviews.html",reviews=mongo.db.Reviews.find(), agencies=mongo.db.Agencies.find(), company=company, name=company['agency_name'], location=company['agency_location'])

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

# @app.route('/add_review', methods=["GET", "POST"])
# def add_review():
#     if request.method == "POST": 
#         review = {
#             "review_title": request.form.get("review_title"),
#             "review_content": request.form.get("review_content"),
#             "agency_name": request.form.get("agency_name"),
#         }
#         mongo.db.Reviews.insert_one(review)
#         flash("Review Successfully Added")
#         return redirect(url_for("get_reviews"))

#     companies = mongo.db.Agencies.find().sort("agency_name", 1)
#     return render_template("addreview.html", companies=companies)

@app.route('/add_review', methods=["GET", "POST"])
def add_review():
    if request.method == "POST":
        formatted_agency_name = request.form.get("agency_name").split(', ')[0]  # Get just the name, ignore the location
        company = mongo.db.Agencies.find_one({"agency_name": formatted_agency_name})   # Load the company from the name (also making sure it exists)
        review = {
            "review_title": request.form.get("review_title"),
            "review_content": request.form.get("review_content"),
            "agency": ObjectId(company["_id"]),
            "positive_review": request.form.get("positive_review"),
            "negative_review": request.form.get("negative_review")
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
    mongo.db.Reviews.delete_one({"_id": ObjectId(review_id)})

    flash("Review deleted successfully")
    print(review_id)
    return render_template("reviews.html",reviews=mongo.db.Reviews.find())

#adding new companies:


@app.route('/add_company', methods=["GET", "POST"])
def add_company():
    if request.method == "POST": 
        company = {
           "agency_name": request.form.get("agency_name"),
           "agency_location": request.form.get("agency_location"),
       }
        mongo.db.Agencies.insert_one(company)
        flash("Company Successfully Added")
    return render_template("addcompany.html")

#editing companies:

@app.route("/edit_company/<agency_id>", methods=["GET", "POST"])
def edit_company(agency_id):
    if request.method == 'POST':
        submit = {
            "agency_name": request.form.get("agency_name"),
            "agency_location": request.form.get("review_title"),
        }
        mongo.db.Agencies.update({"_id": ObjectId(agency_id)}, submit)
        flash("Company Successfully Updated")

    company= mongo.db.Agencies.find_one({"_id": ObjectId(agency_id)})
    companies = mongo.db.Agencies.find().sort("agency_name", 1)
    return render_template("editcompany.html", company=company, companies=companies)

#deleting companies:

@app.route("/remove_company/<agency_id>")
def remove_company(agency_id):
    mongo.db.Agencies.delete_one({"_id": ObjectId(agency_id)})

    flash("Company deleted successfully")
    return render_template("companylist.html",agencies=mongo.db.Agencies.find())



#company list:

@app.route('/company_list')
def company_list():
    return render_template("companylist.html")

#company profile page:

@app.route('/company_profile/<agency>')
def company_profile(agency):
    name = agency.split(', ')[0]
    location = agency.split(', ')[1]
    reviews = mongo.db.Reviews.find({"agency_name": agency})
    return render_template("companyprofile.html", reviews=reviews, name=name, location=location)

@app.route('/company_profile1/<agency_id>')
def company_profile1(agency_id):
    company = mongo.db.Agencies.find_one({"_id": ObjectId(agency_id)})
    reviews = mongo.db.Reviews.find({"agency_name": company['agency_name']})
    return render_template("companyprofile.html", company=company, name=company['agency_name'], location=company['agency_location'], reviews=reviews)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=(os.environ.get('PORT')),
        debug=True)
