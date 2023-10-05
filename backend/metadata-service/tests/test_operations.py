"""Test all Firestore operations"""


from tests.constants import (
    DOCUMENT_ID,
    SUB_COLLECTION,
    CATEGORY_NAME,
    CATEGORY_DOCUMENT,
    DESCRIPTION,
    SUBSCRIPTION_ID,
    OLD_SUBSCRIPTION_ID,
    SUBSCRIPTION_DOCUMENT,
    UPDATE_SUBSCRIPTION_DOCUMENT,
    LISTED_SUBSCRIPTION_DOCUMENT
)
from metadata.operations import (
    user_exists,
    category_exists,
    subscription_exists,
    document_exists,
    list_categories,
    list_subscriptions,
    create_category,
    create_subscription,
    update_category,
    update_subscription,
    remove_category,
    remove_subscription,
    remove_document,
    get_categories_collection,
    get_subscriptions_collection,
    get_subcollection,
    get_collection,
    build_category_document,
    generate_subscription_id
)
from google.cloud import firestore, firestore_v1


def test_firestore_fixture(mock_firestore_database):
    assert isinstance(mock_firestore_database, firestore.Client)


def test_user_exists(mock_firestore_database):
    assert user_exists(DOCUMENT_ID)


def test_category_exists(mock_firestore_database):
    assert category_exists(DOCUMENT_ID, DOCUMENT_ID)


def test_subscription_exists(mock_firestore_database):
    assert subscription_exists(DOCUMENT_ID, DOCUMENT_ID)
    assert subscription_exists(DOCUMENT_ID, SUBSCRIPTION_DOCUMENT)
    assert not subscription_exists(DOCUMENT_ID, [])


def test_document_exists(mock_firestore_database):
    assert document_exists(mock_firestore_database.collection, DOCUMENT_ID)


def test_list_categories(mock_firestore_list_categories):
    result = list_categories(DOCUMENT_ID)

    assert result
    assert isinstance(result, list)
    assert len(result) == 1
    assert result == [ CATEGORY_NAME ]


def test_list_subscriptions(mock_firestore_list_subscriptions):
    result = list_subscriptions(DOCUMENT_ID)
    print(result)

    assert result
    assert result == LISTED_SUBSCRIPTION_DOCUMENT


def test_create_category(mock_firestore_database):
    result = create_category(DOCUMENT_ID, DOCUMENT_ID)

    assert result
    assert result == DOCUMENT_ID


def test_create_subscription(mock_firestore_database):
    result = create_subscription(DOCUMENT_ID, SUBSCRIPTION_DOCUMENT)

    assert result
    assert result == SUBSCRIPTION_ID


def test_update_category(mock_firestore_database):
    result = update_category(DOCUMENT_ID, f"old_{CATEGORY_NAME}", CATEGORY_NAME)

    assert result
    assert result == CATEGORY_NAME


def test_update_subscription_with_id(mock_firestore_database):
    result = update_subscription(DOCUMENT_ID, SUBSCRIPTION_ID, UPDATE_SUBSCRIPTION_DOCUMENT)

    assert result
    assert result == SUBSCRIPTION_ID


def test_update_subscription(mock_firestore_database):
    result = update_subscription(DOCUMENT_ID, OLD_SUBSCRIPTION_ID, SUBSCRIPTION_DOCUMENT)

    assert result
    assert result == SUBSCRIPTION_ID


def test_remove_category(mock_firestore_database):
    result = remove_category(DOCUMENT_ID, DOCUMENT_ID)

    assert result
    assert result == DOCUMENT_ID


def test_remove_subscription(mock_firestore_database):
    result = remove_subscription(DOCUMENT_ID, DOCUMENT_ID)

    assert result
    assert result == DOCUMENT_ID


def test_remove_document(mock_firestore_database):
    result = remove_document(mock_firestore_database.collection, DOCUMENT_ID)

    assert result
    assert result == DOCUMENT_ID


def test_get_categories_collection(mock_firestore_database):
    result = get_categories_collection(DOCUMENT_ID)

    assert result
    assert isinstance(result, firestore_v1.collection.CollectionReference)


def test_get_subscriptions_collection(mock_firestore_database):
    result = get_subscriptions_collection(DOCUMENT_ID)

    assert result
    assert isinstance(result, firestore_v1.collection.CollectionReference)


def test_get_subcollection(mock_firestore_database):
    result = get_subcollection(DOCUMENT_ID, SUB_COLLECTION)

    assert result
    assert isinstance(result, firestore_v1.collection.CollectionReference)


def test_get_collection(mock_firestore_database):
    result = get_collection()

    assert result
    assert isinstance(result, firestore_v1.collection.CollectionReference)


def test_build_category_document():
    assert build_category_document(CATEGORY_NAME) == CATEGORY_DOCUMENT


def test_generate_subscription_id():
    subscription_id = generate_subscription_id(DESCRIPTION)
    assert subscription_id == SUBSCRIPTION_ID
