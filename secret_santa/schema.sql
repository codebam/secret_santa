DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS item;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL,
  name TEXT NOT NULL,
  surname TEXT NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  terms INTEGER NOT NULL DEFAULT 0,
  list TEXT NOT NULL DEFAULT "",
  match INTEGER,
  FOREIGN KEY(match) REFERENCES user(id)
);

CREATE TABLE item (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);