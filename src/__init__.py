from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from src.routes.encode import Encode

# Create application
app = Flask(__name__,
            template_folder="templates",
            static_folder="static")

# Create the API
api = Api(app, prefix="/api/v1/temporenc")

# Configure Swagger UI
SWAGGER_URL = '/api/v1/temporenc/schema'                     # URL
API_URL = '/static/api/v1/temporenc/schema/api-schema.json'  # Path to Swagger.json file

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Temporenc API | Schema"
    },
)

# Set Endpoints
app.register_blueprint(swaggerui_blueprint)       # /schema
api.add_resource(Encode, '/encode/<iso_string>')  # /encode/<iso_string>
