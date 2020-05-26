# Recommender Web Service bases on movies 


## Download data

    curl http://files.grouplens.org/datasets/movielens/ml-1m.zip -o ml-1m.zip

    unzip -o ml-1m.zip

## Create tables

    create table interactions (
        user_id integer, 
        item_id integer, 
        event_value integer,
        timestamp varchar(20),
        event_type varchar(20)
    )

    CREATE TABLE movies (
        item_id integer,
        title  varchar(255),
        genre varchar(255)
    )

## Create csv files using pandas
    pip install -r requirements.txt

    python pandas_set_up.py

## Load data

    psql -d [database] --user=Adetola -c "COPY interactions(user_id, item_id, event_value, timestamp,event_type) FROM './interactions.csv' csv header;"

    psql -d [database] --user=Adetola -c "COPY movies(item_id, title, genre) FROM './movies.csv' csv header;"

## select query on data

    select interactions.user_id, movies.title, interactions.event_value, movies.genre from movies, interactions where movies.item_id = interactions.item_id

## To run web service

    pip install -r requirements_flask.txt

    python recommender_service.py


## Get Ratings given a user id
    http://127.0.0.1:5000/movies/ratings/2


## Get movies given a title
    http://127.0.0.1:5000/movies?title=Boss