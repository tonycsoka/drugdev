from drugdev import app, db
from drugdev.models import Contact, ContactSchema
from flask_restful import Resource, Api
from flask import jsonify

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
            return '', 403

    def post(self, username):
        pass

    def put(self, username):
        pass


api.add_resource(ContactCall, '/api/contact/<string:username>')


class ContactDelete(Resource):
    def get(self, username):
        contact = Contact.query.filter_by(username=username)
        contact.delete()
        db.session.commit()


api.add_resource(ContactDelete '/api/contact/delete/<string:username>')

