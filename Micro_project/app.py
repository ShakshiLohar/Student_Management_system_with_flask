from flask import Flask, render_template,request
import json
import os

app = Flask(__name__)

student = []

def load_data():

    global student

    path = os.path.join(os.path.dirname(__file__),"student.json" )

    try:

        with open(path, "r") as file:

            student = json.load(file)

    except:

        student = []

def save_data():

    path = os.path.join(os.path.dirname(__file__),"student.json")

    with open(path, "w") as file:

        json.dump(student, file)

@app.route("/", methods=["GET", "POST"])
def home():

    load_data()

    if request.method == "POST":

        roll_no = int(request.form["roll"])

        name = request.form["name"]

        marks = int(request.form["marks"])

        student_data = {
            "Roll_no": roll_no,
            "name": name,
            "marks": marks
        }

        student.append(student_data)

        save_data()

    return render_template(
        "index.html",
        students=student
    )

@app.route("/add", methods=["GET", "POST"])
def add():

    load_data()

    if request.method == "POST":
            try:

                roll = int(request.form["roll"])

                name = request.form["name"]

                marks = int(request.form["marks"])
                if not roll or not name or not marks:
                    return render_template(
                    "add.html",
                    error="All fields are required"
                    )

                student_data = {
                "Roll_no": roll,
                "name": name,
                "marks": marks}

                student.append(student_data)

                save_data()
                return "Student Added Successfully"
            except ValueError:
                return render_template(
                "add.html",
                error="Invalid Input")
    return render_template("add.html")


@app.route("/display")
def display():

    load_data()

    return render_template(
        "display.html",
        students=student
    )

@app.route("/search", methods=["GET", "POST"])
def search():
    load_data()

    found=None
    error=None
    if request.method=="POST":
        try:
            roll=int(request.form["roll"])
            for i in student:
                if i["Roll_no"]==roll:
                    found=i
                    break
            if found is None:

                error = "Student Not Found"

        except ValueError:

            error = "Invalid Input"
        
    return render_template("search.html",student=found,error=error)

@app.route("/update", methods=["GET", "POST"])
def update():
    load_data()
    success=None
    error=None
    if request.method=="POST":
        try:
            roll = int(request.form["roll"])

            field = request.form["field"].lower()

            new_value = request.form["value"]

            if field not in ["name", "marks"]:

                error = "Invalid Field"

            else:

                found = False

                for i in student:

                    if i["Roll_no"] == roll:

                        if field == "marks":

                            new_value = int(new_value)

                        i[field] = new_value

                        save_data()

                        success = "Student Updated Successfully"

                        found = True
                        break

                if found == False:

                    error = "Student Not Found"

        except ValueError:
            error="Invalid Input"
    
    return render_template("update.html",student=success,error=error)

@app.route("/delete", methods=["GET", "POST"])
def delete():

    load_data()

    success = None
    error = None

    if request.method == "POST":

        try:

            roll = int(request.form["roll"])

            found = False

            for i in student:

                if i["Roll_no"] == roll:

                    student.remove(i)

                    save_data()

                    success = "Student Deleted Successfully"

                    found = True
                    break

            if found == False:

                error = "Student Not Found"

        except ValueError:

            error = "Invalid Input"

    return render_template("delete.html",success=success,error=error)

app.run(debug=True)
