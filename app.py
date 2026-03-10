from flask import Flask, render_template, request, jsonify
import csv
import os
from datetime import datetime
import base64

app = Flask(__name__)

CSV_FILE="attendance.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE,"w",newline="") as f:
        writer=csv.writer(f)
        writer.writerow(["Name","Roll","Date","Time"])


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register_page")
def register_page():
    return render_template("register.html")


@app.route("/attendance_page")
def attendance_page():
    return render_template("attendance.html")


@app.route("/table_page")
def table_page():
    return render_template("table.html")


@app.route("/percentage_page")
def percentage_page():
    return render_template("percentage.html")


@app.route("/register_user",methods=["POST"])
def register_user():

    data=request.get_json()

    name=data["name"]
    roll=data["roll"]
    image=data["image"]

    img_data=image.split(",")[1]

    img_bytes=base64.b64decode(img_data)

    if not os.path.exists("student_images"):
        os.mkdir("student_images")

    with open(f"student_images/{name}_{roll}.png","wb") as f:
        f.write(img_bytes)

    return jsonify({"message":"Student Registered"})


@app.route("/mark_attendance",methods=["POST"])
def mark():

    data=request.get_json()

    name=data.get("name","Unknown")
    roll=data.get("roll","0")

    date=datetime.now().strftime("%Y-%m-%d")
    time=datetime.now().strftime("%H:%M:%S")

    with open(CSV_FILE,"a",newline="") as f:

        writer=csv.writer(f)
        writer.writerow([name,roll,date,time])

    return jsonify({"message":"Attendance Marked"})


@app.route("/get_attendance")
def get_attendance():

    data=[]

    with open(CSV_FILE,"r") as f:

        reader=csv.reader(f)
        next(reader)

        for row in reader:
            data.append(row)

    return jsonify({"attendance":data})


@app.route("/percentage")
def percentage():

    data={}
    total_days=set()

    with open(CSV_FILE,"r") as f:

        reader=csv.reader(f)
        next(reader)

        for row in reader:

            name=row[0]
            date=row[2]

            total_days.add(date)

            if name in data:
                data[name]+=1
            else:
                data[name]=1

    total=len(total_days)

    result=[]

    for name,present in data.items():

        percent=round((present/total)*100,2)

        result.append([name,percent])

    return jsonify({"percentage":result})


if __name__=="__main__":
    app.run()