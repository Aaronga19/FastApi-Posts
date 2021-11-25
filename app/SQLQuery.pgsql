
/* Pull information */
--INSERT INTO posts (title, content, published, owner_id) VALUES ('From SQL SENTENCE', 'FROM SQL SENTENCE IN A SCRIPT', false, 1) RETURNING *;

--INSERT INTO users (email, password) VALUES ('arcan_diabdo@hotmail.com', 'Micontraseña1234') RETURNING *;

/* to group the number of post from each person*/
--SELECT users.id, users.email, COUNT(posts.id) AS user_post_count FROM posts LEFT JOIN users ON posts.owner_id = users.id GROUP BY users.id;

/* Filters*/
-- SELECT posts.*, COUNT(votes.post_id) FROM posts LEFT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id;

/* DELETE TABLE */
--DROP TABLE votes;
/* CASCADE*/
--DROP TABLE votes CASCADE
/* delete all rows from a table
DELETE FROM posts;
*/