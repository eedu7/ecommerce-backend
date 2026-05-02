from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "stripe": "Health Check"
    }

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("stripe-signature")
    data = {
        "payload": payload,
        "signature": signature,
        "headers": request.headers,
        "cookies": request.cookies,
    }
    print("#" * 25)
    print("#" * 25)
    print(data)
    print("#" * 25)
    print("#" * 25)
    return data
