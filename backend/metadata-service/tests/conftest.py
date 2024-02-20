import pytest
from tests.constants import (
    CATEGORY_DOCUMENT,
    SUBSCRIPTION_DOCUMENT,
    SUBSCRIPTION_ID,
    BUDGET_JSON,
    DOCUMENT_PREFERENCES,
)
from metadata.server import app
from google.cloud import firestore, firestore_v1


# Flask fixtures
@pytest.fixture(scope="function")
def flask_client():
    app.config["TESTING"] = True

    with app.app_context():
        with app.test_client() as client:
            yield client


# Operations fixtures
@pytest.fixture(scope="function")
def mock_firestore_database_before_request(
    mock_firestore_client,
    mock_firestore_document_reference,
    mock_firestore_collection_reference,
):
    document_mock = mock_firestore_document_reference
    collection_mock = mock_firestore_collection_reference

    document_mock.get.return_value = firestore_v1.document.DocumentSnapshot(
        reference=document_mock,
        data={},
        exists=False,
        read_time=None,
        create_time=None,
        update_time=None,
    )

    collection_mock.document.return_value = document_mock

    mock_firestore_client.collection.return_value = collection_mock

    return mock_firestore_client


@pytest.fixture(scope="function")
def mock_firestore_user_budget(
    mock_firestore_client,
    mock_firestore_document_reference,
    mock_firestore_collection_reference,
    mock_firestore_document_snapshot,
):
    document_mock = mock_firestore_document_reference
    collection_mock = mock_firestore_collection_reference
    document_snapshot_mock = mock_firestore_document_snapshot

    document_snapshot_mock.to_dict.return_value = BUDGET_JSON
    document_mock.get.return_value = document_snapshot_mock
    collection_mock.document.return_value = document_mock

    mock_firestore_client.collection.return_value = collection_mock

    return mock_firestore_client


@pytest.fixture(scope="function")
def mock_firestore_user_preferences(
    mock_firestore_client,
    mock_firestore_document_reference,
    mock_firestore_collection_reference,
    mock_firestore_document_snapshot,
):
    document_mock = mock_firestore_document_reference
    collection_mock = mock_firestore_collection_reference
    document_snapshot_mock = mock_firestore_document_snapshot

    document_snapshot_mock.to_dict.return_value = DOCUMENT_PREFERENCES
    document_mock.get.return_value = document_snapshot_mock
    collection_mock.document.return_value = document_mock

    mock_firestore_client.collection.return_value = collection_mock

    return mock_firestore_client


@pytest.fixture(scope="function")
def mock_firestore_categories_subcollection_with_document(
    mock_firestore_user_subcollection, mock_firestore_document_snapshot
):
    document_snapshot_mock = mock_firestore_document_snapshot
    document_snapshot_mock.to_dict.return_value = CATEGORY_DOCUMENT

    mock_firestore_user_subcollection.collection.document.collection.stream.return_value = [
        document_snapshot_mock
    ]
    return mock_firestore_user_subcollection


@pytest.fixture(scope="function")
def mock_firestore_subscriptions_subcollection_with_document(
    mock_firestore_user_subcollection, mock_firestore_document_snapshot
):
    document_snapshot_mock = mock_firestore_document_snapshot
    document_snapshot_mock.id = SUBSCRIPTION_ID
    document_snapshot_mock.to_dict.return_value = SUBSCRIPTION_DOCUMENT

    mock_firestore_user_subcollection.collection.document.collection.stream.return_value = [
        document_snapshot_mock
    ]
    return mock_firestore_user_subcollection


@pytest.fixture(scope="function")
def mock_firestore_subcollection_without_document(mocker, mock_firestore_client):
    document_mock = mocker.create_autospec(firestore_v1.document.DocumentReference)
    collection_mock = mocker.create_autospec(
        firestore_v1.collection.CollectionReference
    )

    subcollection_mock = mocker.create_autospec(
        firestore_v1.collection.CollectionReference
    )
    subcollection_document_mock = mocker.create_autospec(
        firestore_v1.document.DocumentReference
    )

    subcollection_document_mock.get.return_value = (
        firestore_v1.document.DocumentSnapshot(
            reference=subcollection_document_mock,
            data={},
            exists=False,
            read_time=None,
            create_time=None,
            update_time=None,
        )
    )

    subcollection_document_mock.collection.return_value = subcollection_mock
    subcollection_mock.document.return_value = subcollection_document_mock

    document_mock.collection.return_value = subcollection_mock
    collection_mock.document.return_value = document_mock

    mock_firestore_client.collection.return_value = collection_mock

    return mock_firestore_client


# Helper fixtures
@pytest.fixture(scope="function", autouse=True)
def mock_firestore_client(mocker):
    return mocker.patch("metadata.operations.DB", spec=firestore.Client)


@pytest.fixture(scope="function")
def mock_firestore_document_reference(mocker):
    return mocker.create_autospec(firestore_v1.document.DocumentReference)


@pytest.fixture(scope="function")
def mock_firestore_collection_reference(mocker):
    return mocker.create_autospec(firestore_v1.collection.CollectionReference)


@pytest.fixture(scope="function")
def mock_firestore_write_batch(mocker):
    return mocker.create_autospec(firestore_v1.WriteBatch)


@pytest.fixture(scope="function")
def mock_firestore_document_snapshot(mocker):
    document_snapshot = mocker.create_autospec(firestore_v1.document.DocumentSnapshot)
    document_snapshot.exists = True
    return document_snapshot


@pytest.fixture(scope="function")
def mock_firestore_user_subcollection(
    mock_firestore_client,
    mock_firestore_document_reference,
    mock_firestore_collection_reference,
    mock_firestore_document_snapshot,
    mock_firestore_write_batch,
):
    document_mock = mock_firestore_document_reference
    collection_mock = mock_firestore_collection_reference

    subcollection_mock = mock_firestore_collection_reference
    subcollection_document_mock = mock_firestore_document_reference

    document_snapshot_mock = mock_firestore_document_snapshot

    subcollection_document_mock.get.return_value = document_snapshot_mock
    subcollection_document_mock.collection.return_value = subcollection_mock

    subcollection_mock.document.return_value = subcollection_document_mock
    subcollection_mock.stream.return_value = [document_snapshot_mock]

    document_mock.collection.return_value = subcollection_mock
    collection_mock.document.return_value = document_mock

    mock_firestore_client.collection.return_value = collection_mock
    mock_firestore_client.batch.return_value = mock_firestore_write_batch

    return mock_firestore_client
