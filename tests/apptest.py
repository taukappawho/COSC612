from requests import request
import unittest

class TestAuthorizationChanges(unittest.TestCase):

    def setUp(self):
        #login credentials
        self.login_url = "https://recipe.naurot.com/login"
        self.payload = {'name': 'James2', 'password': 'naurot'}
        self.headers = {}
        self.files = []
        
        self.james_user_id=1
        self.john_user_id=2
        self.james1_user_id=6
        self.bhuvan_user_id=8
        self.james2_user_id=9
        self.jamie_user_id=10
        
        self.url_change_auth = "https://recipe.naurot.com/admin/change_auth"

        self.lvl_none=0
        self.lvl_user=1
        self.lvl_admin=2

    def get_token(self):
        response = request("POST", self.login_url, headers=self.headers, data=self.payload, files=self.files)
        response_data = response.json()
        token = response_data["token"]
        return token
    
    def get_auth(self):
        return f"Bearer {self.get_token()}"
    
    '''RAISE AUTHORIZATION'''

    def test_user_with_none_admin_logged_in(self):
        headers = {'Authorization': self.get_auth()}
        url = f"{self.url_change_auth}?id={self.jamie_user_id}&lvl={self.lvl_user}"
        print(url)

        response = request("PATCH", url, headers=headers, data=self.payload, files=self.files)
        print(response.text)
        self.assertIn(f"user[{self.jamie_user_id}]['auth'] = {self.lvl_user}", response.text, "Failed to raise authorization to user.")

    def test_user_with_user_level_admin_logged_in(self):
        headers = {'Authorization': self.get_auth()}
        url = f"{self.url_change_auth}?id={self.jamie_user_id}&lvl={self.lvl_admin}"
        print(url)

        response = request("PATCH", url, headers=headers, data=self.payload, files=self.files)
        print(response.text)
        self.assertIn(f"user[{self.jamie_user_id}]['auth'] = {self.lvl_admin}", response.text, "Failed to raise authorization to admin.")

    def test_user_with_admin_level_admin_logged_in(self):
        headers = {'Authorization': self.get_auth()}
        url = f"{self.url_change_auth}?id={self.jamie_user_id}&lvl={self.lvl_admin}"
        print(url)

        response = request("PATCH", url, headers=headers, data=self.payload, files=self.files)
        print(response.text)
        self.assertIn(f"user[{self.jamie_user_id}]['auth'] = {self.lvl_admin}", response.text, "Failed to raise authorization to admin.")

    def test_invalid_user_admin_logged_in(self):
        invalid_id=-1
        headers = {'Authorization': self.get_auth()}
        url = f"{self.url_change_auth}?id={invalid_id}&lvl={self.lvl_admin}"
        print(url)

        response = request("PATCH", url, headers=headers, data=self.payload, files=self.files)
        print(response.text)
        #bug encountered
        self.assertNotIn(f"user[{invalid_id}]['auth'] = {self.lvl_admin}", response.text, "Invalid ID raised to Admin.")

    def test_valid_user_admin_not_logged_in(self):
        wrong_token='Bearer token'
        headers = {'Authorization': wrong_token}
        url = f"{self.url_change_auth}?id={self.jamie_user_id}&lvl={self.lvl_admin}"
        print(url)

        response = request("PATCH", url, headers=headers, data=self.payload, files=self.files)
        print(response.text)

    def test_user_with_invalid_authorization_level(self):
        invalid_lvl=3
        headers = {'Authorization': self.get_auth()}
        url = f"{self.url_change_auth}?id={self.jamie_user_id}&lvl={invalid_lvl}"
        print(url)

        response = request("PATCH", url, headers=headers, data=self.payload, files=self.files)
        print(response.text)
        #bug encountered
        self.assertNotIn(f"user[{self.jamie_user_id}]['auth'] = {invalid_lvl}", response.text, "Valid ID raised to invalid level.") 


    '''LOWER AUTHORIZATION'''
        
    '''def test_user_with_admin_level_admin_logged_in(self):
        headers = {'Authorization': self.get_auth()}
        url = f"{self.url_change_auth}?id={self.user_id}&lvl=2"
        print(url)

        response = request("PATCH", url, headers=headers, data=self.payload, files=self.files)
    def test_user_with_user_level_admin_logged_in(self):
        headers = {'Authorization': self.get_auth()}
        url = f"{self.url_change_auth}?id={self.user_id}&lvl=2"
        print(url)

        response = request("PATCH", url, headers=headers, data=self.payload, files=self.files)
    def test_user_does_not_exist_admin_logged_in(self):
        headers = {'Authorization': self.get_auth()}
        url = f"{self.url_change_auth}?id={self.user_id}&lvl=2"
        print(url)

        response = request("PATCH", url, headers=headers, data=self.payload, files=self.files)
    def test_valid_user_admin_not_logged_in(self):
        headers = {'Authorization': self.get_auth()}
        url = f"{self.url_change_auth}?id={self.user_id}&lvl=2"
        print(url)

        response = request("PATCH", url, headers=headers, data=self.payload, files=self.files)
    def test_empty_user_string_admin_logged_in(self):
        headers = {'Authorization': self.get_auth()}
        url = f"{self.url_change_auth}?id={self.user_id}&lvl=2"
        print(url)

        response = request("PATCH", url, headers=headers, data=self.payload, files=self.files)
    def test_user_with_invalid_authorization_level(self):
        headers = {'Authorization': self.get_auth()}
        url = f"{self.url_change_auth}?id={self.user_id}&lvl=2"
        print(url)

        response = request("PATCH", url, headers=headers, data=self.payload, files=self.files)'''


if __name__ == "__main__":
    unittest.main()