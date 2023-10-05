from hashlib import md5
from google.cloud import firestore


# String constants
DOCUMENT_ID = "document id"
COLLECTION = "COLLECTION"
SUB_COLLECTION = "SUB-COLLECTION"
CATEGORY_NAME = "category"

DESCRIPTION = "this is a test"
SUBSCRIPTION_ID = md5(DESCRIPTION.encode()).hexdigest()
OLD_SUBSCRIPTION_ID = md5(f"{DESCRIPTION} - old".encode()).hexdigest()


# Input constants
CATEGORY_INPUT_JSON = {
    "name": "Health"
}
SUBSCRIPTION_ALL_REQUIRED_JSON = {
    "category": "Entertainment",
    "description": "Disney+",
    "price": 13.99,
    "type": "month",
    "renewalDate": "01"
}
SUBSCRIPTION_JSON = (
    {"category": "Entertainment"},
    {"price": 13.99},
    {"description": "Disney+"}
)


# Firestore document constants
CATEGORY_DOCUMENT = {
    "name": CATEGORY_NAME,
    "lastModifiedTimestamp": firestore.SERVER_TIMESTAMP
}
SUBSCRIPTION_DOCUMENT = {
    "description": DESCRIPTION
}
UPDATE_SUBSCRIPTION_DOCUMENT = {
    "category": CATEGORY_NAME
}
LISTED_SUBSCRIPTION_DOCUMENT = [{
    f"{SUBSCRIPTION_ID}": {
        "description": DESCRIPTION
    }
}]


## Invalid input constants
INVALID_CATEGORY = "C4r"
INVALID_CATEGORY_JSON = {
    "invalid-key": "Health"
}
INVALID_SUBSCRIPTION = "invalid-id"
INVALID_SUBSCRIPTION_JSON = {
    "invalidField": "invalidValue"
}
