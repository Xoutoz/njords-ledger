import logging as log
import traceback
from uuid import uuid4
from google.cloud.bigquery.table import RowIterator as RowIterator
from google.api_core.exceptions import BadRequest
from google.cloud import bigquery
from analytics.query_builder import build_sql_query, build_transactional_query
from analytics.config import (
    DATASET_ID,
    TABLE_ID,
    SELECT_OPERATION,
    INSERT_OPERATION,
    UPDATE_OPERATION,
    DELETE_OPERATION
)


BQ = bigquery.Client()


def get_expenses(user_id: str, date_lower_bound: str, date_higher_bound: str) -> dict:
    """
    Retrieves expenses from BigQuery for a given user ID and date range.

    Args:
        user_id: The ID of the user whose expenses to retrieve.
        date_lower_bound: The lower bound of the date range to retrieve expenses for (inclusive).
        date_higher_bound: The upper bound of the date range to retrieve expenses for (inclusive).

    Returns:
        A dictionary containing the following information about the expenses:

            * job_id: The ID of the query job.
            * state: The state of the query job, such as `SUCCESS` or `ERROR`.
            * labels: The labels associated with the query job.
            * result: The results in a pyarrow.Table object of the query job, if the query job 
            completed successfully.
    """

    sql_query = build_sql_query(
        DATASET_ID,
        TABLE_ID,
        statement=SELECT_OPERATION,
        fields=["id", "date", "description", "price", "category", "is_subscription"],
        where=[
            {
                "field": "date",
                "operator": "BETWEEN",
                "value": [date_lower_bound, date_higher_bound]
            },
            {
                "field": "owner",
                "operator": "=", "value": user_id
            },
        ],
        order=[
            {
                "field": "date"
            },
            {
                "field": "category"
            }
        ]
    )

    return run_query_job(sql_query, build_bigquery_job_config(user_id))


def add_expense(user_id: str, expense: dict | list) -> dict:
    """
    Adds one or more expenses to BigQuery for a given user ID.

    Args:
        user_id: The ID of the user to add expenses for.
        expense: A dictionary or list of dictionaries containing the expense data. Each expense must have the following keys:

            * date: The date of the expense.
            * description: A description of the expense.
            * price: The price of the expense.
            * is_subscription: If the expense is subscription.
            * category: The category of the expense.

    Returns:
        A dictionary containing the following information about the inserted expenses:

            * job_id: The ID of the query job.
            * state: The state of the query job, such as `SUCCESS` or `ERROR`.
            * labels: The labels associated with the query job.
    """

    if isinstance(expense, list) and len(expense) > 1:
        insert_queries = []
        for element in expense:
            fields = ["id"]
            values = [uuid4().hex]

            for field in list(element.keys()):
                fields.append(field)
            
            for value in list(element.values()):
                values.append(value)

            fields.append("owner")            
            values.append(user_id)

            insert_queries.append(build_sql_query(
                DATASET_ID,
                TABLE_ID,
                statement=INSERT_OPERATION,
                fields=fields,
                values=values
            ))
        
        sql_query = build_transactional_query(insert_queries)
    
    else:
        expense_keys = expense.keys() if isinstance(expense, dict) else expense[0].keys()
        expense_values = expense.values() if isinstance(expense, dict) else expense[0].values()

        fields = ["id"]
        values = [uuid4().hex]

        for field in list(expense_keys):
            fields.append(field)

        for value in list(expense_values):
            values.append(value)

        fields.append("owner")
        values.append(user_id)

        sql_query = build_sql_query(
            DATASET_ID,
            TABLE_ID,
            statement=INSERT_OPERATION,
            fields=fields,
            values=values
        )

    return run_query_job(sql_query, build_bigquery_job_config(user_id))


def update_expense(user_id: str, expense_id: str | list, expense_changes: dict | list) -> dict:
    """
    Updates one or more expenses in BigQuery for a given user ID.

    Args:
        user_id: The ID of the user to update expenses for.
        expense_id: The ID of the expense to update, or a list of IDs of expenses to update.
        expense_changes: A dictionary or list of dictionaries containing the expense changes.

    Returns:
        A dictionary containing the following information about the updated expenses:

            * job_id: The ID of the query job.
            * state: The state of the query job, such as `SUCCESS` or `ERROR`.
            * labels: The labels associated with the query job.
    """

    # expense_changes and expense_id must have the same size
    if isinstance(expense_changes, list) and len(expense_changes) > 1 \
        and isinstance(expense_id, list) and len(expense_id) > 1:
        update_queries = []

        for index, expense in enumerate(expense_changes):
            fields_to_update = [{"field": key, "value": value} for key, value in expense.items()]

            update_queries.append(build_sql_query(
                DATASET_ID,
                TABLE_ID,
                statement=UPDATE_OPERATION,
                set = fields_to_update,
                where=[
                    {
                        "field": "id",
                        "operator": "=",
                        "value": expense_id[index]
                    }
                ]
            ))
            
        sql_query = build_transactional_query(update_queries)

    elif (isinstance(expense_changes, dict) or (isinstance(expense_changes, list) and len(expense_changes) == 1)) \
        and (isinstance(expense_id, str) or (isinstance(expense_id, list) and len(expense_id) == 1)):
        expense = expense_changes.items() if isinstance(expense_changes, dict) else expense_changes[0].items()
        fields_to_update = [{"field": key, "value": value} for key, value in expense]

        sql_query = build_sql_query(
            DATASET_ID,
            TABLE_ID,
            statement=UPDATE_OPERATION,
            set = fields_to_update,
            where=[
                {
                    "field": "id",
                    "operator": "=",
                    "value": expense_id if isinstance(expense_id, str) else expense_id[0]
                }
            ]
        )
    else:
        return

    return run_query_job(sql_query, build_bigquery_job_config(user_id))


def delete_expense(user_id: str, expense_id: str | list) -> dict:
    """
    Deletes one or more expenses from BigQuery for a given user ID.

    Args:
        user_id: The ID of the user to delete expenses for.
        expense_id: The ID of the expense to delete, or a list of IDs of expenses to delete.

    Returns:
        A dictionary containing the following information about the deleted expenses:

            * job_id: The ID of the query job.
            * state: The state of the query job, such as `SUCCESS` or `ERROR`.
            * labels: The labels associated with the query job.
    """

    ids_to_remove = {
        "field": "id",
        "operator": "IN" if isinstance(expense_id, list) else "=",
        "value": expense_id
    }
    
    sql_query = build_sql_query(
        DATASET_ID,
        TABLE_ID,
        statement=DELETE_OPERATION,
        where=ids_to_remove
    )

    return run_query_job(sql_query, build_bigquery_job_config(user_id))


def run_query_job(query: str, query_job_config: bigquery.QueryJobConfig) -> dict:
    """
    Runs a BigQuery query job.

    Args:
        query: The BigQuery query to run.
        query_job_config: A BigQuery query job configuration object.

    Returns:
        A dictionary containing the following information about the query job:

            * job_id: The ID of the query job.
            * state: The state of the query job, such as `SUCCESS` or `ERROR`.
            * labels: The labels associated with the query job.
            * result: The results in a pyarrow.Table object of the query job, 
            if the query job is a SELECT query and the query job completed successfully.

    Example usage:

    ```python
    import bigquery

    query = SELECT
      name,
      SUM(price) AS total_price
    FROM
      `project.dataset.table`
    GROUP BY
      name
    ORDER BY
      total_price DESC

    query_job_config = bigquery.QueryJobConfig()
    query_job_config.destination = bigquery.TableReference(project="my-project", 
        dataset="my-dataset", table_id="my-table")

    query_job_result = run_query_job(query, query_job_config)

    if query_job_result["state"] == "SUCCESS":
        results = query_job_result["result"]
    else:
        # Handle the error.
        pass
    ```
    """

    job = BQ.query(query, job_config=query_job_config)

    try:
        result = job.result()
        state = "SUCCESS"

    except BadRequest as err:
        log.error("BigQuery query job failed: %s", err.message)
        log.error(traceback.format_exc())

        result = None
        state = "ERROR"

    output = {
        "job_id": job.job_id,
        "state": state,
        "labels": job.labels
    }

    if result and job.statement_type == "SELECT":
        output["result"] = result.to_arrow()
    return output


def build_bigquery_job_config(user_id: str) -> bigquery.QueryJobConfig:
    """Builds a BigQuery job configuration.

    Returns:
    A bigquery.QueryJobConfig object.
    """

    return bigquery.QueryJobConfig(
        use_query_cache=True,
        labels={ "user": user_id }
    )
