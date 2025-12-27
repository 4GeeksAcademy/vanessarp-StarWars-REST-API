from flask import jsonify, url_for

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def generate_sitemap(app):
    links = ['/admin/']
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if "/admin/" not in url:
                links.append(url)

    links_html = "".join(["<li><a href='" + y + "'>" + y + "</a></li>" for y in links])
    return """
    <div style=" text-align: center; background-image: url('https://wallpapercave.com/wp/4oh3plg.jpg');background-size: cover; background-position: center;min-height: 100vh; color: white; ">
        <div style="text-align: center;">
        <img style="max-height: 200px" src='https://static-blog.onlyoffice.com/wp-content/uploads/2025/09/25100709/Screenshot-1497-e1758784050706.png' />
        <h1>welcomes you to your Star Wars API!!</h1>
        <p>API HOST: <script>document.write('<input style="padding: 5px; width: 300px" type="text" value="'+window.location.href+'" />');</script></p>
       
        <p>Remember to specify a real endpoint path like: </p>
        <ul  list-style: none; padding: 0; margin: 40px auto; width: fit-content;  text-align: center;  text-decoration: none;">"""+links_html+"</ul></div>"
