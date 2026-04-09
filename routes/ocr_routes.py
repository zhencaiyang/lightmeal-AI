from flask import Blueprint, request, jsonify
import base64
from io import BytesIO
from PIL import Image
import pytesseract

# 创建蓝图
ocr_bp = Blueprint('ocr', __name__)

@ocr_bp.route('/ocr', methods=['POST'])
def ocr_recognition():
    """OCR图片文字识别接口"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "没有上传图片文件"}), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({"error": "图片文件名为空"}), 400
        
        # 处理图片
        image = Image.open(image_file.stream)
        
        # OCR识别
        text = pytesseract.image_to_string(image, lang='chi_sim')
        
        # 清理识别结果
        clean_text = text.strip().replace('\n', ' ').replace('\r', ' ')
        
        return jsonify({
            "text": clean_text,
            "status": "success"
        })
        
    except Exception as e:
        print(f"OCR识别错误: {str(e)}")
        return jsonify({
            "error": f"识别失败: {str(e)}",
            "status": "error"
        }), 500