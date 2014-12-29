drop table if exists messages;
create table messages (
	id integer primary key autoincrement,
	user text not null,
	text text not null,
	read integer not null
);