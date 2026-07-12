DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS fornecedor;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE fornecedor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nome TEXT NOT NULL,
    empresa TEXT NOT NULL,
    categoria TEXT NOT NULL,
    telefone TEXT NOT NULL,
    email TEXT,
    cidade TEXT,
    observacoes TEXT,
    FOREIGN KEY (author_id) REFERENCES user (id)
);