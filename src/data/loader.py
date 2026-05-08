"""
Provides pre-built, reusable data loading/filtering methods for each analytical object in the Operation Insight project/

The DataLoader sits between the DatabaseConnector (which handles the raw db connection)
and the notebooks/analysis implementations.

Its job is to know what data is needed and how to fetch it.

Usage:
    from src.data.loader import DataLoader

    loader = DataLoader()

    # E.g: Fetch data showing annual crime count
    df = loader.get_annual_crime_counts()
"""

# Imports from built-in implementations
import logging

# Imports from 3rd-party packages
import pandas as pd

# Imports from project
from src.database.connector import DatabaseConnector

# Initialize logging for the data loader class
logger = logging.getLogger(__name__)

class DataLoader:
    """
    Provides structured, pre-build data loading/filtering methods for each analytical objective
    in the Operation Insight project.

    Each method corresponds to a specific analytical need and returns a clean, ready-to-analyse pandas DataFrame.

    Example:
        loader = DataLoader()\n
        df = loader.get_annual_crime_counts()
    """

    def __init__(self):
        """
        Initializes the DataLoader object
        """
        self.db = DatabaseConnector()
        logger.info(f"DataLoader initialized")

    def dataset_summary(self) -> pd.DataFrame:
        """
        Return a high-level summary of the full dataset.
        Useful for the introduction section of an analysis.
        """
        sql = """
            SELECT
                COUNT(*) AS total_incidents,
                MIN(year) AS earliest_year,
                MAX(year) AS latest_year,
                COUNT(DISTINCT primary_type) AS crime_types,
                COUNT(DISTINCT district) AS districts,
                COUNT(DISTINCT community_area) AS community_areas,
                SUM(arrest) AS total_arrests,
                ROUND(AVG(arrest) * 100, 2) AS arrest_rate,
                SUM(domestic) AS total_domestic_incidents
            FROM incidents;
        """

        return self.db.query(sql)


    def get_crime_type_list(self) -> pd.DataFrame:
        """
        Return all unique crime types and their total counts.
        """
        sql = """
            SELECT
                primary_type,
                COUNT(*) AS total_incidents
            FROM incidents
            GROUP BY primary_type
            ORDER BY total_incidents DESC;
        """

        return self.db.query(sql)


    def get_annual_crime_counts(self):
        """
        Return total crime incidents per year across all crime types.
        Used to plot the crime trend line
        """
        sql = """
            SELECT
                year,
                COUNT(*) AS total_incidents
            FROM incidents
            GROUP BY year
            ORDER BY year;
        """

        return self.db.query(sql)