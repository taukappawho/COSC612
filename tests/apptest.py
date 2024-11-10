import unittest
from main.backend.app import admin_change_auth

class TestAdminChangeAuth(unittest.TestCase):
    
    def setUp(self):
        self.admin_logged_in = True  #simulate admin logged-in state
        self.existing_users = {"testUser": "none"}  #simulate a basic user authorization level store

    def admin_change_auth(self, user, level, admin_logged_in):
        if not admin_logged_in:
            raise PermissionError("Admin privileges required")
        if user not in self.existing_users:
            raise ValueError("User does not exist")
        if level not in ["none", "user", "admin"]:
            raise ValueError("Invalid authorization level")
        #changing authorization level
        self.existing_users[user] = level
        return self.existing_users[user]

    def test_raise_authorization_to_user(self):
        user = "testUser"
        level = "user"
        self.assertEqual(self.admin_change_auth(user, level, self.admin_logged_in), "user")

    def test_raise_authorization_to_admin(self):
        user = "testUser"
        level = "admin"
        self.assertEqual(self.admin_change_auth(user, level, self.admin_logged_in), "admin")

    def test_no_change_on_admin_level(self):
        user = "testUser"
        level = "admin"
        self.existing_users[user] = "admin"
        self.assertEqual(self.admin_change_auth(user, level, self.admin_logged_in), "admin")

    def test_invalid_user(self):
        user = "invalidUser"
        level = "none"
        with self.assertRaises(ValueError, msg="User does not exist"):
            self.admin_change_auth(user, level, self.admin_logged_in)

    def test_admin_logged_out(self):
        user = "testUser"
        level = "user"
        self.admin_logged_in = False
        with self.assertRaises(PermissionError, msg="Admin privileges required"):
            self.admin_change_auth(user, level, self.admin_logged_in)

    def test_invalid_level(self):
        user = "testUser"
        level = "superuser"
        with self.assertRaises(ValueError, msg="Invalid authorization level"):
            self.admin_change_auth(user, level, self.admin_logged_in)

if __name__ == '__main__':
    unittest.main()
