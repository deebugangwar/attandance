from flask import Flask, render_template, jsonify, request, send_file
import register
import train
import recognize
import csv
import os
from datetime import datetime

app = Flask(__name__)



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



@app.route("/download_csv")
def download_csv():

    file_path = "attendance.csv"

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)

    return "No attendance file found!"



@app.route("/register_user")
def register_user():
    name = request.args.get("name")
    roll = request.args.get("roll")

    result = register.register_face(name, roll)
    train.train_model()

    return jsonify({"message": result})


@app.route("/percentage")
def percentage():

    data = {}
    total_days = set()

    if os.path.exists("attendance.csv"):

        with open("attendance.csv", "r") as f:
            reader = csv.reader(f)
            next(reader, None)

            for row in reader:
                name = row[0]
                date = row[2]

                total_days.add(date)

                if name in data:
                    data[name] += 1
                else:
                    data[name] = 1

    total_working_days = len(total_days)

    result = []

    for name, present_days in data.items():
        percent = round((present_days / total_working_days) * 100, 2)
        result.append([name, percent])

    return jsonify({"percentage": result})


@app.route("/percentage_page")
def percentage_page():
    return render_template("percentage.html")









@app.route("/start_attendance")
def start_attendance():
    result = recognize.start_recognition()
    return jsonify({"message": result})



@app.route("/get_attendance")
def get_attendance():

    view_type = request.args.get("type") 
    data = []

    if os.path.exists("attendance.csv"):

        with open("attendance.csv", "r") as f:
            reader = csv.reader(f)
            next(reader, None)

            today = datetime.now().strftime("%Y-%m-%d")

            for row in reader:

                if view_type == "today":
                    if row[2] == today:
                        data.append(row)
                else:
                    data.append(row)

    return jsonify({"attendance": data})



if __name__ == "__main__":
    app.run(debug=True)