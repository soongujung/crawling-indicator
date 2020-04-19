create table loan_household_month
(
    stat_name  varchar(40) null,
    stat_code  varchar(20) null,
    item_code1 varchar(20) null,
    item_name1 varchar(20) null,
    item_code2 varchar(20) null,
    item_name2 varchar(20) null,
    item_code3 varchar(20) null,
    item_name3 varchar(20) null,
    data_value varchar(20) null,
    time       varchar(14) not null
        primary key
);

create index loan_household_month_time_index
    on loan_household_month (time);

