from lib.template import render_template

template = """
<!DOCTYPE html>
        <html>
            <head>
                <title>test</title>
            </head>
            <body>
                {{ test }}
            </body>
        </html>
"""

def test_render_template():
    rendered_template = render_template(template, {"test": "replaced!"})
    assert rendered_template == """
<!DOCTYPE html>
        <html>
            <head>
                <title>test</title>
            </head>
            <body>
                replaced!
            </body>
        </html>
"""