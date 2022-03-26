from fastapi import APIRouter

from src.models.model import Order, OrderOut
import src.config.database as db
from src.temp.aggregations import usr_addrs, unwind_user_address, remove_addr_id, order_prod, unwind_order_prod, \
    remove_prod_id

order = APIRouter()


@order.get('/getOrders', response_model=list[OrderOut])
async def list_orders():
    """ Devuelve todos los pedidos """

    orders = []
    for order in db.mydb.orders.find():
        orders.append(Order(**order))
    return {'orders': orders}


@order.get("/order/{order_id}")
def get_order_by_id(order_id: str, user_id: str):
    """ Devuelve un pedido por su ID """

    pipeline1 = [
        usr_addrs,
        unwind_user_address,
        remove_addr_id
    ]

    for it1 in db.mydb.users.aggregate(pipeline1):
        if str(it1.get('_id')) == user_id:
            it1.pop('_id')

    pipeline2 = [
        order_prod,
        unwind_order_prod,
        remove_prod_id
    ]

    for it2 in db.mydb.orders.aggregate(pipeline2):
        if str(it2.get('_id')) == order_id:
            it2.pop('_id')
            it2.update({'user': it1})
            print(it2)