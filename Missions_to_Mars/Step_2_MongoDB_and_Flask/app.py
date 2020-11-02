# /* -------- Flask ----------- */

from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars  # scrape_mars.py


# Create an instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route('/')
def index():
	mars_info = mongo.db.mars_info.find_one()
	return render_template("index.html", mars_info=mars_info)

@app.route('/scrape')
def scrape():
	mars_info = mongo.db.mars_info
	mars_data = scrape_mars.scrape_info()
	mars_info.update({}, mars_data, upsert=True)
	
	return redirect("/", code=302)


if __name__ == "__main__":
	app.run(debug=True)