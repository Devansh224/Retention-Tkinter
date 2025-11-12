from db_connection import create_connection

def add_task(user_id, title, description=None, subject_id=None, chapter_id=None):
    conn = create_connection(); cur = conn.cursor()
    cur.execute("""
        INSERT INTO tasks (user_id, title, description, subject_id, chapter_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, title, description, subject_id, chapter_id))
    conn.commit(); cur.close(); conn.close()

def get_tasks(user_id, only_pending=False):
    conn = create_connection(); cur = conn.cursor()
    query = """
        SELECT id, title, description, subject_id, chapter_id, completed
        FROM tasks WHERE user_id=%s
    """
    if only_pending:
        query += " AND completed=FALSE"
    query += " ORDER BY created_at DESC"
    cur.execute(query, (user_id,))
    tasks = cur.fetchall()
    cur.close(); conn.close()
    return tasks

def mark_task_done(task_id):
    conn = create_connection(); cur = conn.cursor()
    cur.execute("UPDATE tasks SET completed=TRUE WHERE id=%s", (task_id,))
    conn.commit(); cur.close(); conn.close()

def delete_task(task_id):
    conn = create_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    conn.commit(); cur.close(); conn.close()
