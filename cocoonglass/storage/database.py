import sqlite3
import os

class NoteIndex:
    def __init__(self, base_path):
        self.db_path = os.path.join(base_path, 'index.db')
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY,
                title TEXT,
                category TEXT,
                created_at TEXT,
                file_path TEXT,
                content_preview TEXT
            )
        ''')
        cursor.execute('CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(id UNINDEXED, content)')
        conn.commit()
        conn.close()

    def index_note(self, note_id, title, category, created_at, file_path, content):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO notes (id, title, category, created_at, file_path, content_preview)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (note_id, title, category, created_at, file_path, content[:200]))

        cursor.execute('DELETE FROM notes_fts WHERE id = ?', (note_id,))
        cursor.execute('INSERT INTO notes_fts (id, content) VALUES (?, ?)', (note_id, content))

        conn.commit()
        conn.close()

    def search_notes(self, query):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT n.id, n.title, n.category, n.created_at, n.file_path
            FROM notes n
            JOIN notes_fts f ON n.id = f.id
            WHERE f.content MATCH ?
            ORDER BY rank
        ''', (query,))
        results = cursor.fetchall()
        conn.close()
        return results
