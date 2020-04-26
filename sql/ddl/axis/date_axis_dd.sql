/**
 * yyyyMMdd 시간축 테이블
 */
create table date_axis_dd
(
	yyyy varchar(4) null,
	mm varchar(2) null,
	dd varchar(2) null,
	yyyymmdd date not null
);

create unique index date_axis_dd_yyyymmdd_uindex
	on date_axis_dd (yyyymmdd);

alter table date_axis_dd
	add constraint date_axis_dd_pk
		primary key (yyyymmdd);


