import unittest
from unittest import mock
from nose.tools import assert_raises
from app.models.record_manager import MongoService
from app.models.exceptions import RecordExistenceError, RecordInExistenceError


class TestRecordManager(unittest.TestCase):
    def setUp(self):
        self.mongo_service = MongoService()
        self.payload = {
            "Location": "Mumbai",
            "Name": "Test_Gowrav",
            "Organisation": "LTTS"
        }

    @mock.patch('pymongo.collection.Collection.insert_one')
    @mock.patch('app.models.record_manager.MongoService.fetch_record')
    @mock.patch('app.models.record_manager.MongoService.validate_payload')
    def test_01_create_new_single_record_success(self, mock_validate_payload, mock_fetch_record, mock_find):
        mock_fetch_record.return_value = "there is a record"
        mock_validate_payload.return_value = "Valid Payload"
        mock_find.return_value = {'_id': '1234', 'Location': 'Mumbai', 'Name': 'Test_Gowrav',
                                  'Organisation': 'LTTS'}
        response = self.mongo_service.create_record(payload=self.payload)
        expected_result = {
            'message': "Successfully inserted data {'Location': 'Mumbai', 'Name': 'Test_Gowrav', 'Organisation': "
                       "'LTTS'} into the database"}

        self.assertEqual(expected_result, response)

    @mock.patch('pymongo.collection.Collection.insert_one')
    @mock.patch('requests.get')
    @mock.patch('app.models.record_manager.MongoService.validate_payload')
    def test_02_create_new_multiple_record_success(self, mock_validate_payload, mock_get, mock_find):
        mock_get.return_value.status_code = 404
        mock_validate_payload.return_value = "Valid Payload"
        mock_find.return_value = {'_id': '1234', 'Location': 'Mumbai', 'Name': 'Test_Gowrav_2',
                                  'Organisation': 'LTTS'}
        response = self.mongo_service.create_record(payload=[self.payload])
        self.assertTrue(response)

    def test_03_invalid_payload(self):
        del self.payload['Name']
        with assert_raises(KeyError):
            self.mongo_service.create_record(payload=self.payload)

    @mock.patch('app.models.record_manager.MongoService.create_connection')
    def test_04_connection_exception(self, mock_create_connection):
        mock_create_connection.side_effect = Exception("Connection Exception")
        with assert_raises(Exception):
            self.mongo_service.create_record(payload=self.payload)

    @mock.patch('app.models.record_manager.MongoService.fetch_record')
    def test_05_invalid_payload(self, mock_fetch_record):
        mock_fetch_record.return_value = {"No record ": ""}
        self.payload.update({'Name': 'Abhi'})
        with self.assertRaises(RecordExistenceError):
            self.mongo_service.create_record(payload=self.payload)

    @mock.patch('app.models.record_manager.MongoService.fetch_record')
    def test_06_record_inexistence_error(self, mock_fetch_record):
        mock_fetch_record.return_value = "No record "
        self.payload.update({'Name': 123})
        with self.assertRaises(RecordInExistenceError):
            self.mongo_service.delete_record(id=self.payload['Name'])

    @mock.patch('app.models.record_manager.MongoService.fetch_record')
    def test_07_invalid_payload(self, mock_fetch_record):
        mock_fetch_record.return_value = {"message": "Record doesn't exist"}
        self.payload.update({'Name': 'Abhi'})
        with self.assertRaises(RecordExistenceError):
            self.mongo_service.create_record(payload=[self.payload])

    @mock.patch('pymongo.collection.Collection.update_one')
    @mock.patch('app.models.record_manager.MongoService.fetch_record')
    def test_08_update_record_success(self, mock_fetch_record, mock_update_one):
        mock_fetch_record.return_value = "there is a record"
        mock_update_one.return_value = {'Message': "Record {'Name': 'Test_Gowrav'} updated in the database"}
        del self.payload["Location"]
        self.payload.update({"Organisation": "LT"})
        response = self.mongo_service.update_record(payload=self.payload)
        expected_response = {'Message': "Record {'Name': 'Test_Gowrav'} updated in the database"}
        self.assertEqual(expected_response, response)

    @mock.patch('app.models.record_manager.MongoService.fetch_record')
    def test_09_update_record_fails_due_to_no_record_exists_error(self, mock_fetch_record):
        mock_fetch_record.return_value = "No record present in the database"
        payload = {"Name": 123, "Location": "Hyderadad"}
        with self.assertRaises(RecordInExistenceError):
            self.mongo_service.update_record(payload=payload)

    @mock.patch('app.models.record_manager.MongoService.fetch_record')
    @mock.patch('app.models.record_manager.MongoService.validate_payload')
    def test_10_delete_record_success(self, mock_validate_payload, mock_fetch_record):
        mock_fetch_record.return_value = {'_id': '1234', 'Location': 'Mumbai', 'Name': 'Test_Gowrav',
                                          'Organisation': 'LTTS'}
        mock_validate_payload.return_value = "Valid Payload"
        response = self.mongo_service.delete_record(id=self.payload["Name"])
        expected_result = {'Message': 'Deleted record Test_Gowrav'}
        self.assertEqual(expected_result, response)

