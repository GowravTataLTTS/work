from pymongo import MongoClient
import json
from bson import json_util
import requests
from app.models.exceptions import RecordExistenceError, RecordInExistenceError, \
    InvalidPayloadException


class MongoService:

    def __init__(self):
        self.get_url = "http://127.0.0.1:5000/record/{}"

    @staticmethod
    def create_connection():
        try:
            conn = MongoClient('localhost', 27017)
            # creating a database
            db = conn.database
            # creating a collection under the database
            return db.my_test_database
        except Exception as e:
            msg = f'Failed to establish a connection. Error:{e}'
            raise Exception(msg)

    def create_record(self, payload: dict or list) -> dict:
        """
            This method takes the payload as input and validates the payload and updates it to the database
            :param payload: input payload that is required to create a record
            :return: dictionary consisting of the status of the record creation
        """
        try:
            connection = self.create_connection()
            if isinstance(payload, list):
                for record in payload:
                    self.validate_payload(payload=record)
                    url = self.get_url.format(record["Name"])
                    response = requests.get(url=url)
                    if response.status_code == 200:
                        raise RecordExistenceError(f'Record {record} already exists')
                connection.insert_many(payload)
            else:
                self.validate_payload(payload)
                url = self.get_url.format(payload["Name"])
                response = requests.get(url=url)
                if response.status_code == 200:
                    msg = f'Record {payload["Name"]} already exists'
                    raise RecordExistenceError(msg)
                connection.insert_one(payload)
            msg = {"message": f"Successfully inserted data {payload} into the database"}
            return msg
        except KeyError as e:
            raise KeyError(e.args[0])
        except RecordExistenceError as e:
            raise RecordExistenceError(e)
        except Exception as e:
            msg = f"Encountered exception while creating record. Error:{e}"
            raise Exception(msg)

    def fetch_record(self, id=None) -> list or dict:
        """
            this method fetches the records that are present in the database
            :param id: record that is to be fetched
            :return: list of all the records or an individual record that is passed
        """
        connection = self.create_connection()
        if id:
            record = connection.find_one({"Name": f"{id}"})
            if record:
                return json.loads(json_util.dumps(record))
            msg = f"No record with id {id}"
            raise RecordInExistenceError(msg)
        else:
            return json_util.dumps(connection.find())

    def update_record(self, payload: dict) -> dict:
        """
            this method updates the data for a record in the database
            :param payload: input payload which is to be required for updating the value in the database
            :return: dictionary showing the status of the record
        """
        if not payload["Name"]:
            raise KeyError("Name is required in the payload")
        if len(payload) < 2:
            msg = "Requires one or more attributes to update the payload"
            raise InvalidPayloadException(msg)
        url = self.get_url.format(payload["Name"])
        response = requests.get(url=url)
        if response.status_code == 404:
            msg = f'Record {payload["Name"]} doesnt exists'
            raise RecordInExistenceError(msg)
        connection = self.create_connection()
        filters = {"Name": payload["Name"]}
        new_values = {"$set": payload}
        connection.update_one(filters, new_values)
        message = {"Message": f"Record {filters} updated in the database"}
        return message

    def delete_record(self, id: str) -> dict:
        """
            this method deletes the record that is present in the database
            :param id: id is the record name that is to be deleted
            :return: string consisting of the deleted status
        """
        connection = self.create_connection()
        url = self.get_url.format(id)
        response = requests.get(url=url)
        if response.status_code == 200:
            record = json.loads(response.text)
            del record["_id"]
            connection.delete_one(record)
            msg = {"Message": f"Deleted record {id}"}
            return msg
        msg = f"No record {id} in the database"
        raise RecordInExistenceError(msg)

    @staticmethod
    def validate_payload(payload: dict) -> str:
        required_keys = ("Name", "Organisation", "Location")
        for key in required_keys:
            if key not in payload.keys():
                msg = f'{key} is required in payload'
                raise KeyError(msg)
        return "Valid Payload"
