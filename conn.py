import sqlite3
import datetime
import streamlit as st

# DB 연결
db_conn = st.secrets["sqlite"]["DB_PATH"]
conn = sqlite3.connect(db_conn, check_same_thread=False)
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

# DB Insert
def insertDB(now, tran_source_text, selected_label1, selected_label2, selected_label3, translated_text, gptMessage) :
    c.execute('''
        INSERT INTO translation_history (timestamp, original_kr, source_lang, target_lang, tone, translated_en, polished_en)
        VALUES (?, ?, ?, ?, ?, ?, ?)''', 
        (
        now,
        tran_source_text,
        selected_label1,
        selected_label2,
        selected_label3,
        translated_text,
        gptMessage
    ))
    conn.commit()
    conn.close()

conn.close()
