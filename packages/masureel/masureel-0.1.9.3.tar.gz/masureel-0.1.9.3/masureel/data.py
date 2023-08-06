import os
import csv
import json
from airtable import Airtable
from .product import Product


tb = None


def get_json(filename):
    with open(os.path.join(os.path.dirname(__file__), 'data', filename)) as f:
        return json.load(f)

def update_product_topviews(topviews):
    tb = Airtable(table_name="Collectie", base_id="appVz0Sb0OZ0Cwng7",
                  api_key=os.getenv('AIRTABLE_API_KEY'))

    pds = tb.get_all()
    for p in pds:
        if p["fields"]["code"] in topviews:
            print("update topview")
            tb.update(p["id"], {"Topview found":True})


def get_products_by_collection(collection):
    tb = Airtable(table_name="Collectie", base_id="appVz0Sb0OZ0Cwng7",
                  api_key=os.getenv('AIRTABLE_API_KEY'))
    result = tb.search('collection', collection.lower())
    ret = {}
    for r in result:
        ret[r['fields']['code']] = Product(r)
    return ret


def get_products():
    tb = Airtable(table_name="Collectie", base_id="appVz0Sb0OZ0Cwng7",
                  api_key=os.getenv('AIRTABLE_API_KEY'))
    table_list = tb.get_all()
    return json_to_products(table_list)


def json_to_products(json):
    pdList = []
    for j in json:
        pdList.append(Product(j))
    return pdList


def get_tool_database():
    basepath = os.path.dirname(__file__)
    dct = {}
    with open(os.path.join(basepath, 'data', 'database.csv')) as f:
        aList = csv.reader(f, delimiter=';')
        for row in aList:
            if row[0] == 'Material':
                dct[row[5].split('|')[0]] = {
                    'name': row[5].split('|')[1], 'type': row[4]}
                # lst.append(temp)
    return dct
