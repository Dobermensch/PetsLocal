from app import app
import json
import unittest

class FlaskTests(unittest.TestCase): 

    @classmethod
    def setUpClass(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
##        app.config['SQLALCHEMY_DATABASE_URI'] = maybe add database tests?
        self.app = app.test_client()
        pass 

    @classmethod
    def tearDownClass(cls):
        pass 

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 

    def tearDown(self):
        pass 

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/') 

        # assert the status code of the response
        self.assertEqual(result.status_code, 200) 

    def test_subscribe_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/subscribe') 

        # assert the response data
        self.assertEqual(result.status_code, 200)

    def test_api_status_get_all(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/get/all')
        
        # assert the response data
        self.assertEqual(result.status_code, 200)

    def test_api_data_get_all(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/get/all')

        ##Convert the data from bytes to json
        my_json = result.data.decode('utf8').replace("'", '"')
        ##Load the json into a python dict
        data = json.loads(my_json)
        
        # assert the response data
        self.assertEqual(len(data), 2)

    def test_api_status_get_all_pets(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/get/pets')
        
        # assert the response data
        self.assertEqual(result.status_code, 200)

    def test_api_data_get_all_pets(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/get/pets')

        ##Convert the data from bytes to json
        my_json = result.data.decode('utf8').replace("'", '"')
        ##Load the json into a python dict
        data = json.loads(my_json)
        
        
        # assert the response data
        self.assertEqual(len(data), 1)

if __name__ == "__main__":
    unittest.main()
