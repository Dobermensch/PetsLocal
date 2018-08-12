from app import app
import unittest

class FlaskTests(unittest.TestCase): 

    @classmethod
    def setUpClass(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
##        app.config['SQLALCHEMY_DATABASE_URI'] =
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

if __name__ == "__main__":
    unittest.main()
