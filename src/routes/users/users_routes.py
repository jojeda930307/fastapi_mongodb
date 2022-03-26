from fastapi import APIRouter

from src.models.model import UserOut, UserIn
import src.config.database as db

user = APIRouter()


@user.get('/getUsers', response_model=list[UserOut])
async def list_users():
    """ Devuelve todos los usuarios """

    users = []
    for user in db.mydb.users.find():
        addr_id = user.get('address')
        if not addr_id:
            users.append(UserOut(**user))
            return users
        for item in db.mydb.addressUsers.find():
            if addr_id == item.get('_id'):
                user['address'] = item
                users.append(UserOut(**user))
    return users


@user.get("/user/{user_id}")
def get_user_by_id(user_id: str):
    """ Devuelve un usuario por su ID """

    for user in db.mydb.users.find():
        if str(user.get('_id')) == user_id:
            address_id = user.get('address')
            if not address_id:
                return UserOut(**user)
            for item in db.mydb.addressUsers.find():
                if address_id == item.get('_id'):
                    user['address'] = item
                    return UserOut(**user)


@user.post('/user', response_model=UserOut)
async def create_user(user: UserIn):
    """ Inserta un nuevo usuario en la base de datos """

    if hasattr(user, 'id'):
        delattr(user, 'id')
    new_user = db.mydb.users.insert_one(user.dict())
    created_user = db.mydb.users.find_one({"_id": new_user.inserted_id})
    return UserOut(**created_user)


@user.put('/user/{user_id}')
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


@user.delete('/user/{user_id}')
async def delete_user(user_id: str):
    """ Elimina los datos de un usuario """

    for user in db.mydb.users.find():
        if str(user.get('_id')) == user_id:
            db.mydb.users.delete_one(user)
    return {"message": "El usuario fue eliminado correctamente"}