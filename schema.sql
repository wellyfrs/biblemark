CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  display_name TEXT NOT NULL,
  created DATETIME NOT NULL DEFAULT current_timestamp
);

CREATE TABLE version (
    internal_id TEXT PRIMARY KEY,
    external_id TEXT NOT NULL,
    lang TEXT NOT NULL,
    name TEXT NOT NULL,
    disabled BOOLEAN NOT NULL CHECK (disabled IN (0, 1)) DEFAULT 0,
    UNIQUE(external_id)
);

CREATE TABLE mark (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  color TEXT,
  note TEXT,
  marked DATETIME NOT NULL DEFAULT current_timestamp,
  FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE marked_verse (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  version_id TEXT NOT NULL,
  book_id TEXT NOT NULL,
  chapter_id TEXT NOT NULL, /* chapter ID as text to support cases like "intro" */
  verse_number INTEGER NOT NULL, /* positive integer */
  mark_id INTEGER NOT NULL,
  visibility BOOLEAN NOT NULL CHECK (visibility IN (0, 1)),
  FOREIGN KEY(version_id) REFERENCES version(internal_id) ON DELETE CASCADE,
  FOREIGN KEY(mark_id) REFERENCES mark(id) ON DELETE CASCADE,
  UNIQUE(version_id, book_id, chapter_id, verse_number, mark_id)
);
