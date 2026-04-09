#!/usr/bin/env python
"""
食品识别系统启动脚本
"""

from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("🚀 食品识别系统启动中...")
    print("📡 服务地址: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)