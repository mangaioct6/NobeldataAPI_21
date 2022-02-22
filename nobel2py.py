
from flask import Flask, render_template, json, request,redirect,url_for
import os

# creating an object for flask app
app = Flask(__name__)

# route decorator helps us to create an endpoints for our API
@app.route("/")
def hi():
    return "Nobel data!" 

# this route will print all our nobel data
@app.route("/all")
def nobel():
    json_url = os.path.join(app.static_folder,"","nobel.json")
    nobel_data = json.load(open(json_url))
    # render template always looks into templates folder
    return render_template('index.html', data=nobel_data)
    

@app.route("/add", methods=['POST','GET'])
def form():

    if request.method == 'POST':
        year = request.form['year']        
        category = request.form['category']
        laureants = request.form['laureants']
        noble_prize = { "year":year,
                    "category":category,
                    "laureants":laureants
                    }
        json_url = os.path.join(app.static_folder,"","nobel.json")
        with open(json_url,"r+") as file:
            nobel_data = json.load(file)
            nobel_data["prizes"].append(noble_prize)
            file.seek(0)
            json.dump(nobel_data, file)
        
        #Adding details
        #text_success = "Data successfully added: " + str(noble_prize)
        return redirect(url_for("get_year",year=year))
    else:    
         #form_url = os.path.join("templates","form.html")
         return render_template('form.html')#form_url#get_year(form_url)


@app.route("/year/<year>",methods=['GET'])
def get_year(year):
    json_url = os.path.join(app.static_folder,"","nobel.json")
    if request.method == 'GET':
        nobel_data = json.load(open(json_url))
        data = nobel_data['prizes']
        year = request.view_args['year']
        output_data = [i for i in data if i['year']==year]
        return render_template('index.html',data=output_data)
   
    
if __name__ == "__main__":
    app.run(debug = True)