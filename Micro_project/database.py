import sqlite3

def get_connection():
    connection = sqlite3.connect("student.db")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_table():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll_no INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO subjects (subject_id, subject_name)
        VALUES
            (1, 'DBMS'),
            (2, 'Data Structures'),
            (3, 'Operating System'),
            (4, 'Computer Networking'),
            (5, 'Python')
    """)
    

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
    mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    marks INTEGER NOT NULL,

    FOREIGN KEY (roll_no) REFERENCES students(roll_no),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),

    UNIQUE (roll_no, subject_id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no INTEGER NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('Present', 'Absent')),
        FOREIGN KEY (roll_no) REFERENCES students(roll_no),
        UNIQUE (roll_no, date)
    )
    """)

    connection.commit()
    connection.close()


create_table()