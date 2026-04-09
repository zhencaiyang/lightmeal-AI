from flask import Blueprint, request, jsonify

# 创建蓝图
user_bp = Blueprint('user', __name__)

@user_bp.route('/record_info', methods=['POST'])
def record_info():
    """记录用户基本信息"""
    print("收到用户信息记录请求")
    data = request.get_json() or {}
    height = data.get("height", "")
    weight = data.get("weight", "")
    
    # 这里可以添加数据验证和数据库保存逻辑
    print(f"收到用户信息 - 身高: {height}, 体重: {weight}")
    
    return jsonify({"message": f"用户信息已记录：身高{height}cm，体重{weight}kg"})

@user_bp.route('/user/profile', methods=['GET'])
def get_user_profile():
    """获取用户档案信息"""
    # 这里可以添加获取用户档案的逻辑
    return jsonify({"profile": {}})