import unittest
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.app import create_app
from backend.config.config import Config
from backend.services.prediction_service import PredictionService
from backend.services.database_service import DatabaseService

class TestInsureAIProBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.pred_service = PredictionService()
        cls.db_service = DatabaseService(Config.DATABASE_PATH)

    def test_01_health_endpoint(self):
        res = self.client.get('/api/health')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'healthy')

    def test_02_model_info_endpoint(self):
        res = self.client.get('/api/model-info')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])

    def test_03_prediction_multi_model(self):
        payload = {
            "age": 35, "sex": "female", "bmi": 28.5, "children": 2, "smoker": "no", "region": "southeast"
        }
        res = self.client.post('/api/predict', json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('multi_model_estimates', data['data'])
        self.assertIn('agreement_pct', data['data'])
        self.assertIn('expected_range', data['data'])
        self.assertIn('advisory_package', data['data'])

    def test_04_chatbot(self):
        res = self.client.post('/api/chatbot', json={
            "message": "Why is my premium high?",
            "context": {"predicted_charge": 42000, "risk_level": "High", "smoker": "yes", "bmi": 31.2}
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('reply', data)

    def test_05_whatif_simulation(self):
        baseline = {"age": 40, "sex": "male", "bmi": 30.0, "children": 1, "smoker": "yes", "region": "southeast"}
        overrides = {"simulated_smoker": "no", "simulated_bmi": 24.0}
        res = self.client.post('/api/simulate', json={"baseline": baseline, "overrides": overrides})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('annual_savings', data['data'])

    def test_06_admin_telemetry(self):
        res = self.client.get('/api/admin/stats')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('total_predictions', data['data'])

    def test_07_swagger_docs(self):
        res = self.client.get('/api/docs')
        self.assertEqual(res.status_code, 200)
        res_json = self.client.get('/api/docs/swagger.json')
        self.assertEqual(res_json.status_code, 200)

    def test_08_multi_format_export(self):
        pred_res = self.pred_service.predict({
            "age": 42, "sex": "male", "bmi": 31.2, "children": 1, "smoker": "yes", "region": "southwest"
        })
        for fmt in ["pdf", "json", "csv"]:
            res = self.client.post('/api/export', json={"format": fmt, "prediction": pred_res})
            self.assertEqual(res.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        for f in os.listdir("backend"):
            if f.startswith("export_temp") or f.startswith("temp_report"):
                try:
                    os.remove(os.path.join("backend", f))
                except Exception:
                    pass

if __name__ == '__main__':
    unittest.main()

