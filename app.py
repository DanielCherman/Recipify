####Import for the flask app####
import math
import os
import bcrypt
from flask import Flask, render_template, redirect, request, url_for, flash, session, Blueprint
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from forms import Login, Register, Recipe
from flask_login import LoginManager, login_required
from flask_wtf.csrf import CSRFProtect

#DEFINE FLASK APP and CRSF
csrf = CSRFProtect()
app = Flask(__name__)

#Configure the Mongo DB and secret key
app.config["MONGO_URI"] = "mongodb+srv://recepie:recepie@zina.bbmfj.mongodb.net/recipe"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "secret")
mongo = PyMongo(app)

#Define the Login Manager
login_manager = LoginManager(app)
csrf.init_app(app)

#Home/Index page endpoint
@app.route('/', methods=['POST', 'GET'])
def index():

    current_page = int(request.args.get('current_page', 1))
    total_pages = mongo.db.Recipes.estimated_document_count()

    pages = range(1, 
                int
                (math.ceil
                (total_pages / 5)
                )
                + 1)
    recipes_meta_data = mongo.db.Recipes.find().sort('_id', pymongo.DESCENDING).skip((current_page - 1)*5).limit(5)

    return render_template("index.html", recipe=recipes_meta_data, pages=pages, current_page=current_page)

#Get details of the recipe (recipe_id as argument) 
@app.route('/recipes/<recipe_id>', methods=['POST', 'GET'])
def recipe(recipe_id):
    
    recipe_details = mongo.db.Recipes.find_one({"_id": ObjectId(recipe_id)})

    return render_template('recipe.html', recipe=recipe_details, title=recipe_details['recipe_name'])

#Delete the recipe from the db and can be deleted by admins/prievlaged users
@app.route('/delete/<recipe_id>', methods=['POST', 'GET', 'DELETE'])
def delete(recipe_id):

    #Check if username is present in the session created
    if 'username' not in session:
        flash('Username not found!!!')
        return redirect('recipe/<recipe_id>')

    rep = mongo.db.Recipes.find_one({'_id': ObjectId(recipe_id)})

    #Check if user has sufficient permissions
    if rep['username'] != session['username']:
        flash('Insufficient permissions for this user')
        return redirect(url_for('register'))
    
    mongo.db.Recipes.remove({'_id': ObjectId(recipe_id)})
    flash('Recipe removed')
    
    return redirect(url_for('index'))

#Endpoint to edit the recipe 
@app.route('/editrecipe/<recipe_id>', methods=['GET', 'POST'])
def editrecipe(recipe_id):

    #Check if username is present in the session created
    if 'username' not in session:
        flash('Not possible for non-members! Please create an account.')
        return redirect(url_for('register'))

    form = Recipe()
    find_recipe = mongo.db.Recipes.find_one({'_id': ObjectId(recipe_id)})
    
    #Check if user has sufficient permissions
    if find_recipe['username'] != session['username']:
        flash('Insufficient permissions')
        return redirect(url_for('register'))

    if request.method == 'GET':
        form = Recipe(data=find_recipe)
        return render_template('edit_recipe.html', recipe=find_recipe,
                               form=form, title="Edit Recipe")

    if form.validate_on_submit:
        recipes = mongo.db.Recipes
        recipes.update_one({'_id': ObjectId(recipe_id), }, {
            '$set': {'recipe_name': request.form['recipe_name'],
                     'recipe_type': request.form['recipe_type'],
                     'recipe_desc': request.form['recipe_desc'],
                     'serving': request.form['serving'],
                     'prep_time': request.form['prep_time'],
                     'cook_time': request.form['cook_time'],
                     'ingredients': request.form.getlist('ingredients'),
                     'method': request.form.getlist('methods'),
                     'img_url': request.form['img_url']}})

        flash('Recipe updated')
        return redirect(url_for('recipe', recipe_id=recipe_id))

    return render_template(url_for('recipe', recipe_id=recipe_id))

#endpoint to add the recipe to DB
@app.route('/addrecipe', methods=['GET', 'POST'])
def addrecipe():
    #Check if username is present in the session created
    if 'username' not in session:
        flash('Requires to have an account')
        return redirect(url_for('register'))

    form = Recipe()
    #Add the recipe in the DB
    if request.method == 'POST' and form.validate_on_submit():
        recipe = mongo.db.Recipes
        recipe.insert_one({'recipe_name': request.form['recipe_name'],
                       'recipe_type': request.form['recipe_type'],
                       'recipe_desc': request.form['recipe_desc'],
                       'serving': request.form['serving'],
                       'prep_time': request.form['prep_time'],
                       'cook_time': request.form['cook_time'],
                       'ingredients': request.form.getlist('ingredients'),
                       'method': request.form.getlist('methods'),
                       'img_url': request.form['img_url'],
                       'username': session['username']
                       })

        flash('Recipe created')
        return redirect(url_for('index'))

    return render_template('addrecipe.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #Check if logged in flag is present in the session created
    if 'logged in' in session:
        return redirect(url_for('index'))

    form = Login()
    if request.method == "POST" and form.validate_on_submit:
        existing_user = mongo.db.users.find_one({'name': request.form['username']})

        #User not found in the DB       
        if existing_user is None:
            flash('User not found in DB')
            return redirect(url_for('login'))

        #Encrypting/Encoding the password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), existing_user['password']):
            session['username'] = request.form['username']
            session['logged in'] = True

            return redirect(url_for('index'))
        flash('Invalid credentials')

    return render_template('login.html', form=form)

#endpoint to register the user in the DB
@app.route('/register', methods=['GET', 'POST'])
def register():

    if 'username' in session:
        return redirect(url_for('index'))

    form = Register()
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        #Encrypting/Encoding the password
        if existing_user is None:
            
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'),bcrypt.gensalt())
            users.insert_one({'name': request.form['username'], 'password': hashpass})
 
            session['username'] = request.form['username']
            session['password'] = request.form['password']

            flash('User have been created')           
            return redirect(url_for('index'))

        flash('That username already exists!')

    return render_template('register.html', form=form)

#Endpoint to search for a specific recipe
@app.route('/search', methods=["GET", "POST"])
def search():
    current_page = int(request.args.get('current_page', 1))

    search_db = request.args['search_db']

    total = mongo.db.Recipes.find({'$text': {'$search': search_db}})
    
    t_total = len([r for r in total])
    
    pages = range(1, int(math.ceil(t_total / 5)) + 1)

    results = mongo.db.Recipes.find({'$text': {'$search': search_db}}).sort(
        '_id', pymongo.ASCENDING).skip((current_page - 1)*5).limit(
            5)

    if 'logged_in' in session:
        current_user = mongo.db.users.find_one()
        return render_template('search.html',
                               results=results, pages=pages,
                               current_page=current_page,
                               search_db=search_db, current_user=current_user,
                               title="Your Results", t_total=t_total)
    else:
        return render_template('search.html',
                               results=results, pages=pages,
                               current_page=current_page, search_db=search_db,
                               title="Your Results", t_total=t_total)

#Endpoint to logout of the user session
@app.route('/logout')
def logout():
    """Clear the session"""
    session.clear()
    # flash('You were logged out', category='info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=app.debug, port=8000, host='127.0.0.1')