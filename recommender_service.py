from flask import Flask, Response, request, jsonify
import pg8000
import json
import yaml

app = Flask(__name__)
conn = None
cursor = None

with open("database.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile)
        database_variables = cfg["dev"]
        # use our connection values to establish a connection
        user = database_variables['user']
        database = database_variables['db']
        conn = pg8000.connect(user=user, database=database)
        cursor = conn.cursor()

@app.route('/movies/ratings/<id>')
def get_ratings_by_id(id):

    query = '''select interactions.user_id, movies.title, interactions.event_value, movies.genre 
                from movies, interactions 
                where movies.item_id = interactions.item_id
                and interactions.user_id = '{id}';'''.format(id=id)
    result = {}
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        result = json.dumps(rows, separators=(',', ':'))
    except Exception as err:
        print("Exception: {0}".format(err))
        cursor.execute("ROLLBACK")
    
    return result

@app.route('/movies')
def get_movies_by_title():
    title = request.args.get('title')
    query = '''select * from movies where title like '%{title}%';'''.format(title=title)
    results = {}
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        results = json.dumps(rows, separators=(',', ':'))
    except Exception as err:
        print("Exception: {0}".format(err))
        cursor.execute("ROLLBACK")
    
    return results

if __name__ == '__main__':
    
    app.debug = True
    app.run()