import json
import os
from dotenv import load_dotenv
from bson.json_util import dumps
from django.http import JsonResponse
from pymongo import MongoClient

from .base64_decoder import base64_decode
from .query_val_getter import get_values
from .supported_operators import supported_operators

load_dotenv()
username = os.getenv('MONGODBUSERNAME')
password = os.getenv('MONGODBPASSWORD')
db_url = os.getenv('MONGO_URI')

client = MongoClient(db_url)
db = client['test']


def get_data(request):
    body = json.loads(request.body)
    pipeline = []
    products_collection = db['products']

    limit = 10
    page = 1
    query_obj = {}
    if "limit" in body:
        limit = body["limit"]

    if "page" in body:
        page = body["page"]
    if "fields_required" in body:
        decoded = base64_decode(body, 'fields_required')
        data = json.loads(decoded)
        fields_obj = {}
        for key in data:
            fields_obj[key] = 1

        projection = {
            "$project": fields_obj
        }

        pipeline.append(projection)

    if "sort" in body:
        decoded = base64_decode(body, 'sort')
        data = json.loads(decoded)
        field = data["field"]
        order = data["order"]
        sort_res = {
            "$sort": {
                field: order
            }
        }

        pipeline.append(sort_res)

    if "brand" in body:
        query_obj["brand"] = body["brand"]

    if "title" in body:
        query_obj["title"] = body["title"]

    if "category" in body:
        query_obj["category"] = body["category"]

    if "stock" in body:
        pass

    if "price" in body:
        val, operator = get_values(body, "price")
        present, operator_type = supported_operators(operator)
        if present:
            query_obj['price'] = {
                operator_type: val
            }

    if "rating" in body:
        val, operator = get_values(body, "rating")
        present, operator_type = supported_operators(operator)
        if present:
            query_obj['rating'] = {
                operator_type: val
            }

    if "stock" in body:
        val, operator = get_values(body, "stock")
        present, operator_type = supported_operators(operator)
        if present:
            query_obj['stock'] = {
                operator_type: val
            }

    if len(query_obj.keys()) > 0:
        match_data = {
            '$match': query_obj
        }
        pipeline.append(match_data)

    pagination = {
        '$facet': {
            'metadata': [
                {'$count': 'total'},
                {'$addFields': {'page': int(page)}}
            ],
            'data': [
                {'$skip': (int(page) - 1) * int(limit)},
                {'$limit': int(limit)}
            ]
        }
    }

    pipeline.append(pagination)

    db_data = products_collection.aggregate(pipeline)
    res_data = json.loads(dumps(db_data))
    if "metadata" in res_data[0] and "data" in res_data[0]:
        res_data = res_data[0]['data']

    return JsonResponse(res_data, safe=False)
