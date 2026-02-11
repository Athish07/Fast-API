import os
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER")  
AZURE_SQL_DB     = os.getenv("AZURE_SQL_DB") 
AZURE_SQL_USER   = os.getenv("AZURE_SQL_USER")     
AZURE_SQL_PWD    = os.getenv("AZURE_SQL_PWD")
ODBC_DRIVER      = os.getenv("ODBC_DRIVER", "ODBC Driver 18 for SQL Server")

assert AZURE_SQL_SERVER, "AZURE_SQL_SERVER is missing"
assert AZURE_SQL_DB,     "AZURE_SQL_DB is missing"
assert AZURE_SQL_USER,   "AZURE_SQL_USER is missing"
assert AZURE_SQL_PWD,    "AZURE_SQL_PWD is missing"
assert ODBC_DRIVER,      "ODBC_DRIVER is missing"

odbc_str = (
    f"DRIVER={{{ODBC_DRIVER}}};"
    f"SERVER={AZURE_SQL_SERVER};"
    f"DATABASE={AZURE_SQL_DB};"
    f"UID={AZURE_SQL_USER};"
    f"PWD={AZURE_SQL_PWD};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

connection_uri = "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(odbc_str)

engine = create_engine(connection_uri, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        