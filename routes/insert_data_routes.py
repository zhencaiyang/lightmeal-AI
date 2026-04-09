from flask import Blueprint, request, jsonify
from Mysql.Mysql_conn import insert_user_info, get_conn
import traceback

insert_data_bp=Blueprint('insert_data', __name__)

@insert_data_bp.route('/test_db_connection', methods=['GET'])
def test_db_connection():
    """
    测试数据库连接
    """
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return jsonify({
            "status": "success",
            "message": "数据库连接正常",
            "test_result": result
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "数据库连接失败",
            "error": str(e)
        }), 500


@insert_data_bp.route('/insert_data', methods=['POST'])
def insert_data():
    data = request.get_json() or {}
    username = data.get("username", "")
    gender = data.get("gender", "")
    height = data.get("height", "")
    weight = data.get("weight", "")
    insert_user_info(username,gender,height,weight)
    return jsonify({"message": "数据插入成功"})