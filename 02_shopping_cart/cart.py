from cart_item import CartItem
from product import Product


class Cart:
    def __init__(self):
        self.items: list[CartItem] = []

    def add_item(self, product: Product, quantity: int) -> None:
        if type(quantity) is not int or quantity < 1:
            raise ValueError("数量は1以上の整数にしてください")
        self.items.append(CartItem(product, quantity))

    def total(self) -> int:
        return sum(item.subtotal() for item in self.items)
