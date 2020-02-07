from flask import Flask
from flask_restful import reqparse, Api, Resource

app = Flask(__name__)
api = Api(app)

class Run(Resource):

    def get(self):
        return {
            "current_url": api.url_for(self),
          }, 200


# Setup the Api resource routing here
RESOURCES = [
  (Run, '/run'),
]

for resource, endpoint in RESOURCES:
    api.add_resource(resource, endpoint)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000)
