create schema chess_db;
use chess_db;

create table Single_Move
(
    id           int auto_increment
        primary key,
    starting_fen varchar(256) not null,
    ending_fen   varchar(256) not null,
    gain         float        null,
    type         varchar(256) null,
    move         varchar(256) not null,
    to_move      varchar(16)  null
);

create table Game
(
    Id          int auto_increment,
    white_level int         null,
    black_level int         null,
    outcome     varchar(32) null,
    constraint Game_pk
        primary key (Id)
);

create table Mate_In_N
(
    id            int auto_increment
        primary key,
    starting_fen  varchar(256) null,
    to_move       varchar(32)  null,
    moves_to_mate int          null,
    game_id       int          null,
    constraint Mate_In_N__Game_fk
        foreign key (game_id) references Game (Id)
);
