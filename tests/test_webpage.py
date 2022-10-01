from unittest.mock import patch
from lib.webpage import load_webpage, default_route
import os


def test_load_webpage():
    webpage = load_webpage(f"{os.getcwd()}/tests/resources/test.html")
    assert webpage == """<!DOCTYPE html>
        <html>
            <head>
                <title>test</title>
            </head>
            <body>
                {{ test }}
            </body>
        </html>"""

@patch("lib.webpage.template.render_template")
@patch("lib.webpage.load_webpage")
def test_default_route(mock_webpage, render_template):
    webpage = default_route()
    mock_webpage.assert_called_with('webpages/default.html')


