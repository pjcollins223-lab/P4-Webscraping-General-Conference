#Juliana Merkley
#step 3 of this scraping project, create a database to hold the data
#and functions to retrieve it

import pandas as pd
from sqlalchemy import create_engine, text

#database connection (password should be changed depending on who's using it)
DB_USER = "postgres"
DB_PASSWORD = "12345"  # CHANGE THIS TO YOUR OWN PASSWORD
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "is303"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

#biggest issue i've run into is here
def test_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connection successful!")
    except Exception as e:
        print("Connection failed:", e)


#drop table if it already exists
def drop_table():
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS general_conference"))
        conn.commit()


#save the data, talk by talk
def save_to_db(talk_dict):
    try:
        df = pd.DataFrame([talk_dict])  # MUST be in list

        df.to_sql(
            "general_conference",
            engine,
            if_exists="append",  # IMPORTANT
            index=False
        )

    except Exception as e:
        print("Error saving to database:", e)


#takes table and puts it into a df
def load_all_data():
    try:
        query = "SELECT * FROM general_conference"
        df = pd.read_sql(query, engine)
        return df

    except Exception as e:
        print("No data found. Please scrape data first.")
        return None

#whole list of talks
def get_talk_list():
    df = load_all_data()

    if df is not None:
        return df[["Speaker_Name", "Talk_Name"]]
    else:
        return None

#returns single talk
def get_single_talk(index):
    df = load_all_data()

    if df is not None:
        try:
            return df.iloc[index]
        except:
            print("Invalid selection.")
            return None
    else:
        return None


#if needed
def preview_data():
    """
    Prints first few rows of table (for testing).
    """
    df = load_all_data()

    if df is not None:
        print(df.head())