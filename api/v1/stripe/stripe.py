import stripe
from fastapi import APIRouter, Request

from core.config import config
from core.exceptions import BadRequestException

stripe.api_key = config.STRIPE_SECRET_KEY

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"stripe": "Health Check"}


@router.post("/webhook")
async def stripe_webhook(request: Request):
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


    result = {
        "created": event["created"],
        "id": event["id"],
        "type": event["type"]
    }
    print("#" * 8)
    print("#" * 8)
    print(event)
    print("#" * 8)
    print("#" * 8)
    print(result)
    print("#" * 8)
    print("#" * 8)
    
