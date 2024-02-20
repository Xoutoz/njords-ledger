"""Microservice endpoint handlers."""

import json
import logging
import os
import traceback

from flask import Flask, Response, abort, request
from werkzeug.exceptions import HTTPException

from metadata.operations import (
    category_exists,
    create_category,
    create_subscription,
    get_budget,
    get_user_preferences,
    list_categories,
    list_subscriptions,
    remove_budget,
    remove_category,
    remove_subscription,
    set_budget,
    set_user_preferences,
    subscription_exists,
    update_category,
    update_subscription,
    user_exists,
)
from metadata.validations import (
    are_preferences_valid,
    is_budget_valid,
    is_category_valid,
    is_subscription_valid,
)

# Flask server object and related constants
app = Flask(os.getenv("SERVICE_NAME", __name__))
PORT = int(os.getenv("PORT", str(5000)))
HOST = os.getenv("K_SERVICE") if os.getenv("K_SERVICE") is not None else "127.0.0.1"


@app.before_request
def user_validation() -> Response | None:
    """Validate the user ID in the request URL before processing the request.

    Returns
    -------
    flask.Response: A response object, if the user ID is not found.
    """
    user_id = request.path.split("/")[2]
    if not user_exists(user_id):
        return abort(404, "User not found")


@app.after_request
def after_request_handler(response) -> Response:
    """
    Log the Response result.

    Args:
        response (Response): The response object.

    Returns
    -------
        Response: The response object.
    """
    log_message = f"[{request.method}] - HOST{request.path} - {response.status}"
    app.logger.info(log_message)
    return response


@app.route("/users/<user_id>/categories", methods=["GET", "POST"])
@app.route("/users/<user_id>/categories/<category>", methods=["PUT", "DELETE", "HEAD"])
def handle_categories(user_id: str, category: str = None) -> Response:
    """Process requests to get, create, update, delete or verify user categories.

    Args:
        user_id (str): The ID of the user.
        category (str, optional): The name of the category to update,
            delete or verify. Defaults to None.

    Returns
    -------
        flask.Response: A response object.
    """
    # Extract input body
    data = request.json if request.is_json else None

    # Validations
    validate_category_input(user_id, category, data, request.method)

    # Request process
    match request.method:
        # To indicate if a given category is registered or not
        case "HEAD":
            return "", 204

        case "GET":
            return list_categories(user_id)

        case "POST":
            category_name = create_category(user_id, data["name"])
            return f"Category '{category_name}' was submitted successfully", 201

        case "PUT":
            new_category_name = data["name"]
            update_category(
                user_id, old_category_name=category, new_category_name=new_category_name
            )
            return f"Category '{category}' was updated to '{new_category_name}' \
successfully"

        case "DELETE":
            remove_category(user_id, category)
            return "", 204

        case _:
            return


@app.route("/users/<user_id>/subscriptions", methods=["GET", "POST"])
@app.route("/users/<user_id>/subscriptions/<subscription>", methods=["PUT", "DELETE"])
def handle_subscriptions(user_id: str, subscription: str = None) -> Response:
    """Process requests to get, create, update or delete user subscriptions.

    Args:
        user_id (str): The ID of the user.
        subscription (str, optional): The ID of the subscription to update or
            delete. Defaults to None.

    Returns
    -------
        flask.Response: A response object.
    """
    # Extract inputs
    data = request.json if request.is_json else None

    # Validations
    validate_subscription_input(user_id, subscription, data, request.method)

    match request.method:
        case "GET":
            return list_subscriptions(user_id)

        case "POST":
            subscription_id = create_subscription(user_id, data)
            return f"Subscription '{subscription_id}' was submitted successfully", 201

        case "PUT":
            subscription_id = update_subscription(
                user_id, subscription_id=subscription, data=data
            )
            message = (
                f"Subscription '{subscription}' was updated successfully"
                if subscription_id == subscription
                else f"Subscription '{subscription}' was updated to \
'{subscription_id}' successfully"
            )
            return message

        case "DELETE":
            remove_subscription(user_id, subscription)
            return "", 204

        case _:
            return


@app.route("/users/<user_id>/budget", methods=["GET", "POST", "DELETE"])
def handle_budget(user_id: str) -> Response:
    """Process requests to get, create or delete user budget.

    Args:
        user_id (str): The ID of the user.

    Returns
    -------
        flask.Response: A response object.
    """
    # Request process
    match request.method:
        case "GET":
            budget_result = get_budget(user_id)
            return budget_result if budget_result else {"budget": 0}

        case "POST":
            data = request.json if request.is_json else None

            if data and is_budget_valid(data):
                set_budget(user_id, data["budget"])
                return "Budget was submitted successfully", 201
            else:
                abort(400, "Given request payload is not well-formed.")
        case "DELETE":
            remove_budget(user_id)
            return "", 204

        case _:
            return


@app.route("/users/<user_id>/preferences", methods=["GET", "PATCH"])
def handle_preferences(user_id: str) -> Response:
    """Process requests to get, create or delete user charts preferences.

    Args:
        user_id (str): The ID of the user.

    Returns
    -------
        flask.Response: A response object.
    """
    # Request process
    match request.method:
        case "GET":
            return get_user_preferences(user_id)

        case "PATCH":
            data = request.json if request.is_json else None

            if data and are_preferences_valid(data):
                set_user_preferences(user_id, data)
                return "Budget was submitted successfully", 201
            else:
                abort(400, "Given request payload is not well-formed.")

        case _:
            return


def validate_category_input(
    user_id: str, category: str, data: dict, method: str
) -> None:
    """Validate category input.

    Args:
        user_id (str): User ID
        category (str): Category name
        data (dict): Category data
        method (str): HTTP method

    Raises
    ------
        HTTPException: If the input is not valid.
    """
    if data:
        if not is_category_valid(data):
            abort(400, "Given category is not valid")

        if category_exists(user_id, data["name"]) and method == "POST":
            abort(409, "Given category already exists")

    if category:
        if not is_category_valid(category):
            abort(400, "Selected category is not valid")

        if not category_exists(user_id, category):
            abort(404, "Given category does not exist")


## Validation helper functions
def validate_subscription_input(
    user_id: str, subscription: str, data: dict, method: str
) -> None:
    """Validate subscription input.

    Args:
        user_id (str): The ID of the user.
        subscription (str): The ID of the subscription.
        data (dict): The request body.
        method (str): The HTTP method of the request.

    Raises
    ------
        HTTPException: If the input is not valid.
    """
    if subscription:
        # Check if subscription ID is well-formed
        if not is_subscription_valid(subscription):
            abort(400, "Selected subscription is not valid")

        elif not subscription_exists(user_id, subscription):
            abort(404, "Given subscription does not exist")

    if data:
        # Check if request body is well-formed
        if not is_subscription_valid(data, is_all_required=method == "POST"):
            abort(400, "Selected subscription is not valid")

        # Check if given category exists
        if "category" in data:
            if not category_exists(user_id, data["category"]):
                abort(404, "Given category does not exist")


## Error handler
@app.errorhandler(HTTPException)
def handle_http_exception(error: HTTPException) -> Response:
    """Return JSON instead of HTML for HTTP errors."""
    response = error.get_response()

    # Replace the body with JSON
    response.data = json.dumps(
        {
            "code": error.code,
            "name": error.name,
            "description": error.description,
        }
    )
    response.content_type = "application/json"

    app.logger.error(response.data)

    return response


@app.errorhandler(Exception)
def handle_exception(_: Exception) -> Response:
    """Return JSON instead of HTML for internal errors."""
    data = {"code": 500, "name": "Server internal error"}

    response = Response(
        response=json.dumps(data), status=500, mimetype="application/json"
    )

    data["stacktrace"] = traceback.format_exc()
    app.logger.critical(data)

    return response


# main driver function
def main(_):
    """Server runner."""
    app.run(host=HOST, port=PORT)


if __name__ == "__main__":
    main()

else:
    # To bring Flask logs to gunicorn
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
