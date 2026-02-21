set search_path to sql_receipt;

drop table if exists purchase_log;

create table purchase_log(
    dt varchar(20),
    order_id bigint,
    user_id varchar(20),
    purchase_amount bigint
);

insert into purchase_log values
                             ('2014-01-01',1,'user0001',13900),
                             ('2014-01-01',2,'user0002',10616),
                             ('2014-01-02',3,'user0003',21000),
                             ('2014-01-02',4,'user0004',14800),
                             ('2014-01-03',5,'user0005',13000),
                             ('2014-01-03',6,'user0005',30000),
                             ('2014-01-04',7,'user0001',15000),
                             ('2014-01-04',8,'user0003',22000),
                             ('2014-01-05',9,'user0002',11000),
                             ('2014-01-05',10,'user0004',16000),
                             ('2014-01-06',11,'user0005',18000),
                             ('2014-01-06',12,'user0001',25000),
                             ('2014-01-07',13,'user0003',10000),
                             ('2014-01-07',14,'user0002',19000),
                             -- 2014 Data (Jan-Mar)
                             ('2014-01-08',15,'user0001',13900),
                             ('2014-01-09',16,'user0002',10616),
                             ('2014-01-10',17,'user0003',21000),
                             ('2014-02-01',18,'user0004',14800),
                             ('2014-02-02',19,'user0005',13000),
                             ('2014-02-03',20,'user0005',30000),
                             ('2014-03-01',21,'user0001',15000),
                             ('2014-03-02',22,'user0003',22000),
                             ('2014-03-03',23,'user0002',11000),
                             -- 2014 Data (Apr-Dec)
                             ('2014-04-01',33,'user0001',16000), ('2014-04-02',34,'user0002',12000),
                             ('2014-05-01',35,'user0003',23000), ('2014-05-02',36,'user0004',17000),
                             ('2014-06-01',37,'user0005',19000), ('2014-06-02',38,'user0001',26000),
                             ('2014-07-01',39,'user0002',13000), ('2014-07-02',40,'user0003',24000),
                             ('2014-08-01',41,'user0004',18000), ('2014-08-02',42,'user0005',20000),
                             ('2014-09-01',43,'user0001',27000), ('2014-09-02',44,'user0002',14000),
                             ('2014-10-01',45,'user0003',25000), ('2014-10-02',46,'user0004',19000),
                             ('2014-11-01',47,'user0005',21000), ('2014-11-02',48,'user0001',28000),
                             ('2014-12-01',49,'user0002',15000), ('2014-12-02',50,'user0003',26000),
                             -- 2015 Data (Jan-Mar)
                             ('2015-01-01',24,'user0001',14500),
                             ('2015-01-02',25,'user0002',11216),
                             ('2015-01-03',26,'user0003',22000),
                             ('2015-02-01',27,'user0004',15800),
                             ('2015-02-02',28,'user0005',14000),
                             ('2015-02-03',29,'user0005',32000),
                             ('2015-03-01',30,'user0001',16000),
                             ('2015-03-02',31,'user0003',23000),
                             ('2015-03-03',32,'user0002',12000),
                             -- 2015 Data (Apr-Dec)
                             ('2015-04-01',51,'user0001',17000), ('2015-04-02',52,'user0002',13000),
                             ('2015-05-01',53,'user0003',24000), ('2015-05-02',54,'user0004',18000),
                             ('2015-06-01',55,'user0005',20000), ('2015-06-02',56,'user0001',27000),
                             ('2015-07-01',57,'user0002',14000), ('2015-07-02',58,'user0003',25000),
                             ('2015-08-01',59,'user0004',19000), ('2015-08-02',60,'user0005',21000),
                             ('2015-09-01',61,'user0001',28000), ('2015-09-02',62,'user0002',15000),
                             ('2015-10-01',63,'user0003',26000), ('2015-10-02',64,'user0004',20000),
                             ('2015-11-01',65,'user0005',22000), ('2015-11-02',66,'user0001',29000),
                             ('2015-12-01',67,'user0002',16000), ('2015-12-02',68,'user0003',27000);


-- 1. 날짜별 매출 집계하기
/*
 매출 집계하는 업무에서는 가로 축에 날짜, 세로 축에 금액을 표현하는 그래프를 사용함.
 날짜별로 매출을 집계하고, 동시에 평균 구매액을 집계
 */

-- 코드 9-1 날짜별 매출과 평균 구매액을 집계하는 쿼리
select
    dt
    , count(*) as purchase_count
    , sum(purchase_amount) as total_amount
    , avg(purchase_amount) as avg_amount
from purchase_log
group by dt
order by dt;

-- 2. 이동평균을 사용한 날짜별 추이 보기
/*
 7일 동안의 평균 매출을 사용한 7일 이동평균으로 표현
 */

-- 코드 9-2 날짜별 매출과 7일 이동평균을 집계하는 쿼리
select
    dt
    , sum(purchase_amount) as total_amount
    -- 최근 최대 7일 동안의 평균 계산하기
    , avg(sum(purchase_amount))
        over(order by dt rows between 6 preceding and current row)
        as seven_day_avg
    -- 최근 7일 동안의 평균을 확실하게 계산하기
    , case
        when
            7 = count(*)
            over(order by dt rows between 6 preceding and current row )
        then
            avg(sum(purchase_amount))
            over(order by dt rows between 6 preceding and current row)
    end
    as seven_day_avg_strict
from purchase_log
group by dt
order by dt;

-- 3. 당월 매출 누계 구하기

-- 코드 9-3 날짜별 매출과 당월 누계 매출을 집계하는 쿼리

/*

sum(sum(purchase_amount))

바깥 sum은 윈도우 함수로 동작합니다.

안쪽 sum(purchase_amount)는 날짜별 합계(total_amount)를 의미합니다.

즉, "날짜별 합계를 다시 누적해서 더한다"는 뜻이에요.

over(...)
윈도우 함수의 범위를 지정하는 구문입니다.

partition by substring(dt, 1, 7)
→ dt에서 연-월(2014-01)을 추출해서, 같은 월끼리 묶습니다. 즉, 월별 누계를 계산하기 위한 그룹화.

order by dt
→ 날짜 순으로 정렬해서 누적합을 계산합니다.

rows unbounded preceding
→ "현재 행까지, 그 이전 모든 행을 포함"이라는 뜻. 즉, 누적합을 구하는 조건입니다.
 */
select
    dt
    -- '연-월' 추출하기
    -- PostgreSQL, Hive, Redshift, SparkSQL의 경우 substring로 '연-월' 부분 추출하기
    , substring(dt, 1, 7) as year_month
    , sum(purchase_amount) as total_amount
    , sum(sum(purchase_amount))
    -- PostgreSQL, Hive, Redshift, SparkSQL의 경우는 다음과 같다.
    over(partition by substring(dt, 1, 7) order by dt rows unbounded preceding)
    -- BigQuery의 경우 substring을 substr로 수정하기
    -- over(partition by substr(dt, 1, 7) order by dt rows unbounded preceding)
    as agg_amount
from purchase_log
group by dt
order by dt;

/*
 가독성 측면에서 수정할 수 있는 부분이 있음. 반복해서 나오는 SUM(purchase_amount)과 substring(dt, 1, 7)
 을 WITH 구문으로 외부로 빼고, 알기 쉽게 이름을 붙여주자.
 substring 함수로 연과 월을 추출하는 부분은 '연', '월', '일' 이라는 3개로 분할하고 결합하는 방법 사용
 */

-- 코드 9-4 날짜별 매출을 일시 테이블로 만드는 쿼리
 with
     daily_purchase as (
         select
             dt
            -- 연, 월, 일을 각각 추출하기
            , substring(dt, 1, 4) as year
            , substring(dt, 6, 2) as month
            , substring(dt, 9, 2) as date
            , sum(purchase_amount) as purchase_amount
         from purchase_log
         group by dt
     )
 select * from daily_purchase order by dt;

-- 코드 9-5 daily_purchase 테이블에 대해 당월 누계 매출을 집계하는 쿼리
with
    daily_purchase as (
        select
            dt
             -- 연, 월, 일을 각각 추출하기
             , substring(dt, 1, 4) as year
             , substring(dt, 6, 2) as month
             , substring(dt, 9, 2) as date
             , sum(purchase_amount) as purchase_amount
        from purchase_log
        group by dt
    )
    select
        dt
        , concat(year, '-', month) as year_month
        , purchase_amount
        , sum(purchase_amount)
            over(partition by year, month order by dt rows unbounded preceding)
        as agg_amount
from daily_purchase order by dt;

-- 4. 월별 매출의 작대비 구하기
/*
 월별 매출 추이를 추출해서 작년의 해당 월의 매출과 비교
 작년과 올해의 월별 매출을 각각 계산하고, 월로 결합해서 작대비를 계산하는 방법도 있지만,
 이번 절에서는 JOIN을 사용하지 않고 작대비를 계산하는 방법을 소개
 */

-- 코드 9-6 월별 매출과 작대비를 계산하는 쿼리
with
    daily_purchase as (
        select
            dt
             -- 연, 월, 일을 각각 추출하기
             , substring(dt, 1, 4) as year
             , substring(dt, 6, 2) as month
             , substring(dt, 9, 2) as date
             , sum(purchase_amount) as purchase_amount
        from purchase_log
        group by dt
    )
select
    month
    , sum(case year when '2014' then purchase_amount end) as amount_2014
    , sum(case year when '2015' then purchase_amount end) as amount_2015
    , 100.0
        * sum(case year when '2015' then purchase_amount end)
        / sum(case year when '2014' then purchase_amount end)
    as rate
from daily_purchase
group by month
order by month;

-- 5. Z 차트로 업적의 추이 확인하기

/*
 Z 차트는 '월차매출', '매출누계', '이동년계'라는 3개의 지표로 구성되어,
 계절 변동의 영향을 배제하고 트랜드를 분석하는 방법
 월차매출 : 매출 합계를 월별로 집계
 매출누계 : 해당 월의 매출에 이전월까지의 매출 누계를 합한 값
 이동년계 : 해당 월의 매출에 과거 11개월의 매출을 합한 값
 매출누계가 직선 : 월차매출이 일정, 오른쪽으로 갈수록 기울기가 급해지는 경우는 최근 매출 상승
 이동년계는 오른쪽 위로 올라간다면 매출이 오르는 경향
 */

-- 코드 9-7 2015년 매출에 대한 Z 차트를 작성하는 쿼리
with
    daily_purchase as (
        select
            dt
             -- 연, 월, 일을 각각 추출하기
             , substring(dt, 1, 4) as year
             , substring(dt, 6, 2) as month
             , substring(dt, 9, 2) as date
             , sum(purchase_amount) as purchase_amount
        from purchase_log
        group by dt
    )
    , monthly_purchase as (
        -- 월별 매출 집계하기
    select
        year
        , month
        , sum(purchase_amount) as amount
    from daily_purchase
    group by year, month
)
, calc_index as (
    select
        year
        , month
        , amount
        -- 2015년의 누계 매출 집계하기
        , sum(case when year = '2015' then amount end)
            over(order by year, month rows unbounded preceding)
        as agg_amount
        -- 당월부터 11개월 이전까지의 매출 합계(이동년계) 집계하기
        , sum(amount)
            over(order by year, month rows between 11 preceding and current row)
        as year_avg_amount
    from monthly_purchase
    order by year, month
)
-- 마지막으로 2015년의 데이터만 압축하기
select
    concat(year, '-', month) as year_month
    , amount
    , agg_amount
    , year_avg_amount
from calc_index
where
    year='2015'
order by year_month;

-- 6. 매출을 파악할 때 중요 포인트
/*
 매출이라는 결과의 원인이라고 할 수 있는 구매 횟수, 구매 단가 등의
 주변 데이터를 고려해야 '왜'라는 이유를 알 수 있음.
 */

-- 코드 9-8 매출과 관련된 지표를 집계하는 쿼리
with
    daily_purchase as (
        select
            dt
             -- 연, 월, 일을 각각 추출하기
             , substring(dt, 1, 4) as year
             , substring(dt, 6, 2) as month
             , substring(dt, 9, 2) as date
             , sum(purchase_amount) as purchase_amount
             , count(order_id) as orders
        from purchase_log
        group by dt
    ), monthly_purchase as (
        select
            year
            , month
            , sum(orders) as orders
            , avg(purchase_amount) as avg_amount
            , sum(purchase_amount) as monthly
        from daily_purchase
        group by year, month
)
select
    concat(year,'-',month) as year_month
    , orders
    , avg_amount
    , monthly
    , sum(monthly)
        over(partition by year order by month rows unbounded preceding)
        as agg_amount
        -- 12개월 전의 매출 구하기
    , lag(monthly, 12)
        over(order by year, month)
    as last_year
    -- 12개월 전의 매출과 비교해서 비율 구하기
    , 100.0
        * monthly
        / lag(monthly, 12)
        over (order by year, month)
    as rate
from monthly_purchase
order by year_month;

/*
 이번 예제를 윈도 함수 없이 작성하려면, 각각의 지표마다 select 구문을 만들고
 최종적으로 그 결과를 하나의 테이블로 결합해야 한다.
 하지만, select 구문을 여러 개 사용하면 데이터를 여러 번 읽어 들이므로 성능적으로 바람직하다고 할 수 없음
 현재 예제는 중간 테이블 monthly_purchase 테이블을 with 구문으로 만들 필요 없이, 하나의 select 구문으로도 곧바로
 최종 결과를 계산할 수 있음. 하지만 이렇게 계산 과정에 해당하는 컬럼도 임시 테이블을 사용해 만들어두면 가독성이 향상됨.
 */