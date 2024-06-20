from db import db
from datetime import datetime

class ProductTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    date_of_sale = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    sold = db.Column(db.Boolean, nullable=False)

    def __init__(self, title, description, price, date_of_sale, category, sold):
        self.title = title
        self.description = description
        self.price = price
        self.date_of_sale = date_of_sale
        self.category = category
        self.sold = sold
