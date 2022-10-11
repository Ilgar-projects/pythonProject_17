from flask import request
from flask_restx import Resource

from config import api, app, db
from models import Movie, Genre
from schemas import MovieSchema, GenreSchema

movie_ns = api.namespace("movies")
movies_schemas = MovieSchema(many=True)
movies_schema = MovieSchema()


@movie_ns.route("/")
class MovieViews(Resource):
    def get(self):
        query = Movie.query  # Select * from movie

        director_id = request.args.get('director_id')
        if director_id:
            query = query.filter(Movie.director_id == director_id)  # + where director_id = director_id

        if genre_id := request.args.get('genre_id'):
            query = query.filter(Movie.genre_id == genre_id)  # + and

        return movies_schemas.dump(query)

    def post(self):
        data = request.json
        try:
            db.session.add(
                Movie(
                    **data
                )
            )
            db.session.commit()
            return "Данные добавлены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200


@movie_ns.route("/<int:pid>")
class MovieViews(Resource):
    def get(self, pid):
        query = Movie.query.get(pid)
        return movies_schema.dump(query)

    def put(self, pid):
        data = request.json
        try:
            db.session.query(Movie).filter(Movie.id == pid).update(data)
            db.session.commit()
            return "Данные обновлены", 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

    def delete(self, pid):
        try:
            db.session.query(Movie).filter(Movie.id == pid).delete()
            db.session.commit()
            return "Данные удалены", 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

genre_ns = api.namespace("genres")
genre_schemas = GenreSchema(many=True)
genre_schema = GenreSchema()


@genre_ns.route("/")
class GenreViews(Resource):
    def get(self):
        query = Genre.query  # Select * from movie


        return genre_schemas.dump(query)

    def post(self):
        data = request.json
        try:
            db.session.add(
                Genre(
                    **data
                )
            )
            db.session.commit()
            return "Данные добавлены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200


@movie_ns.route("/<int:pid>")
class GenreViews(Resource):
    def get(self, pid):
        query = Genre.query.get(pid)
        return movies_schema.dump(query)

    def put(self, pid):
        data = request.json
        try:
            db.session.query(Genre).filter(Genre.id == pid).update(data)
            db.session.commit()
            return "Данные обновлены", 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

    def delete(self, pid):
        try:
            db.session.query(Genre).filter(Genre.id == pid).delete()
            db.session.commit()
            return "Данные удалены", 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, 200

if __name__ == '__main__':
    app.run(debug=True)
