set search_path to sql_receipt;

-- 10강 다면적인 축을 사용해 데이터 집약하기
/*
 매출의 시계열뿐만 아니라 상품의 카테고리, 가격 등을 조합해서 데이터의 특징을 추출해 리포팅하는 방법을 소개
 EC 사이트를 가정해서 샘플 데이터 생성
 EC 사이트는 한 번 주문으로 여러 상품을 구매할 수 있음.
 따라서 하나의 order_id에 여러 정보가 포함되어 있음.
 */

drop table if exists purchase_detail_log;
create table purchase_detail_log(
    dt varchar(20),
    order_id bigint,
    user_id varchar(20),
    item_id varchar(20),
    price bigint,
    category varchar(20),
    sub_category varchar(20)
);

insert into purchase_detail_log values
                                    ('2017-01-08', 48291, 'usr33395', 'lad533', 37300, 'ladys_fashion', 'bag'),
                                    ('2017-01-10', 50001, 'usr12345', 'men123', 25000, 'mens_fashion', 'shirt'),
                                    ('2017-01-10', 50001, 'usr12345', 'acc456', 12000, 'accessories', 'earring'),
                                    ('2017-01-11', 50002, 'usr67890', 'kid789', 18000, 'kids_fashion', 'toy'),
                                    ('2017-01-11', 50002, 'usr67890', 'ele012', 89000, 'electronics', 'headphone'),
                                    ('2017-01-11', 50002, 'usr67890', 'bty345', 34000, 'beauty', 'lipstick'),
                                    ('2017-01-12', 50003, 'usr54321', 'bks678', 15000, 'books', 'fiction'),
                                    -- 추가 데이터
                                    ('2017-01-13', 50004, 'usr11111', 'ele012', 89000, 'electronics', 'headphone'),
                                    ('2017-01-13', 50004, 'usr11111', 'lad533', 38000, 'ladys_fashion', 'bag'),
                                    ('2017-01-13', 50004, 'usr11111', 'men123', 26000, 'mens_fashion', 'shirt'),
                                    ('2017-01-13', 50004, 'usr11111', 'bks678', 15500, 'books', 'fiction'),
                                    ('2017-01-14', 50005, 'usr22222', 'ele012', 91000, 'electronics', 'headphone'),
                                    ('2017-01-14', 50005, 'usr22222', 'ele200', 120000, 'electronics', 'tv'),
                                    ('2017-01-14', 50005, 'usr22222', 'bty345', 35000, 'beauty', 'lipstick'),
                                    ('2017-01-14', 50005, 'usr22222', 'bty400', 22000, 'beauty', 'cream'),
                                    ('2017-01-14', 50005, 'usr22222', 'acc456', 12500, 'accessories', 'earring'),
                                    ('2017-01-15', 50006, 'usr33333', 'lad533', 39000, 'ladys_fashion', 'bag'),
                                    ('2017-01-15', 50006, 'usr33333', 'lad600', 55000, 'ladys_fashion', 'dress'),
                                    ('2017-01-15', 50006, 'usr33333', 'men123', 27000, 'mens_fashion', 'shirt'),
                                    ('2017-01-15', 50006, 'usr33333', 'men300', 45000, 'mens_fashion', 'pants'),
                                    ('2017-01-15', 50006, 'usr33333', 'kid789', 19000, 'kids_fashion', 'toy'),
                                    ('2017-01-15', 50006, 'usr33333', 'kid800', 28000, 'kids_fashion', 'clothes'),
                                    ('2017-01-16', 50007, 'usr44444', 'bks678', 16000, 'books', 'fiction'),
                                    ('2017-01-16', 50007, 'usr44444', 'bks700', 21000, 'books', 'non-fiction'),
                                    ('2017-01-16', 50007, 'usr44444', 'ele012', 92000, 'electronics', 'headphone'),
                                    ('2017-01-16', 50007, 'usr44444', 'acc456', 13000, 'accessories', 'earring'),
                                    ('2017-01-16', 50007, 'usr44444', 'lad533', 40000, 'ladys_fashion', 'bag'),
                                    -- 2017년 2월 데이터
                                    ('2017-02-01', 50008, 'usr55555', 'men123', 28000, 'mens_fashion', 'shirt'),
                                    ('2017-02-01', 50008, 'usr55555', 'bks678', 17000, 'books', 'fiction'),
                                    ('2017-02-03', 50009, 'usr66666', 'ele012', 93000, 'electronics', 'headphone'),
                                    ('2017-02-03', 50009, 'usr66666', 'kid789', 20000, 'kids_fashion', 'toy'),
                                    ('2017-02-05', 50010, 'usr77777', 'lad533', 41000, 'ladys_fashion', 'bag'),
                                    ('2017-02-05', 50010, 'usr77777', 'bty345', 36000, 'beauty', 'lipstick'),
                                    ('2017-02-10', 50011, 'usr88888', 'ele200', 125000, 'electronics', 'tv'),
                                    ('2017-02-10', 50011, 'usr88888', 'acc456', 14000, 'accessories', 'earring'),
                                    -- 2017년 3월 데이터
                                    ('2017-03-02', 50012, 'usr99999', 'bks700', 22000, 'books', 'non-fiction'),
                                    ('2017-03-02', 50012, 'usr99999', 'lad600', 56000, 'ladys_fashion', 'dress'),
                                    ('2017-03-02', 50012, 'usr99999', 'men300', 46000, 'mens_fashion', 'pants'),
                                    ('2017-03-08', 50013, 'usr10101', 'kid800', 29000, 'kids_fashion', 'clothes'),
                                    ('2017-03-15', 50014, 'usr12121', 'bty400', 23000, 'beauty', 'cream'),
                                    ('2017-03-15', 50014, 'usr12121', 'lad533', 42000, 'ladys_fashion', 'bag'),
                                    -- 2017년 4월 데이터
                                    ('2017-04-01', 50015, 'usr13131', 'ele012', 95000, 'electronics', 'headphone'),
                                    ('2017-04-01', 50015, 'usr13131', 'men123', 29000, 'mens_fashion', 'shirt'),
                                    ('2017-04-04', 50016, 'usr14141', 'acc456', 15000, 'accessories', 'earring'),
                                    ('2017-04-04', 50016, 'usr14141', 'bks678', 18000, 'books', 'fiction'),
                                    ('2017-04-10', 50017, 'usr15151', 'bty345', 37000, 'beauty', 'lipstick'),
                                    ('2017-04-10', 50017, 'usr15151', 'kid789', 21000, 'kids_fashion', 'toy');


-- 1. 카테고리별 매출과 소계 계산하기
-- 코드 10-1 카테고리별 매출과 소계를 동시에 구하는 쿼리
with
    sub_category_amount as (
        -- 소 카테고리의 매출 집계하기
        select
            category as category
            , sub_category as sub_category
            , sum(price) as amount
        from purchase_detail_log
        group by category, sub_category
    )
    , category_amount as (
    -- 대 카테고리의 매출 집계하기
    select category
         , 'all'      as sub_category
         , sum(price) as amount
    from purchase_detail_log
    group by category
    )
, total_amount as (
    -- 전체 매출 집계하기
    select
        'all' as category
        , 'all' as sub_category
        , sum(price) as amount
    from purchase_detail_log
)
        select category, sub_category, amount from sub_category_amount
union all select category, sub_category, amount from category_amount
union all select category, sub_category, amount from total_amount;

/*
 위와 같은 SQL을 사용하면 하나의 쿼리로 카테고리별 소계와 총계를 동시에 계산할 수 있음.
 그런데 UNION ALL을 사용해 테이블을 결합하는 방법은 테이블을 여러 번 불러오고,
 데이터를 결합하는 비용도 발생하므로 성능이 좋지 않음.
 SQL99에서 도입된 'ROLLUP'을 구현하는 PostgreSQL, Hive, SparkSQL에서는 조금 더 쉽고 성능 좋은 쿼리를 만들 수 있음
 */

 -- 코드 10-2 ROLLUP을 사용해서 카테고리별 매출과 소계를 동시에 구하는 쿼리
select
    coalesce(category,'all') as category
    , coalesce(sub_category, 'all') as sub_category
    , sum(price) as amount
from purchase_detail_log
group by
    rollup(category, sub_category);

/*
 ROLLUP은 GROUP BY의 확장으로, 지정한 컬럼을 단계적으로 그룹화해서 소계와 총계를 자동으로 계산합니다.

ROLLUP(category, sub_category) →
소카테고리별 합계
대카테고리별 합계
전체 합계

UNION ALL로 여러 번 집계하는 것보다 훨씬 간단하고 성능도 좋습니다.
 */

 -- 2. ABC 분석으로 잘 팔리는 상품 판별하기
/*
 ABC 분석은 재고 관리 등에서 사용하는 분석 방법. 매출 중요도에 따라 상품을 나누고,
 그에 맞게 전략을 만들 때 사용함.
 예를 들어, 매출의 70%는 상위 5개의 상품으로 구성되어 있다는 것을 알 수 있음.
 일반적으로 상위 70%를 A등급, 상위 70 ~ 90% 를 B 등급, 상위 90 ~ 100% 를 C 등급
 */

/*
 데이터를 작성하는 방법은 다음과 같음.
 1. 매출이 높은 순서로 데이터를 정렬
 2. 매출 합계를 집계
 3. 매출 합계를 기반으로 각 데이터가 차지하는 비율을 계산하고, 구성비를 구함
 4. 계산한 카테고리의 구성비를 기반으로 구성비누계를 구함.

 등급까지 SQL에서 구하면, 등급 분류 방법이 변경되었을 때 SQL을 수정해야 함.
 따라서 SQL이 아니라, 리포트를 만드는 쪽에서 등급을 나누는 편이 좋음.
 */

-- 코드 10-3 매출 구성비누계와 ABC 등급을 계산하는 쿼리
with
    monthly_sales as (
        select
            category
            -- 항목별 매출 계산하기
            , sum(price) as amount
        from purchase_detail_log
        where
            dt between '2017-01-01' and '2017-01-31'
        group by category
    )
    , sales_composition_ratio as (
        select
            category
            , amount
            -- 구성비: 100.0 * <항목별 매출> / <전체 매출>
            , 100.0 * amount / sum(amount) over() as composition_ratio
            -- 구성비 누계: 100.0 * <항목별 구계 매출> / <전체 매출>
            , 100.0 * sum(amount) over(order by amount desc)
            / sum(amount) over() as cumulative_ratio
        from monthly_sales
)
select
    *
    -- 구성비 누계 범위에 따라 순위 붙이기
    , case
        when cumulative_ratio between 0 and 70 then 'A'
        when cumulative_ratio between 70 and 90 then 'B'
        when cumulative_ratio between 90 and 100 then 'C'
    end as abc_rank
from sales_composition_ratio
order by amount desc;

-- 3. 팬 차트로 상품의 매출 증가율 확인하기
/*
 팬 차트란 어떤 기준 시점을 100%로 두고, 이후의 숫자 변동을 확인할 수 있게 해주는 그래프
 예를 들어 상품 또는 카테고리별 매출 금액의 추이를 판단하는 경우,
 매출 금액이 크면 쉽게 경향을 판단할 수 있지만 작은 변화는 그래프에서 변화를 확인하기조차 어려움
 이로 인해 트렌드 변화와 성장 분야를 놓칠 수 있음.
 */

-- 코드 10-4 팬 차트 작성 때 필요한 데이터를 구하는 쿼리
with
    daily_category_amount as (
        select
            dt
            , category
            , substring(dt, 1, 4) as year
            , substring(dt, 6, 2) as month
            , substring(dt, 9, 2) as date
            , sum(price) as amount
            from purchase_detail_log
            group by dt, category
    )
    , monthly_category_amount as (
        select
            concat(year, '-', month) as year_month
            , category
            , sum(amount) as amount
        from daily_category_amount
        group by year, month, category
)
select
    year_month
    , category
    , amount
    , first_value(amount)
        over(partition by category order by year_month, category rows unbounded preceding)
    as base_amount
    , 100.0
        * amount
        / first_value(amount) over (partition by category order by year_month, category rows unbounded preceding) as rate
from monthly_category_amount
order by year_month, category;

/*
 팬 차트를 만들 때 확실히 해두어야 하는 것은, 어떤 시점에서의 매출 금액을 기준점으로 채택할 것인가
 반드시 근거를 가지고 기준점을 채택해야 한다.
 */

-- 4. 히스토그램으로 구매 가격대 집계하기

/*
 히스토그램을 만들려면 일단 다음과 같은 도수 분포표를 만들어야 한다.
 1. 최댓값, 최솟값, 범위(최댓값 - 최솟값)를 구한다.
 2. 범위를 기반으로 몇 개의 계급으로 나눌지 결정하고, 각 계급의 하한과 상한을 구한다.
 3. 각 계급에 들어가는 데이터 개수(도수)를 구하고, 이를 표로 정리한다.
 */

-- 임의의 계층 수로 히스토그램 만들기
-- 코드 10-5 최댓값, 최솟값, 범위를 구하는 쿼리
with
    stats as (
        select
            max(price) as max_price
            , min(price) as min_price
            , max(price) - min(price) as range_price
            -- 계층 수
            , 10 as bucket_num
        from purchase_detail_log
    )
select * from stats;

/*
 참고로 SQL 관련 시스템은 대부분 히스토그램을 작성하는 함수가 표준 제공됨.
 예를 들어 PostgreSQL은 앞의 과정을 width_bucket 함수로 한 번에 구할 수 있음
 */

 -- 코드 10-6 데이터의 계층을 구하는 쿼리
with
    stats as (
        select
            max(price) as max_price
             , min(price) as min_price
             , max(price) - min(price) as range_price
             -- 계층 수
             , 10 as bucket_num
        from purchase_detail_log
    )
    , purcase_log_with_bucket as (
        select
            price
            , min_price
            , price - min_price as diff
            , 1.0 * range_price / bucket_num as bucket_range
            -- 계층 판정 : FLOOR(<정규화 금액> / <계층 범위>)
            , floor(
              1.0 * (price - min_price)
              / (1.0 * range_price / bucket_num)
              -- index가 1부터 시작하므로 1만큼 더하기
              ) + 1 as bucket
        from purchase_detail_log, stats
)
select *
from purcase_log_with_bucket
order by price;

/*
 위의 출력 결과에서는 계급 범위를 10으로 지정했으므로 최댓값은 '11'로 판정됨.
 모든 레코드가 지정한 범위 내부에 들어갈 수 있게 쿼리를 개선
 */

 -- 코드 10-7 계급 상한 값을 조정한 쿼리
with
    stats as (
        select
            max(price) + 1 as max_price
             , min(price) as min_price
             , max(price) + 1 - min(price) as range_price
             -- 계층 수
             , 10 as bucket_num
        from purchase_detail_log
    )
   , purcase_log_with_bucket as (
    select
        price
         , min_price
         , price - min_price as diff
         , 1.0 * range_price / bucket_num as bucket_range
         -- 계층 판정 : FLOOR(<정규화 금액> / <계층 범위>)
         , floor(
                   1.0 * (price - min_price)
                       / (1.0 * range_price / bucket_num)
               -- index가 1부터 시작하므로 1만큼 더하기
           ) + 1 as bucket
    from purchase_detail_log, stats
)
select *
from purcase_log_with_bucket
order by price;


-- 코드 10-8 히스토그램을 구하는 쿼리
with
    stats as (
        select
            max(price) + 1 as max_price
             , min(price) as min_price
             , max(price) + 1 - min(price) as range_price
             -- 계층 수
             , 10 as bucket_num
        from purchase_detail_log
    )
   , purcase_log_with_bucket as (
    select
        price
         , min_price
         , price - min_price as diff
         , 1.0 * range_price / bucket_num as bucket_range
         -- 계층 판정 : FLOOR(<정규화 금액> / <계층 범위>)
         , floor(
                   1.0 * (price - min_price)
                       / (1.0 * range_price / bucket_num)
               -- index가 1부터 시작하므로 1만큼 더하기
           ) + 1 as bucket
    from purchase_detail_log, stats
)
select bucket
    , min_price + bucket_range * (bucket -1) as lower_limit
    , min_price + bucket_range * bucket as upper_limit
    -- 도수 세기
    , count(price) as num_purchase
    -- 합계 금액 계산하기
    , sum(price) as total_amount
from purcase_log_with_bucket
group by
    bucket, min_price, bucket_range
order by bucket;


-- 임의의 계층 너비로 히스토그램 작성하기
/*
 소수점으로 계층을 구분한 리포트는 직감적이지 않음.
 리포트를 만들 때는 리포트를 받아 보는 쪽에서도 쉽게 이해하고 납득할 수 있게 계층을 구분하는 것이 좋음

 */

-- 코드 10-9 히스토그램의 상한과 하한을 수동으로 조정한 쿼리
with
    stats as (
        select
            -- 금액의 최댓값
            100000 as max_price
            -- 금액의 최솟값
             , 0 as min_price
            -- 금액의 범위
             , 100000 as range_price
             -- 계층 수
             , 10 as bucket_num
        from purchase_detail_log
    )
   , purcase_log_with_bucket as (
    select
        price
         , min_price
         , price - min_price as diff
         , 1.0 * range_price / bucket_num as bucket_range
         -- 계층 판정 : FLOOR(<정규화 금액> / <계층 범위>)
         , floor(
                   1.0 * (price - min_price)
                       / (1.0 * range_price / bucket_num)
               -- index가 1부터 시작하므로 1만큼 더하기
           ) + 1 as bucket
    from purchase_detail_log cross join stats
)
select bucket
     , min_price + bucket_range * (bucket -1) as lower_limit
     , min_price + bucket_range * bucket as upper_limit
     -- 도수 세기
     , count(price) as num_purchase
     -- 합계 금액 계산하기
     , sum(price) as total_amount
from purcase_log_with_bucket
group by
    bucket, min_price, bucket_range
order by bucket;

-- 위의 중복 문제 수정 코드
with stats as (
    select
        100000 as max_price,
        0 as min_price,
        100000 as range_price,
        10 as bucket_num
)
   , purcase_log_with_bucket as (
    select
        p.price,
        s.min_price,
        p.price - s.min_price as diff,
        1.0 * s.range_price / s.bucket_num as bucket_range,
        floor(
                1.0 * (p.price - s.min_price) / (1.0 * s.range_price / s.bucket_num)
        ) + 1 as bucket
    from purchase_detail_log p
             cross join stats s
)
select bucket,
       min_price + bucket_range * (bucket -1) as lower_limit,
       min_price + bucket_range * bucket as upper_limit,
       count(*) as num_purchase,
       sum(price) as total_amount
from purcase_log_with_bucket
group by bucket, min_price, bucket_range
order by bucket;

/*
 히스토그램이 나누어진 경우
 히스토그램 산이 2개로 나누어진 경우가 있을 수 도 있음.
 이런 경우에는 서로 다른 모집단을 기반으로, 하나의 데이터를 도출한 경우일 수 있음.
 
 */
