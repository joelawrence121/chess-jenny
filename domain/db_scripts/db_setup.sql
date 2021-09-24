create table puzzle
(
	id int auto_increment
		primary key,
	starting_fen varchar(32) not null,
	ending_fen varchar(32) not null,
	moves int not null,
	gain int null,
	mate tinyint(1) not null
);

alter table puzzle drop column mate;

alter table puzzle
	add type varchar(32) null;

alter table puzzle change moves move int not null;

alter table puzzle modify starting_fen varchar(256) not null;

alter table puzzle modify ending_fen varchar(256) not null;

alter table puzzle modify gain float null;

alter table puzzle modify type varchar(256) null;

alter table puzzle modify move varchar(256) not null after type;

alter table puzzle
	add to_move varchar(16) null;