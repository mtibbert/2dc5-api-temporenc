from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from src.routes.encode.encode_bp import encode_bp

# Prefix for routes
url_prefix = "/api/v1/temporenc"

# Create application
app = Flask(__name__,
            template_folder="templates",
            static_folder="static")

# Create the API
api = Api(app, prefix=url_prefix)

# Configure Swagger UI
SWAGGER_URL = f"{url_prefix}/schema"                     # URL
API_URL = f"/static{url_prefix}/schema/api-schema.json"  # Path to Swagger.json file

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Temporenc API | Schema"
    },
)

# Set Endpoints
app.register_blueprint(encode_bp, url_prefix=url_prefix)   # /encode
app.register_blueprint(swaggerui_blueprint)                # Swagger UI
