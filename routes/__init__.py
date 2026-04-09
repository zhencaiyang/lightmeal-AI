# Routes package initialization
from .allergen_routes import allergen_bp
from .ocr_routes import ocr_bp
from .user_routes import user_bp
from .insert_data_routes import insert_data_bp

__all__ = ['allergen_bp', 'ocr_bp', 'user_bp','insert_data_bp']
