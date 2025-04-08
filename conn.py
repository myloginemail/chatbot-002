import sqlite3
import datetime
import streamlit as st

# DB 연결
db_conn = st.secrets['db']['DB_NAME']
conn = sqlite3.connect(db_conn)
c = conn.cursor()

# 테이블 생성
c.execute('''
CREATE TABLE IF NOT EXISTS translation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    original_kr TEXT,
    source_lang TEXT,
    target_lang TEXT,
    tone TEXT,
    translated_en TEXT,
    polished_en TEXT
)
''')
conn.commit()
