from app import db
import base64
import os
import re
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #tasks = db.relationship('Task', backref='author')
    token = db.Column(db.String(32), index = True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_password(kwargs.get('password', ''))

    def __repr__(self):
        return f"<User {self.id}|{self.username}>"
    
    def update(self,**kwargs):
        allowed_fields = {'first_name', 'last_name', 'email', 'username', 'password'}
        
        def camel_to_snake(string):
            return re.sub("([A-Z][A-Za-z]*)","_\1", string).lower()
        
        for key, value in kwargs.items():
            snake_key = camel_to_snake(key)
            if snake_key in allowed_fields:
                if snake_key == 'password':
                    self.set_password(value)
                else:
                    setattr(self, snake_key, value)
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)
        self.save()

    def check_password(self, plain_text_password):
        return check_password_hash(self.password, plain_text_password)

    def to_dict(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "username": self.username,
            "email": self.email
        }
        
    def get_token(self):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(minutes=1):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode("utf-8") 
        self.token_expiration = now + timedelta(hours=1)
        self.save()
        return self.token
        
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # In SQL - task_id INTEGER NOT NULL, FOREIGN KEY(task_id) REFERENCES task_id
    #user_id = db.Column(db.Integer, db.ForeignKey('user_id'), nullable=False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save()
        
    def __repr__(self):
        return f"<Task {self.id}|{self.title}>"
    
    def update(self, **kwargs):
        allowed_fields = {"title", "description"}
    
        def camel_to_snake(string):
            return re.sub("([A-Z][A-Za-z]*)","_\1", string).lower()
        for key, value in kwargs.items():
            snake_key = camel_to_snake(key)
            if snake_key in allowed_fields:
                setattr(self, snake_key, value)
        self.save()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.add(self)
        db.session.commit()
        
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "createdAt": self.created_at,
        }
    
    