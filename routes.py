from flask import Blueprint, request, jsonify
from models import ProductTransaction
from db import db
from sqlalchemy import func

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/transactions', methods=['GET'])
def get_transactions():
    month = request.args.get('month')
    search = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    query = ProductTransaction.query
    if month:
        query = query.filter(func.strftime('%m', ProductTransaction.date_of_sale) == month.zfill(2))
    if search:
        query = query.filter(
            (ProductTransaction.title.like(f'%{search}%')) |
            (ProductTransaction.description.like(f'%{search}%')) |
            (ProductTransaction.price.like(f'%{search}%'))
        )
    transactions = query.paginate(page, per_page, False).items

    return jsonify([{
        'id': transaction.id,
        'title': transaction.title,
        'description': transaction.description,
        'price': transaction.price,
        'date_of_sale': transaction.date_of_sale.strftime('%Y-%m-%d'),
        'category': transaction.category,
        'sold': transaction.sold
    } for transaction in transactions])

@main_blueprint.route('/statistics', methods=['GET'])
def get_statistics():
    month = request.args.get('month')

    query = ProductTransaction.query
    if month:
        query = query.filter(func.strftime('%m', ProductTransaction.date_of_sale) == month.zfill(2))

    total_sales_amount = db.session.query(func.sum(ProductTransaction.price)).filter(ProductTransaction.sold.is_(True)).scalar()
    total_sold_items = db.session.query(func.count(ProductTransaction.id)).filter(ProductTransaction.sold.is_(True)).scalar()
    total_not_sold_items = db.session.query(func.count(ProductTransaction.id)).filter(ProductTransaction.sold.is_(False)).scalar()

    return jsonify({
        'total_sales_amount': total_sales_amount,
        'total_sold_items': total_sold_items,
        'total_not_sold_items': total_not_sold_items
    })

@main_blueprint.route('/bar-chart', methods=['GET'])
def get_bar_chart():
    month = request.args.get('month')

    price_ranges = [
        (0, 100), (101, 200), (201, 300), (301, 400), (401, 500),
        (501, 600), (601, 700), (701, 800), (801, 900), (901, float('inf'))
    ]

    query = ProductTransaction.query
    if month:
        query = query.filter(func.strftime('%m', ProductTransaction.date_of_sale) == month.zfill(2))

    price_data = {}
    for range_start, range_end in price_ranges:
        count = query.filter(
            ProductTransaction.price.between(range_start, range_end if range_end != float('inf') else 1e10)
        ).count()
        price_data[f'{range_start}-{range_end}'] = count

    return jsonify(price_data)
