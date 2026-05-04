import stripe
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from stripe import StripeClient
from stripe.params import PaymentLinkCreateParams

from app.models import DBOrder, OrderStatus, PaymentStatus
from core.config import config
from core.dependencies.controller import OrderControllerDep
from core.exceptions import BadRequestException

stripe.api_key = config.STRIPE_SECRET_KEY

router = APIRouter()

client = StripeClient(config.STRIPE_SECRET_KEY)


@router.get("/health")
async def health_check():
    return {"stripe": "Health Check"}


@router.get("/checkout")
async def checkout():
    data: PaymentLinkCreateParams = {
        "line_items": [
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "T-shirt"},
                    "unit_amount": 2000,
                },
                "quantity": 1,
            }
        ],
    }
    payment_link = client.payment_links.create(
        data,
    )

    return RedirectResponse(payment_link.url)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "T-shirt"},
                    "unit_amount": 2000,
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )
    return {"session_id": session.id}


@router.post("/webhook")
async def stripe_webhook(request: Request, controller: OrderControllerDep):
    payload = await request.body()
    signature = request.headers.get("stripe-signature")

    if not signature:
        raise BadRequestException("Missing stripe-signature header")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=signature, secret=config.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise BadRequestException("Invalid signature")
    except Exception as exc:
        raise BadRequestException(str(exc))

    stripe_checkout_session_id = event["data"]["object"]["id"]
    event_type = event["type"]

    order: DBOrder = await controller.get_by_stripe_checkout_session_id(
        stripe_checkout_session_id
    )

    match event_type:
        case "checkout.session.completed":
            order.payment_status = PaymentStatus.PAID
            order.status = OrderStatus.PROCESSING
        case "payment_intent.payment_failed":
            order.payment_status = PaymentStatus.FAILED
            order.status = OrderStatus.FAILED
        case "charge.refunded":
            order.payment_status = PaymentStatus.REFUNDED
            order.status = OrderStatus.REFUNDED
        case _:
            order.payment_status = PaymentStatus.REFUNDED
            order.status = OrderStatus.DELIVERED
    
    await controller.commit()
