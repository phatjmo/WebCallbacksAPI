from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask.ext.mysql import MySQL



mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'jay'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jay'
app.config['MYSQL_DATABASE_DB'] = 'ItemListDb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


mysql.init_app(app)

api = Api(app)

class AuthenticateUser(Resource):
    def post(self):
        try:
            # Parse the arguments

            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email address for Authentication')
            parser.add_argument('password', type=str, help='Password for Authentication')
            args = parser.parse_args()

            _userEmail = args['email']
            _userPassword = args['password']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_AuthenticateUser',(_userEmail,))
            data = cursor.fetchall()

            
            if(len(data)>0):
                if(str(data[0][2])==_userPassword):
                    return {'status':200,'UserId':str(data[0][0])}
                else:
                    return {'status':100,'message':'Authentication failure'}

        except Exception as e:
            return {'error': str(e)}


class GetMyLeads(Resource):
    def get(self):
        try: 
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str)
            args = parser.parse_args()

            _centerId = args['id']

            # conn = mysql.connect()
            # cursor = conn.cursor()
            # cursor.callproc('sp_GetAllItems',(_userId,))
            # data = cursor.fetchall()

            # items_list=[];
            # for item in data:
            #     i = {
            #         'Id':item[0],
            #         'Item':item[1]
            #     }
            #     items_list.append(i)
            leads_list = LEADSTORE.pop(_centerId)

            return {'StatusCode':'200','leads':leads_list}

        except Exception as e:
            return {'error': str(e)}

class AddItem(Resource):
    def post(self):
        try: 
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str)
            parser.add_argument('item', type=str)
            args = parser.parse_args()

            _userId = args['id']
            _item = args['item']

            print _userId;

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_AddItems',(_userId,_item))
            data = cursor.fetchall()

            conn.commit()
            return {'StatusCode':'200','Message': 'Success'}

        except Exception as e:
            return {'error': str(e)}
        
                

class WebCallback(Resource):
    """
    {
        "PHONE_NUMBER": "04...",
        "FIRST_NAME" : "John",
        "LAST_NAME" : "Smith",
        "ADDRESS" : "123 N. Streetname St. #109",
        "CITY" : "Sydney",
        "STATE" : "QLD",
        "ZIP" : "4000",
        "COMPANY" : "ABC Corp.",
        "EMAIL" : "jsmith@abccorp.tld",
        "PPRG" : "PPRG"
    }
    """
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('phone', type=str, help='Phone Number to import')
            parser.add_argument('firstName', type=str, help='First Name')
            parser.add_argument('lastName', type=str, help='Last Name')
            parser.add_argument('street', type=str, help='Street Address')
            parser.add_argument('city', type=str, help='City')
            parser.add_argument('county', type=str, help='State')
            parser.add_argument('postCode', type=str, help='Postal Code')
            parser.add_argument('subId', type=str, help='Company Name')
            parser.add_argument('email', type=str, help='Email Address')
            parser.add_argument('gender', type=str, help='Campaign Code')
            parser.add_argument('received', type=str, help='Campaign Code')
            parser.add_argument('leadId', type=str, help='Campaign Code')
            parser.add_argument('dob', type=str, help='Campaign Code')
            args = parser.parse_args()

            _phoneNumber = args['PHONE_NUMBER']
            _firstName = args['FIRST_NAME']
            _lastName = args['LAST_NAME']
            _address = args['ADDRESS']
            _city = args['CITY']
            _state = args['STATE']
            _zip = args['ZIP']
            _company = args['COMPANY']
            _email = args['EMAIL']
            _pprg = args['PPRG']

            LEADSTORE.append([_phoneNumber,_firstName,_lastName,_address,_city,_state,_zip,_company,_email,_pprg])

            # conn = mysql.connect()
            # cursor = conn.cursor()
            # cursor.callproc('spWebCallback',(_phoneNumber,_firstName,_lastName,_address,_city,_state,_zip,_company,_email,_pprg))
            # data = cursor.fetchall()

            # if len(data) is 0:
            #     conn.commit()
            #     return {'StatusCode':'200','Message': 'Lead Imported'}
            # else:
            #     return {'StatusCode':'1000','Message': str(data[0])}

            return {'StatusCode':'200','Message': 'Lead Imported'}

        except Exception as e:
            return {'error': str(e)}



api.add_resource(WebCallback, '/api/1.0/WEBCALLBACKS')

if __name__ == '__main__':
    app.run(debug=True)
