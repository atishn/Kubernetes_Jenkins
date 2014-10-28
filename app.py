from flask import Flask
from flask.ext import restful

from app.api.ListPods import ListPods

app = Flask(__name__)
api = restful.Api(app)

# Set local vars
app.config.update(
    KUBE_ROOT=".." 
)

# kube-up

# list pods - to make sure works
api.add_resource(ListPods, '/list-pods')


if __name__ == "__main__":
    app.run()