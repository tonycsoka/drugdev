from drugdev import db, ma


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)  # Assume unique usernames
    email = db.Column(db.String(150))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    def __repr__(self):
        return f'<User {self.username}>'


class ContactSchema(ma.ModelSchema):
    class Meta:
        model = Contact
        fields = ['uri', 'username', 'email', 'first_name', 'last_name']
    uri = ma.Hyperlinks(ma.URLFor('contactcall_get', username='<username>'))


