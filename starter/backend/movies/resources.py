from flask import jsonify, request
from flask.views import MethodView

# Dummy database to hold movie examples
movies = {
    "123": {"title": "Top Gun: Maverick", "description": "Fighter planes"},
    "456": {"title": "Sonic the Hedgehog", "description": "Blue Sega character"},
    "789": {"title": "A Quiet Place", "description": "Scary monsters"},
}


class Movies(MethodView):

    def get(self, movie_id):
        if movie_id is None:
            return jsonify({
                "movies": [
                    {
                        "id": movie_id,
                        "title": movie["title"],
                    }
                    for movie_id, movie in movies.items()
                ]
            })

        movie = movies.get(str(movie_id))

        if movie is None:
            return jsonify({"error": "Movie not found"}), 404

        return jsonify({
            "movie": {
                "id": str(movie_id),
                **movie
            }
        })

    def post(self):
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "JSON body is required"}), 400

        title = data.get("title")
        description = data.get("description")

        if not title or not description:
            return jsonify({
                "error": "title and description are required"
            }), 400

        movie_id = str(max([int(i) for i in movies.keys()] or [0]) + 1)

        movies[movie_id] = {
            "title": title,
            "description": description,
        }

        return jsonify({
            "movie": {
                "id": movie_id,
                **movies[movie_id]
            }
        }), 201

    def put(self, movie_id):
        movie_id = str(movie_id)

        if movie_id not in movies:
            return jsonify({"error": "Movie not found"}), 404

        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "JSON body is required"}), 400

        if "title" in data:
            movies[movie_id]["title"] = data["title"]

        if "description" in data:
            movies[movie_id]["description"] = data["description"]

        return jsonify({
            "movie": {
                "id": movie_id,
                **movies[movie_id]
            }
        })

    def delete(self, movie_id):
        movie_id = str(movie_id)

        if movie_id not in movies:
            return jsonify({"error": "Movie not found"}), 404

        deleted_movie = movies.pop(movie_id)

        return jsonify({
            "message": "Movie deleted",
            "movie": {
                "id": movie_id,
                **deleted_movie
            }
        })
