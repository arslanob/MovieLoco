"""SQLAlchemy models for Movie Locations App."""

from datetime import datetime
from enum import auto
from platform import release

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    bio = db.Column(
        db.Text,
    )

    posts = db.relationship('Post')


    likes = db.relationship(
        'Post',
        secondary="likes"
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"


    @classmethod
    def edit_password(cls, username, new_password):

        user = cls.query.filter_by(username=username).first()

        hashed_pwd = bcrypt.generate_password_hash(new_password).decode('UTF-8')
        
        user.password = hashed_pwd

        db.session.commit()

        return user   


    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = cls(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Post(db.Model):
    """An individual post."""

    __tablename__ = 'posts'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title = db.Column(
        db.String(50),
        nullable=False,
    )

    description = db.Column(
        db.String(250),
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    location_id = db.Column(
        db.Integer,
        db.ForeignKey('locations.id', ondelete='CASCADE'),
        nullable=False,
    )

    movie_id = db.Column(
        db.Integer,
        db.ForeignKey('movies.id', ondelete='CASCADE'),
        nullable=False,
    )

    user = db.relationship('User', overlaps="posts")
    location = db.relationship('Location', backref='posts')
    movie = db.relationship('Movie', backref='posts')

    def serialize(self):
        return {
            "id":self.id,
            "title": self.title,
            "descripton": self.description,
            "created_at": self.created_at,
            "image_url": self.image_url,
            "user_id": self.user_id,
            "location_id": self.location_id,
            "movie_id": self.movie_id,
            "movie_title":self.movie.title,
            "lat":self.location.lat,
            "lng":self.location.lng,
            "city":self.location.city,
            "state":self.location.state,
            "country":self.location.country,
        }


class Location(db.Model):
    """An individual location."""

    __tablename__ = 'locations'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    lat = db.Column(
        db.Float,
        nullable=False
    )

    lng = db.Column(
        db.Float,
        nullable=False
    )

    address = db.Column(
        db.String,
    )
    city = db.Column(
        db.String,
    )
    state = db.Column(
        db.String,
    )
    country = db.Column(
        db.String,
    )
    zipcode = db.Column(
        db.Integer,
    )

class Movie(db.Model):
    """An individual movie."""

    __tablename__ = 'movies'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title = db.Column(
        db.String,
        nullable=False
    )

    popularity = db.Column(
        db.Float,
    )

    poster_path = db.Column(
        db.Text,
        default="/5VTN0pR8gcqV3EPUHHfMGnJYN9L.jpg",
    )

    release_date = db.Column(
        db.String,
    )


    def serialize(self):
        return {
            "id":self.id,
            "popularity": self.popularity,
            "poster_path": self.poster_path,
            "release_date": self.release_date,
            "title": self.title
        }

class Likes(db.Model):
    """Mapping user likes."""

    __tablename__ = 'likes' 

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id', ondelete='cascade'),
    )


def connect_db(app):
    db.app = app
    db.init_app(app)
