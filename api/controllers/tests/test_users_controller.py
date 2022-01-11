import unittest
from unittest.mock import Mock, patch
import json
from api import app
# from api.services import userService as service
from api.data.entities import User
from hamcrest import assert_that, equal_to, has_key


class BaseUsersControllerTest(unittest.TestCase):

    def __init__(self, endpoint, *args, **kwargs):
        super(BaseUsersControllerTest, self).__init__(*args, **kwargs)
        self.ADDRESS = f"/api/v1/users/{endpoint}"

        print(self.ADDRESS)
    def post(self, address, body):
        with(app.test_client(self) as c):
            return c.post(address, data=json.dumps(body), content_type="application/json")

    def test_response_when_no_request_body(self):
        route = self.ADDRESS
        data = {}
        response = self.post(route, data)
        body = response.get_json()

        assert_that(response.status_code, equal_to(406))
        assert_that(body["message"], equal_to("Request body was not found"))

class RegisterUsersTest(BaseUsersControllerTest):
    
    def __init__(self, *args, **kwargs):
        super(RegisterUsersTest, self).__init__("register", *args, **kwargs)
        self.BASE_ROUTE = self.ADDRESS
    
    # def test_response_when_no_request_body(self):
    #     route = self.BASE_ROUTE
    #     data = {}
    #     response = self.post(route, data)
    #     body = response.get_json()

    #     assert_that(response.status_code, equal_to(406))
    #     assert_that(body["message"], equal_to("Request body was not found"))

    def test_response_when_username_missing(self):
        route = self.BASE_ROUTE 
        data = {
            "password": "TEST"
        }

        response = self.post(route, data)
        body = response.get_json()

        assert_that(response.status_code, equal_to(401))
        assert_that(body["message"]["username"][0],
                    equal_to("Username is required"))

    def test_response_when_password_missing(self):
        route = self.BASE_ROUTE
        data = {
            "username": "TEST"
        }

        response = self.post(route, data)
        body = response.get_json()

        assert_that(response.status_code, equal_to(401))
        assert_that(body["message"]["password"][0],
                    equal_to("Password is required"))

    @patch("api.controllers.users_controller.service")
    def test_response_when_ok(self, service):

        mock_data = {
            "username": "mock_username",
            "password": "mock_password"
        }
        mock_user = User(mock_data["username"], mock_data["password"])

        service.create(mock_user).return_value = mock_user

        route = self.BASE_ROUTE
        response = self.post(route, mock_data)
        body = response.get_json()

        expected_response_keys = ["accessToken", "expiresOn", "user"]
        assert_that(response.status_code, equal_to(200))

        for key in expected_response_keys:
            assert_that(body, has_key(key))


# class AuthenticateUsersTest(unittest.TestCase):
#     def __init__(self, *args, **kwargs):
#         super(AuthenticateUsersTest, self).__init__(*args, **kwargs)
#         self.BASE_ROUTE = self.ADDRESS + "/auth"



class DeleteUsersTest(unittest.TestCase):
    pass


class UpdateUserTest(unittest.TestCase):
    pass


class GetUserTest(unittest.TestCase):
    pass


class GetAllUsersTest(unittest.TestCase):
    pass


def run():
    unittest.main(module=__name__)


if (__name__ == "__main__"):
    unittest.main()
