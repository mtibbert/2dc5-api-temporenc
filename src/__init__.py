from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from src.routes.encode import Encode

# Create application
app = Flask(__name__,
            template_folder="templates")
# Create the API
api = Api(app)

# Set Endpoints
api.add_resource(Encode, '/api/v1/temporenc/encode/<iso_string>')

# Swagger config
# TODO: #7 Extract Swagger Meta to an External File
template = {
    "version": "3.0.1",
    "info": {
        'title': 'Temporenc API',
        "summary": "api which encodes and decodes dates.",
        "description":
            "<h2>A Temporenc API</h2>" +
            "<ul>"
            "<li>Encodes date, time, and datetime ISO strings.<br/>" +
            "<li>Decodes Temporenc encoded values." +
            "</ul>",
        "contact": {
            "name": "Temporenc API Support",
            "email": "temporenc.api.support.v@qneni.com"},
        "version": "3.0.1",
    },
    "basePath": "/api/v1/temporenc/encode",
}

swagger = Swagger(app, template=template)
