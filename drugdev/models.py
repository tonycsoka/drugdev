from drugdev import db, ma


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)  # Assume unique usernames
    first_name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    emails = db.relationship('Email', backref='contact', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)

    def __repr__(self):
        return f'<Email {self.email}>'


class EmailSchema(ma.ModelSchema):
    class Meta:
        model = Email
        fields = ['email']


class ContactSchema(ma.ModelSchema):
    class Meta:
        model = Contact
    uri = ma.Hyperlinks(ma.URLFor('contactcall', username='<username>'))
    emails = ma.Nested(EmailSchema, many=True)
