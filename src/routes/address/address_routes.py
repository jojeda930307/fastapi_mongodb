from fastapi import APIRouter

from src.models.address.address_model import UserAddress
import src.config.database as db

address = APIRouter()


@address.get('/getAddress', response_model=list[UserAddress], tags=['Address'])
async def list_address():
    """ Devuelve todas las direcciones """

    l_address = []
    for address in db.mydb.addressUsers.find():
        l_address.append(UserAddress(**address))
    return l_address


@address.post('/address/{user_id}', response_model=UserAddress, tags=['Address'])
async def create_address(user_id: str, address: UserAddress):
    """ Inserta una dirección de usuario en la base de datos """

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


