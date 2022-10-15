def render_template(loaded_html, variables):
    """
    Function to support simple Jinja like substitutions.
    e.g. {"test": "WOO HOO"} would replace {{ test }} in template with WOO HOO

    params:
        loaded_html(str): Full copy of the loaded html opened and read
        variables(dict): Dictionary containing mappings and replacement values as shown above.
    """
    modified_html = loaded_html
    for key, value in variables.items():
        modified_html = modified_html.replace("{{ " + key + " }}", value)
    return modified_html
