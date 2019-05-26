from bookshelf import get_model
from flask import Blueprint, current_app, jsonify, render_template, request


type_crud = Blueprint('type_crud', __name__)


@type_crud.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict()

        book_type = get_model().create_type(data)

        return jsonify(book_type)



