import pyarrow
import pyarrow.compute as pc
import numpy as np


def total_expenses(table: pyarrow.Table) -> float:
    """Calculates the total expenses in a table.

    Args:
        table: A pyarrow.Table containing the expense data.

    Returns:
        The total expenses, rounded to two decimal places.
    """

    return pc.round(pc.sum(table.column("price")), ndigits=2)


def group_by_category(table: pyarrow.Table) -> dict:
    """Groups the expenses in a table by category.

    Args:
        table: A pyarrow.Table containing the expense data.

    Returns:
        A dictionary of expense totals by category, rounded to two decimal places.
    """

    result = table.group_by("category").aggregate([("price", "sum")])
    return result.set_column(
        result.column_names.index("price_sum"),
        "price",
        pc.round(result.column("price_sum"), ndigits=2)
    ).to_pydict()


def group_by_date(table: pyarrow.Table, group_by: str = "MONTH") -> dict:
    """Groups the expenses in a table by date.

    Args:
        table: A pyarrow.Table containing the expense data.
        group_by: The date grouping frequency, either "MONTH" or "DAY".

    Returns:
        A dictionary of expense totals by date, rounded to two decimal places.
    """

    date_format = ""
    match group_by.upper():
        case "MONTH":
            date_format = "%Y-%m"
        case "DAY":
            date_format = "%m-%d"

    result = table.set_column(
        table.column_names.index("date"), "date", pc.strftime(table.column("date"), date_format)
    )

    result = result.group_by("date").aggregate([("price", "sum")])

    return result.set_column(
        result.column_names.index("price_sum"),
        "price",
        pc.round(result.column("price_sum"), ndigits=2)
    ).to_pydict()


def get_subscription_expenses_percentage(table: pyarrow.Table) -> dict:
    """
    Calculates the percentage of subscription expenses in the given table.

    Args:
        table: A PyArrow table containing the expense data.

    Returns:
        A dictionary containing the subscription expenses percentage for each subscription type.
    """
    
    result = table.group_by("is_subscription").aggregate([("price", "sum")])
    percentage_col = pc.round(pc.multiply(pc.divide(result.column("price_sum"), total_expenses(table)), 100), ndigits=0)
    
    return result.set_column(result.column_names.index("price_sum"), "price", percentage_col).to_pydict()


def get_expenses_table(table: pyarrow.Table) -> list:
    """Generates a row format table of expenses.

    Args:
        table: A pyarrow.Table containing the expense data.

    Returns:
        A list of lists representing the expense table, with the first list containing the header row.
    """

    transformed_table = table.set_column(
        table.column_names.index("date"), "date", pc.strftime(table.column("date"), "%Y-%m-%d")
    )

    table_data = np.array([col.to_numpy() for col in transformed_table]).T
    table_headers = np.array([transformed_table.column_names])

    return np.vstack((table_headers, table_data)).tolist()
