"""Flask app for Cupcakes"""

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, request, jsonify, json
from models import db, connect_db, Cupcake, DEFAULT_IMAGE

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = 'JohnathonAppleseed452'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
# debug = DebugToolbarExtension(app)

db.create_all()


def serialize_cupcake(cupcake):
    """Serialize cupcake for use in jsonifying"""

    return {
        'id': cupcake.id,
        'flavor': cupcake.flavor,
        'size': cupcake.size,
        'rating': cupcake.rating,
        'image': cupcake.image
    }


@app.route('/', methods=['GET'])
def get_main_page():
    """Returns the main page"""

    return render_template('main.html')


@app.route('/api/cupcakes', methods=['GET'])
def get_cupcakes():
    """Gets the list of all cupcakes"""

    cupcakes = Cupcake.query.all()
    serialize = [serialize_cupcake(c) for c in cupcakes]
    return jsonify(cupcakes=serialize)


@app.route('/api/cupcakes/<cupcake_id>', methods=['GET'])
def get_cupcake(cupcake_id):
    """Gets the specified cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=serialize_cupcake(cupcake))


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Creates a new cupcake"""

    data = request.json
    cupcake = Cupcake(flavor=data.get('flavor', None), size=data.get('size', None),
                      rating=data.get('rating', None), image=data.get('image', None))
    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=serialize_cupcake(cupcake)), 201


@app.route('/api/cupcakes/<cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Updates the specified cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.json
    cupcake.flavor = data.get('flavor')
    cupcake.size = data.get('size')
    cupcake.rating = data.get('rating')
    cupcake.image = data.get('image')
    db.session.commit()
    return jsonify(cupcake=serialize_cupcake(cupcake))


@app.route('/api/cupcakes/<cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Deletes the specified cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message='Deleted')
