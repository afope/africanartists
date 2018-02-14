import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class Artists(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    bio = Column(String(2000), nullable=False)
    country = Column(String(250), nullable=False)
    imageUrl = Column(String(450), nullable=False)
    category = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)

# class for artists Database
    @property
    def serialize(self):
        # return artist data in serializable format
        return {
            'id': self.id,
            'name': self.name,
            'bio': self.bio,
            'category': self.category,
            'imageUrl': self.imageUrl,
            'country': self.country
        }


class Projects(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    description = Column(String(500), nullable=False)
    imageUrl = Column(String(250))
    artist_id = Column(Integer, ForeignKey('artists.id'))
    artists = relationship(Artists)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


# class for projects Database

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'title': self.title,
            'id': self.id,
            'description': self.description,
            'imageUrl': self.imageUrl
        }



engine = create_engine('sqlite:///artistswithusers.db')
Base.metadata.create_all(engine)
