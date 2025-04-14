import json
import pymysql
import pymysql.cursors
import qr_barcode_module.error_messages as error
from qr_barcode_module.db import get_db_connection

def get_product_by_keyword(keyword):
    db_connect = get_db_connection()
    cursor = db_connect.cursor(pymysql.cursors.DictCursor)