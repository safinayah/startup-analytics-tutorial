from flask import Flask

def create_app():
    """Simple application factory for tutorial dashboard only"""
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Register main blueprint
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app