"""a

"""

import json
import os

from flask import Flask, request, abort
from werkzeug.exceptions import HTTPException

from metadata.validations import (
    is_category_valid,
    is_subscription_valid
)
from metadata.operations import (
    category_exists,
    user_exists,
    list_categories,
    create_category,
    update_category,
    remove_category,
    subscription_exists,
    list_subscriptions,
    create_subscription,
    update_subscription,
    remove_subscription
)


# FLASK SERVER OBJECT
app = Flask(os.getenv("SERVICE_NAME", __name__))


@app.before_request
def user_validation():
    user_id = request.path.split("/")[2]
    if not user_exists(user_id):
        return "User not found", 404

@app.route("/users/<user_id>/categories", methods = ['GET', 'POST'])
@app.route("/users/<user_id>/categories/<category>", methods = ['PUT', 'DELETE'])
def handle_categories(user_id, category=None):
    """Processes requests to get, create, update, or delete user categories.

    Args:
        user_id (str): The ID of the user.
        category (str, optional): The name of the category to update, or delete. Defaults to None.

    Returns:
        str | NoReturn: A response object.
    """
    # Extract input body
    data = request.json if request.is_json else None

    # Validations
    validate_category_input(user_id, category, data)

    # Request process
    match request.method:
        case 'GET':
            return list_categories(user_id)

        case 'POST':
            category_name = create_category(user_id, data["name"])
            return f"Category '{category_name}' was submitted successfully"

        case 'PUT':
            new_category_name = data['name']
            update_category(user_id, old_category_name=category, new_category_name=new_category_name)
            return f"Category '{category}' was updated to '{new_category_name}' successfully"

        case 'DELETE':
            remove_category(user_id, category)
            return f"Category '{category}' was removed successfully"

        case _ :
            return abort(405, "Method not implemented")


@app.route("/users/<user_id>/subscriptions", methods = ['GET', 'POST'])
@app.route("/users/<user_id>/subscriptions/<subscription>", methods = ['PUT', 'DELETE'])
def handle_subscriptions(user_id, subscription=None):

    # Extract inputs
    data = request.json if request.is_json else None

    # Validations
    validate_subscription_input(user_id, subscription, data, request.method)

    match request.method:
        case 'GET':
            return list_subscriptions(user_id)

        case 'POST':
            subscription_id = create_subscription(user_id, data)
            return f"Subscription '{subscription_id}' was submitted successfully"

        case 'PUT':
            subscription_id = update_subscription(user_id, subscription_id=subscription, data=data)
            message = f"Subscription '{subscription}' was updated successfully" \
                if subscription_id == subscription else \
                f"Subscription '{subscription}' was updated to '{subscription_id}' successfully"
            return message

        case 'DELETE':
            remove_subscription(user_id, subscription)
            return f"Subscription '{subscription}' was removed successfully"

        case _ :
            return abort(405, "Method not implemented")


@app.route("/users/<user_id>/budget", methods = ['GET', 'POST'])
def handle_budget(user_id):
    """_summary_

    Args:
        user_id (_type_): _description_

    Returns:
        _type_: _description_
    """

    # # Request process
    # match request.method:
    #     case 'GET':
    #         return get_budget(user_id)

    #     case 'POST':
    #         data = request.json
    #         category_name = set_budget(user_id, data["name"])
    #         return f"Category '{category_name}' was submitted successfully"

    #     case _ :
    #         return abort(405, "Method not implemented")
    
    return abort(405, "Method not implemented")


def validate_category_input(user_id: str, category: str, data: dict):
    if data:
        if not is_category_valid(data):
            abort(400, "Given category is not valid")

        if category_exists(user_id, data["name"]):
            abort(409, "Given category already exists")

    if category:
        if not is_category_valid(category):
            abort(400, "Selected category is not valid")

        if not category_exists(user_id, category):
            abort(404, "Given category does not exist")


## Validation helper functions
def validate_subscription_input(user_id: str, subscription: str, data: dict, method: str):
    if subscription:
        # Check if subscription ID is well-formed
        if not is_subscription_valid(subscription):
            abort(400, "Selected subscription is not valid")

        elif not subscription_exists(user_id, subscription):
            abort(404, "Given subscription does not exist")

    if data:
        # Check if request body is well-formed
        if not is_subscription_valid(data, is_all_required=method == 'POST'):
            abort(400, "Selected subscription is not valid")

        # Check if given category exists
        if "category" in data:
            if not category_exists(user_id, data["category"]):
                abort(404, "Given category does not exist")

        # Check if subscription is registered before adding
        if "description" in data and method == 'POST':
            if subscription_exists(user_id, data):
                abort(409, "Given subscription already exists")


## Error handler
@app.errorhandler(HTTPException)
def handle_exception(error):
    """Return JSON instead of HTML for HTTP errors."""
    response = error.get_response()

    # Replace the body with JSON
    response.data = json.dumps({
        "code": error.code,
        "name": error.name,
        "description": error.description,
    })
    response.content_type = "application/json"
    return response


# main driver function
def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
