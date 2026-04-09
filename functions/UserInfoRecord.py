
from Mysql import Mysql_conn
from flask import Flask, request, jsonify
from flask_cors import CORS  # <-- 必须加

from Mysql.Mysql_conn import insert_user_info

app = Flask(__name__)
CORS(app)  # <-- 必须加

@app.route("/")
def home():
    return app.send_static_file("index.html")  # 或 render_template

@app.route("/api/record_info", methods=["POST"])
def record_info():
    insert_user_info(height=request.json.get("height"), weight=request.json.get("weight"))
    print("录入成功")
if __name__ == '__main__':
    app.run(debug=True)