from flask import Flask, render_template, request, redirect, url_for,jsonify,flash
app = Flask(__name__)

# #Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
#
# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]
#
#
# #Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# json api here
@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def menuJSON(restaurant_id):
    menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(Menu=[i.serialize for i in menu])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id,menu_id):
    menu = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=[menu.serialize])


# get and post
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    # return "This page will show all my restaurants"
    restaurants = session.query(Restaurant).all()
    return render_template('Restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new',methods=['Get','POST'])
def newRestaurant():
    if request.method == 'POST':
        new_Restaurant = Restaurant(name = request.form['name'])
        session.add(new_Restaurant)
        session.commit()
        flash("New Restaurant Created!")
        return redirect(url_for('showRestaurants'))
    else:
    # return "This page will be for making a new restaurant"
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit',methods=['Get','POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        restaurant.name=request.form['name']
        session.add(restaurant)
        session.commit()
        flash("Restaurant Successfully Edited!")
        return redirect(url_for('showRestaurants'))
    else:
    # return "This page will be for editing restaurant %s"%restaurant_id
        return render_template('editRestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete',methods=['Get','POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash("Restaurant Successfully Deleted!")
        return redirect(url_for('showRestaurants'))
    else:
    # return "This page will be for deleting restaurant %s"%restaurant_id
        return render_template('deleteRestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    # return "This Page is the menu for restaurant %s"%restaurant_id
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('menu.html',restaurant = restaurant, items = items)

@app.route('/restaurant/<int:restaurant_id>/menu/new',methods=['Get','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        menu = MenuItem(name = request.form['name'], description=request.form['Description'],price=request.form['Price'],restaurant_id=restaurant_id,course=request.form['course'])
        session.add(menu)
        session.commit()
        flash("MenuItem Created!")
        return redirect(url_for("showMenu",restaurant_id=restaurant_id))
    else:
    # return "This page is for making a new menu item for restaurant %s"%restaurant_id
        return render_template('newMenuItem.html',restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',methods=['Get','POST'])
def editMenuItem(restaurant_id,menu_id):
    if request.method == 'POST':
        menu = session.query(MenuItem).filter_by(id=menu_id).one()
        menu.name = request.form['name']
        session.add(menu)
        session.commit()
        flash("MenuItem  Successfully Edited!")
        return redirect(url_for("showMenu",restaurant_id=restaurant_id))
    else:
    # return "This page is for editing menu item %s"%menu_id
        return render_template('editMenuItem.html',restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',methods=['Get','POST'])
def deleteMenuItem(restaurant_id,menu_id):
    menu = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(menu)
        session.commit()
        flash("MenuItem Successfully Deleted!")
        return redirect(url_for("showMenu",restaurant_id=restaurant_id))
    else:
    # return "This page is for deleting menu item %s"%menu_id
        return render_template('deleteMenuItem.html', item = menu,restaurant_id=restaurant_id)


if __name__== '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
