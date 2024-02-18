from flask import Flask, jsonify, request, Response

app = Flask(__name__)

# Non-confidential data in JSON format
data = {
    "message": "Hello, world!"
}

# Application configuration values
config = {
    "debug": True,
    "port": 5000
}

# Secrets (authorization credentials)
secrets = {
    "username": "admin",
    "password": "password123"
}

# Auth token
auth_token = None

@app.route('/')
def index():
    return jsonify(data)

@app.route('/config')
def get_config():
    return jsonify(config)

@app.route('/secrets')
def get_secrets():
    if check_auth(request):
        return jsonify(secrets)
    else:
        return Response('Unauthorized', 401)

# Health check
@app.route('/health')
def health_check():
    return "OK"


@app.route('/auth', methods=['POST'])
def authenticate():
    global auth_token
    auth = request.authorization
    if not auth or auth.username != secrets['username'] or auth.password != secrets['password']:
        return Response('Unauthorized', 401)
    else:
        auth_token = "some_random_token_abcabc"
        return jsonify({"token": auth_token})

def check_auth(request):
    global auth_token
    if 'Authorization' in request.headers and request.headers['Authorization'] == f'Bearer {auth_token}':
        return True
    return False


# To test auth:
# curl -X POST http://localhost:5000/auth -u admin:password123
# curl -X GET http://localhost:5000/secrets -H "Authorization: Bearer some_random_token_abcabc"

if __name__ == '__main__':
    app.run(debug=config['debug'], port=config['port'])

