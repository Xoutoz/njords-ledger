"""Functions to interact with Firestore database."""

from copy import deepcopy as copy
from hashlib import md5

from google.cloud import firestore, firestore_v1

from metadata.config import (
    CATEGORIES_COLLECTION,
    SUBSCRIPTIONS_COLLECTION,
    USERS_COLLECTION,
)

## Firestore Client
DB = firestore.Client()


def user_exists(user_id: str) -> bool:
    """Check whether a user with the specified ID exists in the database.

    Args:
        user_id (str): The ID of the user to check.

    Returns
    -------
        bool: True if the user exists, False otherwise.
    """
    return document_exists(get_collection(), user_id)


def category_exists(user_id: str, category_name: str) -> bool:
    """Check if a category with the given name exists for the specified user.

    Args:
        user_id (str): The ID of the user to check for.
        category_name (str): The name of the category to check for.

    Returns
    -------
        bool: True if the category exists, False otherwise.
    """
    return document_exists(get_categories_collection(user_id), category_name.lower())


def subscription_exists(user_id: str, subscription: str | dict) -> bool:
    """Check if a subscription exists for a given user.

    Args:
        user_id (str): The ID of the user to check for subscriptions.
        subscription (str | dict): The subscription to check for. If a string is
            provided, it is assumed to be the subscription ID. If a dictionary is
            provided, it is assumed to be a subscription object and the subscription
            ID will be generated from the description.

    Returns
    -------
        bool: True if the subscription exists, False otherwise.
    """
    match subscription:
        case str():
            return document_exists(get_subscriptions_collection(user_id), subscription)
        case dict():
            return document_exists(
                get_subscriptions_collection(user_id),
                generate_subscription_id(subscription["description"]),
            )
        case _:
            return False


def document_exists(
    collection: firestore_v1.collection.CollectionReference, document_id: str
) -> bool:
    """Check whether a document exists in a Firestore collection.

    Args:
        collection: The Firestore collection reference.
        document_id: The ID of the document to check.

    Returns
    -------
        True if the document exists, False otherwise.
    """
    return collection.document(document_id).get([]).exists


def list_categories(user_id: str) -> list:
    """List all categories for a given user.

    Args:
        user_id (str): The ID of the user.

    Returns
    -------
        list: A list of category names.
    """
    return [
        document.to_dict()["name"]
        for document in get_categories_collection(user_id).stream()
    ]


def list_subscriptions(user_id: str) -> list:
    """List all subscriptions for a given user.

    Args:
        user_id (str): The ID of the user to list subscriptions for.

    Returns
    -------
        list: A list of subscriptions, where each subscription is a dictionary
        containing the subscription ID and the subscription data.
    """
    return [
        {document.id: document.to_dict()}
        for document in get_subscriptions_collection(user_id).stream()
    ]


def get_budget(user_id: str) -> dict:
    """Get user's budget.

    Args:
        user_id: The ID of the user to get the budget for.

    Returns
    -------
        dict: A dictionary containing the user's budget.
    """
    return get_collection().document(user_id).get(["budget"]).to_dict()


def get_user_preferences(user_id: str) -> dict:
    """Retrieve the preferences for a given user.

    Args:
    user_id : The ID of the user whose preferences to retrieve.

    Returns
    -------
    dict
        A dictionary containing the user's preferences.
    """
    return {
        key: value
        for key, value in get_collection()
        .document(user_id)
        .get(["preferences"])
        .to_dict()["preferences"]
        .items()
    }


def create_category(user_id: str, category_name: str) -> str:
    """Add a new category to the user's collection.

    Args:
        user_id: The ID of the user to add the category to.
        category_name: The name of the category to add.

    Returns
    -------
        The name of the newly created category.
    """
    get_categories_collection(user_id).document(category_name.lower()).set(
        build_category_document(category_name)
    )
    return category_name


def create_subscription(user_id: str, subscription: dict) -> str:
    """Create a new subscription for the specified user.

    Args:
        user_id (str): The ID of the user to create the subscription for.
        subscription (dict): The subscription data.

    Returns
    -------
        str: The ID of the newly created subscription.
    """
    document_id = generate_subscription_id(subscription["description"])
    get_subscriptions_collection(user_id).document(document_id).set(subscription)
    return document_id


def set_budget(user_id: str, value: float) -> None:
    """Update the budget for the specified user.

    Args:
        user_id (str): The ID of the user to update.
        value (float): The new budget value.
    """
    get_collection().document(user_id).update({"budget": value})


def set_user_preferences(user_id: str, preferences: dict) -> None:
    """Update the user preferences in the database.

    Args:
        user_id (str): The ID of the user whose preferences are being updated.
        preferences (dict): The new preferences for the user.
    """
    get_collection().document(user_id).update({"preferences": preferences})


def update_category(
    user_id: str, old_category_name: str, new_category_name: str
) -> str:
    """Update a user's category by renaming the existing category with a new name.

    Args:
        user_id (str): The ID of the user whose category is being updated.
        old_category_name (str): The name of the category that is being renamed.
        new_category_name (str): The new name for the category.

    Returns
    -------
        str: The new category name.
    """
    # Create a batch
    batch = DB.batch()

    # Create new category
    new_category_ref = get_categories_collection(user_id).document(
        new_category_name.lower()
    )
    batch.set(new_category_ref, build_category_document(new_category_name))

    # Delete old category
    old_category_ref = get_categories_collection(user_id).document(
        old_category_name.lower()
    )
    batch.delete(old_category_ref)

    batch.commit()
    return new_category_name


def update_subscription(user_id: str, subscription_id: str, data: dict) -> str:
    """Update an existing subscription.

    Args:
        user_id (str): The ID of the user owning the subscription.
        subscription_id (str): The ID of the subscription to update.
        data (dict): The updated subscription data.

    Returns
    -------
        str: The new subscription ID if the description was changed,
        otherwise the original subscription ID.
    """
    if (
        "description" in data
        and generate_subscription_id(data["description"]) != subscription_id
    ):
        # Generate subscription ID
        new_subscription_id = generate_subscription_id(data["description"])

        # Get stored document
        old_subscription_ref = get_subscriptions_collection(user_id).document(
            subscription_id
        )
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
        new_subscription_ref = get_subscriptions_collection(user_id).document(
            new_subscription_id
        )
        batch.set(new_subscription_ref, new_subscription)

        # Delete old subscription
        old_subscription_ref = get_subscriptions_collection(user_id).document(
            subscription_id
        )
        batch.delete(old_subscription_ref)

        batch.commit()

        return new_subscription_id

    subscription_ref = get_subscriptions_collection(user_id).document(subscription_id)
    subscription_ref.update(data)

    return subscription_id


def remove_category(user_id: str, category_name: str) -> str:
    """Remove a category from the user's categories collection.

    Args:
        user_id (str): The ID of the user.
        category_name (str): The name of the category to remove.

    Returns
    -------
        str: The name of the category that was removed.
    """
    return remove_document(get_categories_collection(user_id), category_name.lower())


def remove_subscription(user_id: str, subscription_id: str) -> str:
    """Remove a subscription from a user.

    Args:
        user_id (str): The ID of the user.
        subscription_id (str): The ID of the subscription.

    Returns
    -------
        str: The ID of the removed subscription.
    """
    return remove_document(get_subscriptions_collection(user_id), subscription_id)


def remove_budget(user_id: str) -> None:
    """Remove the budget field from the user's document in the Firestore database.

    Args:
        user_id (str): The ID of the user whose budget should be removed.
    """
    get_collection().document(user_id).update({"budget": firestore.DELETE_FIELD})


def remove_document(
    collection: firestore_v1.collection.CollectionReference, document_id: str
) -> str:
    """Remove a document from a Firestore collection.

    Args:
        collection: The Firestore collection to remove the document from.
        document_id: The ID of the document to remove.

    Returns
    -------
        The ID of the removed document.
    """
    collection.document(document_id).delete()
    return document_id


def get_categories_collection(
    user_id: str,
) -> firestore_v1.collection.CollectionReference:
    """Retrieve the Firestore collection reference for a user's categories.

    Args:
        user_id (str): The unique identifier of the user.

    Returns
    -------
        firestore_v1.collection.CollectionReference: The Firestore collection reference
            for the user's categories.
    """
    return get_subcollection(user_id, CATEGORIES_COLLECTION)


def get_subscriptions_collection(
    user_id: str,
) -> firestore_v1.collection.CollectionReference:
    """Get the subscriptions collection reference for the given user.

    Args:
        user_id: The ID of the user to get the subscriptions collection for.

    Returns
    -------
        The subscriptions collection reference.
    """
    return get_subcollection(user_id, SUBSCRIPTIONS_COLLECTION)


def get_subcollection(
    user_id: str, collection_id: str
) -> firestore_v1.collection.CollectionReference:
    """Get a subcollection of a user's collection.

    Args:
        user_id (str): The ID of the user.
        collection_id (str): The ID of the collection.

    Returns
    -------
        firestore_v1.collection.CollectionReference: The subcollection.
    """
    return get_collection().document(user_id).collection(collection_id)


def get_collection() -> firestore_v1.collection.CollectionReference:
    """Get the Firestore collection reference for users.

    Returns
    -------
        The Firestore collection reference for users.
    """
    return DB.collection(USERS_COLLECTION)


# Helper functions
def build_category_document(category_name: str) -> dict:
    """Build a dictionary representing a category for storage in Firestore.

    Args:
        category_name (str): The name of the category.

    Returns
    -------
        dict: A dictionary representing the category.
    """
    return {"name": category_name, "lastModifiedTimestamp": firestore.SERVER_TIMESTAMP}


def generate_subscription_id(description: str) -> str:
    """Generate a unique subscription ID based on the provided description.

    Args:
        description (str): The description of the subscription.

    Returns
    -------
        str: The generated subscription ID.
    """
    return md5(description.encode(), usedforsecurity=False).hexdigest()
