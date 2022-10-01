from lib.utils import retrieve_auth_variables, auth_variables_valid, get_base_path, join_path
import os

fake_auth = {
    "SSIDS_PASSWORD": {
        "MYSSID": "MYPASSWORD"
    },
    "BASE_URL": "http://baby.example.com/api/",
    "AUTHORIZATION": {
        "CF-Access-Client-Id": "my cloudfront tunnel id",
        "CF-Access-Client-Secret": "my cloudfront tunnel secret",
        "Authorization": "Token my baby buddy token "
    }
}

def test_retrieve_auth_variables():
    auth = retrieve_auth_variables(f"{os.getcwd()}/tests/resources/fake_auth.json")
    assert auth == fake_auth

def test_failed_retrieve_auth_variables():
    auth = retrieve_auth_variables(f"{os.getcwd()}/tests/resources/fake.json")
    assert auth == None

def test_auth_variables_valid():
    auth = retrieve_auth_variables(f"{os.getcwd()}/tests/resources/fake_auth.json")
    valid = auth_variables_valid(auth)
    assert valid == True

def test_auth_variables_invalid():
    auth = retrieve_auth_variables(f"{os.getcwd()}/tests/resources/fake_auth.json")
    valid = auth_variables_valid(None)
    assert valid == False

def test_auth_variables_invalid_wrong():
    auth = retrieve_auth_variables(f"{os.getcwd()}/tests/fake_false_auth.json")
    valid = auth_variables_valid(None)
    assert valid == False

def test_get_base_path():
    path = get_base_path("test/best/rest")
    assert path == "test/best"

def test_join_path():
    path = join_path("test", "rest")
    assert path == "test/rest"