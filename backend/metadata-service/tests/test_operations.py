"""Test all Firestore operations"""


import pytest
from tests.constants import (
    DOCUMENT_ID,
    SUB_COLLECTION,
    CATEGORY_NAME,
    CATEGORY_DOCUMENT,
    DESCRIPTION,
    SUBSCRIPTION_ID,
    NEW_SUBSCRIPTION_ID,
    SUBSCRIPTION_DOCUMENT,
    NEW_SUBSCRIPTION_WITH_DESCRIPTION_JSON,
    NEW_SUBSCRIPTION_WITHOUT_DESCRIPTION_JSON,
    LISTED_SUBSCRIPTION_DOCUMENT,
    BUDGET_JSON,
    PREFERENCES_JSON,
)
from metadata.operations import (
    user_exists,
    category_exists,
    subscription_exists,
    document_exists,
    list_categories,
    list_subscriptions,
    get_budget,
    get_user_preferences,
    create_category,
    create_subscription,
    set_budget,
    set_user_preferences,
    update_category,
    update_subscription,
    remove_category,
    remove_subscription,
    remove_budget,
    remove_document,
    get_categories_collection,
    get_subscriptions_collection,
    get_subcollection,
    get_collection,
    build_category_document,
    generate_subscription_id,
)
from google.cloud import firestore, firestore_v1


def test_firestore_fixture(mock_firestore_user_subcollection):
    assert isinstance(mock_firestore_user_subcollection, firestore.Client)


def test_user_exists(mock_firestore_user_subcollection):
    assert user_exists(DOCUMENT_ID)


def test_category_exists(mock_firestore_user_subcollection):
    assert category_exists(DOCUMENT_ID, DOCUMENT_ID)


def test_subscription_exists(mock_firestore_user_subcollection):
    assert subscription_exists(DOCUMENT_ID, DOCUMENT_ID)
    assert subscription_exists(DOCUMENT_ID, SUBSCRIPTION_DOCUMENT)
    assert not subscription_exists(DOCUMENT_ID, [])


def test_document_exists(mock_firestore_user_subcollection):
    assert document_exists(mock_firestore_user_subcollection.collection, DOCUMENT_ID)


def test_list_categories(mock_firestore_categories_subcollection_with_document):
    actual_result = list_categories(DOCUMENT_ID)

    assert isinstance(actual_result, list)
    assert len(actual_result) == 1
    assert actual_result == [CATEGORY_NAME]


def test_list_subscriptions(mock_firestore_subscriptions_subcollection_with_document):
    actual_result = list_subscriptions(DOCUMENT_ID)

    assert actual_result
    assert actual_result == LISTED_SUBSCRIPTION_DOCUMENT


def test_get_budget(mock_firestore_user_budget):
    actual_result = get_budget(DOCUMENT_ID)

    assert actual_result
    assert actual_result == BUDGET_JSON


def test_get_user_preferences(mock_firestore_user_preferences):
    actual_result = get_user_preferences(DOCUMENT_ID)

    assert actual_result
    assert actual_result == PREFERENCES_JSON


def test_create_category(mock_firestore_user_subcollection):
    actual_result = create_category(DOCUMENT_ID, DOCUMENT_ID)

    assert actual_result
    assert actual_result == DOCUMENT_ID


def test_create_subscription(mock_firestore_user_subcollection):
    actual_result = create_subscription(DOCUMENT_ID, SUBSCRIPTION_DOCUMENT)

    assert actual_result
    assert actual_result == SUBSCRIPTION_ID


def test_set_budget(mock_firestore_user_budget):
    try:
        set_budget(DOCUMENT_ID, BUDGET_JSON["budget"])
        assert True
    except Exception:
        assert False


def test_set_user_preferences(mock_firestore_user_preferences):
    try:
        set_user_preferences(DOCUMENT_ID, PREFERENCES_JSON)
        assert True
    except Exception:
        assert False


def test_update_category(mock_firestore_user_subcollection):
    actual_result = update_category(DOCUMENT_ID, f"old_{CATEGORY_NAME}", CATEGORY_NAME)

    assert actual_result
    assert actual_result == CATEGORY_NAME


@pytest.mark.parametrize(
    "document, expected_result",
    [
        (NEW_SUBSCRIPTION_WITH_DESCRIPTION_JSON, NEW_SUBSCRIPTION_ID),
        (NEW_SUBSCRIPTION_WITHOUT_DESCRIPTION_JSON, SUBSCRIPTION_ID),
    ],
)
def test_update_subscription(
    document, expected_result, mock_firestore_user_subcollection
):
    actual_result = update_subscription(DOCUMENT_ID, SUBSCRIPTION_ID, document)

    assert actual_result
    assert actual_result == expected_result


def test_remove_category(mock_firestore_user_subcollection):
    actual_result = remove_category(DOCUMENT_ID, DOCUMENT_ID)

    assert actual_result
    assert actual_result == DOCUMENT_ID


def test_remove_subscription(mock_firestore_user_subcollection):
    actual_result = remove_subscription(DOCUMENT_ID, DOCUMENT_ID)

    assert actual_result
    assert actual_result == DOCUMENT_ID


def test_set_budget(mock_firestore_user_budget):
    try:
        remove_budget(DOCUMENT_ID)
        assert True
    except Exception:
        assert False


def test_remove_document(mock_firestore_user_subcollection):
    actual_result = remove_document(
        mock_firestore_user_subcollection.collection, DOCUMENT_ID
    )

    assert actual_result
    assert actual_result == DOCUMENT_ID


def test_get_categories_collection(mock_firestore_user_subcollection):
    actual_result = get_categories_collection(DOCUMENT_ID)

    assert actual_result
    assert isinstance(actual_result, firestore_v1.collection.CollectionReference)


def test_get_subscriptions_collection(mock_firestore_user_subcollection):
    actual_result = get_subscriptions_collection(DOCUMENT_ID)

    assert actual_result
    assert isinstance(actual_result, firestore_v1.collection.CollectionReference)


def test_get_subcollection(mock_firestore_user_subcollection):
    actual_result = get_subcollection(DOCUMENT_ID, SUB_COLLECTION)

    assert actual_result
    assert isinstance(actual_result, firestore_v1.collection.CollectionReference)


def test_get_collection(mock_firestore_user_subcollection):
    actual_result = get_collection()

    assert actual_result
    assert isinstance(actual_result, firestore_v1.collection.CollectionReference)


def test_build_category_document():
    assert build_category_document(CATEGORY_NAME) == CATEGORY_DOCUMENT


def test_generate_subscription_id():
    subscription_id = generate_subscription_id(DESCRIPTION)
    assert subscription_id == SUBSCRIPTION_ID
