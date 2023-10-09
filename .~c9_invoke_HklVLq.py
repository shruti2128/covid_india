import os
import requests
import json
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)


app.config["TEMPLATES_AUTO_RELOAD"] = True
url1 = "https://covid-19-india-data-by-zt.p.rapidapi.com/GetIndiaStateCodesAndNames"
headers1 = {
        'x-rapidapi-key': "3266c6d5abmshfe4d6aae0d7c3f5p1d105ajsn8f95315d6d96",
        'x-rapidapi-host': "covid-19-india-data-by-zt.p.rapidapi.com" }
response1 = requests.request("GET", url1, headers=headers1)
r1 =json.loads(response1.text)
s = []
for i in r1["data"]:
    s.append(i["name"])

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cases",methods=["GET", "POST"])
def cases():
   state = request.form.get("state")
   dist = request.form.get("district")
   if request.method == "POST":
       if not state or state not in s:
           apology = "Incorrect state"
           return render_template("apology.html", apology = apology)
       if not dist:
          url = "https://covid-19-india-data-by-zt.p.rapidapi.com/GetIndiaStateWiseData"

          headers = {
          'x-rapidapi-key': "3266c6d5abmshfe4d6aae0d7c3f5p1d105ajsn8f95315d6d96",
          'x-rapidapi-host': "covid-19-india-data-by-zt.p.rapidapi.com"
          }

          response = requests.request("GET", url, headers=headers)
          r =json.loads(response.text)
          for i in r["data"]:
           if state == i['name'][:
               return render_template("case1.html",i = i)
       url = "https://covid-19-india-data-by-zt.p.rapidapi.com/GetIndiaDistrictWiseDataForState"

       headers = {
       'x-rapidapi-key': "3266c6d5abmshfe4d6aae0d7c3f5p1d105ajsn8f95315d6d96",
       'x-rapidapi-host': "covid-19-india-data-by-zt.p.rapidapi.com"
       }
       for i in r1["data"]:
           if state == i['name']:
              querystring = {"statecode": i['code'] }

       response = requests.request("GET", url, headers=headers, params=querystring)

       r =json.loads(response.text)
       for i in r["data"]:
           if dist == i['name']:
               print(i)
               return render_template("case.html",i = i, s = s, state = state)
   else:
     return render_template("cases.html", s = s, state = state)

@app.route("/vaccine",methods = ["GET", "POST"])
def vaccine():
    if request.method == "POST":
     url = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/api-covid-data/reports/IND"

     headers = {
      'x-rapidapi-key': "3266c6d5abmshfe4d6aae0d7c3f5p1d105ajsn8f95315d6d96",
      'x-rapidapi-host': "vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com"
     }

     response = requests.request("GET", url, headers=headers)

     print(response.text)
    
    else:
        return render_template("vaccine.html")

@app.route("/zones",methods = ["GET", "POST"])
def zones():
     if request.method == "POST":
         state = request.form.get("state")
         url = "https://covid-19-india-data-by-zt.p.rapidapi.com/GetIndiaDistrictWiseZonesForState"
         headers = {
             'x-rapidapi-key': "3266c6d5abmshfe4d6aae0d7c3f5p1d105ajsn8f95315d6d96",
             'x-rapidapi-host': "covid-19-india-data-by-zt.p.rapidapi.com"
         }
         for i in r1["data"]:
           if state == i['name']:
              querystring = {"statecode": i['code'] }

         response = requests.request("GET", url, headers=headers, params=querystring)
         r =json.loads(response.text)["data"]
         return render_template("zone1.html",r = r, state = state)
     
     else:
        return render_template("zones.html")

@app.route("/tests",methods = ["GET", "POST"])
def tests():
    if request.method == "POST":
        state = request.form.get("state")
        url = "https://covid-19-india-data-by-zt.p.rapidapi.com/GetIndiaAllTestedSamplesDataForState"
        headers = {
         'x-rapidapi-key': "3266c6d5abmshfe4d6aae0d7c3f5p1d105ajsn8f95315d6d96",
         'x-rapidapi-host': "covid-19-india-data-by-zt.p.rapidapi.com"
        }
        for i in r1["data"]:
           if state == i['name']:
              querystring = {"statecode": i['code'] }

        response = requests.request("GET", url, headers=headers, params=querystring)


        r = json.loads(response.text)["records"]
        r = r[len(r)-1]['cases']['data']
        return render_template("test1.html",r = r)
    else:
       return render_template("tests.html") 
     