def render_template(loaded_html, variables):
    modified_html = loaded_html
    for key, value in variables.items():
        modified_html = modified_html.replace("{{ " + key + " }}", value)
    return modified_html
