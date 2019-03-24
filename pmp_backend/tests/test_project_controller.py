import unittest
import json
from app import db, app
from requests.auth import _basic_auth_str
from app.api_module.helpers import string_generator
import warnings
from app.api_module.models import Project,Company
import jwt


class ProjectsTest(unittest.TestCase):
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

    def test_create_project(self):
        """ test project creation """
        warnings.simplefilter("ignore")
        request_token = self.client().get('/api/login/',
                                          headers={'Content-Type': 'application/json',
                                                   'Authorization': _basic_auth_str(self.user.get('username'),
                                                                                    self.user.get('password'))})
        json_data = json.loads(request_token.data)
        self.user['token'] = json_data.get('token')

        json_project = {"name": "CS673-Team2", "comment": "PM Tool",
                     "company_id": 1}

        request_project_create = self.client().post('/api/project/', headers={'Content-Type': 'application/json',
                                                                        'x-access-token': self.user['token']},
                                                 data=json.dumps(json_project))
        json_data = json.loads(request_project_create.data)
        self.assertTrue(json_data.get('message'))
        self.assertEqual(json_data.get('message'), 'New project created!')
        self.assertEqual(request_project_create.status_code, 200)

    def test_project_instance(self):
        json_project = {"name": "CS673-Team2", "comment": "PM Tool","company_id":1}
        proj = Project(json_project=json_project)
        self.assertIsInstance(proj, Project)

    def test_get_user(self):
        """ test to get all project under a company """
        warnings.simplefilter("ignore")
        request_token = self.client().get('/api/login/',
                                          headers={'Content-Type': 'application/json',
                                                   'Authorization': _basic_auth_str(self.user.get('username'),
                                                                                    self.user.get('password'))})
        json_data = json.loads(request_token.data)
        self.user['token'] = json_data.get('token')

        company = Company.query.filter_by(name="ANZ").first()


        request_get_project = self.client().get('/api/project/company/'+str(company.id)+'/', headers={'Content-Type': 'application/json',
                                                                'Authorization': _basic_auth_str(self.user.get('username'),
                                                                self.user.get('password')),
                                                                'x-access-token': self.user.get('token')})
        get_data = json.loads(request_get_project.data)
        result= get_data.get('projects')
        self.assertTrue(get_data.get('projects'))
        print(*[i for i in result],sep='\n')

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