from flask_restx import Resource, reqparse

from src.ext import api
from src.models import Plant


parser = reqparse.RequestParser()
parser.add_argument("page", type=int, default=1, required=True)
parser.add_argument("search", type=str, required=False)
parser.add_argument("sort", type=str, required=False)

limit = 10

@api.route("/plant")
class PlantAPI(Resource):
    @api.expect(parser)
    def get(self,):
        args = parser.parse_args()
        page = args['page']
        search = args['search']
        sort = args['sort']

        plants = Plant.query

        if search:
            plants = plants.filter(Plant.name.ilike(f"%{search}%"))

        if sort == "asc":
            plants = plants.order_by(Plant.name.asc())
        elif sort == "desc":
            plants = plants.order_by(Plant.name.desc())

        plants = plants.limit(limit).offset((page - 1) * limit)

        plants_json = [{"id": plant.id,
                        "name" : plant.name,
                        "eng_name" : plant.eng_name,
                        "lat_name": plant.lat_name,
                        "image": plant.image} for plant in plants]

        return plants_json, 200

@api.route("/plant/<int:id>")  # Route for a specific plant
class PlantAPI(Resource):
    def get(self, id):
        plant = Plant.query.get_or_404(id)
        plants_json = [{"id": plant.id,
                        "name": plant.name,
                        "eng_name": plant.eng_name,
                        "lat_name": plant.lat_name,
                        "image": plant.image}]
        return plants_json, 200