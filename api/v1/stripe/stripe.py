from pprint import pprint

import stripe
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from stripe import StripeClient
from stripe.params import PaymentLinkCreateParams

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

    result = {"created": event["created"], "id": event["id"], "type": event["type"]}

    exists = await controller.repository.get_one_by_filters(
        {"stripe_checkout_session_id": event["data"]["object"]["id"]}
    )

    print("%" * 8)
    print("Payment ID", event["data"]["object"]["id"])
    print("%" * 8)
    print("%" * 8)
    pprint(result)
    print("%" * 8)
    print("%" * 8)
    print("%" * 8)
    pprint(exists)
    print("%" * 8)
    print("%" * 8)
    print("%" * 8)
    print("%" * 8)
    pprint(event)
    print("%" * 8)
    print("%" * 8)
    print("%" * 8)
    print("%" * 8)
    print("%" * 8)

    # print("#" * 8)
    # print("#" * 8)
    # print(event)
    # print("#" * 8)
    # print("#" * 8)
    # print(result)
    # print("#" * 8)
    # print("#" * 8)
