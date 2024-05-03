#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable = False)
    cities = relationship('City', backref='state', cascade='all, delete, delete-orphan')

    @property
    def cities(self):
        '''
        returns list of city instance with state_id equal to current state.id
        filestorage relationship between State and City
        '''
        from models import storage
        relate_cities = []
        cities = storage.all(city)
        for city in cities.values():
            if city.state_id == self.id:
                relate_cities.append(city)
        return relate_cities        