import uvicorn
from fastapi import FastAPI, HTTPException

import src.database as db
from src.models import UserIn, UserOut, Product, UserAddress, Order, OrderOut
from src.aggregations import order_prod, order_user,unwind_order_prod, unwind_order_user,\
    unwind_user_address, remove_addr_id, remove_prod_id, usr_addrs

app = FastAPI()


@app.get('/welcome')
async def welcome():
    return "Welcome to the first app in FastApi"


@app.get('/database_names')
async def get_database():
    dblist = db.myclient.list_database_names()
    if "myFirstDatabase" in dblist:
        return "The database exists."
    else:
        return f"The database not exists. This are all databases: >>>>>> {dblist}"


@app.get('/getUsers')
async def list_users():
    """ Devuelve todos los usuarios """

    users = []
    for user in db.mydb.users.find():
        users.append(UserOut(**user))
    return {'users': users}


@app.get('/getAddress')
async def list_address():
    """ Devuelve todas las direcciones """

    l_address = []
    for address in db.mydb.addressUsers.find():
        l_address.append(UserAddress(**address))
    return {'address': l_address}


@app.get('/getOrders')
async def list_orders():
    """ Devuelve todos los pedidos """

    orders = []
    for order in db.mydb.orders.find():
        orders.append(Order(**order))
    return {'orders': orders}


@app.get('/getProducts')
async def list_products():
    """ Devuelve todos los productos """

    products = []
    for product in db.mydb.products.find():
        products.append(Product(**product))
    return {'product': products}


@app.get("/user/{user_id}")
def get_user_by_id(user_id: str):
    """ Devuelve un usuario por su ID """

    for user in db.mydb.users.find():
        if str(user.get('_id')) == user_id:
            return UserOut(**user)


@app.get("/order/{order_id}")
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

@app.post('/user')
async def create_user(user: UserIn):
    """ Inserta un nuevo usuario en la base de datos """

    if hasattr(user, 'id'):
        delattr(user, 'id')
    new_user = db.mydb.users.insert_one(user.dict())
    created_user = db.mydb.users.find_one({"_id": new_user.inserted_id})
    return UserOut(**created_user)


@app.put('/user/{user_id}')
async def update_user(user_id: str, update_user: UserIn):
    """ Actualiza los datos de un usuario """

    if hasattr(update_user, 'id'):
        delattr(update_user, 'id')

    for user in db.mydb.users.find():
        if str(user.get('_id')) == user_id:
            new_values = {"$set": update_user.dict()}
            db.mydb.users.update_one(user, new_values)
            updated_user = db.mydb.users.find_one({"_id": user.get('_id')})
    return UserOut(**updated_user)


@app.delete('/user/{user_id}')
async def delete_user(user_id: str):
    """ Elimina los datos de un usuario """

    for user in db.mydb.users.find():
        if str(user.get('_id')) == user_id:
            db.mydb.users.delete_one(user)
    return {"message": "El usuario fue eliminado correctamente"}


@app.post('/address/{user_id}', response_model=UserAddress)
async def create_address(user_id: str, address: UserAddress):
    """ Inserta un nuevo usuario en la base de datos """

    if hasattr(address, 'id'):
        delattr(address, 'id')
    for user in db.mydb.users.find():
        if str(user.get('_id')) == user_id:
            new_address = db.mydb.addressUsers.insert_one(address.dict())
            created_address = db.mydb.addressUsers.find_one({"_id": new_address.inserted_id})
            # new_field = {"$set": {'address': created_address}}
            # db.mydb.users.update_one(user, new_field) esto hay que arreglarlo está insertando address dentro de users
            db.mydb.users.update_one(user, {"$set": {'address': created_address.get('_id')}})
    return created_address


@app.post('/create_orders/{user_id}', response_model=Order)
async def create_order(user_id: str, order: Order):
    """ Inserta un nuevo usuario en la base de datos """

    if hasattr(order, 'id'):
        delattr(order, 'id')
    for user in db.mydb.users.find():
        if str(user.get('_id')) == user_id:
            if not user.get('address'):
                raise HTTPException(status_code=404, detail={"message": "Debe proporcionar una dirección de envío"})
            else:
                new_order = db.mydb.orders.insert_one(order.dict())
                created_order = db.mydb.orders.find_one({"_id": new_order.inserted_id})
                if not created_order.get('user'):
                    created_order['user'] = user.get('_id')
                    db.mydb.orders.update_one({"user": None}, {"$set": {'user': user.get('_id')}})
    return created_order


if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=5000, log_level="info", reload=True)
