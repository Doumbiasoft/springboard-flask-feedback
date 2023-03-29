
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)
    with app.app_context():
         db.create_all() 

def hash_function(value):
      return flask_bcrypt.generate_password_hash(value).decode("utf8")

def hash_function_check(old_password_hash,new_password_hash):
      return flask_bcrypt.check_password_hash(old_password_hash, new_password_hash)

class User(db.Model):
    """User Model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    reset_token = db.Column(db.Text, unique=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    feedbacks = db.relationship("Feedback", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name} {self.username} {self.email}>"

    def get_users():
        return User.query
    
    def get_user_by_id(id):
        return User.query.get_or_404(id)
    
    def add_users(user):
        final_user=user
        db.session.add(final_user)
        try:
            db.session.commit()
        except:
            return False
        return final_user
    
    def update_users(id, firstname, lastname, email,is_admin):
        user = User.query.get_or_404(id)
        user.first_name = firstname
        user.last_name = lastname
        user.is_admin = is_admin
        if email != user.email and User.query.filter(User.email == email).count() == 0:
            user.email = email
        db.session.add(user)
        try:
            db.session.commit()
        except:
            return False
        return user
    
    def delete_users(id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        try:
            db.session.commit()
        except:
            return False
        return True
    
    def update_password(id, password):
        user = User.query.get_or_404(id)
        user.password = password
        db.session.add(user)
        try:
            db.session.commit()
        except:
            return False
        return True
    
    @classmethod
    def register(cls, first_name, last_name, username, email, password):
        """Register user w/hashed password & return user."""

        password_hashed = flask_bcrypt.generate_password_hash(password).decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(first_name=first_name, last_name=last_name,username=username,email=email,password=password_hashed)
    
    @classmethod
    def login(cls, username, password):
        """Validate that user exists & password is correct. Return user if valid; else return False."""

        user = User.query.filter_by(username=username).first()

        if user and flask_bcrypt.check_password_hash(user.password, password):
            #return user instance
            return user
        else:
            return False
      

class Feedback(db.Model):
    """Feedback Model"""

    __tablename__ = "feedbacks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime,nullable=False, default=datetime.datetime.now)
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)

    @property
    def friendly_date(self):
        """Return formatted date."""
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    
    def __repr__(self):
        return f"<Feedback {self.id} {self.title} {self.content} {self.friendly_date}>"
    
    def get_feedbacks():
        return Feedback.query
    
    def get_feedback_by_id(id):
        return Feedback.query.get_or_404(id)
    
    def add_feedback(username, title, content):
      user = User.query.filter(User.username == username).first()
      if user is None:
          return False
      else:
        new_feedback = Feedback(title=title,
                        content=content,
                        username=user.username)
        db.session.add(new_feedback)
        try:
            db.session.commit()
        except:
            return False
        return True
      
    def update_feedback(id, title, content):
        feedback = Feedback.query.get_or_404(id)
        feedback.title = title
        feedback.content = content
        db.session.add(feedback)
        try:
            db.session.commit()
        except:
            return False
        return True
    
    def delete_feedback(id):
        feedback = Feedback.query.get_or_404(id)
        db.session.delete(feedback)
        try:
            db.session.commit()
        except:
            return False
        return True



