from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Artists, Projects

app = Flask(__name__)

engine = create_engine('sqlite:///artistdatabase.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# json endpoints for /artists/json
@app.route('/artists/JSON/')
def artistJSON():
    artists = session.query(Artists).all()
    return jsonify(Artists=[artist.serialize for artist in artists])

# json endpoints for /artists/<int:artist_id>/projects/JSON/'
@app.route('/artists/<int:artist_id>/projects/JSON/')
def showprojectsJSON(artist_id):
    projects = session.query(Projects).all()
    return jsonify(Projects=[project.serialize for project in projects])

# json endpoints for /artists/<int:artist_id>/projects/<int:project_id>/JSON/'
@app.route('/artists/<int:artist_id>/projects/<int:project_id>/JSON')
def projectItemJSON(artist_id, project_id):
    projectItem = session.query(Projects).filter_by(id=project_id).one()
    return jsonify(Projects=projectItem.serialize)

@app.route('/')
@app.route('/artists/')
def showArtists():
    artists = session.query(Artists).all()
    output = ''
    return render_template('artists.html', artists=artists)

@app.route('/artists/new/', methods =['GET', 'POST'])
def newArtist():
    if request.method == 'POST':
        newArtistItem = Artists(name = request.form['name'], bio = request.form['bio'], country = request.form['country'], category = request.form['category'], imageUrl = request.form['imageUrl'])
        session.add(newArtistItem)
        session.commit()
        flash("New artist added!")
        return redirect(url_for('showArtists'))
    else:
        return render_template('newartist.html')

@app.route('/artists/<int:artist_id>/edit/', methods = ['GET', 'POST'])
def editArtist(artist_id):
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
        flash("Artist details edited!")
        return redirect(url_for('showArtists', artist_id = artist_id))
    else:
        return render_template('editartist.html', artist_id=artist_id)

@app.route('/artists/<int:artist_id>/delete/', methods = ['GET', 'POST'])
def deleteArtist(artist_id):
    artistToDelete = session.query(Artists).filter_by(id=artist_id).one()
    if request.method == 'POST':
        session.delete(artistToDelete)
        session.commit()
        flash("Artist deleted!")
        return redirect(url_for('showArtists', artist_id=artist_id))
    return render_template('deleteartist.html', artist_id=artist_id)


@app.route('/artists/<int:artist_id>/projects/')
@app.route('/artists/<int:artist_id>/')
def showProjects(artist_id):
    projects = session.query(Projects).all()
    output = ''
    return render_template('projects.html', projects=projects)

@app.route('/artists/<int:artist_id>/projects/new/', methods = ['GET', 'POST'])
def newProject(artist_id):
    if request.method == 'POST':
        newProjectItem = Projects(title = request.form['title'], description = request.form['description'],imageUrl = request.form['imageUrl'], artist_id=artist_id)
        session.add(newProjectItem)
        session.commit()
        flash("New Project added!")
        return redirect(url_for('showProjects', artist_id=artist_id))
    else:
        return render_template('newproject.html',artist_id=artist_id)

@app.route('/artists/<int:artist_id>/projects/<int:project_id>/edit/', methods = ['GET', 'POST'])
def editProject(artist_id, project_id):
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
        flash(" details edited!")
        return redirect(url_for('showProjects', artist_id = artist_id))
    else:
        return render_template('editproject.html', artist_id=artist_id, project_id=project_id, item=editedProjectItem)

@app.route('/artists/<int:artist_id>/projects/<int:project_id>/delete/', methods=['GET', 'POST'])
def deleteProject(artist_id, project_id):
    projectToDelete = session.query(Projects).filter_by(id=project_id).one()
    if request.method == 'POST':
        session.delete(projectToDelete)
        session.commit()
        return redirect(url_for('showProjects', artist_id=artist_id, project_id=project_id))
    return render_template('deleteartist.html', artist_id=artist_id, project_id=project_id)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
