"""Test all Metadata service endpoints"""


import pytest
from tests.constants import (
    USER_ID,
    INEXISTENT_USER_ID,
    CATEGORY_NAME,
    LISTED_SUBSCRIPTION_DOCUMENT,
    NEW_CATEGORY_NAME,
    CATEGORY_INPUT_JSON,
    INVALID_CATEGORY_JSON,
    BUDGET_JSON,
    INVALID_BUDGET_JSON,
    PREFERENCES_JSON,
    INVALID_PREFERENCES_JSON,
    SUBSCRIPTION_ALL_REQUIRED_JSON,
    SUBSCRIPTION_ID,
    NEW_SUBSCRIPTION_ID,
    NEW_SUBSCRIPTION_WITH_DESCRIPTION_JSON,
    NEW_SUBSCRIPTION_WITHOUT_DESCRIPTION_JSON,
    INVALID_SUBSCRIPTION_JSON,
)


def test_user_not_found(flask_client, mock_firestore_database_before_request):
    response = flask_client.get(f"/users/{INEXISTENT_USER_ID}/categories")

    assert response.status_code == 404


def test_not_existing_endpoint(
    flask_client, mock_firestore_categories_subcollection_with_document
):
    response = flask_client.get(f"/users/{USER_ID}/test")

    assert response.status_code == 404


def test_subscription_method_not_implemented(
    flask_client, mock_firestore_categories_subcollection_with_document
):
    response = flask_client.patch(f"/users/{USER_ID}/subscriptions")

    assert response.status_code == 405


def test_category_method_not_implemented(
    flask_client, mock_firestore_categories_subcollection_with_document
):
    response = flask_client.patch(f"/users/{USER_ID}/categories")

    assert response.status_code == 405


def test_category_request_endpoint_malformed(
    flask_client, mock_firestore_categories_subcollection_with_document
):
    response_put = flask_client.put(f"/users/{USER_ID}/categories")
    response_delete = flask_client.delete(f"/users/{USER_ID}/categories")

    assert response_put.status_code == 405
    assert response_delete.status_code == 405


def test_list_categories(
    flask_client, mock_firestore_categories_subcollection_with_document
):
    response = flask_client.get(f"/users/{USER_ID}/categories")

    assert response.status_code == 200
    assert response.is_json
    assert response.json == [CATEGORY_NAME]


def test_list_subscriptions(
    flask_client, mock_firestore_subscriptions_subcollection_with_document
):
    response = flask_client.get(f"/users/{USER_ID}/subscriptions")

    assert response.status_code == 200
    assert response.is_json
    assert response.json == LISTED_SUBSCRIPTION_DOCUMENT


def test_add_category(flask_client, mock_firestore_subcollection_without_document):
    response = flask_client.post(
        f"/users/{USER_ID}/categories", json=CATEGORY_INPUT_JSON
    )

    assert response.status_code == 201
    assert (
        response.get_data(as_text=True)
        == f"Category '{CATEGORY_NAME}' was submitted successfully"
    )


def test_add_subscription(
    flask_client, mock_firestore_categories_subcollection_with_document
):
    response = flask_client.post(
        f"/users/{USER_ID}/subscriptions", json=SUBSCRIPTION_ALL_REQUIRED_JSON
    )

    assert response.status_code == 201
    assert (
        response.get_data(as_text=True)
        == f"Subscription '{SUBSCRIPTION_ID}' was submitted successfully"
    )


def test_add_subscription_request_malformed(
    flask_client, mock_firestore_subcollection_without_document
):
    response = flask_client.post(
        f"/users/{USER_ID}/subscriptions",
        json=NEW_SUBSCRIPTION_WITHOUT_DESCRIPTION_JSON,
    )

    assert response.status_code == 400


def test_add_subscription_category_not_found(
    flask_client, mock_firestore_subcollection_without_document
):
    response = flask_client.post(
        f"/users/{USER_ID}/subscriptions", json=SUBSCRIPTION_ALL_REQUIRED_JSON
    )

    assert response.status_code == 404


def test_add_category_conflict(
    flask_client, mock_firestore_categories_subcollection_with_document
):
    response = flask_client.post(
        f"/users/{USER_ID}/categories", json=CATEGORY_INPUT_JSON
    )

    assert response.status_code == 409


def test_add_category_request_malformed(
    flask_client, mock_firestore_subcollection_without_document
):
    response = flask_client.post(
        f"/users/{USER_ID}/categories", json=INVALID_CATEGORY_JSON
    )

    assert response.status_code == 400


def test_update_category(
    flask_client, mock_firestore_categories_subcollection_with_document
):
    data = {"name": NEW_CATEGORY_NAME}
    response = flask_client.put(
        f"/users/{USER_ID}/categories/{CATEGORY_NAME}", json=data
    )

    assert response.status_code == 200
    assert (
        response.get_data(as_text=True)
        == f"Category '{CATEGORY_NAME}' was updated to '{NEW_CATEGORY_NAME}' successfully"
    )


def test_update_category_not_found(
    flask_client, mock_firestore_subcollection_without_document
):
    data = {"name": NEW_CATEGORY_NAME}
    response = flask_client.put(
        f"/users/{USER_ID}/categories/{CATEGORY_NAME}", json=data
    )

    assert response.status_code == 404


@pytest.mark.parametrize(
    "json_payload, expected_result",
    [
        (
            NEW_SUBSCRIPTION_WITH_DESCRIPTION_JSON,
            f"Subscription '{SUBSCRIPTION_ID}' was updated to '{NEW_SUBSCRIPTION_ID}' successfully",
        ),
        (
            NEW_SUBSCRIPTION_WITHOUT_DESCRIPTION_JSON,
            f"Subscription '{SUBSCRIPTION_ID}' was updated successfully",
        ),
    ],
)
def test_update_subscription(
    json_payload,
    expected_result,
    flask_client,
    mock_firestore_subscriptions_subcollection_with_document,
):
    response = flask_client.put(
        f"/users/{USER_ID}/subscriptions/{SUBSCRIPTION_ID}", json=json_payload
    )

    assert response.status_code == 200
    assert response.get_data(as_text=True) == expected_result


def test_update_subscription_request_malformed(
    flask_client, mock_firestore_subcollection_without_document
):
    response = flask_client.put(
        f"/users/{USER_ID}/subscriptions/{NEW_CATEGORY_NAME}",
        json=NEW_SUBSCRIPTION_WITHOUT_DESCRIPTION_JSON,
    )

    assert response.status_code == 400


def test_update_subscription_request_payload_malformed(
    flask_client, mock_firestore_subscriptions_subcollection_with_document
):
    response = flask_client.put(
        f"/users/{USER_ID}/subscriptions/{SUBSCRIPTION_ID}",
        json=INVALID_SUBSCRIPTION_JSON,
    )

    assert response.status_code == 400


@pytest.mark.parametrize(
    "json_payload, subscription_id",
    [
        (NEW_SUBSCRIPTION_WITH_DESCRIPTION_JSON, SUBSCRIPTION_ID),
        (NEW_SUBSCRIPTION_WITHOUT_DESCRIPTION_JSON, SUBSCRIPTION_ID),
        ({"name": NEW_CATEGORY_NAME}, SUBSCRIPTION_ID),
    ],
)
def test_update_subscription_not_found(
    json_payload,
    subscription_id,
    flask_client,
    mock_firestore_subcollection_without_document,
):
    response = flask_client.put(
        f"/users/{USER_ID}/subscriptions/{subscription_id}", json=json_payload
    )

    assert response.status_code == 404


def test_remove_category(
    flask_client, mock_firestore_categories_subcollection_with_document
):
    response = flask_client.delete(f"/users/{USER_ID}/categories/{CATEGORY_NAME}")

    assert response.status_code == 204


def test_remove_category_not_found(
    flask_client, mock_firestore_subcollection_without_document
):
    response = flask_client.delete(f"/users/{USER_ID}/categories/{CATEGORY_NAME}")

    assert response.status_code == 404


def test_remove_subscription(
    flask_client, mock_firestore_subscriptions_subcollection_with_document
):
    response = flask_client.delete(f"/users/{USER_ID}/subscriptions/{SUBSCRIPTION_ID}")

    assert response.status_code == 204


def test_remove_subscription_request_malformed(
    flask_client, mock_firestore_subcollection_without_document
):
    response = flask_client.delete(f"/users/{USER_ID}/subscriptions/{CATEGORY_NAME}")

    assert response.status_code == 400


def test_remove_subscription_not_found(
    flask_client, mock_firestore_subcollection_without_document
):
    response = flask_client.delete(f"/users/{USER_ID}/subscriptions/{SUBSCRIPTION_ID}")

    assert response.status_code == 404


def test_head_category(
    flask_client, mock_firestore_categories_subcollection_with_document
):
    response = flask_client.head(f"/users/{USER_ID}/categories/{CATEGORY_NAME}")

    assert response.status_code == 204


def test_head_category_not_found(
    flask_client, mock_firestore_subcollection_without_document
):
    response = flask_client.head(f"/users/{USER_ID}/categories/{CATEGORY_NAME}")

    assert response.status_code == 404


def test_get_budget(flask_client, mock_firestore_user_budget):
    response = flask_client.get(f"/users/{USER_ID}/budget")

    assert response.status_code == 200
    assert response.is_json
    assert response.json == BUDGET_JSON


def test_set_budget(flask_client, mock_firestore_user_budget):
    response = flask_client.post(f"/users/{USER_ID}/budget", json=BUDGET_JSON)

    assert response.status_code == 201


def test_set_budget_request_malformed(flask_client, mock_firestore_user_budget):
    response = flask_client.post(f"/users/{USER_ID}/budget", json=INVALID_BUDGET_JSON)

    assert response.status_code == 400


def test_remove_budget(flask_client, mock_firestore_user_budget):
    response = flask_client.delete(f"/users/{USER_ID}/budget")

    assert response.status_code == 204


def test_budget_method_not_implemented(flask_client, mock_firestore_user_budget):
    response = flask_client.post(f"/users/{USER_ID}/preferences")

    assert response.status_code == 405


def test_get_preferences(flask_client, mock_firestore_user_preferences):
    response = flask_client.get(f"/users/{USER_ID}/preferences")

    assert response.status_code == 200
    assert response.is_json
    assert response.json == PREFERENCES_JSON


def test_set_preferences(flask_client, mock_firestore_user_preferences):
    response = flask_client.patch(
        f"/users/{USER_ID}/preferences", json=PREFERENCES_JSON
    )

    assert response.status_code == 201


def test_set_preferences_request_malformed(
    flask_client, mock_firestore_user_preferences
):
    response = flask_client.patch(
        f"/users/{USER_ID}/preferences", json=INVALID_PREFERENCES_JSON
    )

    assert response.status_code == 400


def test_preferences_method_not_implemented(
    flask_client, mock_firestore_user_preferences
):
    response = flask_client.post(f"/users/{USER_ID}/preferences")

    assert response.status_code == 405
