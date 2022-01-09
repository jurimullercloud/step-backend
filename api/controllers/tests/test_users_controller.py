import unittest
import json
from api import app
from hamcrest import assert_that, equal_to



class RegisterUsersTest(unittest.TestCase):
    BASE_ROUTE = "/api/v1/users/register"


    def post(self, address, body):
        with(app.test_client(self) as c):
            return c.post(address, data = json.dumps(body), content_type = "application/json")


    def test_response_when_no_request_body(self):
        route = self.BASE_ROUTE
        data = {}
        response = self.post(route, data)
        body = response.get_json()

        assert_that(response.status_code, equal_to(406))
        assert_that(body["message"], equal_to("Request body was not found"))


    def test_response_when_username_missing(self):
        route = self.BASE_ROUTE
        data = {
            "password": "TEST"
        }

        response = self.post(route, data)
        body = response.get_json()

        assert_that(response.status_code, equal_to(401))
        assert_that(body["message"]["username"][0], equal_to("Username is required"))

    def test_response_when_password_missing(self):
        route = self.BASE_ROUTE
        data = {
            "username": "TEST"
        }

        response = self.post(route, data)
        body = response.get_json()

        assert_that(response.status_code, equal_to(401))
        assert_that(body["message"]["password"][0], equal_to("Password is required"))

    
    def test_response_when_ok(self):
        with(app.test_client(self) as c):
            pass

class AuthenticateUsersTest(unittest.TestCase):
    pass

class DeleteUsersTest(unittest.TestCase):
    pass

class UpdateUserTest(unittest.TestCase):
    pass

class GetUserTest(unittest.TestCase):
    pass

class GetAllUsersTest(unittest.TestCase):
    pass





def run():
    unittest.main(module = __name__)

if (__name__ == "__main__"):
    unittest.main()

