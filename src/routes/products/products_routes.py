from fastapi import APIRouter

from src.models.model import Product
import src.config.database as db

product = APIRouter()


@product.get('/getProducts')
async def list_products():
    """ Devuelve todos los productos """

    products = []
    for product in db.mydb.products.find():
        products.append(Product(**product))
    return {'product': products}