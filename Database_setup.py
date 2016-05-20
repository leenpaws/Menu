# Configuration-sets up dependencies

from sqlalchemy import \
    Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

#to create a base class that class code will inherit
Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'
    #mapper
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)




class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(300))
    description = Column(String(300))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)




##insert at end of file
engine = create_engine( 'sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
#base.metadata.bind = egneine
#dbsession = sessionmaker (bind = engine)
#session = DBSession()
#myFirstRestaurant = Restaurant(name = "Pizza Palace")
