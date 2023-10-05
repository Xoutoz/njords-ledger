DATASET_ID = "dataset"
TABLE_ID   = "table"

SELECT_OPERATION = "select"
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