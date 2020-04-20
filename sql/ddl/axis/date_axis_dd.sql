/**
 * yyyyMMdd 시간축 테이블
 */
create table DATE_AXIS_DD
(
    v_yyyy varchar(4) not null,
    v_mm   varchar(2) not null,
    v_dd   varchar(2) not null,
    v_date varchar(6) not null
        primary key
)
    comment '일별 시간축';

create index DATE_SERIES_DD_v_date_index
    on DATE_AXIS_DD (v_date);
