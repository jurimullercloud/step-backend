from typing import Dict
import unittest
from unittest.mock import patch
import json
from api import app
from api.data.entities import User
from api.utils.auth import generate_password_hash
from hamcrest import assert_that, equal_to, has_key


class BaseUsersControllerTest:

    def __init__(self, to):
        self.to = to
        self.ROUTE = "/api/v1/users" + to
        self.mock_user_login_data = {
            "username": "mock_username",
            "password": "mock_password"
        }

    def post(self, address, body, headers: Dict = None):
        with app.test_client(self) as c:
            return c.post(address, data=json.dumps(body),
                          content_type="application/json",
                          headers=headers)

    def put(self, address, body, headers: Dict = None):
        with app.test_client(self) as c:
            return c.put(address,
                        data=json.dumps(body),
                        content_type="application/json",
                        headers=headers)

    def get(self, address, headers: Dict = None):
        with app.test_client(self) as c:
            return c.get(address,headers=headers)

    def delete(self, address, headers: Dict = None):
        with app.test_client(self) as c:
            return c.delete(address, headers=headers)

    def _is_no_request_body_testable(self):
        return self.to == "/register" \
            or self.to == "/auth"

    def _is_username_password_testable(self):
        return self.to == "/register" \
            or self.to == "/auth"

    def _get_http_response(self, route, method: str, body: Dict = None, headers: Dict = None):
        
        if (method == "PUT"):
            response = self.put(route, body = body, headers=headers)  # sending empty body
        elif (method == "GET"):
            response = self.get(self.ROUTE, headers=headers)
        elif (method == "DELETE"):
            response = self.delete(self.ROUTE, headers=headers)
        else:
            response = self.post(self.ROUTE, body = body, headers=headers) 

        return response

    def test_response_when_no_request_body(self):
        if (self._is_no_request_body_testable()):
            data = {}
            response = self.post(self.ROUTE, data)
            body = response.get_json()

            assert_that(response.status_code, equal_to(406))
            assert_that(body["message"], equal_to(
                "Request body was not found"))
        else:
            self.skipTest("Skipping no request body test")

    def test_response_when_username_missing(self):
        if self._is_username_password_testable():
            data = {
                "password": self.mock_user_login_data["password"]
            }

            response = self.post(self.ROUTE, data)
            body = response.get_json()

            assert_that(response.status_code, equal_to(401))
            assert_that(body["message"]["username"][0],
                        equal_to("Username is required"))
        else:
            self.skipTest("Skipping username validation Test")

    def test_response_when_password_missing(self):

        if self._is_username_password_testable():
            data = {
                "username": self.mock_user_login_data["username"]
            }

            response = self.post(self.ROUTE, data)
            body = response.get_json()

            assert_that(response.status_code, equal_to(401))
            assert_that(body["message"]["password"][0],
                        equal_to("Password is required"))
        else:
            self.skipTest("Skipping password validation Test")

    def when_no_auth_token_present(self, method: str):

        response = self._get_http_response(self.ROUTE, method, body = {}, headers = None) 
        body = response.get_json()

        assert_that(response.status_code, equal_to(400))
        assert_that(body["message"], equal_to(
            "Authorization header not found"))

    @patch("api.utils.auth.jwt")
    def when_auth_token_is_invalid(self, method, jwt_mock):

        jwt_mock.decode.side_effect = Exception("Invalid token")
        mock_token = "Beaer mocktoken"
        response = self._get_http_response(self.ROUTE, method, body = {}, headers={"Authorization": mock_token})
        body = response.get_json()
        assert_that(response.status_code, equal_to(401))
        assert_that(body["message"], "Invalid token")
    
    @patch("api.controllers.users_controller.service")
    @patch("api.utils.auth.jwt")
    def when_no_user_found(self, method, jwt_mock, service):
        jwt_mock.decode.return_value = {}
        mock_token = "Bearer mocktoken"

        service.get_by_id.return_value = None

        response = self._get_http_response(self.ROUTE,
                            method,
                            body=self.mock_user_login_data,
                            headers={"Authorization": mock_token})
        body = response.get_json()

        assert_that(response.status_code, equal_to(404))
        assert_that(body["message"], equal_to("User not found"))

class RegisterUsersTest(unittest.TestCase, BaseUsersControllerTest):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        BaseUsersControllerTest.__init__(self, to="/register")

    @patch("api.controllers.users_controller.service")
    def test_response_when_ok(self, service):

        mock_user = User(self.mock_user_login_data["username"],
                         self.mock_user_login_data["password"])

        service.create(mock_user).return_value = mock_user

        response = self.post(self.ROUTE, self.mock_user_login_data)
        body = response.get_json()

        expected_response_keys = ["accessToken", "expiresOn", "user"]
        assert_that(response.status_code, equal_to(200))

        for key in expected_response_keys:
            assert_that(body, has_key(key))


class AuthenticateUsersTest(unittest.TestCase, BaseUsersControllerTest):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        BaseUsersControllerTest.__init__(self, to="/auth")

    @patch("api.controllers.users_controller.service")
    def test_response_when_no_user_found(self, service):
        service.get_by_filter.return_value = None

        response = self.post(self.ROUTE, self.mock_user_login_data)
        body = response.get_json()
        assert_that(response.status_code, equal_to(404))
        assert_that(body["message"], equal_to("User not found"))

    @patch("api.controllers.users_controller.service")
    def test_response_when_no_password_match(self, service):
        username = self.mock_user_login_data["username"]
        wrong_password = "wrong_password"
        actual_password_hash = generate_password_hash(
            self.mock_user_login_data["password"])

        service.get_by_filter.return_value = User(username=username,
                                                  password=actual_password_hash)
        data = {
            "username": username,
            "password": wrong_password
        }

        response = self.post(self.ROUTE, body=data)
        body = response.get_json()

        assert_that(response.status_code, equal_to(403))
        assert_that(body["message"], "Invalid user credentials")

    @patch("api.controllers.users_controller.service")
    def test_response_when_user_authenticated(self, service):
        username = self.mock_user_login_data["username"]
        password = self.mock_user_login_data["password"]

        actual_password_hash = generate_password_hash(password)
        service.get_by_filter.return_value = User(username=username,
                                                  password=actual_password_hash)

        response = self.post(self.ROUTE, body=self.mock_user_login_data)
        body = response.get_json()

        assert_that(response.status_code, equal_to(200))
        expected_response_keys = ["accessToken", "expiresOn", "user"]

        for key in expected_response_keys:
            assert_that(body, has_key(key))
        assert_that(body["user"]["username"], equal_to(username))


class UpdateUserTest(unittest.TestCase, BaseUsersControllerTest):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        BaseUsersControllerTest.__init__(self, to="/12")

    def test_when_no_auth_token_present(self):
        self.when_no_auth_token_present("PUT")

    def test_when_auth_token_is_invalid(self):
        self.when_auth_token_is_invalid("PUT")

    
    def test_when_no_user_found(self):
        self.when_no_user_found("PUT") 

    @patch("api.controllers.users_controller.service")
    @patch("api.utils.auth.jwt")
    def test_when_no_request_body(self, jwt_mock, service):
        jwt_mock.decode.return_value = {}
        mock_token = "Bearer mocktoken"

        service.get_by_id.return_value = User(username=self.mock_user_login_data["username"],
                                              password=self.mock_user_login_data["password"])

        response = self.put(self.ROUTE,
                            body={},
                            headers={"Authorization": mock_token})

        body = response.get_json()
        assert_that(response.status_code, equal_to(400))
        assert_that(body["message"], "Found empty request body")

    @patch("api.controllers.users_controller.service")
    @patch("api.utils.auth.jwt")
    def test_when_update_ok(self, jwt_mock, service):
        jwt_mock.decode.return_value = {}
        mock_token = "Bearer mocktoken"

        service.get_by_id.return_value = User(
            username=self.mock_user_login_data["username"],
            password=self.mock_user_login_data["password"])

        data = {
            "username": self.mock_user_login_data["username"],
            "password": "Changed Password"
        }

        changed_password_hash = generate_password_hash(data["password"])
        service.update.return_value = User(username=data["username"],
                                           password=changed_password_hash)

        response = self.put(self.ROUTE,
                            body=self.mock_user_login_data,
                            headers={"Authorization": mock_token})
        body = response.get_json()

        assert_that(response.status_code, equal_to(200))
        assert_that(body["message"], "Update is successful")
        assert_that(body["user"]["username"], data["username"])


class GetUserTest(unittest.TestCase, BaseUsersControllerTest):
    

    def __init__(self,*args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        BaseUsersControllerTest.__init__(self, to = "/12")

    def test_when_no_auth_token_present(self):
        self.when_no_auth_token_present("GET")

    def test_when_auth_token_is_invalid(self):
        self.when_auth_token_is_invalid("GET")

    def test_when_no_user_found(self):
        self.when_no_user_found("GET")


    @patch("api.controllers.users_controller.service")
    @patch("api.utils.auth.jwt")
    def test_response_when_ok(self, jwt_mock, service):
        jwt_mock.decode.return_value = {}
        mock_token = "Bearer mocktoken"

        mock_password_hash = generate_password_hash(self.mock_user_login_data["password"])
        service.get_by_id.return_value = User(username=self.mock_user_login_data["username"],
                                              password=mock_password_hash)

        response = self._get_http_response(self.ROUTE, "GET",
                                            headers={"Authorization": mock_token})             
        body = response.get_json()


        assert_that(response.status_code, equal_to(200))
        assert_that(body["message"], "Get user successful")


def run():
    unittest.main(module=__name__)


if (__name__ == "__main__"):
    unittest.main()
