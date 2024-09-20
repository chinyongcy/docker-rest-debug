from flask import Flask, request, jsonify
import socket

app = Flask(__name__)
app.json.sort_keys = False

# Get Server IP
server_hostname = socket.gethostname()
server_ip = socket.gethostbyname(server_hostname)
# Initialise empty array for testing
users = []


# Catch All
@app.route(
    "/",
    defaults={"my_path": ""},
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"],
)
@app.route(
    "/<path:my_path>",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"],
)
def catch_all(my_path):
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr

    if request.is_json:
        body_type = "json"
        body_content = request.get_json()
    elif request.form:
        body_type = "form"
        body_content = request.form.to_dict()
    else:
        body_type = "raw"
        body_content = request.data.decode("utf-8")

    request_details = {
        "path": request.path,
        "method": request.method,
        "Server Hostname": server_hostname,
        "Server IP": server_ip,
        "Client IP": client_ip,
        "Headers": dict(request.headers),
    }

    if request.args:
        request_details["Params"] = dict(request.args)
    if body_content:
        request_details["Body"] = {"type": body_type, "content": body_content}

    return (
        jsonify(request_details),
        200,
    )


@app.route("/users", methods=["GET", "POST", "PUT", "DELETE"])
def get_user():
    match request.method:
        case "GET":
            # Return all users if any exist
            if users:
                return (
                    jsonify(
                        {"message": f"{len(users)} user(s) found!", "users": users}
                    ),
                    200,
                )
            else:
                return jsonify({"message": "There are no users yet!"}), 404

        case "POST":
            if not request.is_json or "username" not in request.json:
                return (
                    jsonify(
                        {
                            "message": "Ensure that your request has a json body with username. E.g. {'username': 'john'}"
                        }
                    ),
                    400,
                )
            # Add a new user
            new_user = request.json.get("username")
            if new_user and new_user not in users:
                users.append(new_user)
                return jsonify({"message": f"User {new_user} added!"}), 201
            else:
                return (
                    jsonify({"message": f"user '{new_user}' already exists!"}),
                    400,
                )

        case "PUT":
            # Update a user's name
            old_user = request.json.get("old_username")
            new_user = request.json.get("new_username")
            if old_user in users:
                users[users.index(old_user)] = new_user
                return (
                    jsonify({"message": f"User {old_user} updated to {new_user}!"}),
                    200,
                )
            else:
                return jsonify({"message": "User not found!"}), 404

        case "DELETE":
            # Delete a user
            user_to_delete = request.json.get("username")
            if user_to_delete in users:
                users.remove(user_to_delete)
                return jsonify({"message": f"User {user_to_delete} deleted!"}), 200
            else:
                return jsonify({"message": "User not found!"}), 404


@app.route("/user_id", methods=["GET"])
def get_user_id():
    if "username" not in request.args:
        return jsonify({"message": "Please pass 'username' in params/args!"}), 400
    username = request.args.get("username")
    if username not in users:
        return jsonify({"message": "User not found!"}), 404
    else:
        return jsonify(
            {"message": {"username": username, "user_id": users.index(username)}}
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
