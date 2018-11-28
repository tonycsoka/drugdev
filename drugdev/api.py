from drugdev import app, db
from drugdev.models import Contact, ContactSchema
from flask_restful import Resource, Api, reqparse

api = Api(app=app)


class ContactsCall(Resource):
    def get(self):
        contacts = Contact.query.all()
        contacts_schema = ContactSchema(many=True)
        return {'/api/contacts': contacts_schema.dump(contacts).data}


api.add_resource(ContactsCall, '/api/contacts')


class ContactCall(Resource):
    def get(self, username):
        contact = Contact.query.filter_by(username=username).first()
        contacts_schema = ContactSchema()

        if contact:
            return {'/api/contact/'+username: contacts_schema.dump(contact).data}
        else:
            return {'/api/contact/'+username:  'unknown'}, 204

    def post(self, username):
        from sqlalchemy.exc import IntegrityError
        parser = reqparse.RequestParser()
        parser.add_argument('email')
        parser.add_argument('last_name')
        parser.add_argument('first_name')

        args = parser.parse_args()

        contact = Contact(username=username,
                          email=args['email'],
                          first_name=args['first_name'],
                          last_name=args['last_name'])

        try:
            db.session.add(contact)
            db.session.commit()
        except IntegrityError as ierror:
            db.session.rollback()
            return {'/api/contact/'+username: 'already exists'}, 405
        finally:
            db.session.commit()

        return f'post : {username}', 201

    def put(self, username):
        parser = reqparse.RequestParser()
        parser.add_argument('email')
        parser.add_argument('last_name')
        parser.add_argument('first_name')
        parser.add_argument('username')

        contact = Contact.query.filter_by(username=username).first()

        args = parser.parse_args()

        if args['username']:
            contact.username = args['username']
        if args['email']:
            contact.email = args['email']
        if args['last_name']:
            contact.last_name = args['last_name']
        if args['first_name']:
            contact.first_name = args['first_name']

        db.session.commit()

        return f'put : {username}', 201

    def delete(self, username):
        contact = Contact.query.filter_by(username=username)
        contact.delete()
        db.session.commit()
        return '', 200


api.add_resource(ContactCall, '/api/contact/<string:username>')

