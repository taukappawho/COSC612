import unittest #for testing
from fastapi.testclient import TestClient #connect to the api
from main.backend import app #the app

#Use Case 1: Admin Raise Authorization
#6 test cases
class TestAdminRaiseAuth(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.valid_token = {"jwt": "valid_admin_token"}
        self.invalid_token = {"jwt": "invalid_token"}

    @patch("main.backend.app.verify_admin")
    @patch("main.backend.app.execute_query")
    def test_user_with_none_admin_logged_in(self, execute_query, verify_admin):
        user_id = 1
        new_level = 1  # Raise from none to user level
        verify_admin.return_value = True
        execute_query.return_value = None

        response = self.client.patch(
            "/admin/change_auth", params={"id": user_id, "lvl": new_level},
            headers={"Authorization": f"Bearer {self.valid_token['jwt']}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["msg"], f"user[{user_id}]['auth'] = {new_level}")

    @patch("main.backend.app.verify_admin")
    @patch("main.backend.app.execute_query")
    def test_user_with_user_level_admin_logged_in(self, execute_query, verify_admin):
        user_id = 2
        new_level = 3  # Raise from user to admin
        verify_admin.return_value = True
        execute_query.return_value = None

        response = self.client.patch(
            "/admin/change_auth", params={"id": user_id, "lvl": new_level},
            headers={"Authorization": f"Bearer {self.valid_token['jwt']}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["msg"], f"user[{user_id}]['auth'] = {new_level}")

    @patch("main.backend.app.verify_admin")
    @patch("main.backend.app.execute_query")
    def test_user_with_admin_level_admin_logged_in(self, execute_query, verify_admin):
        user_id = 3
        new_level = 3  # Keep as admin level
        verify_admin.return_value = True
        execute_query.return_value = None

        response = self.client.patch(
            "/admin/change_auth", params={"id": user_id, "lvl": new_level},
            headers={"Authorization": f"Bearer {self.valid_token['jwt']}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["msg"], f"user[{user_id}]['auth'] = {new_level}")

    @patch("main.backend.app.verify_admin")
    def test_invalid_user_admin_logged_in(self, verify_admin):
        user_id = 9999
        new_level = 1
        verify_admin.return_value = True

        response = self.client.patch(
            "/admin/change_auth", params={"id": user_id, "lvl": new_level},
            headers={"Authorization": f"Bearer {self.valid_token['jwt']}"}
        )
        self.assertEqual(response.status_code, 400)

    @patch("main.backend.app.verify_admin")
    def test_valid_user_admin_not_logged_in(self, verify_admin):
        user_id = 1
        new_level = 2
        verify_admin.side_effect = Exception("Not authorized")

        response = self.client.patch(
            "/admin/change_auth", params={"id": user_id, "lvl": new_level},
            headers={"Authorization": f"Bearer {self.invalid_token['jwt']}"}
        )
        self.assertEqual(response.status_code, 400)

    @patch("main.backend.app.verify_admin")
    def test_user_with_invalid_authorization_level(self, verify_admin):
        user_id = 1
        new_level = 99  # Invalid level
        verify_admin.return_value = True

        response = self.client.patch(
            "/admin/change_auth", params={"id": user_id, "lvl": new_level},
            headers={"Authorization": f"Bearer {self.valid_token['jwt']}"}
        )
        self.assertEqual(response.status_code, 400)

#Use Case 2: Admin Lower Authorization
#6 test cases
class TestAdminLowerAuth(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.valid_token = {"jwt": "valid_admin_token"}

    @patch("main.backend.app.verify_admin")
    @patch("main.backend.app.execute_query")
    def test_user_with_admin_level_admin_logged_in(self, execute_query, verify_admin):
        user_id = 1
        new_level = 2  # Lower from admin to user level
        verify_admin.return_value = True
        execute_query.return_value = None

        response = self.client.patch(
            "/admin/change_auth", params={"id": user_id, "lvl": new_level},
            headers={"Authorization": f"Bearer {self.valid_token['jwt']}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["msg"], f"user[{user_id}]['auth'] = {new_level}")

    @patch("main.backend.app.verify_admin")
    @patch("main.backend.app.execute_query")
    def test_user_with_user_level_admin_logged_in(self, execute_query, verify_admin):
        user_id = 2
        new_level = 0  # Lower from user to none
        verify_admin.return_value = True
        execute_query.return_value = None

        response = self.client.patch(
            "/admin/change_auth", params={"id": user_id, "lvl": new_level},
            headers={"Authorization": f"Bearer {self.valid_token['jwt']}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["msg"], f"user[{user_id}]['auth'] = {new_level}")

    @patch("main.backend.app.verify_admin")
    def test_user_does_not_exist_admin_logged_in(self, verify_admin):
        user_id = 9999
        new_level = 0
        verify_admin.return_value = True

        response = self.client.patch(
            "/admin/change_auth", params={"id": user_id, "lvl": new_level},
            headers={"Authorization": f"Bearer {self.valid_token['jwt']}"}
        )
        self.assertEqual(response.status_code, 400)

    @patch("main.backend.app.verify_admin")
    def test_empty_user_string_admin_logged_in(self, verify_admin):
        new_level = 0
        verify_admin.return_value = True

        response = self.client.patch(
            "/admin/change_auth", params={"id": "", "lvl": new_level},
            headers={"Authorization": f"Bearer {self.valid_token['jwt']}"}
        )
        self.assertEqual(response.status_code, 400)

    @patch("main.backend.app.verify_admin")
    def test_user_with_invalid_authorization_level(self, verify_admin):
        user_id = 1
        new_level = -1  # Invalid level
        verify_admin.return_value = True

        response = self.client.patch(
            "/admin/change_auth", params={"id": user_id, "lvl": new_level},
            headers={"Authorization": f"Bearer {self.valid_token['jwt']}"}
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
