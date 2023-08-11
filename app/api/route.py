from app.api import api
from flask import request, jsonify
from app import guard
import flask_praetorian
from app.utils import (
    registration_new_user,
    unregistration_user,
    create_new_notes,
    get_notes_by_user_or_dashboard,
    edit_note_by_id,
    delete_note_by_id
)
from app.validation_models import (
    ValidationRequestFieldLogin,
    ValidationRequestFieldRegistration,
    ValidationRequestFieldUnRegistration,
    ValidationRequestFieldCreateNotes,
    ValidationRequestFieldGetNotes,
    ValidationRequestFieldEditNotes,
    ValidationRequestFieldDeleteNotes
)
from pydantic import ValidationError


@api.route('/login', methods=['POST'])
def login():
    """
    Performs user login by analyzing a POST request containing user credentials.
    .. example::
       $ curl http://localhost:5000/API/v1/login -X POST
         -d '{
                "username": "<username>",
                "password": "<password>"
            }'
    :return: Token: string
    """
    try:
        req = request.get_json(force=True)
        ValidationRequestFieldLogin.validate(req)
        user = guard.authenticate(**req)
        return (jsonify({'access_token': guard.encode_jwt_token(user)}), 200)
    except ValidationError as e:
        error_temp = dict(e.errors()[0])
        return (jsonify({"Error": True, 'Status': {"type": error_temp['type'], "location": error_temp['loc'],
                                                   "message": error_temp['msg'], "input": error_temp['input']}}),
                400)


@api.route('/reg-user', methods=['POST'])
@flask_praetorian.auth_required
@flask_praetorian.roles_required("admin")
def register():
    """
    Registers a user by parsing a POST request containing user credentials.
    .. example::
       $ curl http://localhost:5000/API/v1/register -X POST
            -H "Authorization: Bearer <your_token>"
            -d '{
                "username": "<username>",
                "password": "<password>",
                "r_password": "<r_password>"
            }'
    :return: Status: dict
    """
    try:
        req = request.get_json(force=True)
        ValidationRequestFieldRegistration.validate(req)
        status = registration_new_user(**req)
        return (jsonify(status), 200)
    except ValidationError as e:
        error_temp = dict(e.errors()[0])
        return (jsonify({"Error": True, 'Status': {"type": error_temp['type'], "location": error_temp['loc'],
                                                   "message": error_temp['msg'], "input": error_temp['input']}}),
                400)


@api.route('/unreg-user', methods=['POST'])
@flask_praetorian.auth_required
@flask_praetorian.roles_required("admin")
def unregister():
    """
    Unregisters a user by parsing a POST request containing user credentials.
    .. example::
       $ curl http://localhost:5000/API/v1/unreg-user -X POST
            -H "Authorization: Bearer <your_token>"
            -d '{
                "username": "<username>",
            }'
    :return: Status: dict
    """
    try:
        req = request.get_json(force=True)
        ValidationRequestFieldUnRegistration.validate(req)
        status = unregistration_user(**req)
        return (jsonify(status), 200)
    except ValidationError as e:
        error_temp = dict(e.errors()[0])
        return (jsonify({"Error": True, 'Status': {"type": error_temp['type'], "location": error_temp['loc'],
                                                   "message": error_temp['msg'], "input": error_temp['input']}}),
                400)


@api.route('/get-notes', methods=['GET'])
@flask_praetorian.auth_required
@flask_praetorian.roles_accepted("user", "admin")
def get_notes():
    """
    Returns a list of notes.
    .. example::
       $ curl http://localhost:5000/API/v1/get-notes -X GET
       -H "Authorization: Bearer <your_token>"
       -d '{
                "dashboard_title": "<dashboard_title>" or "all",
            }'
    :return: List of notes
    """
    try:
        req = request.get_json(force=True)
        ValidationRequestFieldGetNotes.validate(req)
        user = flask_praetorian.current_user()
        notes = get_notes_by_user_or_dashboard(user=user, **req)
        return (jsonify(notes), 200)
    except ValidationError as e:
        error_temp = dict(e.errors()[0])
        return jsonify({"Error": True, 'Status': {"type": error_temp['type'], "location": error_temp['loc'],
                                                  "message": error_temp['msg'], "input": error_temp['input']}}), 400


@api.route('/create-notes', methods=['POST'])
@flask_praetorian.auth_required
@flask_praetorian.roles_accepted("user", "admin")
def create_notes():
    """
    Creates a new note.
    .. example::
       $ curl http://localhost:5000/API/v1/create-notes -X POST
       -H "Authorization: Bearer <your_token>"
       -d '{
            "dashboard_title": "<dashboard_title>",
            "notes": ["<note1>", "<note2>", ...]
            }'
    :return: Status: dict
    """
    try:
        req = request.get_json(force=True)
        ValidationRequestFieldCreateNotes.validate(req)
        status = create_new_notes(user=flask_praetorian.current_user(), **req)
        return (jsonify(status), 200)
    except ValidationError as e:
        error_temp = dict(e.errors()[0])
        return jsonify({"Error": True, 'Status': {"type": error_temp['type'], "location": error_temp['loc'],
                                                  "message": error_temp['msg'], "input": error_temp['input']}}), 400


@api.route('/edit-notes', methods=['POST'])
@flask_praetorian.auth_required
@flask_praetorian.roles_accepted("user", "admin")
def edit_notes():
    """
    Edits a note.
    .. example::
       $ curl http://localhost:5000/API/v1/edit-notes -X POST
        -H "Authorization: Bearer <your_token>"
        -d '{
                "note_id": <note_id>,
                "note_new_text": "<note_new_text>"
            }'
    :return: Status: dict
    """
    try:
        req = request.get_json(force=True)
        ValidationRequestFieldEditNotes.validate(req)
        status = edit_note_by_id(user=flask_praetorian.current_user(), **req)
        return (jsonify(status), 200)
    except ValidationError as e:
        error_temp = dict(e.errors()[0])
        return jsonify({"Error": True, 'Status': {"type": error_temp['type'], "location": error_temp['loc'],
                                                  "message": error_temp['msg'], "input": error_temp['input']}}), 400


@api.route('/delete-notes', methods=['POST'])
@flask_praetorian.auth_required
@flask_praetorian.roles_accepted("user", "admin")
def delete_notes():
    """
    Deletes a note.
    .. example::
       $ curl http://localhost:5000/API/v1/delete-notes -X POST
        -H "Authorization: Bearer <your_token>"
            -d '{
                    "note_id": <note_id>,
                }'
    :return: Status: dict
    """
    try:
        req = request.get_json(force=True)
        ValidationRequestFieldDeleteNotes.validate(req)
        status = delete_note_by_id(user=flask_praetorian.current_user(), **req)
        return (jsonify(status), 200)
    except ValidationError as e:
        error_temp = dict(e.errors()[0])
        return jsonify({"Error": True, 'Status': {"type": error_temp['type'], "location": error_temp['loc'],
                                                  "message": error_temp['msg'], "input": error_temp['input']}}), 400
