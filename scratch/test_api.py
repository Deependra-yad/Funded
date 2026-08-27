from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import User
from app.security import create_session_token

client = TestClient(app)

db = SessionLocal()
user = db.query(User).first()

token = create_session_token(user.id)

response = client.post("/api/payment/create-order", data={"package_id": 1, "coupon_code": ""}, cookies={"fundeddesk_session": token})
print("STATUS:", response.status_code)
print("BODY:", response.text)

