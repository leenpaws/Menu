from flask import Flask, render_template, request, redirect, url_for, flash, \
    jsonify

# instance with name of running app
# adding database to flask app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Making an API Endpoint (GET Request)
@app.route('/restaurants/JSON/')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(allrestaurants=[i.serialize for i in restaurants])


# Making an API Endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
    # restaurant = restaurantMenuJSON(restaurant_id) doesn't exist in solution code but y??
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItems=[menuItem.serialize])


"""decorator"""


# @app decorator will wrap function inside the app.route function that flash has created
# so either of these routes gets sent from browser function defined here gets executed

@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurant = session.query(Restaurant).all()
    flash('This page will show all my restaurants')
    output = ''
    return render_template('showRestaurants.html')


@app.route('/restaurants/new/', methods=['GET', 'POST'])
# by default the route only responds to get requests but method makes it reposond to whatever you set it to
def newRestaurant():
    if request.method == 'POST':
        newrestaurant = Restaurant(name=request.form['name'])
        session.add(newrestaurant)
        session.commit()
        flash('This page will be for making a new restaurant')
        return redirect(url_for('showrestaurants'))

    #return redirect("/showRestaurants") or redirect(url_for("/restaurant"))
    #it's not the function it's the url, you're trying to build the url

    else:
        return render_template('newrestaurant.html')




@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id,
                                                           ).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        session.commit()
        flash("This page will be for editing restaurant")
        return redirect(url_for('showRestaurants'))
    #url_for(show function) show the endpoint
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template('editRestaurant.html',
                               restaurant_id=restaurant_id, i=editedRestaurant)
#use variables, for example restaurant_id, when it is applicable, otherwise leave out
#this applies to variables that point within also, i.e. restaurant_id/menu_id
#can also directly provide url


@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    itemToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("This page will be for deleting restaurant")
        return redirect(url_for('showrestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant_id=restaurant_id,
                               item=itemToDelete)


# @app.route('/hello'), trailing slash will allow flash to
#  render the page even if it's not there
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by \
        (id=restaurant_id).one()
    items = session.query(MenuItem).filter_by \
        (restaurant_id=restaurant_id)
    return render_template('showMenu.html', restaurant=restaurant, items=items, restaurant_id=restaurant_id)

# Task1: create route for newmenuitem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
# by default the route only responds to get requests but method makes it reposond to whatever you set it to

def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
            'description'], price=request.form['price'],
                           course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash('new menu item created')
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)
        # restaurant = session.query(Restaurant).filter_by \
        #   (id=restaurant_id).one()
        # items = MenuItem()
        # items.name = raw_input(MenuItem.name) + '</br>'
        #  items.course = raw_input(MenuItem.course) + '</br>'
        #   items.price = raw_input(MenuItem.price) + '</br>'
    #    items.description = raw_input(MenuItem.description)+ '</br>'

    # newItem = MenuItem(name= items.name, description=items.description,
    #                   price = items.price, course=items.course, restaurant=restaurant)
    #   session.add(newItem)


#    session.commit()


# Task2: create route for editmenuitem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by \
        (id=restaurant_id).one()
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("menu item edited")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template('editmenuitem.html', restaurant_id=restaurant.id,item=editedItem)

        # task3:create a route for deletemenuitem function here


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by \
        (id=restaurant_id).one()
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("menu item deleted")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', item=itemToDelete, restaurant_id=restaurant_id)


# main is app run by interpreter, other file have __name of pythonfile__
# main is ensuring it can't be imported, by default server is only accessible from host machine

if __name__ == '__main__':
    # debug support ensures server will reload itself
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
