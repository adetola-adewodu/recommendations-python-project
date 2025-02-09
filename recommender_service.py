from flask import Flask, Response, request, jsonify, g
import pg8000
import json
import yaml

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        with open("database.yml", "r") as ymlfile:
            cfg = yaml.safe_load(ymlfile)
            database_variables = cfg["dev"]
            user = database_variables['user']
            database = database_variables['db']
            g.db = pg8000.connect(user=user, database=database)
            g.cursor = g.db.cursor()
    return g.db, g.cursor

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/movies/ratings/<id>')
def get_ratings_by_id(id):
    _, cursor = get_db()
    query = '''SELECT interactions.user_id, movies.title, interactions.event_value, movies.genre 
               FROM movies, interactions 
               WHERE movies.item_id = interactions.item_id
               AND interactions.user_id = %s;'''
    result = {}
    try:
        cursor.execute(query, (id,))
        rows = cursor.fetchall()
        result = json.dumps(rows, separators=(',', ':'))
    except Exception as err:
        print("Exception: {0}".format(err))
        cursor.execute("ROLLBACK")
        return jsonify({"error": str(err)}), 500
    
    return Response(result, mimetype='application/json')

@app.route('/movies')
def get_movies_by_title():
    _, cursor = get_db()
    title = request.args.get('title')
    query = '''select * from movies where title like %s;'''
    results = {}
    try:
        cursor.execute(query, ('%' + title + '%',))
        rows = cursor.fetchall()
        results = json.dumps(rows, separators=(',', ':'))
    except Exception as err:
        print("Exception: {0}".format(err))
        cursor.execute("ROLLBACK")
    
    return results

if __name__ == '__main__':
    app.run(debug=True)