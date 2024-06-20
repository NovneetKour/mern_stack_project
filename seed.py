import requests
from datetime import datetime
from models import ProductTransaction
from db import db, init_db
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product_transactions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
init_db(app)

def fetch_and_seed_data():
    response = requests.get('https://s3.amazonaws.com/roxiler.com/product_transaction.json')
    data = response.json()

    with app.app_context():
        for item in data:
            transaction = ProductTransaction(
                title=item['title'],
                description=item['description'],
                price=item['price'],
                date_of_sale=datetime.strptime(item['dateOfSale'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                category=item['category'],
                sold=item['sold']
            )
            db.session.add(transaction)
        db.session.commit()

if __name__ == '__main__':
    fetch_and_seed_data()
