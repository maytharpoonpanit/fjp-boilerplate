import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # เพิ่มตัวนี้เพื่อความปลอดภัยตามมาตรฐานใหม่

app = Flask(__name__)

# Config
db_url = os.getenv('DATABASE_URL', 'postgresql://admin:password@db:5432/mydatabase')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model ตัวอย่าง
class TestStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

@app.route('/')
def hello_world():
    return {
        "message": "Hello World from Flask!",
        "status": "Container is running",
        "environment": os.getenv('FLASK_ENV', 'not set')
    }

@app.route('/test-db')
def test_db():
    try:
        # ใช้ text() ครอบคำสั่ง SQL เพื่อรองรับ SQLAlchemy 2.0+
        db.session.execute(text('SELECT 1'))
        return jsonify({
            "database": "Connected",
            "connection_string": db_url.split('@')[-1]
        })
    except Exception as e:
        return jsonify({
            "database": "Connection Failed",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)