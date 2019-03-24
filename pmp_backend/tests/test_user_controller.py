import unittest
import json
from app import db, app
from requests.auth import _basic_auth_str
from app.api_module.helpers import string_generator
import warnings
from app.api_module.models import User
import jwt


class UsersTest(unittest.TestCase):
    """
      Users Test Case
    """
    def setUp(self):
        """
        Test Setup
        """
        self.app = app
        self.client = self.app.test_client
        self.user = {
            'username': 'priti@email.com',
            'password': 'admin123',
            'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNTUzMTE3ODU5fQ.h9hVTPF7QHML_ogkzsxP0Q3cUl12NVYRfPUyQ1jEUMM'
        }
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_user_login_with_valid_cred(self):
        """ test user login with valid credentials """
        res = self.client().get('/api/login/',
                                headers={'Content-Type': 'application/json',
                                         'Authorization': _basic_auth_str(self.user.get('username'),
                                                                          self.user.get('password'))})
        json_data = json.loads(res.data)
        self.assertTrue(json_data.get('token'))
        self.assertEqual(res.status_code, 200)

    def test_user_login_with_invalid_cred(self):
        """ test user login with invalid credentials """
        res = self.client().get('/api/login/',
                                headers={'Content-Type': 'application/json',
                                         'Authorization': _basic_auth_str(self.user.get('username'),
                                                                          self.user.get('password')+'une')})
        self.assertEqual(res.status_code, 401)

    # def test_create_user(self):
    #     """ test user creation """
    #     warnings.simplefilter("ignore")
    #     request_token = self.client().get('/api/login/',
    #                                       headers={'Content-Type': 'application/json',
    #                                                'Authorization': _basic_auth_str(self.user.get('username'),
    #                                                                                 self.user.get('password'))})
    #     json_data = json.loads(request_token.data)
    #     self.user['token'] = json_data.get('token')
    #
    #     json_user = {"name": "priti_test", "email": "test@email.com",
    #                  "password": 'hello123', "admin": False,
    #                  "profile": "Software Engineer",
    #                  "skills": ["java", "C#", "Python"]}
    #
    #     request_user_create = self.client().post('/api/user/', headers={'Content-Type': 'application/json',
    #                                                                     'x-access-token': self.user['token']},
    #                                              data=json.dumps(json_user))
    #     json_data = json.loads(request_user_create.data)
    #     self.assertTrue(json_data.get('message'))
    #     self.assertEqual(json_data.get('message'), 'New user created!')
    #     self.assertEqual(request_user_create.status_code, 200)
    #
    # def test_user_instance(self):
    #     json_user = {"name": "priti_test", "email": "test@email.com",
    #                  "password": 'hello123', "admin": False,
    #                  "profile": "Software Engineer",
    #                  "skills": ["java", "C#", "Python"]}
    #     usr = User(name=json_user['name'], email=json_user['email'], password=string_generator(),
    #                admin=False, profile="", skills=json_user['skills'])
    #     self.assertIsInstance(usr, User)
    #
    # def test_get_user(self):
    #     """ test to get a user id """
    #     user1 = {
    #         'user': 'test@email.com',
    #         'pwd': 'hello123'}
    #     warnings.simplefilter("ignore")
    #     request_token = self.client().get('/api/login/',
    #                                       headers={'Content-Type': 'application/json',
    #                                                'Authorization': _basic_auth_str(user1.get('user'),
    #                                                                                 user1.get('pwd'))})
    #     json_data = json.loads(request_token.data)
    #     user1['token'] = json_data.get('token')
    #     user_dict= jwt.decode(user1['token'], app.config.get('SECRET_KEY'))
    #
    #
    #     user_id = str(user_dict['id'])
    #     request_get_user = self.client().get('/api/user/'+user_id+'/', headers={'Content-Type': 'application/json',
    #                                                             'Authorization': _basic_auth_str(self.user.get('username'),
    #                                                             self.user.get('password')),
    #                                                             'x-access-token': self.user.get('token')})
    #     get_data = json.loads(request_get_user.data)
    #     result= get_data.get('user')['email']
    #     self.assertTrue(get_data.get('user'))
    #     self.assertEqual(result,'test@email.com')

    def tearDown(self):
        """
        Tear Down
        """
        with self.app.app_context():
            print("ending the app testing")
            # db.session.remove()
            # db.drop_all()


if __name__ == '__main__':
    unittest.main()