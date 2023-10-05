""" This script defines global variables that contain the names of the
Firestore collections and the schemas of the Firestore documents.
These variables are used for further validation of the data to be
stored in Firestore.
"""

## Firestore Collections
USERS_COLLECTION = "users"
CATEGORIES_COLLECTION = "categories"
SUBSCRIPTIONS_COLLECTION = "subscriptions"

## Regex
CATEGORY_REGEX = r"\b[a-zA-Z-]+\b"
SUBSCRIPTION_ID_REGEX = r"^[a-fA-F0-9]+$"
PRICE_REGEX = r"\d+.\d{1,2}"
TYPE_REGEX = r"(?i)month|(?i)year"
RENEWAL_DATE_REGEX = r"(0[1-9]|[12][0-9]|3[01])?(/(0[1-9]|1[1,2]))?"

## Firestore schemas
CATEGORY_DOCUMENT_SCHEMA = {
    "name": {
        "type": "string",
        "required": True,
        "regex": CATEGORY_REGEX
    }
}

SUBSCRIPTION_SCHEMAS = {
    "category": {
        "type": "string",
        "regex": CATEGORY_REGEX
    },
    "description": {
        "type": "string",
    },
    "price": {
        "type": "number",
        "regex": PRICE_REGEX
    },
    "type": {
        "type": "string",
        "regex": TYPE_REGEX
    },
    "renewalDate": {
        "type": "string",
        "regex": RENEWAL_DATE_REGEX
    }
}
