import pytest
from analytics.process_query import (
    total_expenses,
    group_by_category,
    group_by_date,
    get_subscription_expenses_percentage,
    get_expenses_table
)
import tests.constants as consts


def test_total_expenses(mock_pyarrow_table):
    actual_value = round(total_expenses(mock_pyarrow_table).as_py(), 2)
    expected_value = round(sum(consts.PRICE_LIST), 2)

    assert actual_value == expected_value


def test_group_by_category(mock_pyarrow_table):
    actual_result = group_by_category(mock_pyarrow_table)
    
    expected_result = {
        "price": consts.GROUPED_BY_CAT_PRICE_LIST,
        "category": consts.GROUPED_BY_CAT_NAMES_LIST
    }
    
    assert actual_result == expected_result


@pytest.mark.parametrize("group_by, expected_result", [
    ("MONTH", {
        "date": [consts.GROUPED_BY_MONTHLY_DATE],
        "price": [sum(consts.PRICE_LIST)]
    }),
    ("DAY", {
        "date": consts.GROUPED_BY_DATE_NAMES_LIST,
        "price": consts.GROUPED_BY_DATE_PRICE_LIST
    })
])
def test_group_by_date(mock_pyarrow_table, group_by, expected_result):
    actual_result = group_by_date(mock_pyarrow_table, group_by)

    assert actual_result == expected_result


def test_get_subscription_expenses_percentage(mock_pyarrow_table):
    actual_result = get_subscription_expenses_percentage(mock_pyarrow_table)

    expected_result = {
        "price": consts.GROUPED_BY_SUB_PRICE_PERCENTAGE_LIST,
        "is_subscription": list(set(consts.IS_SUBSCRIPTION_LIST))
    }
    
    assert actual_result == expected_result


def test_get_expenses_table(mock_pyarrow_table):
    actual_result = get_expenses_table(mock_pyarrow_table)
    
    expected_result = [consts.COLUMN_NAMES]
    for idx in range(len(consts.ID_LIST)):
        expected_result.append([
            consts.ID_LIST[idx],
            consts.DATE_LIST[idx],
            consts.DESCRIPTION_LIST[idx],
            consts.PRICE_LIST[idx],
            consts.CATEGORY_LIST[idx],
            consts.IS_SUBSCRIPTION_LIST[idx],
        ])
    
    assert actual_result == expected_result