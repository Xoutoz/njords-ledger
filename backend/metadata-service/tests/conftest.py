"""a
"""
import pytest
from tests.constants import (
    CATEGORY_DOCUMENT,
    SUBSCRIPTION_DOCUMENT,
    SUBSCRIPTION_ID
)
from google.cloud import firestore, firestore_v1
from flask import Flask

# Operations fixtures
@pytest.fixture(scope="function", autouse=True)
def mock_firestore_database(mocker, generate_generic_subcollection):
    firestore_mock = mocker.patch("metadata.operations.DB", spec=firestore.Client)    

    document_mock = mocker.create_autospec(firestore_v1.document.DocumentReference)
    collection_mock = mocker.create_autospec(firestore_v1.collection.CollectionReference)

    document_mock.collection.return_value = generate_generic_subcollection
    collection_mock.document.return_value = document_mock

    firestore_mock.collection.return_value = collection_mock    
    firestore_mock.batch.return_value = mocker.create_autospec(firestore_v1.WriteBatch)

    return firestore_mock


@pytest.fixture(scope="function")
def mock_firestore_list_subscriptions(mocker, mock_firestore_database, generate_subscription_snapshot):
    mock_firestore_database.collection.document.collection.stream.return_value = [ generate_subscription_snapshot ]
    return mock_firestore_database


@pytest.fixture(scope="function")
def mock_firestore_list_categories(mocker, mock_firestore_database, generate_category_snapshot):
    mock_firestore_database.collection.document.collection.stream.return_value = [ generate_category_snapshot ]
    return mock_firestore_database


@pytest.fixture(scope="function")
def generate_generic_subcollection(mocker, generate_document_snapshot):
    subcollection_mock = mocker.create_autospec(firestore_v1.collection.CollectionReference)
    document_mock = mocker.create_autospec(firestore_v1.document.DocumentReference)
    document_snapshot_mock = generate_document_snapshot

    document_mock.get.return_value = document_snapshot_mock
    document_mock.collection.return_value = subcollection_mock

    subcollection_mock.document.return_value = document_mock
    subcollection_mock.stream.return_value = [ document_snapshot_mock ]

    return subcollection_mock


@pytest.fixture(scope="function")
def generate_document_snapshot(mocker, get_document_snapshot_mock):
    document_snapshot_mock = get_document_snapshot_mock
    document_snapshot_mock.exists.return_value = True
    return document_snapshot_mock


@pytest.fixture(scope="function")
def generate_category_snapshot(mocker, get_document_snapshot_mock):
    document_snapshot_mock = get_document_snapshot_mock
    document_snapshot_mock.to_dict.return_value = CATEGORY_DOCUMENT
    return document_snapshot_mock


@pytest.fixture(scope="function")
def generate_subscription_snapshot(mocker, get_document_snapshot_mock):
    document_snapshot_mock = get_document_snapshot_mock
    document_snapshot_mock.id = SUBSCRIPTION_ID
    document_snapshot_mock.to_dict.return_value = SUBSCRIPTION_DOCUMENT
    return document_snapshot_mock


@pytest.fixture(scope="function")
def get_document_snapshot_mock(mocker):
    return mocker.create_autospec(firestore_v1.document.DocumentSnapshot)


# # Flask fixtures
# @pytest.fixture()
# def app():
#     app = create_app()
#     app.config.update({
#         "TESTING": True,
#     })

#     yield app


# @pytest.fixture()
# def client(app):
#     return app.test_client()


# @pytest.fixture()
# def runner(app):
#     return app.test_cli_runner()