CREATE DATABASE IF NOT EXISTS demo;
USE demo;

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS post;
SET FOREIGN_KEY_CHECKS=1;

create table user
(
    id       int          not null
        primary key,
    username varchar(200) not null,
    password varchar(50)  not null,
    constraint username
        unique (username)
);

create table post
(
    id        int                                 not null
        primary key,
    author_id int                                 not null,
    created   timestamp default CURRENT_TIMESTAMP not null,
    title     text                                not null,
    body      text                                not null,
    constraint post_ibfk_1
        foreign key (author_id) references admin (id)
);

create index author_id
    on post (author_id);