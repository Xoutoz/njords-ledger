"""a

"""

from copy import deepcopy as copy
from hashlib import md5
from google.cloud import firestore
from metadata.config import (
    USERS_COLLECTION,
    CATEGORIES_COLLECTION,
    SUBSCRIPTIONS_COLLECTION
)


## Firestore Client
DB = firestore.Client()


def user_exists(user_id):
    return document_exists(get_collection(), user_id)

def category_exists(user_id, category_name):
    return document_exists(get_categories_collection(user_id), category_name.lower())

def subscription_exists(user_id, subscription):
    match subscription:
        case str():
            return document_exists(get_subscriptions_collection(user_id), subscription)
        case dict():
            return document_exists(get_subscriptions_collection(user_id),
                    generate_subscription_id(subscription["description"]))
        case _ :
            return False

def document_exists(collection, document_id):
    return collection.document(document_id).get([]).exists


def list_categories(user_id):
    return [document.to_dict()["name"] for document in get_categories_collection(user_id).stream()]

def list_subscriptions(user_id):
    return [{document.id: document.to_dict()} for document in get_subscriptions_collection(user_id).stream()]


def create_category(user_id, category_name):
    get_categories_collection(user_id) \
        .document(category_name.lower()) \
        .set(build_category_document(category_name))
    return category_name

def create_subscription(user_id, subscription):
    document_id = generate_subscription_id(subscription["description"])
    get_subscriptions_collection(user_id).document(document_id).set(subscription)
    return document_id


def update_category(user_id, old_category_name, new_category_name):
    # Create a batch
    batch = DB.batch()

    # Create new category
    new_category_ref = get_categories_collection(user_id).document(new_category_name.lower())
    batch.set(new_category_ref, build_category_document(new_category_name))

    # Delete old category
    old_category_ref = get_categories_collection(user_id).document(old_category_name.lower())
    batch.delete(old_category_ref)

    batch.commit()
    return new_category_name

def update_subscription(user_id, subscription_id, data):
    if "description" in data and generate_subscription_id(data["description"]) != subscription_id:
        # Generate subscription ID
        new_subscription_id = generate_subscription_id(data["description"])

        # Get stored document
        old_subscription_ref = get_subscriptions_collection(user_id).document(subscription_id)
        old_subscription_snapshot = old_subscription_ref.get()
        old_subscription_document = old_subscription_snapshot.to_dict()

        # Deep copy given input
        new_subscription = copy(data)

        # Add all missing fields
        for field in old_subscription_document.keys():
            if field not in data.keys():
                new_subscription[field] = old_subscription_document[field]

        # Create a batch
        batch = DB.batch()

        # Create new subscription
        new_subscription_ref = get_subscriptions_collection(user_id).document(new_subscription_id)
        batch.set(new_subscription_ref, new_subscription)

        # Delete old subscription
        old_subscription_ref = get_subscriptions_collection(user_id).document(subscription_id)
        batch.delete(old_subscription_ref)

        batch.commit()

        return new_subscription_id
    
    subscription_ref = get_subscriptions_collection(user_id).document(subscription_id)
    subscription_ref.update(data)

    return subscription_id


def remove_category(user_id, category_name):
    return remove_document(get_categories_collection(user_id), category_name.lower())

def remove_subscription(user_id, subscription_id):
    return remove_document(get_subscriptions_collection(user_id), subscription_id)

def remove_document(collection, document_id):
    collection.document(document_id).delete()
    return document_id


def get_categories_collection(user_id):
    return get_subcollection(user_id, CATEGORIES_COLLECTION)

def get_subscriptions_collection(user_id):
    return get_subcollection(user_id, SUBSCRIPTIONS_COLLECTION)

def get_subcollection(user_id, collection_id):
    return get_collection().document(user_id).collection(collection_id)

def get_collection():
    return DB.collection(USERS_COLLECTION)

# Helper functions
def build_category_document(category_name):
    return {
        "name": category_name,
        "lastModifiedTimestamp": firestore.SERVER_TIMESTAMP
    }

def generate_subscription_id(description):
    return md5(description.encode()).hexdigest()
