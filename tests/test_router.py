import base64
import unittest
from app.views.router import app


class TestRouter(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.payload = {
            "Location": "Mumbai",
            "Name": "Test_Tata_Gowrav",
            "Organisation": "LTTS"
        }
        user = "admin"
        password = "password"
        self.headers = {
            "Authorization": "Basic {}".format(
                base64.b64encode(bytes(f"{user}:{password}", "utf-8")).decode("ascii")
            )
        }

    def test_01_token_creation_success(self):
        response = self.app.get("/token", headers=self.headers)
        self.assertEqual(200, response.status_code)

    def test_02_create_record_success(self):
        token_generated = self.app.get("/token", headers=self.headers)
        json_data = token_generated.json['access_token']
        response = self.app.post('/record', json=self.payload, headers={"Authorization": f"Bearer {json_data}"})
        self.assertEqual(200, response.status_code)

    def test_03_create_record_conflict(self):
        token_generated = self.app.get("/token", headers=self.headers)
        json_data = token_generated.json['access_token']
        response = self.app.post('/record', json=self.payload, headers={"Authorization": f"Bearer {json_data}"})
        self.assertEqual(409, response.status_code)

    def test_03_create_record_key_error(self):
        token_generated = self.app.get("/token", headers=self.headers)
        json_data = token_generated.json['access_token']
        del self.payload['Name']
        response = self.app.post('/record', json=self.payload, headers={"Authorization": f"Bearer {json_data}"})
        self.assertEqual(400, response.status_code)

    def test_04_fetch_record_success(self):
        token_generated = self.app.get("/token", headers=self.headers)
        json_data = token_generated.json['access_token']
        response = self.app.get(f'/record/{self.payload["Name"]}', headers={"Authorization": f"Bearer {json_data}"})
        self.assertEqual(200, response.status_code)

    def test_05_fetch_all_records(self):
        token_generated = self.app.get("/token", headers=self.headers)
        json_data = token_generated.json['access_token']
        response = self.app.get('/record', headers={"Authorization": f"Bearer {json_data}"})
        self.assertEqual(200, response.status_code)

    def test_06_fetch_record_not_found_error(self):
        token_generated = self.app.get("/token", headers=self.headers)
        json_data = token_generated.json['access_token']
        response = self.app.get('/record/abc', headers={"Authorization": f"Bearer {json_data}"})
        self.assertEqual(404, response.status_code)

    def test_07_update_record_success(self):
        token_generated = self.app.get("/token", headers=self.headers)
        json_data = token_generated.json['access_token']
        self.payload.update({"Location": "Mumbai"})
        response = self.app.put('/record', json=self.payload, headers={"Authorization": f"Bearer {json_data}"})
        self.assertEqual(200, response.status_code)

    def test_08_update_record_fail_key_error(self):
        token_generated = self.app.get("/token", headers=self.headers)
        json_data = token_generated.json['access_token']
        del self.payload["Name"]
        response = self.app.put('/record', json=self.payload, headers={"Authorization": f"Bearer {json_data}"})
        self.assertEqual(400, response.status_code)

    def test_09_update_record_fail_no_record_error(self):
        token_generated = self.app.get("/token", headers=self.headers)
        json_data = token_generated.json['access_token']
        self.payload.update({"Name": "varwog"})
        response = self.app.put('/record', json=self.payload, headers={"Authorization": f"Bearer {json_data}"})
        self.assertEqual(404, response.status_code)

    def test_10_delete_record_fail_no_record_error(self):
        token_generated = self.app.get("/token", headers=self.headers)
        json_data = token_generated.json['access_token']
        response = self.app.delete('/record/abc', headers={"Authorization": f"Bearer {json_data}"})
        self.assertEqual(404, response.status_code)

    def test_11_delete_record_fail_success(self):
        token_generated = self.app.get("/token", headers=self.headers)
        json_data = token_generated.json['access_token']
        response = self.app.delete(f'/record/{self.payload["Name"]}', headers={"Authorization": f"Bearer {json_data}"})
        self.assertEqual(200, response.status_code)

    def test_12_update_record_failure_invalid_payload(self):
        token_generated = self.app.get("/token", headers=self.headers)
        json_data = token_generated.json['access_token']
        payload = {"Name": self.payload["Name"]}
        response = self.app.put('/record', json=payload, headers={"Authorization": f"Bearer {json_data}"})
        self.assertEqual(400, response.status_code)
