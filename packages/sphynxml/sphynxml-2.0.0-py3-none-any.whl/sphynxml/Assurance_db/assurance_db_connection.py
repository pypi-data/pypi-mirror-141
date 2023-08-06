import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class Assurance_db_connection:
    # TODO: add docstring
    def __init__(self):
        pass

    def connect_to_db(self):
        """Connects to the Assurance db

        Returns:
                A session bound to an engine

        """
        # The url for the connection
        connection_url = "postgresql+psycopg2://postgres:z(>uCysA`Z6>{E(W@195.201.62.2:5432/assurancedatabase"
        # Create an engine for the connection
        engine = create_engine(connection_url)

        return engine

    def execute_query(self, query):
        """Execures an SQL query to the Assurance db

        Parameters:
                query (str): the query to be executed

        Returns:
                The results of the query

        """

        return pd.read_sql(query, self.session.bind)


if __name__ == "__main__":

    ass_db = Assurance_db_connection()
    engine = ass_db.connect_to_db()

    with Session(engine) as session:

        session.commit()

    # names = engine.table_names()
    # print(names)
    # SELECT * FROM assurancedb.tables
    pass
