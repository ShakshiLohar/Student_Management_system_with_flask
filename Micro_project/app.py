from flask import Flask, render_template, request, redirect, url_for
from database import get_connection

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        roll_no = int(request.form["roll"])
        name = request.form["name"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO students (roll_no, name)
            VALUES (?, ?)
        """, (roll_no, name))

        connection.commit()
        connection.close()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    connection.close()

    return render_template(
        "index.html",
        students=students
    )
    
@app.route("/add", methods=["GET", "POST"])
def add():

    success = None
    error = None

    if request.method == "POST":

        try:
            roll = int(request.form["roll"])
            name = request.form["name"]

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO students (roll_no, name)
                VALUES (?, ?)
            """, (roll, name))

            connection.commit()
            connection.close()

            success = "Student Added Successfully"

        except ValueError:
            error = "Roll number and marks must be numbers"

        except Exception as e:
            error = str(e)

    return render_template(
        "add.html",
        success=success,
        error=error
    )

@app.route("/manage_marks", methods=["GET", "POST"])
def manage_marks():
    success = request.args.get("success")
    error = request.args.get("error")

    connection = get_connection()
    cursor = connection.cursor()

    # Get all subjects
    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()

    # Add marks
    if request.method == "POST":
        try:
            roll_no = int(request.form["roll"])
            subject_id = int(request.form["subject"])
            marks = int(request.form["marks"])

            if marks < 0 or marks > 100:
                error = "Marks must be between 0 and 100"
            else:
                cursor.execute("""
                    INSERT INTO marks (roll_no, subject_id, marks)
                    VALUES (?, ?, ?)
                """, (roll_no, subject_id, marks))

                connection.commit()
                success = "Marks Added Successfully"

        except ValueError:
            error = "Invalid Input"

        except Exception:
            error = "Student or Subject Not Found"

    # Get existing marks
    cursor.execute("""
        SELECT
            marks.mark_id,
            students.roll_no,
            students.name,
            subjects.subject_name,
            marks.marks
        FROM marks
        JOIN students
            ON marks.roll_no = students.roll_no
        JOIN subjects
            ON marks.subject_id = subjects.subject_id
        ORDER BY students.roll_no
    """)

    marks_data = cursor.fetchall()

    connection.close()

    return render_template(
        "manage_marks.html",
        subjects=subjects,
        marks=marks_data,
        success=success,
        error=error
    )
    
@app.route("/update_marks", methods=["POST"])
def update_marks():
    try:
        mark_id = int(request.form["mark_id"])
        new_marks = int(request.form["new_marks"])

        if new_marks < 0 or new_marks > 100:
            return redirect(
                url_for(
                    "manage_marks",
                    error="Marks must be between 0 and 100"
                )
            )

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE marks
            SET marks = ?
            WHERE mark_id = ?
        """, (new_marks, mark_id))

        connection.commit()

        if cursor.rowcount == 0:
            connection.close()
            return redirect(
                url_for(
                    "manage_marks",
                    error="Mark ID Not Found"
                )
            )

        connection.close()

        return redirect(
            url_for(
                "manage_marks",
                success="Marks Updated Successfully"
            )
        )

    except ValueError:
        return redirect(
            url_for(
                "manage_marks",
                error="Invalid Input"
            )
        )
        
@app.route("/delete_marks", methods=["POST"])
def delete_marks():
    try:
        mark_id = int(request.form["mark_id"])

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM marks
            WHERE mark_id = ?
        """, (mark_id,))

        connection.commit()

        if cursor.rowcount == 0:
            connection.close()
            return redirect(
                url_for(
                    "manage_marks",
                    error="Mark ID Not Found"
                )
            )

        connection.close()

        return redirect(
            url_for(
                "manage_marks",
                success="Marks Deleted Successfully"
            )
        )

    except ValueError:
        return redirect(
            url_for(
                "manage_marks",
                error="Invalid Mark ID"
            )
        )


    
@app.route("/marks")
def view_marks():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            students.roll_no,
            students.name,
            subjects.subject_name,
            marks.marks
        FROM marks
        JOIN students
            ON marks.roll_no = students.roll_no
        JOIN subjects
            ON marks.subject_id = subjects.subject_id
        ORDER BY students.roll_no
    """)

    marks = cursor.fetchall()

    connection.close()

    return render_template(
        "marks.html",
        marks=marks
    )
    
@app.route("/result", methods=["GET"])
def result():

    roll_no = request.args.get("roll_no")

    if not roll_no:
        return "Roll Number is required"

    try:
        roll_no = int(roll_no)

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                students.roll_no,
                students.name,
                subjects.subject_name,
                marks.marks
            FROM marks
            JOIN students
                ON marks.roll_no = students.roll_no
            JOIN subjects
                ON marks.subject_id = subjects.subject_id
            WHERE students.roll_no = ?
        """, (roll_no,))

        result_data = cursor.fetchall()

        connection.close()

        return render_template(
            "result.html",
            result_data=result_data
        )

    except ValueError:
        return "Invalid Roll Number"

@app.route("/display")
def display():

    connection = get_connection()
    cursor=connection.cursor()
    cursor.execute("select * from students")
    students = cursor.fetchall()
    connection.close()

    return render_template(
        "display.html",
        students=students
    )

@app.route("/search", methods=["GET", "POST"])
def search():
    
    found=None
    error=None
    if request.method=="POST":
        try:
            roll=int(request.form["roll"])
            
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("select * from students where roll_no = ?",(roll,))
            found = cursor.fetchone()
            connection.close()
            
            if found is None:
                error="Student Not Found"
                
        except ValueError:
            error="Invalid Input"
            
        
    return render_template("search.html",student=found,error=error)

@app.route("/update", methods=["GET", "POST"])
def update():

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

                if field == "marks":
                    new_value = int(new_value)
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute(f"""
                    UPDATE students
                    SET {field} = ?
                    WHERE roll_no = ?
                """,(new_value,roll))
                connection.commit()
                
                if cursor.rowcount == 0:
                    error = "Student Not Found"
                else:
                    success = "Student Updated Successfully"

                connection.close()

        except ValueError:
            error="Invalid Input"
    
    return render_template("update.html",student=success,error=error)

@app.route("/delete", methods=["GET", "POST"])
def delete():

    success = None
    error = None

    if request.method == "POST":

        try:

            roll = int(request.form["roll"])

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                "DELETE FROM students WHERE roll_no = ?",
                (roll,)
            )

            connection.commit()

            if cursor.rowcount == 0:
                error = "Student Not Found"
            else:
                success = "Student Deleted Successfully"

            connection.close()

        except ValueError:
            error = "Invalid Input"


    return render_template("delete.html",success=success,error=error)



@app.route("/subjects", methods=["GET", "POST"])
def subjects():

    success = None
    error = None

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        subject_name = request.form["subject_name"].strip()

        if not subject_name:
            error = "Subject name cannot be empty"

        else:
            try:
                cursor.execute("""
                    INSERT INTO subjects (subject_name)
                    VALUES (?)
                """, (subject_name,))

                connection.commit()

                success = "Subject Added Successfully"

            except Exception as e:
                error = str(e)

    cursor.execute("""
        SELECT *
        FROM subjects
        ORDER BY subject_id
    """)

    subjects_data = cursor.fetchall()

    connection.close()

    return render_template(
        "subjects.html",
        subjects=subjects_data,
        success=success,
        error=error
    )
    
@app.route("/update_subject/<int:subject_id>", methods=["GET", "POST"])
def update_subject(subject_id):
    connection = get_connection()
    cursor = connection.cursor()

    # Get current subject
    cursor.execute("""
        SELECT *
        FROM subjects
        WHERE subject_id = ?
    """, (subject_id,))

    subject = cursor.fetchone()

    if subject is None:
        connection.close()
        return "Subject Not Found"

    # Update subject
    if request.method == "POST":
        subject_name = request.form["subject_name"].strip()

        if not subject_name:
            connection.close()
            return "Subject name cannot be empty"

        cursor.execute("""
            UPDATE subjects
            SET subject_name = ?
            WHERE subject_id = ?
        """, (subject_name, subject_id))

        connection.commit()
        connection.close()

        return redirect(url_for("subjects"))

    connection.close()

    return render_template(
        "update_subject.html",
        subject=subject
    )
    
@app.route("/delete_subject/<int:subject_id>", methods=["POST"])
def delete_subject(subject_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM subjects
        WHERE subject_id = ?
    """, (subject_id,))

    connection.commit()
    connection.close()

    return redirect(url_for("subjects"))

@app.route("/attendance", methods=["GET", "POST"])
def attendance():
    success = None
    error = None

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":
        try:
            roll_no = int(request.form["roll_no"])
            date = request.form["date"]
            status = request.form["status"]

            cursor.execute("""
                INSERT INTO attendance (roll_no, date, status)
                VALUES (?, ?, ?)
            """, (roll_no, date, status))

            connection.commit()

            success = "Attendance Marked Successfully"

        except ValueError:
            error = "Invalid Roll Number"

        except Exception as e:
            error = str(e)

    cursor.execute("""
        SELECT
            attendance.attendance_id,
            students.roll_no,
            students.name,
            attendance.date,
            attendance.status
        FROM attendance
        JOIN students
            ON attendance.roll_no = students.roll_no
        ORDER BY attendance.date DESC
    """)

    attendance_data = cursor.fetchall()

    connection.close()

    return render_template(
        "attendance.html",
        attendance=attendance_data,
        success=success,
        error=error
    )

app.run(debug=True)