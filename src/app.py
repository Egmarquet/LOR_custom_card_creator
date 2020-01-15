import sys, os, uuid
sys.path.append("..")
import root
from resources import database, assets
from flask import Flask, session, redirect, url_for, escape, request, send_file
from flask_restful import Resource, Api, reqparse, abort
app = Flask(__name__)
api = Api(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

"""
API:
    /api/session/ : Get new card session. I.e. holds all the cards for a current user
        GET: Returns a cookie with a session_id attached
            as well as:

            session : {
                cards : []
            }

    /api/session/card/ :
        GET : Requires Card ID for the session
            {
                card: {
                    id: 10
                }
            }

            Returns:
            {
                url : (url to card image)
            }

        POST:
            Creates a new card with the specifications

            {
                type : <Card type>,
                name : <text>
                hp : <text if applicable>,
                mana : <text if applicable>,
                pwr : <text if applicable>,
                card_text : <text with formatting>,
                lvl_up_text : <text with formatting>,
                tribe : <text>,
                region : <text>,
                keywords : [],
                image : <blob of image data>
            }


            Returns:
            {
                card : {
                    id : <int>
                    url : url to card image
                    type : <Card type>,
                    namme : <text>,
                    hp : <text if applicable>,
                    mana : <text if applicable>,
                    pwr : <text if applicable>,
                    card_text : <text with formatting>,
                    lvl_up_condition : <text with formatting>,
                    tribe : <text>,
                    region : <text>,
                    keywords : [],
                    image : <blob of image data>
                }
            }

    /api/session/card/image/(card url)

"""

class Session(Resource):
    def get(self):
        """
        Args:
            Cookie containing session_id

        Returns:
            json :
            {
                cards : [<card_id>]
            }

            card_id's associated with the session
        """

        if 'session_id' in session:
            return "You are logged in!", 200
        else:
            """
            Session Creation
                - Create database table entry
                - Create file system for images
            """
            # Session creation
            session_id = database.create_session()
            session['session_id'] = session_id

            # File stucture creation
            os.mkdir(os.path.join(root.ROOT,"sessions",str(session_id)))
            return "Session created!", 200

class Card(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser(bundle_errors=True)
        self.post_parser.add_argument('type', required=True)
        self.post_parser.add_argument('name')
        self.post_parser.add_argument('hp')
        self.post_parser.add_argument('mana')
        self.post_parser.add_argument('pwr')
        self.post_parser.add_argument('card_text')
        self.post_parser.add_argument('lvl_up_text')
        self.post_parser.add_argument('tribe')
        self.post_parser.add_argument('region')
        self.post_parser.add_argument('image')

        self.patch_parser = reqparse.RequestParser(bundle_errors=True)
        self.patch_parser.add_argument('type', required=True)
        self.patch_parser.add_argument('name')
        self.patch_parser.add_argument('hp')
        self.patch_parser.add_argument('mana')
        self.patch_parser.add_argument('pwr')
        self.patch_parser.add_argument('card_text')
        self.patch_parser.add_argument('lvl_up_text')
        self.patch_parser.add_argument('tribe')
        self.patch_parser.add_argument('region')
        self.patch_parser.add_argument('image')


    def post(self):
        if 'session_id' not in session:
            return 'requires GET request from /api/session to set cookie', 401

        else:
            session_id = session['session_id']
            args = self.post_parser.parse_args()

            # Handling card type
            card_type = args['type']
            if card_type not in assets.UNIT_FRAMES:
                return 'Unknown card type', 400

            # Creating data entry
            data = (session_id, args['type'], args['name'], args['hp'], args['mana'], args['pwr'], args['card_text'], args['lvl_up_text'], args['tribe'], args['region'],)
            card_id = database.create_card(data)

            # Creating image directory
            os.mkdir(os.path.join(root.ROOT,"sessions",str(session_id),str(card_id)))

            return card_id, 200

    def patch(self):
        if 'session_id' not in session:
            return 'requires GET request from /api/session to set cookie', 401

if __name__ == '__main__':
    api.add_resource(Session, '/api/session')
    api.add_resource(Card, '/api/session/card')
    app.run(debug=True)
