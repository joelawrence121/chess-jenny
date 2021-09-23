create table Puzzle
(
	id int auto_increment
		primary key,
	starting_fen varchar(32) not null,
	ending_fen varchar(32) not null,
	moves int not null,
	gain int null,
	mate tinyint(1) not null
);