from hashlib import md5
from google.cloud import firestore


# String constants
DOCUMENT_ID = "document id"
COLLECTION = "collection"
SUB_COLLECTION = "sub-collection"
CATEGORY_NAME = "category"

DESCRIPTION = "description1"
NEW_DESCRIPTION = "description2"
SUBSCRIPTION_ID = md5(DESCRIPTION.encode()).hexdigest()
NEW_SUBSCRIPTION_ID = md5(NEW_DESCRIPTION.encode()).hexdigest()


# Input constants
CATEGORY_INPUT_JSON = {"name": CATEGORY_NAME}

SUBSCRIPTION_ALL_REQUIRED_JSON = {
    "category": CATEGORY_NAME,
    "description": DESCRIPTION,
    "price": 1.23,
    "type": "month",
    "renewalDate": "01",
}

NEW_SUBSCRIPTION_WITH_DESCRIPTION_JSON = {
    "category": CATEGORY_NAME,
    "description": NEW_DESCRIPTION,
    "price": 1.23,
}

NEW_SUBSCRIPTION_WITHOUT_DESCRIPTION_JSON = {"category": CATEGORY_NAME, "price": 1.23}

SUBSCRIPTION_JSON = (
    {"category": CATEGORY_NAME},
    {"price": 1.23},
    {"description": DESCRIPTION},
)


# Firestore document constants
CATEGORY_DOCUMENT = {
    "name": CATEGORY_NAME,
    "lastModifiedTimestamp": firestore.SERVER_TIMESTAMP,
}

SUBSCRIPTION_DOCUMENT = {"description": DESCRIPTION}

UPDATE_SUBSCRIPTION_DOCUMENT = {"category": CATEGORY_NAME}

LISTED_SUBSCRIPTION_DOCUMENT = [{f"{SUBSCRIPTION_ID}": {"description": DESCRIPTION}}]


# Invalid input constants
INVALID_CATEGORY = "category1"
INVALID_CATEGORY_JSON = {"invalid-key": CATEGORY_NAME}
INVALID_SUBSCRIPTION = "invalid-id"
INVALID_SUBSCRIPTION_JSON = {"category": CATEGORY_NAME, "invalidField": "invalidValue"}


# Endpoints constants
USER_ID = "test"
INEXISTENT_USER_ID = "id"
NEW_CATEGORY_NAME = CATEGORY_NAME + "-test"

BUDGET_JSON = {"budget": 123}

INVALID_BUDGET_JSON = {"invalid-key": 123}

PREFERENCES_JSON = {
    "colorPalette": "string",
    "defaultDateRange": "",
    "tableRange": 50,
    "timeSeries": "MONTH",
}

DOCUMENT_PREFERENCES = {
    "preferences": {
        "colorPalette": "string",
        "defaultDateRange": "",
        "tableRange": 50,
        "timeSeries": "MONTH",
    }
}

INVALID_PREFERENCES_JSON = {"invalid-key": "invalid-value"}
