import streamlit as st
import psycopg2

cfg = {
    "host": st.secrets["postgres"]["host"],
    "port": st.secrets["postgres"]["port"],
    "dbname": st.secrets["postgres"]["database"],
    "user": st.secrets["postgres"]["user"],
    "password": st.secrets["postgres"]["password"],
    "sslmode": "require",
}

try:
    conn = psycopg2.connect(**cfg)
    print("SUPABASE CONNECTION SUCCESSFUL")

    with conn.cursor() as cur:
        cur.execute("SELECT current_database(), version()")
        print(cur.fetchone())

    conn.close()

except Exception as e:
    print("SUPABASE CONNECTION FAILED:", e)