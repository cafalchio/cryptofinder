import unittest
from app.app import create_app, db, get_logger

logger = get_logger(testing=True)


class BaseTestCase(unittest.TestCase):
    db_connection = "sqlite:///:memory:"

    def setUp(self):
        """Set up the test client and database before each test."""
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            logger.info(f"Created app with {db.engine}")

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.session.rollback()
            db.session.remove()
        logger.info("Clearned app and db")

    def add_coins_to_db(self, coins):
        with self.app.app_context():
            for coin in coins:
                db.session.add(coin)
            db.session.commit()

    def get_response(self, endpoint):
        return self.client.get(endpoint)
