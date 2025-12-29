
from models.db import SessionLocal
from models.sale import Sale
from models.sale_item import SaleItem

def register_sale(cart):
    db = SessionLocal()
    total = sum(i['price']*i['qty'] for i in cart)
    sale = Sale(total=total)
    db.add(sale)
    db.commit()
    for i in cart:
        db.add(SaleItem(sale_id=sale.id, product_id=i['id'], quantity=i['qty']))
    db.commit()
    db.close()
    return sale.id, total
