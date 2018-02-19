import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy import asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Artists, Projects, User
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials

import httplib2
import json
from flask import make_response
import requests




app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "African artists"

engine = create_engine('sqlite:///artistswithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# ADD JSON ENDPOINT HERE

@app.route('/artists/<int:artist_id>/JSON')
def artistJSON(artist_id):
    artist = session.query(Artists).filter_by(id=artist_id).one()
    return jsonify(Artists=artist.serialize)


@app.route('/artists/<int:artist_id>/projects/<int:project_id>/JSON')
def projectJSON(artist_id, project_id):
    projects = session.query(Projects).filter_by(id=project_id).one()
    return jsonify(Projects=projects.serialize)

# Create anti-forgery state token
@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST', 'GET'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
     # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    #see if user exists, if it doesn't make a new one


    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None



# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect/')
def gdisconnect():
    gplus_id = login_session['gplus_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/fbconnect', methods=['GET', 'POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data


    app_id = json.loads(open('fbclientsecrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fbclientsecrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]


    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/artists/')
def showArtists():
    artists = session.query(Artists).order_by(asc(Artists.name))
    if 'username' not in login_session:
        return render_template('public_artists.html', artists=artists)
    else:
        return render_template('artists.html', artists=artists)

@app.route('/artists/new/', methods =['GET', 'POST'])
def newArtist():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newArtistItem = Artists(name = request.form['name'], bio = request.form['bio'], country = request.form['country'], category = request.form['category'], imageUrl = request.form['imageUrl'], user_id=login_session['user_id'])
        session.add(newArtistItem)
        session.commit()
        flash("New artist created")
        return redirect(url_for('showArtists'))
    else:
        return render_template('newartist.html')

@app.route('/artists/<int:artist_id>/edit/', methods = ['GET', 'POST'])
def editArtist(artist_id):
    editedArtistItem = session.query(Artists).filter_by(id=artist_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedArtistItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not allowed to edit this artist. Please create your own artist in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedArtistItem.name = request.form['name']
        if request.form['bio']:
            editedArtistItem.bio = request.form['bio']
        if request.form['category']:
            editedArtistItem.picture = request.form['category']
        if request.form['country']:
            editedArtistItem.country = request.form['country']
        if request.form['imageUrl']:
            editedArtistItem.imageUrl = request.form['imageUrl']
        session.add(editedArtistItem)
        session.commit()
        flash("Artist successfully edited")
        return redirect(url_for('showArtists', artist_id = artist_id))
    else:
        return render_template('editartist.html', a=editedArtistItem, artist_id=artist_id)

@app.route('/artists/<int:artist_id>/delete/', methods = ['GET', 'POST'])
def deleteArtist(artist_id):
    artistToDelete = session.query(Artists).filter_by(id=artist_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if artistToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not allowed to delete this artist. Please create your own artist in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(artistToDelete)
        session.commit()
        flash("Artist successfully deleted")
        return redirect(url_for('showArtists', artist_id=artist_id))
    return render_template('deleteartist.html', a=deleteArtist, artist_id=artist_id)


@app.route('/artists/<int:artist_id>/projects/')
@app.route('/artists/<int:artist_id>/')
def showProjects(artist_id):
    artist = session.query(Artists).filter_by(id=artist_id).one()
    creator = getUserInfo(artist.user_id)
    projects = session.query(Projects).filter_by(artist_id=artist_id).all()
    if 'username' not in login_session or creator != login_session['user_id']:
        return render_template('public_projects.html', projects=projects, artist=artist, creator=creator)
    else:
        return render_template('projects.html', projects=projects, artist=artist, creator=creator)

@app.route('/artists/<int:artist_id>/projects/new/', methods = ['GET', 'POST'])
def newProject(artist_id):
    if 'username' not in login_session:
        return redirect('/login')
    artist = session.query(Artists).filter_by(id=artist_id).one()
    if artist.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not allowed to add project to this artist. Please create your own artist in order to add project.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        newProjectItem = Projects(title = request.form['title'], description = request.form['description'],imageUrl = request.form['imageUrl'], artist_id=artist_id)
        session.add(newProjectItem)
        session.commit()
        flash("New Project created")
        return redirect(url_for('showProjects', artist_id=artist_id))
    else:
        return render_template('newproject.html',artist_id=artist_id)

@app.route('/artists/<int:artist_id>/projects/<int:project_id>/edit/', methods = ['GET', 'POST'])
def editProject(artist_id, project_id):
    editedProjectItem = session.query(Projects).filter_by(id=project_id).one()
    if 'username' not in login_session:
        return redirect('/login')
        return redirect('/login')
    if editedProjectItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not allowed to edit this artist. Please create your own artist in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['title']:
            editedProjectItem.title = request.form['title']
        if request.form['description']:
            editedProjectItem.description = request.form['description']
        if request.form['imageUrl']:
            editedProjectItem.imageUrl = request.form['imageUrl']
        session.add(editedProjectItem)
        session.commit()
        flash("Project edited successfully")
        return redirect(url_for('showProjects', artist_id = artist_id))
    else:
        return render_template('editproject.html', artist_id=artist_id, project_id=project_id, project=editedProjectItem)

@app.route('/artists/<int:artist_id>/projects/<int:project_id>/delete/', methods=['GET', 'POST'])
def deleteProject(artist_id, project_id):
    projectToDelete = session.query(Projects).filter_by(id=project_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if projectToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not allowed to edit this artist. Please create your own artist in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(projectToDelete)
        session.commit()
        flash("Project deleted successfully")
        return redirect(url_for('showProjects', artist_id=artist_id, project_id=project_id))
    else:
        return render_template('deleteartist.html', artist_id=artist_id, project_id=project_id, project=projectToDelete)

# Disconnect based on provider
@app.route('/disconnect/')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showArtists'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showArtists'))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
