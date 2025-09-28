#!/usr/bin/env python3

#===========================================================#
#File Name:			MCPserver.py
#Author:			Pedro Cumino
#Email:				pedro.cumino@gmail.com
#Creation Date:		Thu Sep 25 11:30:36 2025
#Last Modified:		Thu Sep 25 11:30:37 2025
#Description:
#Args:
#Usage:
#===========================================================#

from mcp.server.fastmcp import FastMCP
import json
import pandas as pd
import os
from typing import List, Dict, Any, Optional, Union, Annotated

# Global dataframe - loaded once at module level
CSV_FILE_PATH = "data/cars.csv"

if not os.path.exists(CSV_FILE_PATH):
    raise FileNotFoundError(f"CSV file not found: {CSV_FILE_PATH}")

df_cars = pd.read_csv(CSV_FILE_PATH)

mcp = FastMCP('CarServerMCP')

@mcp.tool()
def filter_cars_by_criteria(
    brand: Annotated[Optional[str], "Brand name filter"] = None,
    model: Annotated[Optional[str], "Model name filter"] = None,
    year_min: Annotated[Optional[int], "Minimum year"] = None,
    year_max: Annotated[Optional[int], "Maximum year"] = None,
    fuel_type: Annotated[Optional[str], "Fuel type filter"] = None,
    engine: Annotated[Optional[float], "Car engine size"] = None,
    color: Annotated[Optional[str], "Car color name"] = None,
    transmission: Annotated[Optional[str], "Transmission type filter"] = None,
    condition: Annotated[Optional[str], "Condition filter"] = None,
    min_mileage: Annotated[Optional[int], "Minimum mileage"] = None,
    max_mileage: Annotated[Optional[int], "Maximum mileage"] = None,
    min_doors: Annotated[Optional[int], "Minimum number of doors"] = None,
    max_doors: Annotated[Optional[int], "Maximum number of doors"] = None,
    limit: Annotated[Optional[int], "Maximum number of results"] = None
) -> List[Dict[str, Any]]:
    """
    Filter cars by {}.

    Use when the query includes multiple criteria at once (e.g., "Toyota 2020-2022 with automatic transmission").
    All conditions are combined with AND logic. Supports exact matches for strings and inclusive ranges for numbers.
    Returns a list of cars matching all filters, limited by the 'limit' parameter.
    """.format(' AND/OR '.join([i for i in df_cars.columns]))
    df = df_cars.copy()
    
    # Apply filters
    if brand:
        df = df[df['brand'].str.upper() == brand.upper()]
    if model:
        df = df[df['model'].str.upper() == model.upper()]
    if year_min:
        df = df[df['year'] >= year_min]
    if year_max:
        df = df[df['year'] <= year_max]
    if fuel_type:
        df = df[df['fuel'].str.upper() == fuel_type.upper()]
    if engine:
        df = df[df['engine'] == engine]
    if color:
        df = df[df['color'].str.upper() == color.upper()]
    if transmission:
        df = df[df['transmission'].str.upper() == transmission.upper()]
    if condition:
        df = df[df['condition'].str.upper() == condition.upper()]
    if min_mileage:
        df = df[df['mileage'] >= min_mileage]
    if max_mileage:
        df = df[df['mileage'] <= max_mileage]
    if min_doors:
        df = df[df['number_doors'] >= min_doors]
    if max_doors:
        df = df[df['number_doors'] <= max_doors]
    
    if limit:
        df = df.head(limit)
    
    res = df.to_dict('records')
    return [
        {str(k): v for k, v in record.items()}
        for record in res
    ]

# @mcp.tool()
# def get_car_by_id(
#     car_id: Annotated[str, "The unique identifier of the car"]
# ) -> Dict[str, Any]:
#     """Get complete car details by unique ID."""
#     car = df_cars[df_cars['id'] == car_id]
    
#     if car.empty:
#         return {}
    
#     return car.iloc[0].to_dict()


# @mcp.tool()
# def search_cars_by_brand(
#     brand: Annotated[str, "Brand name to search for (case-insensitive)"], 
#     limit: Annotated[Optional[int], "Maximum number of results to return"] = None
# ) -> List[Dict[str, Any]]:
#     """Find all cars from a specific brand name only."""
#     filtered_df = df_cars[df_cars['brand'].str.upper() == brand.upper()]
    
#     if limit:
#         filtered_df = filtered_df.head(limit)
    
#     res = filtered_df.to_dict('records')
#     return [
#         {str(k): v for k, v in record.items()}
#         for record in res
#     ]
    





@mcp.tool()
def get_car_statistics() -> Dict[str, Any]:
    """Return comprehensive dataset statistics and summary information."""
    
    stats = {
        'total_cars': len(df_cars),
        'brands': {
            'unique_count': df_cars['brand'].nunique(),
            'list': sorted(df_cars['brand'].unique().tolist())
        },
        'models': {
            'unique_count': df_cars['model'].nunique(),
            'most_common': df_cars['model'].value_counts().head(5).to_dict()
        },
        'years': {
            'min': int(df_cars['year'].min()),
            'max': int(df_cars['year'].max()),
            'average': round(df_cars['year'].mean(), 1)
        },
        'mileage': {
            'min': int(df_cars['mileage'].min()),
            'max': int(df_cars['mileage'].max()),
            'average': round(df_cars['mileage'].mean(), 0)
        },
        'fuel_types': df_cars['fuel'].value_counts().to_dict(),
        'transmissions': df_cars['transmission'].value_counts().to_dict(),
        'conditions': df_cars['condition'].value_counts().to_dict(),
        'doors': df_cars['number_doors'].value_counts().to_dict()
    }
    
    return stats


# @mcp.tool()
# def get_cars_by_condition(
#     condition_preference: Annotated[str, "Preferred condition (NOVO, SEMINOVO, USADO EXCELENTE, etc.)"] = "NOVO", 
#     exact_match: Annotated[bool, "Try to find the exact match or not"] = False
# ) -> List[Dict[str, Any]]:
#     """Filter cars by condition with exact or partial matching."""
#     mask = df_cars['condition'].str.upper().str.contains(condition_preference.upper(), na=False)
#     if exact_match:
#         mask = df_cars['condition'].str.upper() == condition_preference.upper()
#     res = df_cars[mask].to_dict('records')	
#     return [
#         {str(k): v for k, v in record.items()}
#         for record in res
#     ]



@mcp.tool()
def search_cars_by_keyword(
    keyword: Annotated[str, "Keyword to search for"],
    search_fields: Annotated[Optional[List[str]], "Fields to search in. If None, searches in brand, model, color"] = None, 
    limit: Annotated[Optional[int], "Maximum number of results to return"] = None
) -> List[Dict[str, Any]]:
    """Search cars by keyword across multiple fields with partial matching."""
    if search_fields is None:
        search_fields = [i for i in df_cars.columns]
    
    # Create a mask for keyword search
    mask = pd.Series([False] * len(df_cars))
    
    for field in search_fields:
        if field in df_cars.columns:
            mask |= df_cars[field].str.contains(keyword, case=False, na=False)
    
    filtered_df = df_cars[mask]
    if limit:
        filtered_df = filtered_df.head(limit)
    
    res = filtered_df.to_dict('records')
    return [
        {str(k): v for k, v in record.items()}
        for record in res
    ]


@mcp.tool()
def get_available_values(
    column: Annotated[str, "Column name to get unique values from"]
) -> List[str]:
    """Get all unique values from a specific column sorted alphabetically."""
    # Validate column exists
    if column not in df_cars.columns:
        return []
    
    # Get unique values, drop nulls, convert to string, and sort
    unique_values = df_cars[column].dropna().unique()
    
    # Convert all values to string for consistent return type and sort
    return sorted([str(value) for value in unique_values])


@mcp.tool()
def get_column_value_distribution(
    column: Annotated[str, "Column name to analyze value distribution"]
) -> Dict[str, Any]:
    """Analyze value distribution and frequency statistics for a specific column."""
    # Validate column exists
    if column not in df_cars.columns:
        return {}
    
    series = df_cars[column]
    value_counts = series.value_counts()
    
    # Basic statistics
    total_count = series.count()  # Non-null values
    unique_count = series.nunique()
    null_count = series.isnull().sum()
    
    # Most and least common values
    most_common = [str(value_counts.index[0]), int(value_counts.iloc[0])] if not value_counts.empty else ["N/A", 0]
    least_common = [str(value_counts.index[-1]), int(value_counts.iloc[-1])] if not value_counts.empty else ["N/A", 0]
    
    # Convert value counts to string keys for JSON serialization
    value_counts_dict = {str(k): int(v) for k, v in value_counts.to_dict().items()}
    
    # Infer data type
    data_type = str(series.dtype)
    
    return {
        'column_name': column,
        'total_count': int(total_count),
        'unique_count': int(unique_count),
        'null_count': int(null_count),
        'most_common': most_common,
        'least_common': least_common,
        'value_counts': value_counts_dict,
        'data_type': data_type
    }


@mcp.tool()
def get_dataset_columns() -> Dict[str, Any]:
    """Return dataset schema with column names, types, and sample values."""
    total_rows = len(df_cars)
    total_columns = len(df_cars.columns)
    
    columns_info = {}
    
    for column in df_cars.columns:
        series = df_cars[column]
        non_null_count = series.count()
        
        # Get sample values (first 3 unique values)
        sample_values = series.dropna().unique()[:3].tolist()
        
        columns_info[column] = {
            'dtype': str(series.dtype),
            'non_null_count': int(non_null_count),
            'null_count': int(series.isnull().sum()),
            'unique_count': int(series.nunique()),
            'sample_values': [str(val) for val in sample_values]
        }
    
    return {
        'total_columns': total_columns,
        'total_rows': total_rows,
        'columns': columns_info
    }


@mcp.tool()
def get_cars_sorted_by(
    sort_by: Annotated[str, f"Column name to sort by {''.join(list(df_cars.columns))}"],
    ascending: Annotated[bool, "Sort in ascending order if True, descending if False"] = True,
    limit: Annotated[Optional[int], "Maximum number of results"] = None
) -> List[Dict[str, Any]]:
    """Sort cars by any column in ascending or descending order."""

    if 'year' in sort_by.lower() or\
        'month' in sort_by.lower() or\
        'day' in sort_by.lower() or\
        'date' in sort_by.lower():
        sort_by = 'date_added'
    
    sorted_df = df_cars.sort_values(by=sort_by, ascending=ascending)
    
    if limit:
        sorted_df = sorted_df.head(limit)
    
    res = sorted_df.to_dict('records')
    return [
        {str(k): v for k, v in record.items()}
        for record in res
    ]


@mcp.tool()
def get_cars_by_year_range(
    year_min: Annotated[int, "Minimum year (inclusive)"], 
    year_max: Annotated[int, "Maximum year (inclusive)"]
) -> List[Dict[str, Any]]:
    """Filter cars by manufacturing year within inclusive range."""
    filtered_df = df_cars[(df_cars['year'] >= year_min) & (df_cars['year'] <= year_max)]
    res = filtered_df.to_dict('records')
    return [
        {str(k): v for k, v in record.items()}
        for record in res
    ]


# @mcp.tool()
# def get_cars_by_mileage_range(
#     max_mileage: Annotated[int, "Maximum mileage allowed"]
# ) -> List[Dict[str, Any]]:
#     """Filter cars by maximum mileage threshold for low-mileage vehicles."""
#     filtered_df = df_cars[df_cars['mileage'] <= max_mileage]
    
#     res = filtered_df.to_dict('records')
#     return [
#         {str(k): v for k, v in record.items()}
#         for record in res
#     ]


@mcp.tool()
def get_cars_count_by_brand() -> Dict[str, int]:
    """Count available cars by brand returning brand-to-count mapping."""
    return df_cars['brand'].value_counts().to_dict()




@mcp.tool()
def check_value_exists(
    column: Annotated[str, "Column name to check"], 
    value: Annotated[str, "Value to search for"]
) -> Dict[str, Any]:
    """Check if a specific value exists in a column and return match details."""
    if column not in df_cars.columns:
        return {"exists": False, "error": f"Column {column} not found"}
    
    # Check for exact matches and partial matches
    exact_matches = df_cars[df_cars[column].astype(str).str.upper() == str(value).upper()]
    partial_matches = df_cars[df_cars[column].astype(str).str.contains(str(value), case=False, na=False)]
    
    return {
        "exists": len(exact_matches) > 0 or len(partial_matches) > 0,
        "exact_matches": len(exact_matches),
        "partial_matches": len(partial_matches),
        "total_matches": len(partial_matches),
        "sample_matches": partial_matches.head(3).to_dict('records') if len(partial_matches) > 0 else []
    }


@mcp.tool()
def get_grouped_statistics(
    group_by: Annotated[str, "Column to group by"],
    aggregate_field: Annotated[str, "Column to calculate statistics for"],
    operation: Annotated[str, "Operation: 'mean', 'sum', 'count', 'min', 'max'"] = "mean"
) -> Dict[str, Any]:
    """Calculate grouped statistics for a specific field by grouping column."""
    if group_by not in df_cars.columns or aggregate_field not in df_cars.columns:
        return {"error": f"Column not found: {group_by} or {aggregate_field}"}
    
    try:
        grouped = df_cars.groupby(group_by)[aggregate_field]
        
        if operation == "mean":
            result = grouped.mean()
        elif operation == "sum":
            result = grouped.sum()
        elif operation == "count":
            result = grouped.count()
        elif operation == "min":
            result = grouped.min()
        elif operation == "max":
            result = grouped.max()
        else:
            return {"error": f"Unsupported operation: {operation}"}
        
        # Convert to dict and find the group with highest/lowest value
        result_dict = result.to_dict()
        
        if operation in ["mean", "sum", "max"]:
            best_group = max(result_dict.items(), key=lambda x: x[1])
        else:
            best_group = min(result_dict.items(), key=lambda x: x[1])
        
        return {
            "operation": operation,
            "group_by": group_by,
            "aggregate_field": aggregate_field,
            "results": {str(k): float(v) if isinstance(v, (int, float)) else v for k, v in result_dict.items()},
            "best_group": {"name": best_group[0], "value": float(best_group[1])},
            "total_groups": len(result_dict)
        }
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def filter_cars_by_date_range(
    start_date: Annotated[Optional[str], "Start date (YYYY-MM-DD format)"] = None,
    end_date: Annotated[Optional[str], "End date (YYYY-MM-DD format)"] = None,
    year: Annotated[Optional[int], "Specific year to filter by"] = None
) -> List[Dict[str, Any]]:
    """Filter cars by date range or specific year in date_added column."""
    df = df_cars.copy()
    
    if 'date_added' not in df.columns:
        return [{"error": "date_added column not found in dataset"}]
    
    try:
        # Convert date_added to datetime if it's not already
        df['date_added'] = pd.to_datetime(df['date_added'])
        
        if year:
            df = df[df['date_added'].dt.year == year]
        else:
            if start_date:
                df = df[df['date_added'] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df['date_added'] <= pd.to_datetime(end_date)]
        
        res = df.to_dict('records')
        return [
            {str(k): v for k, v in record.items()}
            for record in res
        ]
        
    except Exception as e:
        return [{"error": f"Date filtering error: {str(e)}"}]


@mcp.tool()
def reload_data():
    """Reload the dataframe from the CSV file."""
    global df_cars
    if not os.path.exists(CSV_FILE_PATH):
        raise FileNotFoundError(f"CSV file not found: {CSV_FILE_PATH}")
    df_cars = pd.read_csv(CSV_FILE_PATH)


def main(argv):
    mcp.run(transport='stdio')

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])


