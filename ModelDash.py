import pandas as pd


def count_status_groups(df, year=None):
    """
    Cuenta la cantidad de pozos en cada categoría de 'status_group', filtrados por año si se proporciona.
    
    Args:
    df (pd.DataFrame): DataFrame con las columnas 'status_group' y 'construction_year_imputed'.
    year (int, optional): Año para filtrar los pozos por año de construcción.
    
    Returns:
    int, int, int: Conteos de 'functional', 'functional needs repair' y 'non functional'.
    """
    if 'status_group' not in df.columns or 'construction_year_imputed' not in df.columns:
        raise ValueError("El DataFrame debe contener las columnas 'status_group' y 'construction_year_imputed'.")
    
    filtered_df = df.copy()
    if year is not None:
        filtered_df = filtered_df[filtered_df['construction_year_imputed'] == year]
    
    functional_count = filtered_df[filtered_df['status_group'] == 'functional'].shape[0]
    needs_repair_count = filtered_df[filtered_df['status_group'] == 'functional needs repair'].shape[0]
    non_functional_count = filtered_df[filtered_df['status_group'] == 'non functional'].shape[0]
    
    return functional_count, needs_repair_count, non_functional_count


def wells_by_year(df):
    df = df[df['construction_year_imputed'] >= 60]

    """
    Devuelve dos diccionarios con el número de pozos 'functional' y 'non functional' por año.
    
    Args:
    df (pd.DataFrame): DataFrame con las columnas 'status_group' y 'construction_year_imputed'.
    
    Returns:
    dict, dict: Diccionarios con los años como claves y el número de pozos funcionales y dañados como valores.
    """
    if 'status_group' not in df.columns or 'construction_year_imputed' not in df.columns:
        raise ValueError("El DataFrame debe contener las columnas 'status_group' y 'construction_year_imputed'.")
    
    # Filtrar pozos por estado
    functional_wells = df[df['status_group'] == 'functional']
    non_functional_wells = df[df['status_group'] == 'non functional']
    
    # Agrupar por año de construcción y contar
    functional_counts = functional_wells.groupby('construction_year_imputed').size().to_dict()
    non_functional_counts = non_functional_wells.groupby('construction_year_imputed').size().to_dict()
    
    return functional_counts, non_functional_counts


def filter_wells_for_plot(df, water_quality=None, region=None, well_age=None, 
                          status_group=None, construction_year=None, source=None):
    """
    Filtra pozos según los parámetros dados y devuelve un DataFrame listo para graficar.
    
    Args:
    df (pd.DataFrame): DataFrame original.
    water_quality (str, optional): Filtrar por calidad del agua ('quality_group').
    region (str, optional): Filtrar por región.
    well_age (tuple, optional): Filtrar por rango de edad del pozo (años) como (min_age, max_age).
    status_group (str, optional): Filtrar por estado del pozo ('status_group').
    construction_year (int, optional): Filtrar por año de construcción ('construction_year_imputed').
    source (str, optional): Filtrar por fuente de agua ('source').
    
    Returns:
    pd.DataFrame: DataFrame filtrado con las columnas necesarias para graficar.
    """
    if 'construction_year_imputed' not in df.columns:
        raise ValueError("El DataFrame debe contener la columna 'construction_year_imputed'.")
    
    filtered_df = df.copy()
    
    # Filtrar por calidad del agua
    if water_quality:
        filtered_df = filtered_df[filtered_df['quality_group'] == water_quality]
    
    # Filtrar por región
    if region:
        filtered_df = filtered_df[filtered_df['region'] == region]
    
    # Filtrar por rango de edad del pozo
    if well_age:
        current_year = 2024  # Suponiendo el año actual
        filtered_df['well_age'] = current_year - filtered_df['construction_year_imputed']
        filtered_df = filtered_df[
            (filtered_df['well_age'] >= well_age[0]) & 
            (filtered_df['well_age'] <= well_age[1])
        ]
    
    # Filtrar por estado del pozo
    if status_group:
        filtered_df = filtered_df[filtered_df['status_group'] == status_group]
    
    # Filtrar por año de construcción
    if construction_year:
        filtered_df = filtered_df[filtered_df['construction_year_imputed'] == construction_year]
    
    # Filtrar por fuente de agua
    if source:
        filtered_df = filtered_df[filtered_df['source'] == source]
    
    # Seleccionar columnas necesarias para graficar
    plot_data = filtered_df[['longitude', 'latitude', 'status_group']]
    
    return plot_data
