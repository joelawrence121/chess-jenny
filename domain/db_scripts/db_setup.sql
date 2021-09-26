create table Single_Move
(
	id int auto_increment
		primary key,
	starting_fen varchar(256) not null,
	ending_fen varchar(256) not null,
	gain float null,
	type varchar(256) null,
	move varchar(256) not null,
	to_move varchar(16) null
);
