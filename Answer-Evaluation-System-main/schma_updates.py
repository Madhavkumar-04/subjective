from flask import Flask
from flask_mysqldb import MySQL

def apply_schema_updates(app, mysql):
    """
    Apply schema updates to the MySQL database.
    Adds columns to StudentAnswers and creates EvaluationFeedback table if they don't exist.
    """
    with app.app_context():
        cur = mysql.connection.cursor()

        # List of columns to add to StudentAnswers
        new_columns = [
            ('exact_match_score', 'FLOAT'),
            ('partial_match_score', 'FLOAT'),
            ('cosine_similarity_score', 'FLOAT'),
            ('sentiment_score', 'FLOAT'),
            ('enhanced_sentence_match_score', 'FLOAT'),
            ('multinomial_naive_bayes_score', 'FLOAT'),
            ('semantic_similarity_score', 'FLOAT'),
            ('coherence_score', 'FLOAT'),
            ('relevance_score', 'FLOAT'),
            ('corrected_score', 'FLOAT'),
        ]

        # Check existing columns in StudentAnswers
        cur.execute("SHOW COLUMNS FROM StudentAnswers")
        existing_columns = [row[0] for row in cur.fetchall()]

        # Add missing columns to StudentAnswers
        for column_name, column_type in new_columns:
            if column_name not in existing_columns:
                try:
                    cur.execute(f"ALTER TABLE StudentAnswers ADD COLUMN {column_name} {column_type}")
                    mysql.connection.commit()
                    print(f"Added column {column_name} to StudentAnswers")
                except Exception as e:
                    print(f"Error adding column {column_name}: {str(e)}")
            else:
                print(f"Column {column_name} already exists in StudentAnswers")

        # Check if EvaluationFeedback table exists
        cur.execute("SHOW TABLES LIKE 'EvaluationFeedback'")
        table_exists = cur.fetchone()

        if not table_exists:
            try:
                cur.execute("""
                    CREATE TABLE EvaluationFeedback (
                        feedback_id INT AUTO_INCREMENT PRIMARY KEY,
                        answer_id INT,
                        feedback_text TEXT,
                        corrected_score FLOAT,
                        submitted_by ENUM('teacher', 'admin'),
                        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (answer_id) REFERENCES StudentAnswers(answer_id)
                    )
                """)
                mysql.connection.commit()
                print("Created EvaluationFeedback table")
            except Exception as e:
                print(f"Error creating EvaluationFeedback table: {str(e)}")
        else:
            print("EvaluationFeedback table already exists")

        cur.close()

if __name__ == '__main__':
    # Initialize Flask app and MySQL
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = 'application-portal-application-portal.h.aivencloud.com'
    app.config['MYSQL_PORT'] = 28768
    app.config['MYSQL_USER'] = 'avnadmin'
    app.config['MYSQL_PASSWORD'] = 'AVNS_Jf9TxCISqeiBQWDQjIf'
    app.config['MYSQL_DB'] = 'defaultdb'
    app.config['MYSQL_SSL'] = {'ssl': {'ca': '', 'check_hostname': False}}

    mysql = MySQL(app)

    # Apply schema updates
    apply_schema_updates(app, mysql)