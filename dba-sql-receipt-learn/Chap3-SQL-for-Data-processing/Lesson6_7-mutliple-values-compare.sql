-- 스키마 생성
create schema sql_receipt;
set search_path to sql_receipt;

-- 6강. 여러 개의 값에 대한 조작

-- 데이터 6-2
create table quarterly_sales(
    year varchar(4),
    q1 integer,
    q2 integer,
    q3 integer,
    q4 integer
);

insert into quarterly_sales(year, q1, q2, q3, q4) values
('2015',82000,83000,78000,84000),
('2016',85000,85000,80000,81000),
('2017',92000,81000,null,null);

select * from quarterly_sales;

-- 분기별 매출 증감 판정하기
select year, q1, q2,
       case
           when q1 < q2 then '+'
           when q1 = q2 then ' '
           else '-'
       end as judge_q1_q2,
       q2-q1 as diff_q2_q1,
       sign(q2-q1) as sign_q2_q1
from quarterly_sales
order by year;

-- 연간 평균 4분기 매출 계산하기
select year,
    (coalesce(q1,0) + coalesce(q2,0) + coalesce(q3,0) + coalesce(q4,0))
    / nullif(sign(coalesce(q1,0)) + sign(coalesce(q2,0)) + sign(coalesce(q3,0)) + sign(coalesce(q4,0)),0)
    as average
from quarterly_sales
order by year;

-- 데이터 6-3 광고 통계 정보
drop table if exists advertising_stats;
create table advertising_stats(
    dt date,
    ad_id integer,
    impressions bigint,
    clicks integer
);

insert into advertising_stats(dt, ad_id, impressions, clicks) values
('2017-04-01',1,100000,3000),
('2017-04-01',2,120000,1200),
('2017-04-01',3,500000,10000),
('2017-04-02',1,0,0),
('2017-04-02',2,130000,1400),
('2017-04-02',3,620000,15000);

select * from advertising_stats;

/*
 하나하나 구할 때 ctr_as_percent 컬럼처럼 click에 100.0을 곱해 계산하면,
 자료형 변환이 자동으로 이루어지므로 쿼리가 간단해짐
 */
-- CTR 계산
select dt, ad_id,
       cast(clicks as double precision) / impressions as ctr,
       100.0 * clicks / impressions as ctr_as_percent
from advertising_stats
where dt = '2017-04-01'
order by dt, ad_id;

-- 0으로 나누는 것 피하기
select dt, ad_id,
       case when impressions > 0 then 100.0 * clicks / impressions end as ctr_as_percent_by_case,
       100.0 * clicks / nullif(impressions,0) as ctr_as_percent_by_null
from advertising_stats
order by dt, ad_id;

-- 데이터 6-4 일차원 위치 정보
create table location_1d(
    x1 integer,
    x2 integer
);

insert into location_1d(x1, x2) values
(5,10),(10,5),(-2,4),(3,3),(0,1);

select abs(x1-x2) as abs,
       sqrt(power(x1-x2,2)) as rms
from location_1d;

-- 데이터 6-5 이차원 위치 정보
create table location_2d(
    x1 integer,
    y1 integer,
    x2 integer,
    y2 integer
);

insert into location_2d(x1,y1,x2,y2) values
(0,0,2,2),
(3,5,1,2),
(5,3,2,1);

select sqrt(power(x1-x2,2) + power(y1-y2,2)) as dist,
       point(x1,y1) <-> point(x2,y2) as dist_point
from location_2d;

-- 데이터 6-6 사용자 마스터
drop table if exists mst_users_with_dates;
create table mst_users_with_dates(
    user_id varchar(10),
    register_stamp timestamp,
    birth_date date
);

insert into mst_users_with_dates(user_id, register_stamp, birth_date) values
('U001','2016-02-28 10:00:00','2000-02-29'),
('U002','2016-02-29 10:00:00','2000-02-29'),
('U003','2016-03-01 10:00:00','2000-02-29');

-- 미래/과거 날짜 계산
select user_id,
       register_stamp,
       register_stamp + interval '1 hour' as after_1_hour,
       register_stamp - interval '30 minutes' as before_30_minutes,
       register_stamp::date as register_date,
       (register_stamp::date + interval '1 day')::date as after_1_day,
       (register_stamp::date - interval '1 month')::date as before_1_month
from mst_users_with_dates;

-- 두 날짜의 차이 계산
select user_id,
       current_date as today,
       register_stamp::date as register_date,
       current_date - register_stamp::date as diff_days
from mst_users_with_dates;

-- 나이 계산
select user_id,
       current_date as today,
       register_stamp::date as register_date,
       birth_date::date as birth_date,
       extract(year from age(birth_date::date)) as current_age,
       extract(year from age(register_stamp::date, birth_date::date)) as register_age
from mst_users_with_dates;


-- 코드 6-16 등록 시점과 현재 시점의 나이를 문자열로 계산하는 쿼리
select user_id
, substring(register_stamp, 1, 10) as register_date
, birth_date
-- 등록 시점의 나이 계산하기
, floor(
	(cast(replace(substring(register_stamp, 1, 10), '-', '') as integer)
	- cast(replace(birth_date, '-', '') as integer)
	) / 10000
	) as register_age
-- 현재 시점의 나이 계산하기
, floor(
	(cast(replace(cast(current_date as text), '-', '') as integer)
	- cast(replace(birth_date, '-', '') as integer)
	) / 10000
	) as current_age
from mst_users_with_dates;


-- IP 주소 다루기
-- 간단하게 IP 주소를 확인하거나 할 때는 문자열로 다루어도 충분하지만, 
-- IP 주소를 서로 비교하거나 동일한 네트워크의 IP 주소인지 판정할 때는 단순 문자열 비교만으로는 굉장히 코드가 복잡해진다.

-- IP 주소 자료형 활용하기
-- PostgreSQL에는 IP 주소를 다루기 위한 inet 자료형이 구현되어 있음. inet 자료형을 사용하면 IP주소를 쉽게 비교할 수 있다.
-- inet 자료형의 대소를 비교할 때는 < 또는 > 를 사용한다.

-- 코드 6-17 inet 자료형을 사용한 IP 주소 비교 쿼리
select
	cast('127.0.0.1' as inet) < cast('127.0.0.2' as inet) as lt
	, cast('127.0.0.1' as inet) > cast('192.168.0.1' as inet) as gt;

-- 추가로 address/y 형식의 네트워크 범위에 IP 주소가 포함되는지도 판정할 수 있음. 판정에는 << 또는 >> 연산자를 사용함
-- 코드 6-18 inet 자료형을 사용해 IP 주소 범위를 다루는 쿼리
select cast('127.10.22.1' as inet) << cast('127.0.0.0/8' as inet) as is_contained;

-- 정수 또는 문자열로 IP 주소 다루기
-- 코드 6-19 IP 주소에서 4개의 10진수 부분을 추출하는 쿼리
select ip
, cast(split_part(ip, '.', 1) as integer) as ip_part_1
, cast(split_part(ip, '.', 2) as integer) as ip_part_2
, cast(split_part(ip, '.', 3) as integer) as ip_part_3
, cast(split_part(ip, '.', 4) as integer) as ip_part_4
from 
	(select '192.168.0.1' as ip) as t;

-- 코드 6-20 IP 주소를 정수 자료 표기로 변환하는 쿼리
select ip
, cast(split_part(ip, '.', 1) as integer) * 2^24
+ cast(split_part(ip, '.', 2) as integer) * 2^16
+ cast(split_part(ip, '.', 3) as integer) * 2^8
+ cast(split_part(ip, '.', 4) as integer) * 2^0
as ip_integer
from 
	(select '192.168.0.1' as ip) as t;

-- ip 주소를 0으로 메우기; lpad 함수는 지정한 문자 수가 되게 문자열의 왼쪽을 메우는 함
select ip
, lpad(split_part(ip, '.', 1), 3, '0')
	|| lpad(split_part(ip, '.', 2), 3, '0')
	|| lpad(split_part(ip, '.', 3), 3, '0')
	|| lpad(split_part(ip, '.', 4), 3, '0')
	as ip_padding
from 
	(select '192.168.0.1' as ip) as t;

-- 7강. 하나의 테이블에 대한 조
	
-- 데이터 7-2 인기 상품(popular_products) 테이블
drop table if exists popular_products;
create table popular_products(
product_id varchar(10),
category varchar(10),
score integer);

insert into popular_products(product_id, category, score) values
('A001','action',94),
('A002','action',81),
('A003','action',78),
('A004','action',64),
('A005','action',78),
('D001','drama',90),
('D002','drama',82),
('D003','drama',78),
('D004','drama',58);

-- 코드 7-4 윈도 함수의 order by 구문을 사용해 테이블 내부의 순서를 다루는 쿼리
select product_id
, score
	-- 점수 순서로 유일한 순위를 붙임
, row_number() over(order by score desc) as row
	-- 같은 순위를 허용해서 순위를 붙임
, rank() 	   over(order by score DESC) as rank
	-- 같은 순위가 있을 때 같은 순위 다음에 있는 순위를 건너 뛰고 순위를 붙임
, dense_rank() over(order by score desc) as dense_rank
	-- 현재 행보다 앞에 있는 행의 값 추출하기
, lag(product_id) over(order by score desc) as lag1
, lag(product_id, 2) over(order by score desc) as lag2
	-- 현재 행보다 뒤에 있는 행의 값 추출하기
, lead(product_id) over(order by score desc) as lead1
, lead(product_id) over(order by score desc) as lead2
from popular_products
order by row;


-- 코드 7-5 order by 구문과 집약 함수를 조합해서 계산하는 쿼리
select
product_id
, score
	-- 점수 순서로 유일한 순위를 붙임
, row_number() over(order by score desc) as row
	-- 순위 상위부터의 누계 점수 계산하기
, sum(score)
	over(order by score desc
		rows between unbounded preceding and current row)
	as cum_score
	-- 현재 행과 앞 뒤의 행이 가진 값을 기반으로 평균 점수 계산하기
, avg(score)
	over(order by score desc
		rows between 1 preceding and 1 following)
	as local_avg
	-- 순위가 높은 상품 ID 추출하기
, first_value(product_id)
	over(order by score desc
		rows between unbounded preceding and unbounded following)
	as first_value
	-- 순위가 낮은 상품 ID 추출하기
, last_value(product_id)
	over(order by score desc
		rows between unbounded preceding and unbounded following)
	as last_value
from popular_products
order by row;


-- 코드 7-7 윈도 함수를 사용해 카테고리들의 순위를 계산하는 쿼리
select
	category
	, product_id
	, score
	-- 카테고리별로 점수 순서로 정렬하고 유일한 순위를 붙임
	, row_number()
		over(partition by category order by score desc)
	as row
	-- 카테고리별로 같은 순위를 허가하고 순위를 붙임
	, rank()
		over(partition by category order by score desc)
	as rank
	-- 카테고리별로 같은 순위가 있을 때 같은 순위 다음에 있는 순위를 건너 뛰지 않고 순위를 붙임
	, dense_rank()
		over(partition by category order by score desc)
	as dense_rank
from popular_products
order by category, row;

-- 각 카테고리의 상위 n개 추출하기
-- 코드 7-8 카테고리들의 순위 상위 2개까지의 상품을 추출하는 쿼리
select *
from
-- 서브 쿼리 내부에서 순위 계산하기
	(select 
		category
		, product_id
		, score
		-- 카테고리별로 점수 순서로 유일한 순위를 붙임
		, row_number()
			over(partition by category order by score desc)
		as rank
		from popular_products)
	as popular_products_with_rank
-- 외부 쿼리에서 순위 활용해 압축하기
where rank <= 2
order by category, rank;

-- 코드 7-9 카테고리별 순위 최상위 상품을 추출하는 쿼리
-- distinct 구문을 사용해 중복 제거하기
select distinct 
	category
	-- 카테고리별로 순위 최상위 상품 ID 추출하기
	, first_value(product_id)
		over(partition by category order by score desc 
			rows between unbounded preceding and unbounded following)
			as product_id
	from popular_products;

-- 세로 기반 데이터를 가로 기반으로 변환하기

-- 행을 열로 변환하기
-- 데이터 7-3 날짜별 KPI 데이터(daily_kpi) 테이블
create table daily_kpi(
dt date,
indicator varchar(20),
val integer);

insert into daily_kpi(dt, indicator, val) values
('2017-01-01','impressions', 1800),
('2017-01-01','sessions', 500),
('2017-01-01','users', 200),
('2017-01-02','impressions', 2000),
('2017-01-02','sessions', 700),
('2017-01-02','users', 250);

-- 코드 7-10 행으로 저장된 지표 값을 열로 변환하는 쿼리
select
	dt
	, max(case when indicator='impressions' then val end) as impressions
	, max(case when indicator='sessions' then val end) as sessions
	, max(case when indicator='users' then val end) as users
from daily_kpi
group by dt 
order by dt;

-- 데이터 7-4 구매 상세 로그(purchase_detail_log) 테이블
create table purchase_detail_log(
purchase_id bigint,
product_id varchar(10),
price int);

insert into purchase_detail_log(purchase_id, product_id, price) values
(100001, 'A001', 300),
(100001, 'A002', 400),
(100001, 'A003', 200),
(100002, 'D001', 500),
(100002, 'D002', 300),
(100003, 'A001', 300);

-- 코드 7-11 행을 집약해서 쉼표로 구분된 문자열로 반환하기
select
	purchase_id
	-- 상품 ID를 배열에 집약하고 쉼표로 구분된 문자열로 변환하기
	-- PostegreSQL, BigQuery의 경우는 string_agg 사용하기
	, string_agg(product_id, ',') as product_ids
	, sum(price) as amount
	from purchase_detail_log
	group by purchase_id
	order by purchase_id;

-- 열로 표현된 값을 행으로 변환하
-- 컬럼으로 표현된 가로 기반 데이터의 특징은 데이터의 수가 고정되어 있다는 것
-- 예를 들어, 하나의 레코드는 q1부터 q4까지 모두 4개의 데이터로 구성됨. 
-- 행으로 전개할 데이터 수가 고정되었다면, 그러한 데이터 수와 같은 수의 일련 번호를 가진 피벗 테이블을 만들고 CROSS JOIN 하면 됨.

-- 코드 7-12 일련 번호를 가진 피벗 테이블을 사용해 행으로 변환하는 쿼리
select
	q.year
	-- Q1에서 Q4까지의 레이블 이름 출력하기
	, case
		when p.idx = 1 then 'q1'
		when p.idx = 2 then 'q2'
		when p.idx = 3 then 'q3'
		when p.idx = 4 then 'q4'
	end as quarter
	-- Q1에서 Q4까지의 매출 출력하기
	, case 
		when p.idx = 1 then q.q1
		when p.idx = 2 then q.q2
		when p.idx = 3 then q.q3
		when p.idx = 4 then q.q4
	end as sales
from quarterly_sales as q
cross join
	-- 행으로 전개하고 싶은 열의 수만큼 순번 테이블 만들기
	(			select 1 as idx
	union all 	select 2 as idx
	union all 	select 3 as idx
	union all 	select 4 as idx
	) as p;

-- 임의의 길이를 가진 배열을 행으로 전개하기
-- 고정 길이의 데이터를 행으로 전개하는 것은 비교적 간단하지만, 데이터의 길이가 확정되지 않은 경우는 조금 복잡함.
-- 구매 로그 테이블을 사용해 상품 ID들을 레코드로 하나하나 전개하는 예시

-- 테이블 함수를 구현하고 있는 미들웨어라면 배열을 쉽게 레코드로 전개할 수 있음.
-- 이때, 테이블 함수란 함수의 리턴값이 테이블인 함수를 의미함.
-- 대표적인 테이블 함수로는 PostgreSQL과 BigQuery의 unnest 함수. Hive와 SparkSQL의 explode 함수가 있음
-- 이러한 함수는 매개변수로 배열을 받고 배열을 레코드 분할해서 리턴해줌

-- 코드 7-13 테이블 함수를 사용해 배열을 행으로 전개하는 쿼리
select unnest(array['A001','A002','A003']) as product_id;

create table purchase_log as
select
	purchase_id
	-- 상품 ID를 배열에 집약하고 쉼표로 구분된 문자열로 변환하기
	-- PostegreSQL, BigQuery의 경우는 string_agg 사용하기
	, string_agg(product_id, ',') as product_ids
	, sum(price) as amount
	from purchase_detail_log
	group by purchase_id
	order by purchase_id;



-- 코드 7-14 테이블 함수를 사용해 쉼표로 구분된 문자열 데이터를 행으로 전개하는 쿼리
select
	purchase_id
	, product_id
from 
	purchase_log as p
	-- string_to_array 함수로 문자열을 배열로 변환하고, unnest 함수로 테이블로 변환하기
	cross join unnest(string_to_array(product_ids, ',')) as product_id
	
-- 코드 7-15 PostgreSQL에서 쉼표로 구분된 데이터를 행으로 전개하는 쿼리
select
	purchase_id
	-- 쉼표로 구분된 문자열을 한 번에 행으로 전개하기
	, regexp_split_to_table(product_ids, ',') as product_id
	from purchase_log;
	

