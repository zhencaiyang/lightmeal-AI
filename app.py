from dulwich.web import url_prefix
from flask import Flask, render_template
from flask_cors import CORS

# 导入路由模块
from routes.allergen_routes import allergen_bp
from routes.ocr_routes import ocr_bp
from routes.user_routes import user_bp
from routes.insert_data_routes import insert_data_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # 注册蓝图（路由模块）
    app.register_blueprint(allergen_bp, url_prefix='/api')
    app.register_blueprint(ocr_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(insert_data_bp,url_prefix='/api')

    # 主页路由
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)