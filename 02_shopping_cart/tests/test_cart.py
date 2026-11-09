import pytest

from cart import Cart
from product import Product


def test_empty_cart_total():
    cart = Cart()

    result = cart.total()

    assert result == 0
    assert cart.items == []


def test_one_product_total():
    cart = Cart()
    apple = Product(1, "りんご", 200)
    cart.add_item(apple, 1)

    result = cart.total()

    assert result == 200
    assert len(cart.items) == 1
    assert cart.items[0].product is apple


def test_total_uses_quantities():
    cart = Cart()
    cart.add_item(Product(1, "りんご", 200), 2)
    cart.add_item(Product(2, "牛乳", 250), 3)

    result = cart.total()

    assert result == 1150
    assert [item.quantity for item in cart.items] == [2, 3]


@pytest.mark.parametrize("quantity", [0, -1, 1.5, "2", None, True, False])
def test_invalid_quantity_raises_without_changing_cart(quantity):
    cart = Cart()
    existing_product = Product(1, "りんご", 200)
    cart.add_item(existing_product, 1)
    items_before = cart.items.copy()

    with pytest.raises(ValueError, match="数量は1以上の整数にしてください"):
        cart.add_item(Product(2, "牛乳", 250), quantity)

    assert cart.items == items_before
    assert cart.total() == 200


def test_same_product_added_twice_is_kept_as_two_items_and_summed():
    cart = Cart()
    apple = Product(1, "りんご", 200)
    cart.add_item(apple, 2)
    cart.add_item(apple, 3)

    assert len(cart.items) == 2
    assert cart.items[0].product is apple
    assert cart.items[1].product is apple
    assert [item.quantity for item in cart.items] == [2, 3]
    assert cart.total() == 1000
