from flask.ext.restful import reqparse, Resource

from stormy.app.helpers.api_helpers import new_service


class NewService(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('serviceport', type=str)
        parser.add_argument('containerport', type=int)
        parser.add_argument('selectorkey', type=str)
        parser.add_argument('selectorvalue', type=int)

        args = parser.parse_args()

        server_response = new_service(args['name'], args['serviceport'], args['containerport'], args['selectorkey'],
                                      args['selectorvalue'])

        return server_response


class NewMasterService(Resource):
    def get(self):
        server_response = new_service('masterservice', 49171, 8090, 'name', 'jenkinsmaster')
        return server_response
