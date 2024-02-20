import pytest
from analytics.operations import (
    get_expenses,
    add_expense,
    update_expense,
    delete_expense,
    run_query_job,
    build_bigquery_job_config
)
from google.cloud import bigquery
import tests.constants as consts


def test_get_expenses(mock_bigquery_run_query_table_job, mock_pyarrow_table):
    """Tests the get_expenses function with a SELECT statement."""

    actual_result = get_expenses(consts.USER_ID, consts.DATE_LOWER_BOUND, consts.DATE_HIGHER_BOUND)

    expected_result = {
        "job_id": consts.JOB_ID,
        "state": "SUCCESS",
        "labels": consts.JOB_LABELS,
        "result": mock_pyarrow_table
    }
    assert actual_result == expected_result


@pytest.mark.parametrize("expense_changes", [
    (consts.EXPENSES),
    (consts.EXPENSES[0]),
    ([consts.EXPENSES[1]])
])
def test_add_expense(mock_bigquery_run_query_job, expense_changes):
    """Tests the add_expense function with an INSERT statement."""

    actual_result = add_expense(consts.USER_ID, expense_changes)

    expected_result = {
        "job_id": consts.JOB_ID,
        "state": "SUCCESS",
        "labels": consts.JOB_LABELS
    }
    assert actual_result == expected_result


@pytest.mark.parametrize("expense_ids, expense_changes", [
    (consts.ID_LIST, consts.EXPENSES),
    (consts.ID_LIST[0], consts.EXPENSES[0]),
    ([consts.ID_LIST[1]], [consts.EXPENSES[1]])
])
def test_update_expense(mock_bigquery_run_query_job, expense_ids, expense_changes):
    """Tests the update_expense function with an UPDATE statement."""

    actual_result = update_expense(consts.USER_ID, expense_ids, expense_changes)

    expected_result = {
        "job_id": consts.JOB_ID,
        "state": "SUCCESS",
        "labels": consts.JOB_LABELS
    }
    assert actual_result == expected_result


@pytest.mark.parametrize("expense_ids", [
    (consts.ID_LIST),
    (consts.ID_LIST[0]),
    ([consts.ID_LIST[1]])
])
def test_delete_expense(mock_bigquery_run_query_job, expense_ids):
    """Tests the delete_expense function with a DELETE statement."""

    actual_result = delete_expense(consts.USER_ID, expense_ids)

    expected_result = {
        "job_id": consts.JOB_ID,
        "state": "SUCCESS",
        "labels": consts.JOB_LABELS
    }
    assert actual_result == expected_result


def test_run_query_job(mock_bigquery_run_query_table_job, mock_pyarrow_table):
    """Tests the run_query_job function with a SELECT statement."""

    actual_result = run_query_job(consts.RUN_QUERY_JOB_QUERY, None)

    expected_result = {
        "job_id": consts.JOB_ID,
        "state": "SUCCESS",
        "labels": consts.JOB_LABELS,
        "result": mock_pyarrow_table
    }
    assert actual_result == expected_result


def test_build_bigquery_job_config():
    """Tests the build_bigquery_job_config."""

    actual_result = build_bigquery_job_config(consts.USER_ID)
    
    assert isinstance(actual_result, bigquery.QueryJobConfig)
    assert actual_result.use_query_cache == True
    assert actual_result.labels == { "user": consts.USER_ID }
