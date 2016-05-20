from flask import Flask
# instance with name of running app
#adding database to flask app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


"""decorator"""

# @app decorator will wrap function inside the app.route function that flash has created
#so either of these routes gets sent from browser function defined here gets executed

@app.route('/')
#@app.route('/hello'), trailing slash will allow flash to
#  render the page even if it's not there
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by\
        (id = restaurant_id).one()
    items = session.query(MenuItem).filter_by\
        (restaurant_id = restaurant_id)
    '''def HelloWorld():
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id=
                                              restaurant.id)'''
    output = ''
    for i in items:
        output += i.name
        output += '</br>'
        output += i.price
        output += '</br>'
        output += i.description
        output += '</br>'
        output += '</br>'
    return output


#Task1: create route for newmenuitem function here
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/new/')

def newMenuItem(restaurant_id):
    #restaurant = session.query(Restaurant).filter_by \
     #   (id=restaurant_id).one()
    #items = MenuItem()
   # items.name = raw_input(MenuItem.name) + '</br>'
  #  items.course = raw_input(MenuItem.course) + '</br>'
 #   items.price = raw_input(MenuItem.price) + '</br>'
#    items.description = raw_input(MenuItem.description)+ '</br>'

   # newItem = MenuItem(name= items.name, description=items.description,
  #                   price = items.price, course=items.course, restaurant=restaurant)
 #   session.add(newItem)
#    session.commit()
    return "page to create a new menu item.  Task 1 complete"

#Task2: create route for editmenuitem function here

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/')

def editMenuItem(restaurant_id, menu_id):
    return "page to edit a new menu item.  Task 2 complete"

#task3: create a route for deletemenuitem function here

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item here.  Task 3 complete"

# main is app run by interpreter, other file have __name of pythonfile__
# main is ensuring it can't be imported, by default server is only accessible from host machine

if __name__ == '__main__':
#debug support ensures server will reload itself
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
