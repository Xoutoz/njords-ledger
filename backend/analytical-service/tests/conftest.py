import pytest
import tests.constants as consts
import pyarrow as pa
import pyarrow.compute as pc
from google.cloud import bigquery
from analytics.server import app


# BigQuery fixtures
@pytest.fixture(scope="function")
def mock_bigquery_database(mocker):
    return mocker.patch("analytics.operations.BQ", spec=bigquery.Client)


@pytest.fixture(scope="function")
def mock_bigquery_run_query_job(mocker, mock_bigquery_database):
    query_job = mocker.create_autospec(bigquery.QueryJob)

    query_job.job_id = consts.JOB_ID
    query_job.labels = consts.JOB_LABELS

    mock_bigquery_database.query.return_value = query_job

    return mock_bigquery_database


@pytest.fixture(scope="function")
def mock_bigquery_run_query_table_job(mocker, mock_bigquery_database, mock_pyarrow_table):
    row_iterator = mocker.create_autospec(bigquery.table.RowIterator)
    query_job = mocker.create_autospec(bigquery.QueryJob)

    row_iterator.to_arrow.return_value = mock_pyarrow_table

    query_job.job_id = consts.JOB_ID
    query_job.labels = consts.JOB_LABELS
    query_job.statement_type = consts.SELECT_OPERATION.upper()

    query_job.result.return_value = row_iterator

    mock_bigquery_database.query.return_value = query_job

    return mock_bigquery_database


# PyArrow fixtures
@pytest.fixture(scope="function")
def mock_pyarrow_table():
    id = pa.array(consts.ID_LIST)
    date = pc.strptime(consts.DATE_LIST, format='%Y-%m-%d', unit='s')
    description = pa.array(consts.DESCRIPTION_LIST)
    price = pa.array(consts.PRICE_LIST)
    category = pa.array(consts.CATEGORY_LIST)
    is_subscription = pa.array(consts.IS_SUBSCRIPTION_LIST)

    return pa.Table.from_arrays(
        [id, date, description, price, category, is_subscription],
        names = consts.COLUMN_NAMES
    )


# Flask fixtures
@pytest.fixture(scope="function")
def flask_client():
    app.config['TESTING'] = True

    with app.app_context():
        with app.test_client() as client:
            yield client