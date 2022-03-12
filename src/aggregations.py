usr_addrs = {
    "$lookup":
        {
            "from": "addressUsers",
            "localField": "address",
            "foreignField": "_id",
            "as": "address"
        }
}
order_prod = {
    "$lookup":
        {
            "from": "products",
            "localField": "product",
            "foreignField": "_id",
            "as": "product"
        }
}
order_user = {
    "$lookup":
        {
            "from": "users",
            "localField": "user",
            "foreignField": "_id",
            "as": "user"
        }
}
unwind_order_prod = {'$unwind': '$product'}
unwind_order_user = {'$unwind': '$user'}
unwind_user_address = {'$unwind': '$address'}

remove_prod_id = {'$project': {"product._id": 0}}
remove_addr_id = {'$project': {"address._id": 0}}