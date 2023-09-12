from sqlalchemy.orm import aliased


from controllers.OMR_CONNECTION import session
from controllers.Sql_Class import Item, CartItem, Cart, Order, Customer


customer_alias = aliased(Customer)
order_alias = aliased(Order)
cart_alias = aliased(Cart)
cart_item_alias = aliased(CartItem)
item_alias = aliased(Item)

query = session.query(
    customer_alias.id.label('customer_id'),
    customer_alias.name.label('customer_name'),
    order_alias.order_No.label('order_number'),
    cart_item_alias.quantity.label('item_quantity'),
    item_alias.name.label('item_name'),
    item_alias.price.label('item_price')
).select_from(customer_alias)

query = query.outerjoin(order_alias, customer_alias.id == order_alias.customer_id)
query = query.outerjoin(cart_alias, order_alias.cart_id == cart_alias.cart_id)
query = query.outerjoin(cart_item_alias, cart_alias.cart_id == cart_item_alias.cart_id)
query = query.outerjoin(item_alias, cart_item_alias.item_barcode == item_alias.barcode)

query = query.order_by(customer_alias.id, order_alias.order_No, cart_item_alias.id)

results = query.all()


print("Customer ID | Customer Name | Order Number | Item Quantity | Item Name | Item Price")

for result in results:
    print(result)
