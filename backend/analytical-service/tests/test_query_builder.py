import pytest
from analytics.query_builder import (
    build_sql_query,
    build_transactional_query,
    generate_set_clause,
    generate_where_clause,
    generate_order_by_clause,
    generate_group_by_clause
)
import tests.constants as consts


@pytest.mark.parametrize("fields, where, order, group, expected_query", [
    (consts.SELECT_FIELDS, None, None, None, f"{consts.SELECT_FIELDS_RESULT};"),
    (consts.SELECT_FIELD, None, None, None, f"{consts.SELECT_FIELD_RESULT};"),
    (consts.SELECT_FIELD, consts.WHERE_LIST, None, None, consts.SELECT_FIELD_WHERE_LIST_RESULT),
    (consts.SELECT_FIELD, consts.WHERE, None, None, consts.SELECT_FIELD_WHERE_RESULT),
    (consts.SELECT_FIELD, None, consts.ORDER_BY_LIST, None, consts.SELECT_FIELD_ORDER_LIST_RESULT),
    (consts.SELECT_FIELD, None, consts.ORDER_BY, None, consts.SELECT_FIELD_ORDER_RESULT),
    (consts.SELECT_FIELD, None, None, consts.GROUP_BY_LIST, consts.SELECT_FIELD_GROUP_LIST_RESULT),
    (consts.SELECT_FIELD, None, None, consts.GROUP_BY, consts.SELECT_FIELD_GROUP_RESULT)
])
def test_build_sql_query_select(fields, where, order, group, expected_query):
    """Tests the build_sql_query function with a SELECT statement."""
    actual_query = build_sql_query(
        consts.DATASET_ID,
        consts.TABLE_ID,
        statement=consts.SELECT_OPERATION,
        fields=fields,
        where=where,
        order=order,
        group=group
    )

    assert actual_query == expected_query


@pytest.mark.parametrize("fields, values, expected_query", [
    (consts.INSERT_FIELDS, consts.INSERT_VALUES, consts.INSERT_INTO_LIST_RESULT),
    (consts.INSERT_FIELD, consts.INSERT_VALUE, consts.INSERT_INTO_RESULT)
])
def test_build_sql_query_insert(fields, values, expected_query):
    """Tests the build_sql_query function with an INSERT statement."""
    actual_query = build_sql_query(
        consts.DATASET_ID,
        consts.TABLE_ID,
        statement=consts.INSERT_OPERATION,
        fields=fields,
        values=values
    )

    assert actual_query == expected_query


@pytest.mark.parametrize("set, expected_query", [
    (consts.SET_LIST, consts.UPDATE_SET_LIST_RESULT),
    (consts.SET, consts.UPDATE_SET_RESULT)
])
def test_build_sql_query_update(set, expected_query):
    """Tests the build_sql_query function with a UPDATE statement."""
    actual_query = build_sql_query(
        consts.DATASET_ID,
        consts.TABLE_ID,
        statement=consts.UPDATE_OPERATION,
        set=set
    )

    assert actual_query == expected_query


@pytest.mark.parametrize("where, expected_query", [
    (consts.WHERE_LIST, consts.DELETE_WHERE_LIST_RESULT),
    (consts.WHERE, consts.DELETE_WHERE_RESULT)
])
def test_build_sql_query_delete(where, expected_query):
    """Tests the build_sql_query function with a DELETE statement."""
    actual_query = build_sql_query(
        consts.DATASET_ID,
        consts.TABLE_ID,
        statement=consts.DELETE_OPERATION,
        where=where
    )

    assert actual_query == expected_query


@pytest.mark.parametrize("queries, expected_query", [
    ([consts.INSERT_INTO_LIST_RESULT, consts.UPDATE_SET_LIST_RESULT], consts.TRANSACTIONAL_QUERY_RESULT)
])
def test_build_transactional_sql_query(queries, expected_query):
    """Tests the build_transactional_query function with a transaction query."""
    actual_query = build_transactional_query(queries)
    assert actual_query == expected_query


@pytest.mark.parametrize("set_fields, expected_result", [
    (consts.SET_LIST, consts.SET_LIST_RESULT),
    (consts.SET, consts.SET_RESULT)
])
def test_generate_set_clause(set_fields, expected_result):
    """Tests the generate_set_clause function."""

    actual_result = generate_set_clause(set_fields)

    assert actual_result == expected_result


@pytest.mark.parametrize("where_fields, expected_result", [
    (consts.WHERE_LIST, consts.WHERE_LIST_RESULT),
    (consts.WHERE, consts.WHERE_RESULT)
])
def test_generate_where_clause(where_fields, expected_result):
    """Tests the generate_where_clause function."""

    actual_result = generate_where_clause(where_fields)

    assert actual_result == expected_result


@pytest.mark.parametrize("order_fields, expected_result", [
    (consts.ORDER_BY_LIST, consts.ORDER_BY_LIST_RESULT),
    (consts.ORDER_BY, consts.ORDER_BY_RESULT)
])
def test_generate_order_by_clause(order_fields, expected_result):
    """Tests the generate_order_by_clause function."""

    actual_result = generate_order_by_clause(order_fields)

    assert actual_result == expected_result


@pytest.mark.parametrize("group_fields, expected_result", [
    (consts.GROUP_BY_LIST, consts.GROUP_BY_LIST_RESULT),
    (consts.GROUP_BY, consts.GROUP_BY_RESULT)
])
def test_generate_group_by_clause(group_fields, expected_result):
    """Tests the generate_group_by_clause function."""

    actual_result = generate_group_by_clause(group_fields)

    assert actual_result == expected_result
