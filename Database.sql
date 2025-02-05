CREATE TABLE User(
    id INT PRIMARY KEY,
    username VARCHAR(32),
    passsword VARCHAR(64)
)

CREATE TABLE Group(
    id INT PRIMARY KEY,
    title VARCHAR(32)
)

CREATE TABLE User_Group(
    user_id INT,
    group_id INT,
    PRIMARY KEY (user_id, group_id),
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (group_id) REFERENCES Group(id)
)

CREATE TABLE Event(
    id INT PRIMARY KEY,
    beginning DATETIME,
    ending DATETIME,
    title VARCHAR(100)
    descr VARCHAR(500),
    place VARCHAR(100)
)

CREATE TABLE Event_Group(
    event_id INT,
    group_id INT,
    PRIMARY KEY (group_id, event_id),
    FOREIGN KEY (group_id) REFERENCES Group(id),
    FOREIGN KEY (event_it) REFERENCES Event(id)
)

CREATE TABLE Event_user(
    event_id INT,
    user_id INT,
    PRIMARY KEY (user_id, event_id),
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (event_id) REFERENCES Event(id)
)