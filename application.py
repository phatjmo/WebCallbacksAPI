#!/usr/bin/python

"""
Simple Web Callbacks API
"""

import datetime
from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from dateutil.parser import parse
from dateutil.tz import tzutc

application = Flask(__name__)
# application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/stats.db' # 'sqlite://' for :memory:
# application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['PORT'] = 4295
application.config['HOST'] = '0.0.0.0'
application.debug = True
# db = SQLAlchemy(application)
api = Api(application)
auth = HTTPBasicAuth()
webcallbacks = {}

@auth.get_password
def get_password(username):
    """
    Get password for user.
    """
    if username == 'optimise':
        return 'end2endComm'
    return None


@auth.error_handler
def unauthorized():
    """
    Bad Login Credentials
    """
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)

# API Classes
class WebCallbacksAPI(Resource):
    """
    Store Callbacks by Campaign ID
    """
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('leads', type=list, location='json')
        super(WebCallbacksAPI, self).__init__()

    def get(self, pprg):
        """
        Return all leads by PPRG
        """
        # args = self.reqparse.parse_args()
        try:
            return webcallbacks[pprg]
        except KeyError:
            return make_response(jsonify({'message': 'Campaign Not Found'}), 404)


    def post(self, pprg):
        """
        Append Lead to webcallbacks dict by PPRG.
        """
        args = self.reqparse.parse_args()
        print "Appending leads to {}".format(pprg)
        # print args
        if pprg in webcallbacks:
            for lead in args["leads"]:
                webcallbacks[pprg].append(lead)
        else:
            webcallbacks[pprg] = args["leads"]
        # print webcallbacks
        return {'result': True}, 200

    def delete(self, pprg):
        """
        Delete the leads from the webcallbacks dictionary by pprg.
        """
        try:
            del webcallbacks[pprg]
        except KeyError:
            pass
        return {'result': True}


class HealthCheckAPI(Resource):
    """
    Respond to basic healthchecks.
    """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='I cannot tell you your name if you do not give it to me!',
                                   location='json')
        super(HealthCheckAPI, self).__init__()

    def get(self):
        """ Return true if API is working """
        return {"result": True}, 200

    def post(self):
        """ Return the submitted name if POST is functioning. """
        args = self.reqparse.parse_args()
        return {"yournameis": args.name}, 200


# DB Model Classes
# class ChannelHistory(db.Model):
#     """
#     History of unique channels posted to the API
#     """
#     __tablename = 'channel_history'
#     id = db.Column(db.Integer, primary_key=True)
#     channel_id = db.Column(db.String(20), unique=False) # "1491434289.1031765"
#     instance_id = db.Column(db.String(20), unique=False)
#     name = db.Column(db.String(25), unique=False) # "PJSIP/kamailio-0001c4eb"
#     creationtime = db.Column(db.String(28), unique=False)
#     creation_datetime = db.Column(db.DateTime, unique=False)
#     insertion_datetime = db.Column(db.DateTime, unique=False)
#     caller = db.Column(db.String(10), unique=False)
#     caller_city = db.Column(db.String(28), unique=False)
#     caller_state = db.Column(db.String(2), unique=False)
#     caller_country = db.Column(db.String(2), unique=False)
#     caller_lat = db.Column(db.Float, unique=False)
#     caller_long = db.Column(db.Float, unique=False)
#     callee = db.Column(db.String(10), unique=False)
#     callee_city = db.Column(db.String(28), unique=False)
#     callee_state = db.Column(db.String(2), unique=False)
#     callee_country = db.Column(db.String(2), unique=False)
#     callee_lat = db.Column(db.Float, unique=False)
#     callee_long = db.Column(db.Float, unique=False)
#     siteid = db.Column(db.Integer, unique=False)

#     def __init__(self, **data):
#         for key, value in list(data.items()):
#             if key == "id":
#                 setattr(self, "channel_id", value)
#             else:
#                 setattr(self, key, value)

#     @property
#     def serialize(self):
#         """Return a dict without the SQLAlchemy garbage for jsonify."""
#         return {
#             "id": self.id,
#             "channel_id": self.channel_id,
#             "instance_id": self.instance_id,
#             "name": self.name,
#             "creationtime": self.creationtime,
#             "insertiontime": self.insertion_datetime.isoformat(),
#             "caller": self.caller,
#             "caller_city": self.caller_city,
#             "caller_state": self.caller_state,
#             "caller_country": self.caller_country,
#             "caller_lat": self.caller_lat,
#             "caller_long": self.caller_long,
#             "callee": self.callee,
#             "callee_city": self.callee_city,
#             "callee_state": self.callee_state,
#             "callee_country": self.callee_country,
#             "callee_lat": self.callee_lat,
#             "callee_long": self.callee_long,
#             "siteid": self.siteid
#         }

#     @staticmethod
#     def append_channels(channels):
#         """
#         Import the fondata csv file into SQLite memory database.
#         """
#         print("Appending channels to history...")
#         for channel in channels:
#             # print(channel["creationtime"])
#             creation_datetime = parse(channel["creationtime"]) # "2017-04-05T23:18:09.903+0000"
#             # print(creation_datetime)
#             channel["creation_datetime"] = creation_datetime
#             channel["insertion_datetime"] = datetime.datetime.now()
#             # print(channel)
#             if db.session.query(db.func.count(ChannelHistory.id)).filter_by(
#                     instance_id=channel["instance_id"],
#                     creationtime=channel["creationtime"],
#                     channel_id=channel["id"]).scalar() > 0:
#                 print("Channel: {0} on date: {1} is already in this history.".format(channel["id"], channel["creationtime"]))
#                 continue
#             try:
#                 print("Channel: {0} on date: {1} is being added to the history.".format(channel["id"], channel["creationtime"]))
#                 add_channel = ChannelHistory(**channel)
#                 # print(add_channel.serialize)
#                 db.session.add(add_channel)
#                 #db.session.add(ChannelHistory(**channel))
#                 db.session.commit()
#             except Exception, e:
#                 print("Append failed for reasons: {0}".format(str(e)))
#                 db.session.rollback()
#                 return False

#         return True

#     @staticmethod
#     def clear_history(days=0):
#         """
#         Clear channel history older than N days.
#         """
#         clear_date = datetime.datetime.now().date() - datetime.timedelta(days=days)
#         print("Clearing history from {0} and older.".format(clear_date))
#         try:
#             db.session.query(ChannelHistory).filter(ChannelHistory.insertion_datetime <= clear_date).delete()
#         except Exception, e:
#             print("Clear failed for reasons: {0}".format(str(e)))
#             db.session.rollback()
#             return False
#         db.session.commit()
#         return True

api.add_resource(HealthCheckAPI, '/api/v1.0/healthcheck', endpoint='healthcheck')
api.add_resource(WebCallbacksAPI, '/api/v1.0/webcallbacks/<string:pprg>', endpoint='webcallbacks')

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=4295)

