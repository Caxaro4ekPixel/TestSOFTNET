from app import db, guard
import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    dashboards = db.relationship('Dashboard')

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
            if property == 'password':
                value = guard.hash_password(str(value))
            setattr(self, property, value)

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active

    def save(self):
        db.session.add(self)
        db.session.commit()

    def deactivation(self):
        self.is_active = False
        db.session.commit()


class Dashboard(db.Model):
    __tablename__ = 'dashboards'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    user = db.relationship('User', back_populates='dashboards')
    notes = db.relationship('Note')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Dashboard %r>' % self.title


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_create = db.Column(db.DateTime, default=datetime.datetime.now)
    date_edit = db.Column(db.DateTime, default=datetime.datetime.now)
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboards.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    dashboards = db.relationship('Dashboard', back_populates='notes')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def deactivation(self):
        self.is_active = False
        self.date_edit = datetime.datetime.now()
        db.session.commit()

    def __repr__(self):
        return '<Note %r>' % self.text
