import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import User, ChallengePackage, TradingAccount, TradePosition, Certificate, Order
from app.engine.prop_rules import evaluate_account_and_trades
from app.engine.market_data import market_engine

class TestPropFirmPlatform(unittest.TestCase):
    def setUp(self):
        # In-memory SQLite database for unit tests
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.db = self.Session()

        # Create test user
        self.user = User(
            username="TestTrader",
            email="trader@test.com",
            full_name="Alien Trader",
            is_email_verified=True
        )
        self.db.add(self.user)
        self.db.commit()

    def tearDown(self):
        self.db.close()

    def test_challenge_creation_and_rules(self):
        # Create $100,000 2-Step challenge
        account = TradingAccount(
            account_number="BFT-TEST-100K",
            user_id=self.user.id,
            model_type="2-Step",
            platform="WebTrader",
            initial_balance=100000.0,
            current_balance=100000.0,
            current_equity=100000.0,
            daily_starting_equity=100000.0,
            highest_recorded_equity=100000.0,
            phase="Phase 1",
            status="ACTIVE",
            profit_target_pct=8.0,
            max_daily_loss_pct=5.0,
            max_total_loss_pct=10.0,
            min_trading_days=3,
            days_traded=1
        )
        self.db.add(account)
        self.db.commit()

        # Check properties
        self.assertEqual(account.target_amount, 8000.0)
        self.assertEqual(account.max_daily_loss_limit, 5000.0)
        self.assertEqual(account.max_total_loss_limit, 10000.0)
        self.assertEqual(account.current_profit, 0.0)

    def test_trade_pnl_calculation(self):
        # Test Gold (XAUUSD) buy trade
        pnl, exit_price, pips = market_engine.calculate_pnl(
            symbol="XAUUSD",
            order_type="BUY",
            lots=1.0, # 1 lot = 100 oz
            open_price=2380.0
        )
        # If current price is e.g. 2388.50, diff is +8.50 -> 1.0 * 100 * 8.50 = +$850
        self.assertIsInstance(pnl, float)
        self.assertIsInstance(exit_price, float)

    def test_daily_drawdown_breach(self):
        account = TradingAccount(
            account_number="BFT-TEST-BREACH",
            user_id=self.user.id,
            model_type="2-Step",
            platform="WebTrader",
            initial_balance=100000.0,
            current_balance=94000.0, # Lost $6,000 in a day (> 5% max daily limit)
            current_equity=94000.0,
            daily_starting_equity=100000.0,
            phase="Phase 1",
            status="ACTIVE",
            profit_target_pct=8.0,
            max_daily_loss_pct=5.0,
            max_total_loss_pct=10.0
        )
        self.db.add(account)
        self.db.commit()

        state = evaluate_account_and_trades(self.db, account)
        self.assertEqual(state["status"], "BREACHED")
        self.assertIn("Max Daily Loss Exceeded", account.breach_reason)

    def test_profit_target_pass_phase_advance_and_certificate(self):
        account = TradingAccount(
            account_number="BFT-TEST-PASS",
            user_id=self.user.id,
            model_type="2-Step",
            platform="WebTrader",
            initial_balance=100000.0,
            current_balance=108500.0, # Gained +8.5% (Target is 8.0%)
            current_equity=108500.0,
            daily_starting_equity=108500.0,
            phase="Phase 1",
            status="ACTIVE",
            profit_target_pct=8.0,
            max_daily_loss_pct=5.0,
            max_total_loss_pct=10.0,
            min_trading_days=3,
            days_traded=3
        )
        self.db.add(account)
        self.db.commit()

        state = evaluate_account_and_trades(self.db, account)
        # Should advance to Phase 2
        self.assertEqual(state["phase"], "Phase 2")
        self.assertEqual(account.profit_target_pct, 5.0)

        # Check that Certificate was automatically issued
        cert = self.db.query(Certificate).filter(Certificate.account_id == account.id).first()
        self.assertIsNotNone(cert)
        self.assertIn("Phase 1", cert.phase_passed)

if __name__ == "__main__":
    unittest.main()

