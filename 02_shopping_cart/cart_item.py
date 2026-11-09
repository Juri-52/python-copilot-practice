from product import Product


class CartItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    def subtotal(self) -> int:
        # この計算を、READMEの仕様と比較して確認する。
        return self.product.price * self.quantity
