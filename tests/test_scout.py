from unittest.mock import patch
from lib.scout import Scout

with patch('lib.scout.send_api_request') as mock_api:
    scout = Scout("fake_url")

@patch('lib.scout.send_api_request')
def test_init_scout_children(mock_api_request):
    # Test Initializing Scout class
    scout.init_children()
    mock_api_request.assert_called_with("fake_url", "children")

@patch('lib.scout.send_api_request')
def test_init_scout_children(mock_api_request):
    # Test Initializing Scout class
    scout.bottle_feed(0)
    mock_api_request.assert_called_with('fake_url', path='timers', data={'child': 0, 'name': 'feedings'})

@patch('lib.scout.send_api_request')
def test_init_scout_children(mock_api_request):
    # Test Initializing Scout class
    scout.bottle_feed(0)
    mock_api_request.assert_called_with('fake_url', path='timers', data={'child': 0, 'name': 'feedings'})
