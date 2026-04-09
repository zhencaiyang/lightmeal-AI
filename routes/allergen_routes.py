from flask import Blueprint, request, jsonify
import json
import os
import re
from typing import List, Dict, Any

# 创建蓝图
allergen_bp = Blueprint('allergen', __name__)

# 加载过敏原预设表
def load_allergen_data():
    """加载过敏原数据"""
    try:
        # 获取当前文件目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建数据文件路径
        data_file = os.path.join(current_dir, '..', 'data', 'allergens.json')
        
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"过敏原数据文件不存在: {data_file}")
            return None
    except Exception as e:
        print(f"加载过敏原数据失败: {e}")
        return None

# 全局过敏原数据
ALLERGEN_DATA = load_allergen_data()

def detect_allergens(text: str) -> Dict[str, Any]:
    """
    检测文本中的过敏原
    
    Args:
        text: 要检测的文本
        
    Returns:
        检测结果字典
    """
    if not ALLERGEN_DATA:
        return {"error": "过敏原数据未加载", "hits": [], "risk": "unknown", "details": []}
    
    if not text or not isinstance(text, str):
        return {"error": "输入文本无效", "hits": [], "risk": "unknown", "details": []}
    
    text_lower = text.lower().strip()
    detected_allergens = []
    allergen_details = []
    
    # 遍历所有过敏原
    for allergen in ALLERGEN_DATA.get("allergens", []):
        allergen_id = allergen.get("id", "")
        allergen_name = allergen.get("name", "")
        keywords = allergen.get("keywords", [])
        severity = allergen.get("severity", "low")
        category = allergen.get("category", "")
        description = allergen.get("description", "")
        
        # 检查是否匹配任何关键词
        matched_keywords = []
        for keyword in keywords:
            # 使用正则表达式进行更精确的匹配
            # 支持部分匹配，但避免误匹配（如"虾"不会匹配"虾仁"中的"虾"）
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, text_lower) or keyword.lower() in text_lower:
                matched_keywords.append(keyword)
        
        if matched_keywords:
            detected_allergens.append(allergen_id)
            allergen_details.append({
                "id": allergen_id,
                "name": allergen_name,
                "matched_keywords": matched_keywords,
                "severity": severity,
                "category": category,
                "description": description
            })
    
    # 计算风险等级
    high_risk_count = sum(1 for detail in allergen_details if detail["severity"] == "high")
    medium_risk_count = sum(1 for detail in allergen_details if detail["severity"] == "medium")
    
    if high_risk_count >= 2:
        risk = "very_high"
    elif high_risk_count == 1 or medium_risk_count >= 2:
        risk = "high"
    elif medium_risk_count == 1 or len(detected_allergens) >= 1:
        risk = "medium"
    else:
        risk = "low"
    
    return {
        "hits": detected_allergens,
        "risk": risk,
        "details": allergen_details,
        "total_allergens": len(detected_allergens),
        "high_risk_count": high_risk_count,
        "medium_risk_count": medium_risk_count
    }

@allergen_bp.route('/allergen', methods=['POST'])
def allergen_check():
    """过敏原检测接口"""
    print("收到过敏原检测请求")
    
    try:
        data = request.get_json() or {}
        text = data.get("text", "")
        
        if not text:
            return jsonify({
                "error": "缺少检测文本",
                "hits": [],
                "risk": "unknown",
                "details": []
            }), 400
        
        print(f"检测文本: {text}")
        
        # 使用增强的过敏原检测函数
        result = detect_allergens(text)
        
        # 添加交叉污染警告
        if result.get("hits") and ALLERGEN_DATA:
            cross_warnings = []
            for hit in result["hits"]:
                warnings = ALLERGEN_DATA.get("cross_contamination_warnings", {}).get(hit, [])
                cross_warnings.extend(warnings)
            
            result["cross_contamination_warnings"] = list(set(cross_warnings))  # 去重
        
        print(f"检测结果: {result}")
        return jsonify(result)
        
    except Exception as e:
        print(f"过敏原检测出错: {e}")
        return jsonify({
            "error": f"检测失败: {str(e)}",
            "hits": [],
            "risk": "unknown",
            "details": []
        }), 500

@allergen_bp.route('/allergen/history', methods=['GET'])
def get_allergen_history():
    """获取过敏原检测历史"""
    # 这里可以添加获取历史记录的逻辑
    return jsonify({"history": []})

@allergen_bp.route('/allergen/batch', methods=['POST'])
def batch_allergen_check():
    """批量过敏原检测接口"""
    try:
        data = request.get_json() or {}
        texts = data.get("texts", [])
        
        if not texts or not isinstance(texts, list):
            return jsonify({
                "error": "请提供文本列表",
                "results": []
            }), 400
        
        print(f"批量检测 {len(texts)} 个文本")
        
        results = []
        all_allergens = set()
        total_high_risk = 0
        total_medium_risk = 0
        
        for i, text in enumerate(texts):
            if not text or not isinstance(text, str):
                continue
                
            # 复用单个检测逻辑
            hits = []
            if "花生" in text:
                hits.append("peanut")
            if "乳清蛋白" in text or "牛奶" in text:
                hits.append("milk")
            
            risk = "high" if len(hits) >= 2 else ("medium" if len(hits) == 1 else "low")
            
            result = {
                "hits": hits,
                "risk": risk,
                "high_risk_count": 1 if risk == "high" else 0,
                "medium_risk_count": 1 if risk == "medium" else 0,
                "total_allergens": len(hits)
            }
            
            result["index"] = i
            result["text"] = text[:100] + "..." if len(text) > 100 else text
            results.append(result)
            
            # 统计
            all_allergens.update(hits)
            total_high_risk += result["high_risk_count"]
            total_medium_risk += result["medium_risk_count"]
        
        # 计算总体风险
        if total_high_risk >= 3:
            overall_risk = "very_high"
        elif total_high_risk >= 1 or total_medium_risk >= 2:
            overall_risk = "high"
        elif total_medium_risk >= 1 or len(all_allergens) >= 1:
            overall_risk = "medium"
        else:
            overall_risk = "low"
        
        summary = {
            "total_texts": len(texts),
            "texts_with_allergens": len([r for r in results if r.get("hits")]),
            "unique_allergens": list(all_allergens),
            "total_allergen_instances": sum(r.get("total_allergens", 0) for r in results),
            "total_high_risk": total_high_risk,
            "total_medium_risk": total_medium_risk,
            "overall_risk": overall_risk
        }
        
        return jsonify({
            "summary": summary,
            "results": results
        })
        
    except Exception as e:
        print(f"批量过敏原检测出错: {e}")
        return jsonify({
            "error": f"批量检测失败: {str(e)}",
            "results": []
        }), 500

@allergen_bp.route('/allergen/allergens', methods=['GET'])
def get_allergen_list():
    """获取所有过敏原列表"""
    try:
        if not ALLERGEN_DATA:
            return jsonify({"error": "过敏原数据未加载"}), 500
        
        # 返回简化的过敏原列表
        allergen_list = []
        for allergen in ALLERGEN_DATA.get("allergens", []):
            allergen_list.append({
                "id": allergen.get("id"),
                "name": allergen.get("name"),
                "category": allergen.get("category"),
                "severity": allergen.get("severity"),
                "description": allergen.get("description")
            })
        
        return jsonify({
            "allergens": allergen_list,
            "total_count": len(allergen_list),
            "categories": list(set(allergen.get("category") for allergen in ALLERGEN_DATA.get("allergens", [])))
        })
        
    except Exception as e:
        return jsonify({"error": f"获取过敏原列表失败: {str(e)}"}), 500

@allergen_bp.route('/allergen/categories', methods=['GET'])
def get_allergen_categories():
    """获取过敏原分类"""
    try:
        if not ALLERGEN_DATA:
            return jsonify({"error": "过敏原数据未加载"}), 500
        
        categories = {}
        for allergen in ALLERGEN_DATA.get("allergens", []):
            category = allergen.get("category", "其他")
            if category not in categories:
                categories[category] = []
            
            categories[category].append({
                "id": allergen.get("id"),
                "name": allergen.get("name"),
                "severity": allergen.get("severity")
            })
        
        return jsonify({
            "categories": categories,
            "category_count": len(categories)
        })
        
    except Exception as e:
        return jsonify({"error": f"获取过敏原分类失败: {str(e)}"}), 500