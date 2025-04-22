from flask import Flask
from flask_mysqldb import MySQL
import warnings
import nltk

warnings.filterwarnings("ignore")
nltk.download("stopwords")

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.template_folder = 'templates'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'application-portal-application-portal.h.aivencloud.com'
app.config['MYSQL_PORT'] = 28768
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_Jf9TxCISqeiBQWDQjIf'
app.config['MYSQL_DB'] = 'defaultdb'
app.config['MYSQL_SSL'] = {'ssl': {'ca': '', 'check_hostname': False}}  # Optional: for SSL

mysql = MySQL(app)

def create_schema():
    cursor = mysql.connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Admins (
            admin_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(50) NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(50) NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Teachers (
            teacher_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(50) NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tests (
            test_id INT AUTO_INCREMENT PRIMARY KEY,
            test_name VARCHAR(100) NOT NULL,
            teacher_id INT NOT NULL,
            FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id),
            UNIQUE (teacher_id, test_name)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Questions (
            question_id INT AUTO_INCREMENT PRIMARY KEY,
            question_text TEXT NOT NULL,
            test_id INT NOT NULL,
            FOREIGN KEY (test_id) REFERENCES Tests(test_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ExpectedAnswers (
            expectedanswer_id INT AUTO_INCREMENT PRIMARY KEY,
            answer_text TEXT NOT NULL,
            question_id INT NOT NULL,
            FOREIGN KEY (question_id) REFERENCES Questions(question_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS StudentAnswers (
            answer_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT NOT NULL,
            test_id INT NOT NULL,
            question_id INT NOT NULL,
            answer_text TEXT NOT NULL,
            score INT DEFAULT 0,
            FOREIGN KEY (student_id) REFERENCES Students(student_id),
            FOREIGN KEY (test_id) REFERENCES Tests(test_id),
            FOREIGN KEY (question_id) REFERENCES Questions(question_id),
            UNIQUE (student_id, test_id, question_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teacherstudentrelationship (
            relationship_id INT AUTO_INCREMENT PRIMARY KEY,
            teacher_id INT NOT NULL,
            student_id INT NOT NULL,
            FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id),
            FOREIGN KEY (student_id) REFERENCES Students(student_id),
            UNIQUE (teacher_id, student_id)
        );
    """)
    mysql.connection.commit()
    
    # Insert default admin
    cursor.execute("SELECT COUNT(*) FROM Admins;")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO Admins (username, password) VALUES (%s, %s)", ('admin', 'admin123'))
        print("Default admin added.")

    mysql.connection.commit()
    cursor.close()

# Run schema creation once on startup
with app.app_context():
    create_schema()
