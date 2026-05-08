import logging
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv() # Loads the .env file, so `os.getenv()`can read it

logger = logging.getLogger(__name__)

class DatabaseConnector:
    """
    Messages the SQLAlchemy engine and provides a clean interface for running
    SQL queries amd returning results as DataFrames.
    """

    def __init__(self):
        """
        Initialize a DatabaseConnector object
        """
        # When a DatabaseConnector object is created, it immediately
        # builds the engine. No separate "connect" call is needed.
        self.engine = self._create_engine()
        logger.info("DatabaseConnector initialized")

    def query(self, sql: str, params: dict = None) -> pd.DataFrame:
        """
        Execute a SQL query and return results as a DataFrame.
        This is the most-used method.

        Returns:
            pd.DataFrame
        """

        with self.engine.connect() as conn:
            result = conn.execute(text(sql), params or {})
            return pd.DataFrame(result.fetchall(), columns=result.keys())

    def _build_connection_string(self) -> str:
        """
        Builds a connection string from environment variables.
        Note the underscore prefix on the method name - this is a
        Python naming convention signalling that the method is private,
        i.e: for internal use only. Users of this class should not call it directly.

        :return: str
        """
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT", "3306")
        db_name = os.getenv("DB_NAME")
        db_dialect = os.getenv("DB_DIALECT")
        db_driver = os.getenv("DB_DRIVER")

        # Validate that all required variables are present
        missing = [key for (key, val) in {
            "DB_USER": user,
            "DB_PASSWORD": password,
            "DB_HOST": host,
            "DB_NAME": db_name,
            "DB_DIALECT": db_dialect,
            "DB_DRIVER": db_driver,
        }.items() if not val]

        if missing:
            logger.critical("Missing environment variables: {}. Please check your .env file".format(missing))

            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing)}\n"
                f"Please check your .env file."
            )

        return f"{db_dialect}+{db_driver}://{user}:{password}@{host}:{port}/{db_name}"

    def _create_engine(self):
        """Create and verify the SQLAlchemy engine connection."""
        connection_string = self._build_connection_string()
        engine = create_engine(
            connection_string,
            pool_pre_ping=False,  # Checks connection health before using it
        )

        # Test the connection
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection established successfully.")
        except Exception as e:
            logger.critical(f"Database connection failed!", exc_info=e)
            raise ConnectionError(f"Could not connect to the database: {e}")

        return engine

    # def __repr__(self):
    #     """
    #     Return a concise, unambiguous representation of this object.
    #     Such that the object can be recreated from the return value.
    #
    #     This is what Python shows when you print the object directly,
    #     place it in a `repr()` function, or inspect it in a list.
    #
    #     Returns:
    #          str: A developer-friendly string representation of this object
    #     """
    #     return f"DatabaseConnector()"
