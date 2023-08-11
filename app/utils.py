from .models import User, Dashboard, Note
from datetime import datetime


def registration_new_user(username: str, password: str, r_password: str) -> dict:
    check_user = User.query.filter(User.username == username).first()
    if check_user:
        return {"Error": True, "Status": "Username already exists"}
    if password != r_password:
        return {"Error": True, "Status": "Passwords don't match"}

    new_user = User(username=username, password=password, roles="user")
    new_user.save()
    return {"Error": False, "Status": "User created successfully"}


def unregistration_user(username: str) -> dict:
    user = User.query.filter(User.username == username).first()
    if not user:
        return {"Error": True, "Status": "User not found"}
    user.deactivation()
    return {"Error": False, "Status": "User deleted successfully"}


def get_notes_by_user_or_dashboard(user: User, dashboard_title: str) -> dict:
    if dashboard_title == "all":
        notes = {dashboard.title: list(
            map(lambda note: {"id": note.id, "text": note.text, "date_create": note.date_create,
                              "date_edit": note.date_edit}, filter(lambda note: note.is_active, dashboard.notes))) for
            dashboard in user.dashboards}
    else:
        dashboard = Dashboard.query.filter(Dashboard.title == dashboard_title, Dashboard.user_id == user.id).first()
        if not dashboard:
            return {"Error": True, "Status": "Dashboard not found"}
        notes = {dashboard.title: list(
            map(lambda note: {"id": note.id, "text": note.text, "date_create": note.date_create,
                              "date_edit": note.date_edit}, filter(lambda note: note.is_active, dashboard.notes)))}
    return notes


def create_new_notes(user: User, dashboard_title: str, notes: list) -> dict:
    dashboard = Dashboard.query.filter(Dashboard.title == dashboard_title, Dashboard.user_id == user.id).first()
    if not dashboard:
        dashboard = Dashboard(title=dashboard_title, user_id=user.id)
        dashboard.save()
    for note in notes:
        new_note = Note(text=note, dashboard_id=dashboard.id)
        new_note.save()
    return {"Error": False, "Status": "Notes created successfully"}


def edit_note_by_id(user: User, note_id: int, note_new_text: str) -> dict:
    note = Note.query.filter(Note.id == note_id).first()
    if note.dashboards.user_id != user.id:
        return {"Error": True, "Status": "You don't have permission to edit this note"}
    if not note:
        return {"Error": True, "Status": "Note not found"}
    note.text = note_new_text
    note.date_edit = datetime.now()
    note.update()
    return {"Error": False, "Status": "Note updated successfully"}


def delete_note_by_id(user: User, note_id: int) -> dict:
    note = Note.query.filter(Note.id == note_id).first()
    if note.dashboards.user_id != user.id:
        return {"Error": True, "Status": "You don't have permission to delete this note"}
    if not note:
        return {"Error": True, "Status": "Note not found"}
    note.deactivation()
    return {"Error": False, "Status": "Note deleted successfully"}
