import os
from flask import Flask, jsonify
from sqlalchemy import create_all
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ดึงค่า Config จาก Environment Variables ที่เราตั้งไว้ใน docker-compose
db_url = os.getenv('DATABASE_URL', 'postgresql://admin:password@db:5432/mydatabase')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# สร้าง Model ง่ายๆ ไว้ลอง Test Database
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
        # ลอง Query สั้นๆ เพื่อเช็คว่าต่อ DB ติดไหม
        db.session.execute('SELECT 1')
        return jsonify({
            "database": "Connected",
            "connection_string": db_url.split('@')[-1] # โชว์แค่ host/db (ซ่อน password)
        })
    except Exception as e:
        return jsonify({
            "database": "Connection Failed",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    # สร้าง table อัตโนมัติถ้ายังไม่มี
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)