

INSERT INTO posts (title, content, published, owner_id) VALUES ('From SQL SENTENCE', 'FROM SQL SENTENCE IN A SCRIPT', false, 1) RETURNING *;
/*
INSERT INTO users (email, password) VALUES ('arcan_diabdo@hotmail.com', 'Micontraseña1234') RETURNING *;
*/

SELECT * FROM users;

/* DELETE TABLE */
/*DROP TABLE posts;*/

/* delete all rows from a table
DELETE FROM posts;
*/