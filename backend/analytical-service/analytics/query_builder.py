"""Genrate SQL queries with JSON-like data"""

import io


def generate_set_clause(input: list | dict) -> str:
    """Generates a SQL SET clause based on the input.

    Args:
        input: A list or dictionary of conditions, where each condition is a dictionary with the following keys:
            * field: The name of the field to set.
            * value: The value to set the field to.

    Returns:
        A string representing the SQL SET clause.

    Examples:
        >>> generate_set_clause([{"field": "name", "value": "Alice"}, {"field": "age", "value": 25}])
        ' SET name = "Alice", age = 25'

        >>> generate_set_clause({"field": "name", "value": "Alice"})
        ' SET name = "Alice"'
    """

    # Initialize the set_clause builder.
    set_clause_builder = io.StringIO()
    set_clause_builder.write(" SET ")

    # If the input is a list, iterate over the conditions and generate the SET clause.
    if isinstance(input, list):
        for condition in input:
            field = condition["field"]
            value = condition["value"]

            # Convert the value to a string if it is not an int, float, boolean, or numeric string.
            value = f'"{value}"' if isinstance(value, str) and not value.isnumeric() else value

            # Write the field=value pair to the set_clause builder.
            set_clause_builder.write(f'{field} = {value}')

            # Write a comma and space after the field=value pair if it is not the last element in the list.
            if condition != input[-1]:
                set_clause_builder.write(", ")

    # Otherwise, the input is a single condition, so generate the SET clause based on that condition.
    else:
        field = input["field"]
        value = input["value"]

        # Convert the value to a string if it is not an int, float, boolean, or numeric string.
        value = f'"{value}"' if isinstance(value, str) and not value.isnumeric() else value

        # Write the field=value pair to the set_clause builder.
        set_clause_builder.write(f'{field} = {value}')

    # Get the SET clause string from the StringBuilder.
    return set_clause_builder.getvalue()


def generate_where_clause(input: list | dict) -> str:
    """Generates a SQL WHERE clause based on the input.

    Args:
        input: A list of conditions, each of which is a dictionary with the following keys:
            * field: The name of the field to compare.
            * operator: The comparison operator, such as "=", "<", or ">".
            * value: The value to compare the field to.

    Returns:
        A string representing the SQL WHERE clause.

    Examples:
        >>> generate_where_clause([{"field": "name", "operator": "=", "value": "Alice"}, {"field": "age", "operator": ">", "value": 18}])
        ' WHERE name = "Alice" AND age > 18'

        >>> generate_where_clause({"field": "name", "value": "Alice"})
        ' WHERE name = "Alice"'
    """

    # Initialize the where_clause builder.
    where_clause_builder = io.StringIO()
    where_clause_builder.write(" WHERE ")

    # If the input is a list, iterate over the conditions and generate the WHERE clause.
    if isinstance(input, list):
        for condition in input:
            field    = condition["field"]
            operator = condition["operator"].upper()
            value    = condition["value"]

            # If the value is a list and the operator is IN, generate a SQL IN clause.
            if isinstance(value, list) and operator == "IN":
                sql_array = ""
                for element in value:
                    sql_array += f'"{element}"' if isinstance(element, str) and not element.isnumeric() else element
                    if element != value[-1]:
                        sql_array += ", "
                value = f"({sql_array})"

            # If the value is a list and the operator is BETWEEN, generate a SQL BETWEEN clause.
            elif isinstance(value, list) and operator == "BETWEEN":
                sql_between = ""
                for index, element in enumerate(value):
                    sql_between += f'"{element}"' if isinstance(element, str) and not element.isnumeric() else element
                    if index == 0:
                        sql_between += " AND "
                value = sql_between

            else:
                # Convert the value to a string if it is not an int, float, boolean, or numeric string.
                value = f'"{value}"' if isinstance(value, str) and not value.isnumeric() else value

            # Add the field=value pair to the where_clause builder. If the condition is not the last element in the list, add a comma and space.
            where_clause_builder.write(f'{field} {operator} {value}{" AND " if condition != input[-1] else ""}')
    
    # Otherwise, the input is a single condition, so generate the WHERE clause based on that condition.
    else:
        field    = input["field"]
        operator = input["operator"].upper()
        value    = input["value"]

        # If the value is a list and the operator is IN, generate a SQL IN clause.
        if isinstance(value, list) and operator == "IN":
            sql_array = ""
            for element in value:
                sql_array += f'"{element}"' if isinstance(element, str) and not element.isnumeric() else element
                if element != value[-1]:
                    sql_array += ", "
            value = f"({sql_array})"

        # If the value is a list and the operator is BETWEEN, generate a SQL BETWEEN clause.
        elif isinstance(value, list) and operator == "BETWEEN":
            sql_between = ""
            for index, element in enumerate(value):
                sql_between += f'"{element}"' if isinstance(element, str) and not element.isnumeric() else element
                if index == 0:
                    sql_between += " AND "
            value = sql_between

        else:
            # Convert the value to a string if it is not an int, float, boolean, or numeric string.
            value = f'"{value}"' if isinstance(value, str) and not value.isnumeric() else value
        
        # Add the field=value pair to the where_clause builder. If the condition is not the last element in the list, add a comma and space.
        where_clause_builder.write(f'{field} {operator} {value}')

    # Get the WHERE clause string from the StringBuilder.
    return where_clause_builder.getvalue()


def generate_order_by_clause(input: list | dict) -> str:
    """Generates a SQL ORDER BY clause based on the input.

    Args:
        input: A list or dictionary of conditions, where each condition is a dictionary with the following keys:
            * field: The name of the field to order by.
            * sort: The sort order, either "ASC" or "DESC".

    Returns:
        A string representing the SQL ORDER BY clause.
    
    Examples:
        >>> generate_order_by_clause([{"field": "name", "sort": "ASC"}, {"field": "age", "sort": "DESC"}])
        ' ORDER BY name ASC, age DESC'

        >>> generate_order_by_clause({"field": "name"})
        ' ORDER BY name ASC'
    """

    # Initialize the order_by_clause builder.
    order_by_clause_builder = io.StringIO()
    order_by_clause_builder.write(" ORDER BY ")

    # If the input is a list, iterate over the conditions and generate the ORDER BY clause.
    if isinstance(input, list):
        for condition in input:
            field = condition["field"]
            sort = condition["sort"].upper() if "sort" in condition.keys() else "ASC"
            order_by_clause_builder.write(f"{field} {sort}")

            # Write a comma and space after the ordered column if it is not the last element in the list.
            if condition != input[-1]:
                order_by_clause_builder.write(", ")

    # Otherwise, the input is a single condition, so generate the ORDER BY clause based on that condition.
    else:
        field = input["field"]
        sort = input["sort"].upper() if "sort" in input.keys() else "ASC"
        order_by_clause_builder.write(f"{field} {sort}")

    # Get the ORDER BY clause string from the StringBuilder.
    return order_by_clause_builder.getvalue()


def generate_group_by_clause(input: list | str) -> str:
    """Generates a SQL GROUP BY clause based on the input.

    Args:
        input: A list of fields to group by, or a single field to group by.

    Returns:
        A string representing the SQL GROUP BY clause.

    Examples:
        >>> generate_group_by_clause(["name", "age"])
        ' GROUP BY name, age'

        >>> generate_group_by_clause("name")
        ' GROUP BY name'
    """

    # Initialize the group_by_clause builder.
    group_by_clause_builder = io.StringIO()
    group_by_clause_builder.write(" GROUP BY ")

    # If the input is a list, join the fields with a comma and space.
    if isinstance(input, list):
        group_by_clause_builder.write(", ".join(input))

    # Otherwise, the input is a single field, so add it to the group_by_clause variable.
    else:
        group_by_clause_builder.write(f"{input}")

    # Get the GROUP BY clause string from the StringBuilder.
    return group_by_clause_builder.getvalue()


def build_sql_query(dataset_id: str, table_id: str, statement: str, **kwargs) -> str:
    """Builds a SQL query string.

    Args:
        dataset_id: The ID of the BigQuery dataset containing the table.
        table_id: The ID of the BigQuery table to query.
        statement: The type of SQL statement to perform, such as 'SELECT', 'INSERT', 'UPDATE', or 'DELETE'.
        **kwargs: A dictionary of keyword arguments, each of which is a string
            representing the name of a clause to add to the query. The value of each
            keyword argument is a list of arguments specific to the clause.

    Returns:
        A string representing the SQL query.
    """

    # Initialize the query builder.
    query_builder = io.StringIO()

    # Generate the basic query string.
    target    = f"`{dataset_id}.{table_id}`"
    statement = statement.upper()

    match statement:
        case "SELECT":
            fields = kwargs["fields"]
            fields_str = ", ".join(field for field in fields) if isinstance(fields, list) else fields
            query_builder.write(f'{statement} {fields_str} FROM {target}')
        case "INSERT":
            fields = kwargs["fields"]
            values = kwargs["values"]
            fields_str = ", ".join(field for field in fields) if isinstance(fields, list) else fields
            values_str = ", ".join(str(value) if not isinstance(value, str) else \
                                   # Apply quote marks to values that are not numeric or boolean
                                   f'"{value}"' if isinstance(value, str) and not value.isnumeric() else value \
                                    for value in values) if isinstance(values, list) else values
            query_builder.write(f'{statement} INTO {target} ({fields_str}) VALUES ({values_str})')
        case "UPDATE":
            query_builder.write(f'{statement} {target}')
        case "DELETE":
            query_builder.write(f'{statement} FROM {target}')
        case _:
            raise RuntimeError("Statement handler not implemented")

    # Add additional clauses to the query string.
    for key, arg in kwargs.items():

        match key.upper():
            # Add SET clause.
            case "SET":
                if arg:
                    query_builder.write(generate_set_clause(arg))
            
            # Add WHERE clause.
            case "WHERE":
                if arg:
                    query_builder.write(generate_where_clause(arg))

            # Add ORDER BY clause.
            case "ORDER":
                if arg:
                    query_builder.write(generate_order_by_clause(arg))

            # Add GROUP BY clause.
            case "GROUP":
                if arg:
                    query_builder.write(generate_group_by_clause(arg))

    # Get the SQL query string from the StringBuilder.
    query_builder.write(";")
    return query_builder.getvalue()


def build_transactional_query(queries: list) -> str:
    queries_str = "\n".join(queries)
    return f"""
BEGIN
BEGIN TRANSACTION;

{queries_str}

COMMIT TRANSACTION;
END;"""
