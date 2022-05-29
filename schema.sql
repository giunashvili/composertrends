DROP TABLE IF EXISTS packages;
DROP TABLE IF EXISTS downloads;

CREATE TABLE packages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    repository VARCHAR(255) NOT NULL,
    github_stars INTEGER
);

CREATE TABLE downloads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    date TIMESTAMP NOT NULL,
    value INTEGER NOT NULL,
    FOREIGN KEY(package_id) REFERENCES packages(id)
);