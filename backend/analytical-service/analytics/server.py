"""a

"""

import json
import os

from analytics.operations import (
    get_expenses,
    add_expense,
    update_expense,
    delete_expense
)

from analytics.process_query import (
    total_expenses,
    group_by_category,
    group_by_date,
    get_subscription_expenses_percentage,
    get_expenses_table
)

from flask import Flask, request, abort
from werkzeug.exceptions import HTTPException


# FLASK SERVER OBJECT
app = Flask(os.getenv("SERVICE_NAME", __name__))


@app.route("/users/<user_id>/expenses", methods = ['GET', 'POST'])
@app.route("/users/<user_id>/expenses/<expense>", methods = ['PATCH', 'DELETE'])
def handle_categories(user_id, expense=None):
    """Processes requests to get, create, update, or delete user expenses.

    Args:
        user_id (str): The ID of the user.
        expense (str, optional): The ID of the expense to update, or delete. Defaults to None.

    Returns:
        str | NoReturn: A response object.
    """
    # Extract input body
    data = request.json if request.is_json else None

    # Validations
    # validate_category_input(user_id, category, data)

    # Request process
    match request.method:
        case 'GET':
            results = get_expenses(user_id, date_lower_bound=None, date_higher_bound=None)

            if results["state"] == "SUCCESS":
                table = results["result"]
                return {
                    "total_expenses": total_expenses(table),
                    "categories_chart": group_by_category(table),
                    "expenses_time_series": group_by_date(table),
                    "subscriptions_ratio": get_subscription_expenses_percentage(table),
                    "table": get_expenses_table(table)
                }
            else:
                return f"Something went wrong"

            # return f"Category was submitted successfully"

        case 'POST':
            results = add_expense(user_id, data)
            return results["state"]

        case 'PATCH':
            results = update_expense(user_id, data["id"], data["changes"])
            return results["state"]

        case 'DELETE':
            results = delete_expense(user_id, data)
            return results["state"]

        case _ :
            return abort(405, "Method not implemented")


## UNIT TEST EXPLORATION PURPOSES
@app.route("/", methods = ['GET', 'POST'])
def get_data():
    match request.method:
        case 'GET':
            return f"Category was submitted successfully"

        case 'POST':
            return f"Category was submitted successfully"


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
    app.run(debug=True, port=5001)


if __name__ == "__main__":
    main()