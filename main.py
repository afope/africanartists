import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Artists, Projects
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests




app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "African Artists App"

engine = create_engine('sqlite:///artistdatabase.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect/', methods=['POST', 'GET'])
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
    url = ('http://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
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
    userinfo_url = "http://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

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

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect/')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'http://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/artists/')
def showArtists():
    artists = session.query(Artists).all()
    output = ''
    return render_template('artists.html', artists=artists)

@app.route('/artists/new/', methods =['GET', 'POST'])
def newArtist():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newArtistItem = Artists(name = request.form['name'], bio = request.form['bio'], country = request.form['country'], category = request.form['category'], imageUrl = request.form['imageUrl'])
        session.add(newArtistItem)
        session.commit()
        flash("New artist created")
        return redirect(url_for('showArtists'))
    else:
        return render_template('newartist.html')

@app.route('/artists/<int:artist_id>/edit/', methods = ['GET', 'POST'])
def editArtist(artist_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedArtistItem = session.query(Artists).filter_by(id=artist_id).one()
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
    if 'username' not in login_session:
        return redirect('/login')
    artistToDelete = session.query(Artists).filter_by(id=artist_id).one()
    if request.method == 'POST':
        session.delete(artistToDelete)
        session.commit()
        flash("Artist successfully deleted")
        return redirect(url_for('showArtists', artist_id=artist_id))
    return render_template('deleteartist.html', a=deleteArtist, artist_id=artist_id)


@app.route('/artists/<int:artist_id>/projects/')
@app.route('/artists/<int:artist_id>/')
def showProjects(artist_id):
    projects = session.query(Projects).all()
    output = ''
    return render_template('projects.html', projects=projects)

@app.route('/artists/<int:artist_id>/projects/new/', methods = ['GET', 'POST'])
def newProject(artist_id):
    if 'username' not in login_session:
        return redirect('/login')
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
    if 'username' not in login_session:
        return redirect('/login')
    editedProjectItem = session.query(Projects).filter_by(id=project_id).one()
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
    if 'username' not in login_session:
        return redirect('/login')
    projectToDelete = session.query(Projects).filter_by(id=project_id).one()
    if request.method == 'POST':
        session.delete(projectToDelete)
        session.commit()
        flash("Project deleted successfully")
        return redirect(url_for('showProjects', artist_id=artist_id, project_id=project_id))
    else:
        return render_template('deleteartist.html', artist_id=artist_id, project_id=project_id, project=projectToDelete)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
