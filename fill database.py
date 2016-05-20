from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# newEntry = ClassName(property = "value", ...)
#session.add(newEntry)
#session.commit()

myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()
session.query(Restaurant).all()
cheesepizza = MenuItem(name = "Cheese Pizza",
                       description = "Made with all natural" \
                       "ingredients and fresh mozarella",
                       course = "Entree",
                       price = "$8.99",
                       restaurant = myFirstRestaurant)
session.add(cheesepizza)
session.commit()
session.query(MenuItem).all()

firstResult = session.query(Restaurant).first()

veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "/n"

    session.add(urbanVeggieBurger)

    #mark = session.query(Employee).filter_by(name = "Mark Gonzalez").one()
    #session.delte(mark)
    session.commit()
