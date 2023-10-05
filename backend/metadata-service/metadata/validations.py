"""a
"""

import re
from cerberus import Validator
from metadata.config import (
    CATEGORY_DOCUMENT_SCHEMA,
    SUBSCRIPTION_SCHEMAS,
    CATEGORY_REGEX,
    SUBSCRIPTION_ID_REGEX
)


def is_category_valid(category):
    match category:
        case str():
            return isinstance(category, str) and re.match(CATEGORY_REGEX, category)
        case dict():
            validator = Validator(CATEGORY_DOCUMENT_SCHEMA)
            return validator.validate(category)
        case _ :
            return False


def is_subscription_valid(subscription, is_all_required=False):
    match subscription:
        case str():
            return isinstance(subscription, str) and re.match(SUBSCRIPTION_ID_REGEX, subscription)
        case dict():
            validator = Validator(SUBSCRIPTION_SCHEMAS)
            if is_all_required:
                validator.require_all = True
            return validator.validate(subscription) and any(key for key in subscription.keys())
        case _ :
            return False
