from flask import Blueprint, current_app, redirect, render_template, request


error = Blueprint('error', __name__)


@error.route('/404', methods=['GET'])
def error_404():
    return render_template('404.html')


@error.route('/403', methods=['GET'])
def error_403():
    return render_template('403.html')



