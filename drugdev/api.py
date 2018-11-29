from drugdev import app, db
from drugdev.models import Contact, ContactSchema, Email, EmailSchema
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
            email = Email.query.filter_by(email=username).first()
            if email:
                contact = Contact.query.filter_by(id=email.contact_id).first()
                return {'/api/contact/'+contact.username: contacts_schema.dump(contact).data}
            else:
                return {'/api/contact/'+username:  'unknown'}, 204

    def post(self, username):
        from sqlalchemy.exc import IntegrityError
        parser = reqparse.RequestParser()
        parser.add_argument('email')
        parser.add_argument('surname')
        parser.add_argument('first_name')

        args = parser.parse_args()

        contact = Contact(username=username,
                          first_name=args['first_name'],
                          surname=args['surname'])
        email = Email(email=args['email'])

        contact.emails.append(email)

        try:
            db.session.add(contact)
            db.session.add(email)
            db.session.commit()
        except IntegrityError as ierror:
            db.session.rollback()
            return {'/api/contact/'+username: 'already exists'}, 405
        finally:
            db.session.commit()

        return f'post : {username}', 201

    def put(self, username):
        from sqlalchemy.exc import IntegrityError
        parser = reqparse.RequestParser()
        parser.add_argument('email')
        parser.add_argument('surname')
        parser.add_argument('first_name')
        parser.add_argument('username')

        contact = Contact.query.filter_by(username=username).first()

        args = parser.parse_args()

        if args['username']:
            contact.username = args['username']
        if args['email']:
            email = Email(email=args['email'])
            contact.emails.append(email)
            db.session.add(email)
        if args['surname']:
            contact.surname = args['surname']
        if args['first_name']:
            contact.first_name = args['first_name']

        try:
            db.session.commit()
        except IntegrityError as ierror:
            db.session.rollback()
            return {'/api/contact/'+username: 'already exists'}, 405
        finally:
            db.session.commit()

        return f'put : {username}', 201

    def delete(self, username):
        contact = Contact.query.filter_by(username=username).first()
        if contact:
            db.session.delete(contact)
            db.session.commit()
            return '', 200
        return '', 204


api.add_resource(ContactCall, '/api/contact/<string:username>')

