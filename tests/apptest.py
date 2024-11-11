from requests import request
import unittest


class TestAuthorizationChanges(unittest.TestCase):
    """
    Unit test class for authorization level change functionality.
    
    This class contains a total of 13 test cases that verify the behavior of the 
    authorization level change endpoint under various scenarios, split into:
      - **Case 1** (6 tests): Tests for raising authorization levels, ensuring only valid
        users can have their authorization levels increased by an admin.
      - **Case 2** (7 tests): Tests for lowering authorization levels, ensuring that only
        valid users can have their levels decreased by an admin.
    
    Each test checks specific conditions based on user ID and level, covering expected 
    successes, invalid inputs, and unauthorized actions.
    """

    
    def setUp(self):
        """
        Set up test credentials, URLs, and authorization levels.
        
        Initializes login, authorization change URLs, valid and invalid credentials, and the list 
        of user IDs and levels to be tested.
        """
        #login credentials
        self.login_url = "https://recipe.naurot.com/login"
        self.invalid_payload ={'name': 'wet', 'password': 'blanket'} #invalid credentials for testing
        self.valid_payload = {'name': 'James2', 'password': 'naurot'} #james has the only valid credentials
        self.headers = {}
        self.files = []

        #valid user id's
        self.james_user_id=1
        self.john_user_id=2
        self.james1_user_id=6
        self.bhuvan_user_id=8
        self.james2_user_id=9
        self.jamie_user_id=10
        
        self.url_change_auth = "https://recipe.naurot.com/admin/change_auth"

        #valid levels
        self.lvl_none=0
        self.lvl_user=1
        self.lvl_admin=2

    def get_token(self,payload):
        """
        Retrieve the authorization token after a successful login.
        Param:
            payload (dict): Login data containing 'name' and 'password'.
        Returns:
            str: Token string if login is successful, error in response.text otherwise
        """
        response = request("POST", self.login_url, headers=self.headers, data=payload, files=self.files)
        
        if "Login successful" in response.text:
            response_data = response.json()
            token = response_data["token"]
            return token
        
        else:
            print(response.text)
    
    def get_auth(self,payload):
        """
        Correct authorization is 'Bearer 'token''
        Param:
            payload (dict): Login data containing 'name' and 'password'.
        
        Returns:
            str: correct authorization format
        """
        return f"Bearer {self.get_token(payload)}"
    
    def set_headers(self,payload):
        """
        Sets the headers for login
        Param:
            payload (dict): Login data containing 'name' and 'password'.
        
        Returns:
            dict: header values
        """
        return {'Authorization': self.get_auth(payload)}

    def set_url(self,url,id,lvl):
        """
        Sets the url
        Param:
            url (str): change_auth url.
            id (int): user id.
            lvl (int): the level (to be raised or lowered).
        
        Returns:
            str: complete url
        """
        return f"{url}?id={id}&lvl={lvl}"

    '''RAISE AUTHORIZATION'''

    def test_raise_user_with_none_admin_logged_in(self):
        """
        Case 1: Raise authorization from none to user level as an admin.
        Verifies if an admin can successfully raise the authorization level of a user with no previous authorization.
        """
        headers=self.set_headers(self.valid_payload)
        url=self.set_url(self.url_change_auth,self.jamie_user_id,self.lvl_user)
        print(url)

        response = request("PATCH", url, headers=headers, data=self.valid_payload, files=self.files)
        print(response.text)
        self.assertIn(f"user[{self.jamie_user_id}]['auth'] = {self.lvl_user}", response.text, "Failed to raise authorization to user.")

    def test_raise_user_with_user_level_admin_logged_in(self):
        """
        Case 1: Raise authorization from user to admin level.
        Ensures the system allows an admin to promote a user to an admin level.
        """
        headers=self.set_headers(self.valid_payload)
        url=self.set_url(self.url_change_auth,self.jamie_user_id,self.lvl_admin)
        print(url)

        response = request("PATCH", url, headers=headers, data=self.valid_payload, files=self.files)
        print(response.text)
        self.assertIn(f"user[{self.jamie_user_id}]['auth'] = {self.lvl_admin}", response.text, "Failed to raise authorization to admin.")

    def test_raise_user_with_admin_level_admin_logged_in(self):
        """
        Case 1: Attempt to raise an already-admin user.
        Confirms that the authorization level remains admin if already at admin level.
        """
        headers=self.set_headers(self.valid_payload)
        url=self.set_url(self.url_change_auth,self.jamie_user_id,self.lvl_admin)
        print(url)

        response = request("PATCH", url, headers=headers, data=self.valid_payload, files=self.files)
        print(response.text)
        self.assertIn(f"user[{self.jamie_user_id}]['auth'] = {self.lvl_admin}", response.text, "Failed to maintain admin authorization.")

    def test_raise_invalid_user_admin_logged_in(self):
        """
        Case 1: Attempt to raise authorization for an invalid user ID.
        Checks that an invalid user ID cannot be granted admin access.
        """
        invalid_id=-1
        headers=self.set_headers(self.valid_payload)
        url=self.set_url(self.url_change_auth,invalid_id,self.lvl_admin)
        print(url)

        response = request("PATCH", url, headers=headers, data=self.valid_payload, files=self.files)
        print(response.text)
        #bug encountered
        self.assertNotIn(f"user[{invalid_id}]['auth'] = {self.lvl_admin}", response.text, "Invalid ID raised authorization to Admin.")

    def test_raise_valid_user_admin_not_logged_in(self):
        """
        Case 1: Raise authorization level without admin login.
        Validates that authorization level changes are rejected when the user is not an admin.
        """
        headers=self.set_headers(self.invalid_payload)
        url=self.set_url(self.url_change_auth,self.jamie_user_id,self.lvl_admin)
        print(url)

        response = request("PATCH", url, headers=headers, data=self.valid_payload, files=self.files)
        print(response.text)
        self.assertNotIn(f"user[{self.jamie_user_id}]['auth'] = {self.lvl_admin}", response.text, "Failure: Admin is not logged in")

    def test_raise_user_with_invalid_authorization_level(self):
        """
        Case 1: Raise to an invalid authorization level.
        Verifies the system rejects invalid levels above the highest defined level.
        """
        invalid_lvl=3
        headers=self.set_headers(self.valid_payload)
        url=self.set_url(self.url_change_auth,self.jamie_user_id,invalid_lvl)
        print(url)

        response = request("PATCH", url, headers=headers, data=self.valid_payload, files=self.files)
        print(response.text)
        #bug encountered
        self.assertNotIn(f"user[{self.jamie_user_id}]['auth'] = {invalid_lvl}", response.text, "Valid ID raised authorization to invalid level.") 


    '''LOWER AUTHORIZATION'''
        
    def test_lower_user_with_admin_level_admin_logged_in(self):
        """
        Case 2: Lower authorization from admin to user level as an admin.
        Verifies if an admin can successfully raise the authorization level of a user with no previous authorization.
        """
        headers=self.set_headers(self.valid_payload)
        url=self.set_url(self.url_change_auth,self.bhuvan_user_id,self.lvl_user)
        print(url)

        response = request("PATCH", url, headers=headers, data=self.valid_payload, files=self.files)
        print(response.text)
        
        self.assertIn(f"user[{self.bhuvan_user_id}]['auth'] = {self.lvl_user}", response.text, "Failed to lower authorization to user.")

    def test_lower_user_with_user_level_admin_logged_in(self):
        """
        Case 2: Lower authorization from user to none level as an admin.
        Verifies if an admin can successfully lower the authorization level of a user with no previous authorization.
        """
        headers=self.set_headers(self.valid_payload)
        url=self.set_url(self.url_change_auth,self.bhuvan_user_id,self.lvl_none)
        print(url)

        response = request("PATCH", url, headers=headers, data=self.valid_payload, files=self.files)
        print(response.text)
        
        self.assertIn(f"user[{self.bhuvan_user_id}]['auth'] = {self.lvl_none}", response.text, "Failed to lower authorization to none") 

    def test_lower_user_with_none_level_admin_logged_in(self):
        """
        Case 2: Attempt to lower an already-none user.
        Confirms that the authorization level remains none if already at none level.
        """
        headers=self.set_headers(self.valid_payload)
        url=self.set_url(self.url_change_auth,self.bhuvan_user_id,self.lvl_none)
        print(url)

        response = request("PATCH", url, headers=headers, data=self.valid_payload, files=self.files)
        print(response.text)
        self.assertIn(f"user[{self.bhuvan_user_id}]['auth'] = {self.lvl_none}", response.text, "Failed maintain none authorization.")

    def test_lower_user_does_not_exist_admin_logged_in(self):
        """
        Case 2: Attempt to lower authorization for an invalid user ID.
        Checks that an invalid user ID cannot be granted user access.
        """
        invalid_id=-1
        headers=self.set_headers(self.valid_payload)
        url=self.set_url(self.url_change_auth,invalid_id,self.lvl_user)
        print(url)

        response = request("PATCH", url, headers=headers, data=self.valid_payload, files=self.files)
        print(response.text)
        
        self.assertNotIn(f"user[{invalid_id}]['auth'] = {self.lvl_user}", response.text, "Invalid ID lowered authorization to user")

    def test_lower_valid_user_admin_not_logged_in(self):
        """
        Case 2: Lower authorization level without admin login.
        Validates that authorization level changes are rejected when the user is not an admin.
        """
        headers=self.set_headers(self.invalid_payload)
        url=self.set_url(self.url_change_auth,self.bhuvan_user_id,self.lvl_admin)
        print(url)

        response = request("PATCH", url, headers=headers, data=self.invalid_payload, files=self.files)
        print(response.text)

        self.assertNotIn(f"user[{self.bhuvan_user_id}]['auth'] = {self.lvl_admin}", response.text, "Failure: Admin is not logged in")


    def test_lower_empty_user_string_admin_logged_in(self):
        """
        Case 2: Lower authorization level for empty id
        Validates that authorization level changes for empty id's
        """
        empty_id=''
        headers=self.set_headers(self.valid_payload)
        url=self.set_url(self.url_change_auth,empty_id,self.lvl_none)
        print(url)

        response = request("PATCH", url, headers=headers, data=self.valid_payload, files=self.files)
        print(response.text)
        
        self.assertNotIn(f"user[{empty_id}]['auth'] = {self.lvl_none}", response.text, "Failure: Empty user string lowered authorization")

    def test_lower_user_with_invalid_authorization_level(self):
        """
        Case 2: Lower authorization level to invalid level
        Validates that authorization level changes can only be lowered to valid levels
        """
        invalid_lvl=-1
        headers=self.set_headers(self.valid_payload)
        url=self.set_url(self.url_change_auth,self.bhuvan_user_id,invalid_lvl)
        print(url)

        response = request("PATCH", url, headers=headers, data=self.valid_payload, files=self.files)
        print(response.text)
        
        self.assertNotIn(f"user[{self.bhuvan_user_id}]['auth'] = {invalid_lvl}", response.text, "Valid ID lowered authorization to invalid level")


if __name__ == "__main__":
    unittest.main()