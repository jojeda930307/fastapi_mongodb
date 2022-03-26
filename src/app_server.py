import uvicorn
from fastapi import FastAPI

from src.routes.users.users_routes import user
from src.routes.address.address_routes import address
from src.routes.orders.orders_routes import order
from src.routes.products.products_routes import product

app = FastAPI()
app.include_router(user)
app.include_router(address)
app.include_router(order)
app.include_router(product)

if __name__ == '__main__':
    uvicorn.run("app_server:app", host="127.0.0.1", port=5000, log_level="info", reload=True)
