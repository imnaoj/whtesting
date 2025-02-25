from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from app.routes.auth import auth_bp
from app.routes.webhook import webhook_bp
from app.routes.path import path_bp
from app.utils.websocket import socketio, configure_socketio
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # CORS configuration
    CORS(app, 
         origins=app.config['CORS_ORIGINS'],
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    # Initialize MongoDB
    app.mongo = MongoClient(app.config['MONGO_URI'])
    app.db = app.mongo.get_default_database()
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(webhook_bp, url_prefix='/api/webhook')
    app.register_blueprint(path_bp, url_prefix='/api/paths')
    
    # Initialize SocketIO with CORS settings
    configure_socketio(app)
    
    return app 