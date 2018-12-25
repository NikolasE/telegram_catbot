#! /usr/bin/python3

import os
from flask import Flask
from flask import jsonify, request

app = Flask(__name__)


# Add django as interface to Databse
import django
django.setup()

# from django.db.models import Sum
from django_cat_app.models import UserLog
from django.db.models import Sum

@app.route('/total', methods=['GET', 'POST'])
def total_cat_count():
    total_cat_count = UserLog.objects.aggregate(Sum('cat_count'))

    response = jsonify({'cat_count': total_cat_count})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == "__main__":
    port = int(os.environ.get('PORT', '8080'))
    app.run(host='0.0.0.0', port=port, debug=True)
