
#import cleaning_functions as cfun


import pandas as pd
import re
import numpy as np

# VERSION 1.1 - FUNCTIONS AVAILABLE :
#     drop_nan_rows
#     value_snake_case
#     clean_column_names
#     drop_columns
#     drop_columns_with_url
#     replace_organisation_size
#     clean_country_column
#     (NEW) convert_ransom_cost_to_numeric
#     (NEW) ensure_numeric_finite


# VERSION 1.0 :
#     drop_nan_rows
#     value_snake_case
#     clean_column_names
#     drop_columns
#     drop_columns_with_url
#     replace_organisation_size
#     clean_country_column
#     (modified in 1.1) transform_costs 
    

#################################################
def drop_nan_rows(dataframe, columns):
    """
    Drop rows from a DataFrame where specified columns contain NaNs.

    Parameters:
    dataframe (pd.DataFrame): The DataFrame to be modified.
    columns (str or list): The column(s) to check for NaNs.

    Returns:
    pd.DataFrame: A DataFrame with rows containing NaNs in specified columns removed.
    
    Example :
    df = drop_nan_rows(df,['description '])
    """

    # Ensure columns is a list
    if isinstance(columns, str):
        columns = [columns]

    # Drop rows with NaNs in specified columns
    cleaned_dataframe = dataframe.dropna(subset=columns)

    return cleaned_dataframe

#################################################
def value_snake_case(dataframe, columns):
    """
    Convert all values in specified column(s) of a DataFrame to snake case.

    Parameters:
    dataframe (pd.DataFrame): The dataFrame to be modified.
    columns (str or list): The column whose values are to be comverted. Can be a single column or a list.

    Returns:
    pd.DataFrame: A DataFrame with the values in specified columns converted tosnake case.
    
    Examples :
    df = value_snake_case(df, 'column_name') 
    df = value_snake_case(df, ['column1', 'column2', 'column3']) 
    """

    # Ensure columns is a list
    if isinstance(columns, str):
        columns = [columns]

    # Function to convert a string to snake case
    def convert_to_snake_case(s):
        # Replace all non-word characters (except spaces) with ''
        s = re.sub(r'[^\w\s]', '', s)
        # Replace all spaces and underscores with a single underscore
        s = re.sub(r'[\s_]+', '_', s.lower())
        return s

    # Apply the conversion to each specified column
    for col in columns:
        if col in dataframe.columns:
            dataframe[col] = dataframe[col].astype(str).apply(convert_to_snake_case)

    return dataframe

#################################################
def clean_column_names(df):
    """
    Cleans column names of a DataFrame by converting to lowercase, replacing spaces with underscores,
    and removing special characters and symbols.
    
    Parameters:
    df (DataFrame): The input DataFrame
    
    Returns:
    DataFrame: The DataFrame with cleaned column names
    
    exemple:
    df = clean_column_names(df)
    """
    
    # Convert column names to lowercase
    lowercase = lambda x: x.lower()
    df = df.rename(columns=lowercase)
    
    # Replace spaces with underscores in column names
    replace_func = lambda x: x.replace(' ', '_')
    df = df.rename(columns=replace_func)
    
    # Remove special characters and symbols from column names
    pattern = r"[^\w\s]"
    df.columns = [re.sub(pattern, '', col) for col in df.columns]
    
    return df

#################################################
def drop_columns(df, columns_to_drop):
    """
    Drops the specified columns from a DataFrame.
    
    Parameters:
    df (DataFrame): The input DataFrame
    columns_to_drop (list): A list of column names to be dropped
    
    Returns:
    DataFrame: The DataFrame with the specified columns dropped
    
    Example:
    df = drop_columns(df,'description ')
    """
    
    # Drop the specified columns from the DataFrame
    df = df.drop(columns=columns_to_drop)
    
    return df

#################################################
def replace_organisation_size(df, column_name):
    """
    Replaces values in a specified column with labels 'small', 'medium', 'large'.
    
    Parameters:
    df: The input DataFrame
    column_name (str): The name of the column to apply replacements
    
    Returns:
    DataFrame: The DataFrame with replaced values in the specified column
    
    Example:
    
    df = replace_organisation_size(df, 'organisation_size')
    
    """
    
    # Create a dictionary to define the replacements
    replacement_dict = {
        1: 'small',
        5: 'small',
        10: 'medium',
        25: 'medium',
        100: 'large',
        300: 'large'
    }
    
    # Check if the specified column exists in the dataframe
    if column_name in df.columns:
        # Replace values in the specified column using the dictionary
        df[column_name] = df[column_name].map(replacement_dict)
    else:
        raise ValueError(f"Column '{column_name}' not found in DataFrame")

    return df

#################################################
def clean_country_column(dataframe, column_name):
    """
    Clean up a country column in a DataFrame.

    Parameters:
    dataframe (pd.DataFrame): The DataFrame to be modified.
    column_name (str): The name of the column containing country information.

    Returns:
    pd.DataFrame: A DataFrame with a cleaned country column.
    
    Exemple:
    df = clean_country_column(df, 'location')
    """

    def clean_country(value):
        # Convert to snake case
        def to_snake_case(s):
            s = re.sub(r'[^\w\s]', '', s)  # Remove special char
            s = re.sub(r'[\s_]+', '_', s.lower())  # Replace spaces/underscores
            return s

        # Check for multiple countries
        if ',' in value:
            parts = value.split(',')
            # More than one country
            if len(parts) > 2:
                return 'multiple_countries'
            else:
                # Assume last part is the country
                return to_snake_case(parts[-1].strip())

        # Single country
        return to_snake_case(value)

    if column_name in dataframe.columns:
        dataframe[column_name] = dataframe[column_name].astype(str).apply(clean_country)

    return dataframe
#################################################

def convert_ransom_cost_to_numeric(df, column):
    """
    Converts the values within the specified column of a DataFrame to numbers.
    
    Parameters:
    df (DataFrame): The input DataFrame
    column (str): The name of the column to convert
    
    Returns:
    DataFrame: The DataFrame with the converted values in the specified column
    """
    
    # Convert the values in the column to numeric
    df[column] = pd.to_numeric(df[column], errors='coerce')
    # Convert values to millions off dollars
    df[column] = df[column] * 1000000

    return df


#################################################

def ensure_numeric_finite(df, column):
    """
    Ensure that the values in the specified column of the DataFrame are numeric and finite.

    Parameters:
    df : The DataFrame to be modified.
    column (str): The column to be checked and transformed.

    Returns:
    pd.DataFrame: The DataFrame with the transformed column.
    """

    # Convert the column to numeric
    df[column] = pd.to_numeric(df[column], errors='coerce')

    # Now that the column is numeric, apply np.isfinite
    finite_mask = np.isfinite(df[column])

    return df

#              | |
#              | |===( )   //////
#              |_|   |||  | o o|
#                     ||| ( c  )                  ____
#                      ||| \= /                  ||   \_
#                       ||||||                   ||     |
#                       ||||||                ...||__/|-"
#                       ||||||             __|________|__
#                         |||             |______________|
#                         |||             || ||      || ||
#                         |||             || ||      || ||
# ------------------------|||-------------||-||------||-||-------
#                         |__>            || ||      || ||


#      hit any key to continue


