from app import db

# Database tables to store user inputs

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), index=True, unique=False)
    amount = db.Column(db.Numeric(11,2)) # Numeric stores a decimal number with a fixed dp

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), index=True, unique=False)
    amount = db.Column(db.Numeric(11,2))

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), index=True, unique=False)
    amount = db.Column(db.Numeric(11,2))
