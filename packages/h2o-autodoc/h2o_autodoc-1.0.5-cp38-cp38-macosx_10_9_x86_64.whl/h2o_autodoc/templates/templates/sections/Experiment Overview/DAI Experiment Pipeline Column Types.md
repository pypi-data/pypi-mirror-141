Column types are detected and parsed based on the criteria shown in the table below. It is important that Driverless AI interprets the correct column types, because the column types dictate which feature transformations are applied.


{{section.table(
    columns=['Column Type', 'Description'],
    data=[
        ['ID', 'The ID column logic is one of the following: The column is named "id", "Id", "ID" or "iD" exactly. The column contains a significant number of unique values (above “max_relative_cardinality” in the config.toml file or above “Max. allowed fraction of uniques for integer and categorical cols” in the Expert Settings).'],
        ['Categorical', 'The column is a string or integer, with absolute number of unique values less than ' ~ "{:,}".format(config.get_dict().max_absolute_cardinality) ~ ' and fraction of unique values less than ' ~ config.get_dict().max_relative_cardinality ~ '.'],
        ['Numeric', 'A column which contains integers or real values. For an integer column to be considered numeric the unique integer count must be over ' ~ "{:,}".format(config.get_dict().max_int_as_cat_uniques) ~ '.'],
        ['Text', 'A column that contains more than a user-specified or default proportion of rows, which pass the text criteria (the text criteria is based on the number of words, the average word length, and the whole length of the string).'],
        ['Date', 'A column that can be converted to a date using the pandas python package.'],
        ['Date-time', 'A column that can be converted to date-time using the pandas python package.']
    ]
)}}

