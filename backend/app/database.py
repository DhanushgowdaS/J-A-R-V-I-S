"""SQLite persistence for conversations. Uses only Python's standard library."""
import os, sqlite3
from pathlib import Path
from datetime import datetime, timezone

def db_path() -> Path:
    override=os.getenv("JARVIS_DB_PATH")
    if override: return Path(override)
    return Path(__file__).resolve().parents[2] / "data" / "jarvis.sqlite3"

def connect():
    path=db_path()
    path.parent.mkdir(parents=True,exist_ok=True)
    con=sqlite3.connect(path)
    con.row_factory=sqlite3.Row
    return con

def initialize():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY, title TEXT NOT NULL DEFAULT 'New conversation',
            created_at TEXT NOT NULL, updated_at TEXT NOT NULL)""")
        con.execute("""CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT, conversation_id TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('user','assistant','system')),
            content TEXT NOT NULL, created_at TEXT NOT NULL,
            FOREIGN KEY(conversation_id) REFERENCES conversations(id) ON DELETE CASCADE)""")
        con.execute("CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id,id)")
        con.execute("PRAGMA foreign_keys=ON")

def timestamp():
    return datetime.now(timezone.utc).isoformat()

def create_conversation(cid, title="New conversation"):
    initialize()
    now=timestamp()
    with connect() as con:
        con.execute("INSERT OR IGNORE INTO conversations(id,title,created_at,updated_at) VALUES(?,?,?,?)",(cid,title,now,now))

def add_message(cid, role, content):
    initialize(); now=timestamp()
    with connect() as con:
        con.execute("INSERT OR IGNORE INTO conversations(id,title,created_at,updated_at) VALUES(?,?,?,?)",(cid,"New conversation",now,now))
        con.execute("INSERT INTO messages(conversation_id,role,content,created_at) VALUES(?,?,?,?)",(cid,role,content,now))
        if role=="user":
            row=con.execute("SELECT title FROM conversations WHERE id=?",(cid,)).fetchone()
            if row and row["title"]=="New conversation":
                title=content.strip().replace("\n"," ")[:64] or "New conversation"
                con.execute("UPDATE conversations SET title=?,updated_at=? WHERE id=?",(title,now,cid))
        else: con.execute("UPDATE conversations SET updated_at=? WHERE id=?",(now,cid))

def history(cid):
    initialize()
    with connect() as con:
        rows=con.execute("SELECT role,content FROM messages WHERE conversation_id=? ORDER BY id",(cid,)).fetchall()
    return [{"role":r["role"],"content":r["content"]} for r in rows]

def list_conversations(limit=100):
    initialize()
    with connect() as con:
        rows=con.execute("SELECT id,title,created_at,updated_at FROM conversations ORDER BY updated_at DESC LIMIT ?",(limit,)).fetchall()
    return [dict(r) for r in rows]

def delete_conversation(cid):
    initialize()
    with connect() as con:
        con.execute("DELETE FROM messages WHERE conversation_id=?",(cid,))
        cur=con.execute("DELETE FROM conversations WHERE id=?",(cid,))
    return cur.rowcount>0
