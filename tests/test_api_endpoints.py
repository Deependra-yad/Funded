import unittest
from starlette.testclient import TestClient
from app.main import app
from app.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
from app.engine.razorpay_client import verify_razorpay_signature
import hmac
import hashlib

class TestProductionPropFirm(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_unauthenticated_redirect_to_login(self):
        """Verify protected routes strictly redirect unauthenticated requests to /login"""
        protected_routes = [
            "/",
            "/dashboard",
            "/challenges",
            "/challenges/1",
            "/trading",
            "/buy-challenge",
            "/passed-challenges",
            "/ib-program",
            "/orders",
            "/billing",
            "/profile",
            "/admin/simulator"
        ]
        for route in protected_routes:
            res = self.client.get(route, follow_redirects=False)
            self.assertEqual(res.status_code, 307, f"Route {route} did not redirect unauthenticated user")
            self.assertIn("/login", res.headers.get("Location", ""))

    def test_user_registration_and_login_flow(self):
        """Test real registration and login flow with password hashing and session tokens"""
        import uuid
        test_email = f"trader_{uuid.uuid4().hex[:6]}@nexusfunded.com"
        password = "SecurePassword123!"

        # 1. Register
        reg_res = self.client.post("/register", data={
            "full_name": "Jordan Bell",
            "email": test_email,
            "password": password,
            "confirm_password": password
        }, follow_redirects=False)
        self.assertEqual(reg_res.status_code, 303)
        self.assertIn("nexus_session", reg_res.cookies)

        # 2. Access dashboard with session cookie
        dash_res = self.client.get("/dashboard", cookies=reg_res.cookies)
        self.assertEqual(dash_res.status_code, 200)
        self.assertIn("Jordan Bell", dash_res.text)
        self.assertIn("NEXUS", dash_res.text)

        # 3. Logout
        logout_res = self.client.get("/logout", follow_redirects=False)
        self.assertEqual(logout_res.status_code, 303)

        # 4. Login with registered credentials
        login_res = self.client.post("/login", data={
            "email": test_email,
            "password": password
        }, follow_redirects=False)
        self.assertEqual(login_res.status_code, 303)
        self.assertIn("nexus_session", login_res.cookies)

    def test_razorpay_order_and_signature_verification(self):
        """Test Razorpay order creation and HMAC-SHA256 signature verification"""
        # Login with test account
        login_res = self.client.post("/login", data={
            "email": "alien@bharathfundedtrader.com",
            "password": "trader123"
        }, follow_redirects=False)
        cookies = login_res.cookies

        # 1. Create Razorpay order
        order_res = self.client.post("/api/payment/create-order", data={
            "package_id": 4, # $50k
            "coupon_code": "SAVE20"
        }, cookies=cookies)
        self.assertEqual(order_res.status_code, 200)
        order_data = order_res.json()
        self.assertTrue(order_data["success"])
        self.assertEqual(order_data["key_id"], RAZORPAY_KEY_ID)
        self.assertIn("order_id", order_data)

        # 2. Simulate Razorpay payment callback with valid HMAC signature
        rzp_order_id = order_data["order_id"]
        rzp_payment_id = "pay_test_9918204"
        msg = f"{rzp_order_id}|{rzp_payment_id}".encode("utf-8")
        signature = hmac.new(RAZORPAY_KEY_SECRET.encode("utf-8"), msg, hashlib.sha256).hexdigest()

        # 3. Verify payment on server
        verify_res = self.client.post("/api/payment/verify", data={
            "package_id": 4,
            "platform": "WebTrader",
            "coupon_code": "SAVE20",
            "razorpay_order_id": rzp_order_id,
            "razorpay_payment_id": rzp_payment_id,
            "razorpay_signature": signature
        }, cookies=cookies)
        self.assertEqual(verify_res.status_code, 200)
        verify_data = verify_res.json()
        self.assertTrue(verify_data["success"])
        self.assertIn("/trading?account_id=", verify_data["redirect_url"])

    def test_live_trading_execution_and_positions(self):
        """Test live trading order execution for authenticated user"""
        login_res = self.client.post("/login", data={
            "email": "alien@bharathfundedtrader.com",
            "password": "trader123"
        }, follow_redirects=False)
        cookies = login_res.cookies

        # Place BUY order on Gold (XAUUSD)
        trade_res = self.client.post("/api/trade/open", data={
            "account_id": 1,
            "symbol": "XAUUSD",
            "order_type": "BUY",
            "volume_lots": 1.5,
            "stop_loss": 2350.0,
            "take_profit": 2500.0
        }, cookies=cookies)
        self.assertEqual(trade_res.status_code, 200)
        trade_data = trade_res.json()
        self.assertTrue(trade_data["success"])

        # Check account state
        state_res = self.client.get("/api/account/1/state", cookies=cookies)
        self.assertEqual(state_res.status_code, 200)
        st = state_res.json()
        self.assertTrue(len(st["positions"]) > 0)

if __name__ == "__main__":
    unittest.main()
