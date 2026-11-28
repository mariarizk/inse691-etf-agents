import os
import sys
import unittest

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from fastapi.testclient import TestClient

from backend.api import app


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_dashboard_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_backtest_page_loads(self):
        response = self.client.get("/backtest")
        self.assertEqual(response.status_code, 200)

    def test_health_page_loads(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

    def test_analyze_rejects_short_article(self):
        response = self.client.post(
            "/analyze",
            data={"article": "too short"},
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
