from unittest.mock import patch
from lib.scout import Scout, connect_to_baby_buddy, send_api_request
import pytest

with patch('lib.scout.send_api_request') as mock_api:
    scout = Scout("fake_url")

@patch('lib.scout.send_api_request')
def test_init_scout_children(mock_api_request):
    # Test Initializing Scout class
    scout.init_children()
    mock_api_request.assert_called_with("fake_url", "children")

@patch('lib.scout.send_api_request')
def test_bottle_feed(mock_api_request):
    # Test Initializing Scout class
    scout.bottle_feed(0)
    mock_api_request.assert_called_with('fake_url', path='timers', data={'child': 0, 'name': 'feedings'})

@patch('lib.scout.send_api_request')
def test_right_breast(mock_api_request):
    # Test Initializing Scout class
    scout.right_breast(0)
    mock_api_request.assert_called_with('fake_url', path='timers', data={'child': 0, 'name': 'feedings'})

@patch('lib.scout.send_api_request')
def test_left_breast(mock_api_request):
    # Test Initializing Scout class
    scout.left_breast(0)
    mock_api_request.assert_called_with('fake_url', path='timers', data={'child': 0, 'name': 'feedings'})

@patch('lib.scout.send_api_request')
def test_both_breasts(mock_api_request):
    # Test Initializing Scout class
    scout.breast_feed(0)
    mock_api_request.assert_called_with('fake_url', path='timers', data={'child': 0, 'name': 'feedings'})

@patch('lib.scout.send_api_request')
def test_wet_solid_diaper(mock_api_request):
    # Test Initializing Scout class
    scout.wet_solid_diaper(0)
    mock_api_request.assert_called_with('fake_url', 'changes', data={'wet': True, 'solid': True, 'child': 0})

@patch('lib.scout.send_api_request')
def test_solid_diaper(mock_api_request):
    # Test Initializing Scout class
    scout.solid_diaper(0)
    mock_api_request.assert_called_with('fake_url', 'changes', data={'wet': False, 'solid': True, 'child': 0})

@patch('lib.scout.send_api_request')
def test_wet_diaper(mock_api_request):
    # Test Initializing Scout class
    scout.wet_diaper(0)
    mock_api_request.assert_called_with('fake_url', 'changes', data={'wet': True, 'solid': False, 'child': 0})


@patch('lib.scout.send_api_request')
def test_conect_to_baby_buddy(mock_api_request):
    mock_api_request.side_effect = [OSError("test"), {"results": [{"id": 1}]}]
    # Test Initializing Scout class
    scout = connect_to_baby_buddy('fake_url')
    mock_api_request.assert_called_with('fake_url', 'children')

@patch('lib.scout.utils.retrieve_auth_variables')
@patch('lib.scout.requests')
def test_get_send_api_request(mock_request, mock_utils):
    class FakeRequest:
        def __init__(self):
            self.content = '{"test": "test"}'
    fake = FakeRequest()
    mock_request.get.side_effect = [fake]
    mock_utils.side_effect = [{"AUTHORIZATION": {"test": "test"}}, {"AUTHORIZATION": {"test": "test"}}]
    request = send_api_request("test", "best", {"test": "test"})
    assert request == {'test': 'test'}

@patch('lib.scout.utils.retrieve_auth_variables')
@patch('lib.scout.requests')
def test_post_send_api_request(mock_request, mock_utils):
    class FakeRequest:
        def __init__(self):
            self.content = '{"test": "test"}'
    fake = FakeRequest()
    mock_request.post.side_effect = [fake]
    mock_utils.side_effect = [{"AUTHORIZATION": {"test": "test"}}, {"AUTHORIZATION": {"test": "test"}}]
    request = send_api_request("test", "best", {"headers": "headers"}, {"data": "data"})
    assert request == {'test': 'test'}

@patch('lib.scout.send_api_request')
def test_sleep(mock_api_request):
    # Test Initializing Scout class
    scout.sleep(0)
    mock_api_request.assert_called_with('fake_url', path='timers', data={'child': 0, 'name': 'sleep'})

@patch('lib.scout.send_api_request')
def test_tummy_time(mock_api_request):
    # Test Initializing Scout class
    scout.tummy_time(0)
    mock_api_request.assert_called_with('fake_url', path='timers', data={'child': 0, 'name': 'tummy-times'})

@patch('lib.scout.send_api_request')
def test_get_timers(mock_api_request):
    mock_api_request.side_effect = [{"results": [{"name": "sleep", "child": 0, "active": True}]}]
    # Test Initializing Scout class
    timer = scout.get_timer(0, "sleep")
    assert timer == {'active': True, 'child': 0, 'name': 'sleep'} 

@patch('lib.scout.send_api_request')
def test_resolve_timers_current_timer(mock_api_request):
    mock_api_request.side_effect = [{"results": [{"name": "sleep", "child": 0, "active": True, "id": 0}]}, None]
    # Test Initializing Scout class
    timer = scout.resolve_timers(0, "sleep", {"timer": 0})
    assert timer == None

@patch('lib.scout.send_api_request')
def test_next_child(mock_api_request):
    # Test Initializing Scout class
    mock_api_request.side_effect = [{"results": [{"id": 3}]}]
    scout = Scout("fake_url")
    next_child = scout.next_child()
    assert next_child == 3

@patch('lib.scout.send_api_request')
def test_next_child_no_children(mock_api_request):
    # Test Initializing Scout class
    scout = Scout("fake_url")
    with pytest.raises(IndexError) as e:
        next_child = scout.next_child()

@patch('lib.scout.send_api_request')
def test_next_next_child(mock_api_request):
    # Test Initializing Scout class
    mock_api_request.side_effect = [{"results": [{"id": 3}, {"id": 5}]}]
    scout = Scout("fake_url")
    next_child = scout.next_child()
    next_child = scout.next_child()
    assert next_child == 5

@patch('lib.scout.send_api_request')
def test_next_put_of_index_child(mock_api_request):
    # Test Initializing Scout class
    mock_api_request.side_effect = [{"results": [{"id": 3}, {"id": 5}]}]
    scout = Scout("fake_url")
    next_child = scout.next_child()
    next_child = scout.next_child()
    next_child = scout.next_child()
    assert next_child == 3

@patch('lib.scout.send_api_request')
def test_previous_child(mock_api_request):
    # Test Initializing Scout class
    mock_api_request.side_effect = [{"results": [{"id": 3}, {"id": 5}]}]
    scout = Scout("fake_url")
    previous_child = scout.previous_child()
    assert previous_child == 5

@patch('lib.scout.send_api_request')
def test_previous_child_no_children(mock_api_request):
    # Test Initializing Scout class
    scout = Scout("fake_url")
    with pytest.raises(IndexError) as e:
        previous_child = scout.previous_child()

@patch('lib.scout.send_api_request')
def test_previous_previous_child(mock_api_request):
    # Test Initializing Scout class
    mock_api_request.side_effect = [{"results": [{"id": 3}, {"id": 5}]}]
    scout = Scout("fake_url")
    previous_child = scout.previous_child()
    previous_child = scout.previous_child()
    assert previous_child == 3

@patch('lib.scout.send_api_request')
def test_previous_out_of_index_child(mock_api_request):
    # Test Initializing Scout class
    mock_api_request.side_effect = [{"results": [{"id": 3}, {"id": 5}]}]
    scout = Scout("fake_url")
    previous_child = scout.previous_child()
    previous_child = scout.previous_child()
    previous_child = scout.previous_child()
    assert previous_child == 5