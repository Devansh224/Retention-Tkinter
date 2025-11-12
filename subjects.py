# subjects.py
from db_connection import create_connection

def add_subject(user_id: int, name: str):
    conn = create_connection(); cur = conn.cursor()
    cur.execute("INSERT INTO subjects (user_id, name) VALUES (%s, %s)", (user_id, name))
    conn.commit(); cur.close(); conn.close(); return True

def get_subjects(user_id: int):
    conn = create_connection(); cur = conn.cursor()
    cur.execute("SELECT id, name FROM subjects WHERE user_id=%s ORDER BY created_at", (user_id,))
    rows = cur.fetchall(); cur.close(); conn.close(); return rows

def delete_subject(user_id: int, subject_id: int):
    conn = create_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM subjects WHERE user_id=%s AND id=%s", (user_id, subject_id))
    conn.commit(); cur.close(); conn.close(); return True
