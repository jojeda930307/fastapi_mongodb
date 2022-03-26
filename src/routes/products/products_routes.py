from fastapi import APIRouter

from src.models.products.product_model import Product
import src.config.database as db

product = APIRouter()


@product.get('/getProducts', tags=['Products'])
async def list_products():
    """ Devuelve todos los productos """

    products = []
    for product in db.mydb.products.find():
        products.append(Product(**product))
    return {'product': products}