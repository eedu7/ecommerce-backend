from fastapi import APIRouter

from .auth import router as auth_router
from .cart import cart_router
from .cart_item import cart_item_router
from .category import category_router
from .order import order_router
from .order_item import order_item_router
from .product import product_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth")
router.include_router(category_router, prefix="/categories", tags=["Categories"])
router.include_router(product_router, prefix="/products", tags=["Products"])
router.include_router(cart_router, prefix="/carts", tags=["Cart"])
router.include_router(cart_item_router, prefix="/cart-items", tags=["Cart Item"])
router.include_router(order_router, prefix="/orders", tags=["Order"])
router.include_router(order_item_router, prefix="/order-items", tags=["Order Item"])
