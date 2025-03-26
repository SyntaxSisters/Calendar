CREATE TABLE Usr(
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(32),
    password VARCHAR(64)
);

CREATE TABLE Grp(
    id INT PRIMARY KEY,
    title VARCHAR(32)
);

CREATE TABLE Usr_Grp(
    user_id INT,
    group_id INT,
    PRIMARY KEY (user_id, group_id),
    FOREIGN KEY (user_id) REFERENCES Usr(id),
    FOREIGN KEY (group_id) REFERENCES Grp(id)
);

CREATE TABLE Evnt(
    id INT PRIMARY KEY,
    beginning DATETIME,
    ending DATETIME,
    title VARCHAR(100),
    descr VARCHAR(500),
    place VARCHAR(100)
);

CREATE TABLE Event_Group(
    event_id INT,
    group_id INT,
    PRIMARY KEY (group_id, event_id),
    FOREIGN KEY (group_id) REFERENCES Grp(id),
    FOREIGN KEY (event_id) REFERENCES Evnt(id)
);

CREATE TABLE Event_user(
    event_id INT,
    user_id INT,
    PRIMARY KEY (user_id, event_id),
    FOREIGN KEY (user_id) REFERENCES Usr(id),
    FOREIGN KEY (event_id) REFERENCES Evnt(id)
)