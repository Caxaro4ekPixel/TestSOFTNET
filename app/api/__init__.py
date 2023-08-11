from flask import Blueprint

api = Blueprint(
    'API_blueprint',
    __name__,
    url_prefix='/API/v1',
)
