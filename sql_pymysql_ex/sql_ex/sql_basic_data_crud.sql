-- DB 사용선언
-- 실행: ctrl + enter
use db_basic;

-- 테이블 생성하기 : users_info
create table users_info(
	id int primary key auto_increment,
	username varchar(255),
	email varchar(255),
	phone varchar(20),
	website varchar(255),
	regdate datetime
);

-- 테이블 생성하기 : users_info2
create table users_info2(
	id int primary key auto_increment,
	username varchar(255),
	email varchar(255),
	phone varchar(20),
	website varchar(255),
	regdate datetime
);

-- 테이블 삭제(drop)
drop table users_info2;

-- DML : data create
insert into users_info
	(id, username, email, phone, website, regdate)
	value(1, 'kim', 'kim@cozlab.com', '010-1234-5678', 'cozlab.com', '2020-10-24 00:00:00');
insert into users_info
	(id, username, email, phone, website, regdate)
	value(2, 'lee', 'lee@naver.com', '010-1234-5678', 'naver.com', '2020-10-24 00:00:00');
insert into users_info
	(id, username, email, phone, website, regdate)
	value(3, 'hwang', 'hwang@cozlab.com', '010-2356-0978', 'cozlab.com', '2020-10-24 00:00:00');
insert into users_info
	(id, username, email, phone, website, regdate)
	value(4, 'oh', 'oh@naver.com', '010-1234-5678', 'naver.com', '2020-10-24 00:00:00');
insert into users_info
	(id, username, email, phone, website, regdate)
	value(5, 'oh', 'oh@naver.com', '010-1234-5678', 'naver.com', '2020-10-24 00:00:00');


-- DML - Read (데이터 읽기)
-- users_info 테이블의 모든 데이터 읽기
select *
from users_info;

-- 특정 column 데이터 읽기
select username, phone
from users_info as ui

-- DML - Update (특정 column 데이터 수정)
update users_info ui
set email = 'yujeonglee@google.com',
	phone = '010-0904-0430',
	regdate = '2025-10-22'
where id = 1;

-- DML - Delete (특정 레코드 데이터 삭제)
delete from users_info
where id= 3;

-- DML - 테이블 데이터 모두 삭제 (테이블은 존재)
delete from users_info ;

-- DDL - 테이블 삭제
drop table users_info;