DATASET_ID = "dataset"
TABLE_ID   = "table"

SELECT_OPERATION = "select"
INSERT_OPERATION = "insert"
UPDATE_OPERATION = "update"
DELETE_OPERATION = "delete"

# SET section
SET_LIST = [
    {
        "field": "date_col",
        "value": "YYYY-MM-DD"
    },
    {
        "field": "string_col",
        "value": "string"
    },
    {
        "field": "num_col",
        "value": 12.34
    }
]
SET = {
    "field": "string_col",
    "value": "string"
}

SET_LIST_RESULT = ' SET date_col = "YYYY-MM-DD", string_col = "string", num_col = 12.34'
SET_RESULT      = ' SET string_col = "string"'


# WHERE section
WHERE_LIST = [
    {
        "field": "date_col",
        "operator": "BETWEEN",
        "value": ["YYYY-MM-DD", "YYYY-MM-DD"]
    },
    {
        "field": "string_col",
        "operator": "LIKE","value": "D%"
    },
    {
        "field": "string_col2",
        "operator": "IN",
        "value": ["Foo", "Bar", "doe"]
    }
]
WHERE = {
    "field": "date_col",
    "operator": "BETWEEN",
    "value": ["YYYY-MM-DD","YYYY-MM-DD"]
}

WHERE_LIST_RESULT = ' WHERE date_col BETWEEN "YYYY-MM-DD" AND "YYYY-MM-DD" AND string_col LIKE "D%" AND string_col2 IN ("Foo", "Bar", "doe")'
WHERE_RESULT      = ' WHERE date_col BETWEEN "YYYY-MM-DD" AND "YYYY-MM-DD"'


# ORDER BY section
ORDER_BY_LIST = [
    {
        "field": "date_col",
        "sort": "DESC"
    },
    {
        "field": "string_col"
    }
]
ORDER_BY = {
    "field": "date_col",
    "sort": "DESC"
}

ORDER_BY_LIST_RESULT = " ORDER BY date_col DESC, string_col ASC"
ORDER_BY_RESULT      = " ORDER BY date_col DESC"


# GROUP BY section
GROUP_BY_LIST = ["string_col", "int_col"]
GROUP_BY      = "string_col"

GROUP_BY_LIST_RESULT = " GROUP BY string_col, int_col"
GROUP_BY_RESULT      = " GROUP BY string_col"


# SELECT statement
SELECT_FIELDS = ["date_col", "string_col", "int_col"]
SELECT_FIELD  = "int_col"

SELECT_FIELDS_RESULT = f"SELECT date_col, string_col, int_col FROM `{DATASET_ID}.{TABLE_ID}`"
SELECT_FIELD_RESULT  = f"SELECT int_col FROM `{DATASET_ID}.{TABLE_ID}`"

<<<<<<< Updated upstream
SELECT_FIELD_WHERE_LIST_RESULT = f"{SELECT_FIELD_RESULT}{WHERE_LIST_RESULT}"
SELECT_FIELD_WHERE_RESULT      = f"{SELECT_FIELD_RESULT}{WHERE_RESULT}"

SELECT_FIELD_ORDER_LIST_RESULT = f"{SELECT_FIELD_RESULT}{ORDER_BY_LIST_RESULT}"
SELECT_FIELD_ORDER_RESULT      = f"{SELECT_FIELD_RESULT}{ORDER_BY_RESULT}"

SELECT_FIELD_GROUP_LIST_RESULT = f"{SELECT_FIELD_RESULT}{GROUP_BY_LIST_RESULT}"
SELECT_FIELD_GROUP_RESULT      = f"{SELECT_FIELD_RESULT}{GROUP_BY_RESULT}"

UPDATE_SET_LIST_RESULT = f"UPDATE `{DATASET_ID}.{TABLE_ID}`{SET_LIST_RESULT}"
UPDATE_SET_RESULT      = f"UPDATE `{DATASET_ID}.{TABLE_ID}`{SET_RESULT}"

DELETE_WHERE_LIST_RESULT = f"DELETE FROM `{DATASET_ID}.{TABLE_ID}`{WHERE_LIST_RESULT}"
DELETE_WHERE_RESULT      = f"DELETE FROM `{DATASET_ID}.{TABLE_ID}`{WHERE_RESULT}"
=======
SELECT_FIELD_WHERE_LIST_RESULT = f"{SELECT_FIELD_RESULT}{WHERE_LIST_RESULT};"
SELECT_FIELD_WHERE_RESULT      = f"{SELECT_FIELD_RESULT}{WHERE_RESULT};"

SELECT_FIELD_ORDER_LIST_RESULT = f"{SELECT_FIELD_RESULT}{ORDER_BY_LIST_RESULT};"
SELECT_FIELD_ORDER_RESULT      = f"{SELECT_FIELD_RESULT}{ORDER_BY_RESULT};"

SELECT_FIELD_GROUP_LIST_RESULT = f"{SELECT_FIELD_RESULT}{GROUP_BY_LIST_RESULT};"
SELECT_FIELD_GROUP_RESULT      = f"{SELECT_FIELD_RESULT}{GROUP_BY_RESULT};"

# INSERT statement
INSERT_FIELDS = ["date_col", "string_col", "int_col"]
INSERT_FIELD  = "int_col"
INSERT_VALUES = ["YYYY-MM-DD", "string value", "0"]
INSERT_VALUE  = 0

INSERT_INTO_LIST_RESULT = f'INSERT INTO `{DATASET_ID}.{TABLE_ID}` ({", ".join(INSERT_FIELDS)}) VALUES ("YYYY-MM-DD", "string value", 0);'
INSERT_INTO_RESULT      = f"INSERT INTO `{DATASET_ID}.{TABLE_ID}` ({INSERT_FIELD}) VALUES ({INSERT_VALUE});"

# UPDATE statement 
UPDATE_SET_LIST_RESULT = f"UPDATE `{DATASET_ID}.{TABLE_ID}`{SET_LIST_RESULT};"
UPDATE_SET_RESULT      = f"UPDATE `{DATASET_ID}.{TABLE_ID}`{SET_RESULT};"

# DELETE statement
DELETE_WHERE_LIST_RESULT = f"DELETE FROM `{DATASET_ID}.{TABLE_ID}`{WHERE_LIST_RESULT};"
DELETE_WHERE_RESULT      = f"DELETE FROM `{DATASET_ID}.{TABLE_ID}`{WHERE_RESULT};"

# Transactional query
TRANSACTIONAL_QUERY_RESULT = f"""
BEGIN
BEGIN TRANSACTION;

{INSERT_INTO_LIST_RESULT}
{UPDATE_SET_LIST_RESULT}

COMMIT TRANSACTION;
END;"""


# Arrow columns
ID_LIST = ["id1", "id2", "id3", "id4"]
DATE_LIST = ["2000-01-02", "2000-01-05", "2000-01-02", "2000-01-08"]
DESCRIPTION_LIST = ["description1", "description2", "description3", "description4"]
PRICE_LIST = [1.23, 5.67, 8.76, 9.08]
CATEGORY_LIST = ["category1", "category2", "category1", "category3"]
IS_SUBSCRIPTION_LIST = [False, True, False, False]

GROUPED_BY_CAT_PRICE_LIST = [PRICE_LIST[0] + PRICE_LIST[2], PRICE_LIST[1], PRICE_LIST[3]]
GROUPED_BY_CAT_NAMES_LIST = [CATEGORY_LIST[0], CATEGORY_LIST[1], CATEGORY_LIST[3]]

GROUPED_BY_MONTHLY_DATE = "-".join(DATE_LIST[0].split("-")[:2])
GROUPED_BY_DATE_PRICE_LIST = [PRICE_LIST[0] + PRICE_LIST[2], PRICE_LIST[1], PRICE_LIST[3]]
GROUPED_BY_DATE_NAMES_LIST = ["-".join(DATE_LIST[0].split("-")[1:]), "-".join(DATE_LIST[1].split("-")[1:]), "-".join(DATE_LIST[3].split("-")[1:])]

GROUPED_BY_SUB_PRICE_PERCENTAGE_LIST = [
    round((PRICE_LIST[0] + PRICE_LIST[2] + PRICE_LIST[3]) / sum(PRICE_LIST) * 100),
    round(PRICE_LIST[1] / sum(PRICE_LIST) * 100)
]

COLUMN_NAMES = ["id", "date", "description", "price", "category", "is_subscription"]

# Default user ID
USER_ID = "john.doe@example.com"

# Operations contants
RUN_QUERY_JOB_QUERY  = f"SELECT * FROM `{DATASET_ID}.{TABLE_ID}`"
JOB_ID = "job_id"
JOB_LABELS = {
    "label1": "foo",
    "label2": "bar"
}

DATE_LOWER_BOUND = "2000-01-02"
DATE_HIGHER_BOUND = "2000-01-03"

EXPENSES = [
    {
        "date": "2000-01-02",
        "description": "description1",
        "price": 1.23,
        "category": "category1",
        "is_subscription": False
    },
    {
        "date": "2000-01-05",
        "description": "description2",
        "price": 5.67,
        "category": "category1",
        "is_subscription": True
    },
    {
        "date": "2000-01-02",
        "description": "description3",
        "price": 8.76,
        "category": "category1",
        "is_subscription": False
    },
    {
        "date": "2000-01-08",
        "description": "description4",
        "price": 9.08,
        "category": "category3",
        "is_subscription": False
    }
]
>>>>>>> Stashed changes
