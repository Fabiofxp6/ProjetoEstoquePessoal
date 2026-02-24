from flask import Flask
from config import Config
from pymongo import MongoClient
# Importe os dois blueprints
from routes.product_routes import product_bp
from routes.sales_routes import sales_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    client = MongoClient(app.config["MONGO_URI"])
    app.db = client['loja_db']
    
    # REGISTRE OS DOIS AQUI
    app.register_blueprint(sales_bp) # Este cuidará da "/"
    app.register_blueprint(product_bp) # Este cuidará da "/estoque"
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)