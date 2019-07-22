create schema if not exists pet_hotel collate utf8mb4_0900_ai_ci;
use pet_hotel;
create table admin
(
	id varchar(36) not null
		primary key,
	username varchar(200) not null,
	password varchar(96) not null,
	constraint username
		unique (username)
);

create table booking
(
	id varchar(36) not null
		primary key,
	pet_id varchar(36) null,
	check_in_date date null,
	check_out_date date null
);

create table owner
(
	id varchar(36) not null
		primary key,
	first_name varchar(100) null,
	last_name varchar(100) null,
	phone_number varchar(12) null,
	email varchar(200) null,
	constraint admin_email_uindex
		unique (email)
);

create table pet
(
	id varchar(36) not null
		primary key,
	name varchar(200) null,
	date_of_birth date null,
	owner_id varchar(36) null
);
