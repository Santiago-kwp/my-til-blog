set search_path to sql_receipt;

/*
 이번 절에서는 사용자의 서비스 사용을 시계열로 수치화하고 변화를 시각화하는 방법을 소개
 샘플 데이터
 사용자 마스터와 액션 로그 테이블을 사용해 설명하며, SNS 서비스에서 쓰이는 데이터
 */

 -- 데이터 12-2 액션 로그(action_log)
drop table if exists action_log;
create table action_log(
    session char(5), -- 숫자 + 영문 조합 5자리 해시
    user_id char(4),
    action varchar(10), -- view, post, follow, like, comment
    stamp varchar(20) -- 2026.01 ~ 2026.02.05 까지 날짜+시간까지
);

insert into action_log values
                           ('037f2','U001','view','2026-01-03 18:00:00'),
                           ('s3h1d','U001','like','2026-01-03 18:05:31'),
                           ('s3h1d','U001','comment','2026-01-03 18:07:34'),
                           ('a1b2c','U002','view','2026-01-04 09:15:00'),
                           ('a1b2c','U002','follow','2026-01-04 09:20:10'),
                           ('d4e5f','U003','post','2026-01-04 14:30:00'),
                           ('d4e5f','U003','view','2026-01-04 14:35:00'),
                           ('g7h8i','U004','view','2026-01-05 11:00:00'),
                           ('g7h8i','U004','like','2026-01-05 11:02:00'),
                           ('g7h8i','U004','comment','2026-01-05 11:05:00'),
                           ('j0k1l','U005','view','2026-01-05 16:00:00'),
                           ('j0k1l','U005','post','2026-01-05 16:10:00'),
                           ('m3n4o',null,'view','2026-01-06 10:00:00'),
                           ('m3n4o',null,'view','2026-01-06 10:01:00'),
                           ('p6q7r','U006','view','2026-01-06 13:00:00'),
                           ('p6q7r','U006','like','2026-01-06 13:05:00'),
                           ('s9t0u','U007','view','2026-01-07 10:00:00'),
                           ('s9t0u','U007','follow','2026-01-07 10:10:00'),
                           ('v2w3x','U008','view','2026-01-07 15:00:00'),
                           ('v2w3x','U008','post','2026-01-07 15:20:00'),
                           ('y5z6a','U009','view','2026-01-08 09:00:00'),
                           ('y5z6a','U009','comment','2026-01-08 09:05:00'),
                           ('b8c9d','U010','view','2026-01-08 14:00:00'),
                           ('b8c9d','U010','like','2026-01-08 14:10:00'),
                           ('e1f2g','U011','view','2026-01-09 11:00:00'),
                           ('e1f2g','U011','post','2026-01-09 11:30:00'),
                           ('h4i5j',null,'view','2026-01-09 16:00:00'),
                           ('h4i5j',null,'view','2026-01-09 16:01:00'),
                           ('k7l8m','U012','view','2026-01-10 10:00:00'),
                           ('k7l8m','U012','follow','2026-01-10 10:10:00'),
                           ('n0p1q','U013','view','2026-01-10 14:00:00'),
                           ('n0p1q','U013','like','2026-01-10 14:05:00'),
                           ('r3s4t','U014','view','2026-01-11 11:00:00'),
                           ('r3s4t','U014','post','2026-01-11 11:40:00'),
                           ('u6v7w',null,'view','2026-01-11 15:00:00'),
                           ('u6v7w',null,'comment','2026-01-11 15:02:00'),
                           ('x9y0z','U015','view','2026-01-12 10:00:00'),
                           ('x9y0z','U015','like','2026-01-12 10:10:00');


-- 1. 등록 수의 추이와 경향 보기

-- 날짜별 등록 수의 추이
-- 코드 12-1 날짜별 등록 수의 추이를 집계하는 쿼리
select
    register_date
    , count(distinct user_id) as register_count
from mst_users
group by register_date
order by register_date;

-- 월별 등록 수 추이

-- 코드 12-2 매달 등록 수와 전월비를 계산하는 쿼리
with
    mst_users_with_year_month as (
        select
            *
            , substring(register_date, 1, 7) as year_month
        from mst_users
    )
select
    year_month
    , count(distinct user_id) as register_count
    , lag(count(distinct user_id)) over (order by year_month)
    as last_month_count
    , 1.0
        * count(distinct user_id)
        / lag(count(distinct user_id)) over(order by year_month)
    as month_over_month_ratio
from mst_users_with_year_month
group by year_month;

-- 등록 디바이스별 추이

-- 2. 지속률과 정착률 산출하기

/*
 지속률과 정착률의 정의
 지속률: 등록일 기준으로 이후 지정일 동안 사용자가 서비스를 얼마나 이용했는지 나타내는 지표
 정착률: 등록일 기준으로 이후 지정한 7일 동안 사용자가 서비스를 사용했는지 나타내는 지표
    정착은 지속과는 다르게 7일이라는 기간에 한 번이라도 서비스를 사용했다면 정착자로 다룸.
 */

-- 지속률과 정착률 사용 구분하기
/*
 지속률과 정착률의 사용 구분 포인트
 지속률 : 사용자가 매일 사용했으면 하는 서비스. Ex. 뉴스 사이트, 소셜 게임, SNS 등
 정착률 : 사용자에게 어떤 목적이 생겼을 때 사용했으면 하는 서비스. Ex. EC 사이트, 리뷰 사이트, Q&A 사이트, 사진 투고 사이트 등
 */

-- 코드 12-4 로그 최근 일자와 사용자별 등록일의 다음날을 계산하는 쿼리
with
    action_log_with_mst_users as (
        select
            u.user_id
            , u.register_date
            -- 액션 날짜와 로그 전체의 최신 날짜를 날짜 자료형으로 변환하기
            , cast(a.stamp as date) as action_date
            , max(cast(a.stamp as date)) over() latest_date
            -- 등록일 다음날의 날짜 계산하기
            , cast(u.register_date::date + '1 day'::interval as date) as next_day_1
        from mst_users u
        left outer join action_log as a
        on u.user_id = a.user_id
    )
select *
from action_log_with_mst_users
order by register_date;


-- 코드 12-5 사용자의 액션 플래그를 계산하는 쿼리
with
    action_log_with_mst_users as (
        select
            u.user_id
             , u.register_date
             -- 액션 날짜와 로그 전체의 최신 날짜를 날짜 자료형으로 변환하기
             , cast(a.stamp as date) as action_date
             , max(cast(a.stamp as date)) over() latest_date
             -- 등록일 다음날의 날짜 계산하기
             , cast(u.register_date::date + '1 day'::interval as date) as next_day_1
        from mst_users u
                 left outer join action_log as a
                                 on u.user_id = a.user_id
    )
, user_action_flag as (
    select
        user_id
        , register_date
        -- 등록일 다음날에 액션을 했는지 안 했는지를 플래그로 나타내기
        , sign(
          -- 사용자별로 등록일 다음날에 한 액션의 합계 구하기
            sum(
                -- 등록일 다음날이 로그의 최신 날짜 이전인지 확인하기
                case when next_day_1 <= latest_date then
                -- 등록일 다음날의 날짜에 액션을 했다면 1, 안 했다면 0 지정하기
                    case when next_day_1 = action_date then 1 else 0 end
                end
            )
          ) as next_1_day_action
    from action_log_with_mst_users
    group by user_id, register_date
)
select *
from user_action_flag;

/*
 when next_day_1 <= latest_date 코드가 없다면? (문제 상황)
만약 이 조건문이 없다고 가정하고, '2016-11-07'에 가입한 사용자가 있다고 상상해 봅시다.
사용자 정보
user_id: 'U-NEW'
register_date: '2016-11-07'
next_day_1 (등록일 다음날): '2016-11-08'
분석 로직 (조건문이 없을 경우)
이 'U-NEW' 사용자에 대해, 쿼리는 case when '2016-11-08' = action_date then 1 else 0 end를 계산합니다.
하지만 우리가 가진 action_log에는 '2016-11-08' 날짜의 데이터가 아예 존재하지 않습니다.
따라서 '2016-11-08' = action_date 조건은 항상 거짓(false)이 되고, 이 사용자는 모든 로그에 대해 0을 받게 됩니다.
결과적으로 sum(...)의 결과는 0이 되고, sign(0) 또한 0이 됩니다.
잘못된 결론
최종 결과 테이블에서 'U-NEW' 사용자의 next_1_day_action 플래그는 0이 됩니다.
분석가는 이 0을 보고 "이 사용자는 가입 다음 날 행동하지 않았다" 라고 해석하게 됩니다.
하지만 이것은 틀린 해석입니다. 이 사용자는 행동하지 않은 것이 아니라, 행동할 기회 자체가 없었습니다. 즉, 우리는 아직 11월 8일의 데이터를 관찰하지 못했을 뿐입니다.
 */


 -- 코드 12-6 다음날 지속률을 계산하는 쿼리
with
    action_log_with_mst_users as (
        select
            u.user_id
             , u.register_date
             -- 액션 날짜와 로그 전체의 최신 날짜를 날짜 자료형으로 변환하기
             , cast(a.stamp as date) as action_date
             , max(cast(a.stamp as date)) over() latest_date
             -- 등록일 다음날의 날짜 계산하기
             , cast(u.register_date::date + '1 day'::interval as date) as next_day_1
        from mst_users u
                 left outer join action_log as a
                                 on u.user_id = a.user_id
    )
   , user_action_flag as (
    select
        user_id
         , register_date
         -- 등록일 다음날에 액션을 했는지 안 했는지를 플래그로 나타내기
         , sign(
        -- 사용자별로 등록일 다음날에 한 액션의 합계 구하기
            sum(
                -- 등록일 다음날이 로그의 최신 날짜 이전인지 확인하기
                    case when next_day_1 <= latest_date then
                             -- 등록일 다음날의 날짜에 액션을 했다면 1, 안 했다면 0 지정하기
                             case when next_day_1 = action_date then 1 else 0 end
                        end
            )
           ) as next_1_day_action
    from action_log_with_mst_users
    group by user_id, register_date
)
select register_date
    , avg(100.0 * next_1_day_action) as repeat_rate_1_day
from user_action_flag
group by register_date
order by register_date;

-- 코드 12-7 지속률 지표를 관리하는 마스터 테이블을 작성하는 쿼리
with
    repeat_interval(index_name, interval_date) as (
        values
            ('01 day repeat', 1)
            , ('02 day repeat', 2)
            , ('03 day repeat', 3)
            , ('04 day repeat', 4)
            , ('05 day repeat', 5)
            , ('06 day repeat', 6)
            , ('07 day repeat', 7)
    )
select *
from repeat_interval
order by index_name;

-- 코드 12-8 지속률을 세로 기반으로 집계하는 쿼리
with
    repeat_interval(index_name, interval_date) as (
        values
        ('01 day repeat', 1)
             , ('02 day repeat', 2)
             , ('03 day repeat', 3)
             , ('04 day repeat', 4)
             , ('05 day repeat', 5)
             , ('06 day repeat', 6)
             , ('07 day repeat', 7)
    )
    , action_log_with_index_date as (select u.user_id
                                          , u.register_date
                                          -- 액션의 날짜와 로그 전체의 최신 날짜를 날짜 형식으로 변환하기
                                          , cast(a.stamp as date)                                                            as action_date
                                          , max(cast(a.stamp as date)) over ()                                               as latest_date
                                          -- 등록일로부터 n일 후의 날짜 계산하기
                                          , r.index_name
                                          , cast(cast(u.register_date as date) + interval '1 day' * r.interval_date as date) as index_date
                                     from mst_users as u
                                              left outer join action_log as a
                                                              on u.user_id = a.user_id
                                              cross join repeat_interval as r)
    , user_action_flag as (
        select
            user_id
            , register_date
            , index_name
            -- 등록일로부터 n일 후에 액션을 했는지 플래그로 나타내기
            , sign(
              -- 사용자별로 등록일로부터 n일 후에 한 액션의 합계 구하기
                sum(
                    -- 등록일로부터 n일 후가 로그의 최신 날짜 이전인지 확인하기
                    case when index_date <= latest_date then
                        -- 등록일로부터 n일 후의 날짜에 액션을 했다면 1, 아니라면 0 지정하기
                        case when index_date = action_date then 1 else 0 end
                    end
                )
              ) as index_date_action
        from action_log_with_index_date
        group by user_id, register_date, index_name, index_date
)
select
    register_date
    , index_name
    , avg(100.0 * index_date_action) as repeat_rate
from user_action_flag
group by register_date, index_name
order by register_date, index_name;

/*
 중요한 결과: 대부분의 데이터베이스(특히 이 구문이 사용되는 PostgreSQL 등)에서 DATE 타입에 INTERVAL(기간)을 더하면 그 결과는 TIMESTAMP 타입이 됩니다.
예시: '2016-10-01' (date) + interval '7 day' => '2016-10-08 00:00:00' (timestamp)
결과적으로 날짜뿐만 아니라 시간 정보(00:00:00)까지 포함된 값이 생성됩니다.
바깥쪽 cast( ... as date): 타임스탬프(TIMESTAMP)를 날짜(DATE)로 바꾼다. (이유: 다른 날짜 값과 정확하게 비교하기 위해)
 */

-- 정착률 관련 리포트
-- 매일의 n일 정착률 추이
/*
 대책이 의도한 대로의 효과가 있는지 확인하려면 정착률을 매일 집계한 리포트가 필요함.
 참고로 7일 정착률이 극단적으로 낮은 경우에는 정착률이 아니라 '다음날 지속률' ~ '7일 지속률'을 확인해서 문제를 검토하는 것이 일반적
 */

-- 코드 12-9 정착률 지표를 관리하는 마스터 테이블을 작성하는 쿼리
with
    repeat_interval(index_name, interval_begin_date, interval_end_date) as (
        values
            ('07 day retention', 1, 7)
            , ('14 day retention', 8, 14)
            , ('21 day retention', 15, 21)
             , ('28 day retention', 22, 28)
    )
select * from repeat_interval
order by index_name;

-- 코드 12-10 정착률을 계산하는 쿼리
with
    repeat_interval(index_name, interval_begin_date, interval_end_date) as (
        values
        ('07 day retention', 1, 7)
             , ('14 day retention', 8, 14)
             , ('21 day retention', 15, 21)
             , ('28 day retention', 22, 28)
    ), action_log_with_index_date as (
        select
            u.user_id
            , u.register_date
            , cast(a.stamp as date) as action_date
            , max(cast(a.stamp as date)) over() as latest_date
            , r.index_name
            -- 지표의 대상 기간 시작일과 종료일 계산하기
            , cast(u.register_date::date + '1day'::interval * r.interval_begin_date as date) as index_begin_date
            , cast(u.register_date::date + '1day'::interval * r.interval_end_date as date) as index_end_date
        from mst_users as u
        left outer join action_log as a
        on u.user_id = a.user_id
        cross join repeat_interval as r
)
, user_action_flag as (
    select
        user_id
        , register_date
        , index_name
        -- 지표의 대상 기간에 액션을 했는지 플래그로 나타내기
        , sign(
          -- 사용자 별로 대상 기간에 한 액션의 합계 구하기
            sum(
            -- 대상 기간의 종료일이 로그의 최신 날짜 이전인지 확인하기
                case when index_end_date <= latest_date then
                -- 지표의 대상 기간에 액션을 했다면 1, 안 했다면 0 지정하기
                    case when action_date between index_begin_date and index_end_date then 1 else 0 end
                end
            )
          ) as index_date_action
    from action_log_with_index_date
    group by user_id, register_date, index_name, index_begin_date, index_end_date
)
select
    register_date
    , index_name
    , avg(100.0 * index_date_action) as index_rate
from user_action_flag
group by register_date, index_name
order by register_date, index_name;

-- n일 지속률과 n일 정착률의 추이
/*
 n일 지속률과 n일 정착률을 따로 집계하면, 등록 후 며칠간 사용자가 안정적으로 서비스를 사용하는지,
 며칠 후에 서비스를 그만두는 사용자가 많아지는지 등을 알 수 있음.
 만약 지속률과 정착률이 극단적으로 떨어지는 시점이 있다면, 해당 시점을 기준으로 공지사항 등을 전달하거나
 n일 이상 사용한 사용자에게 보너스를 주는 등의 대책을 수행해서 지속률과 정착률이 다시 안정적으로 돌아오는 날까지 사용자를 붙잡을 수 있음
 */

-- 3. 지속과 정착에 영향을 주는 액션 집계하기
/*
 1일 지속률을 개선하려면 등록한 당일 사용자들이 무엇을 했는지 확인하면 됨.
 14일 정착률을 개선하고 싶다면 7일 정착률의 판정 기간 동안 사용자가 어떠한 행동을 했는지 조사하면 됨
 사용자의 1일 지속률이 높고, 비사용자의 1일 지속률이 낮은 액션이 1일 지속률에 더 영향을 준다고 할 수 있음.
 추가로 사용에 영향을 많이 주는 액션의 사용률이 낮다면, 사용자들이 해당 액션을 할 수 있게 설명을 추가하거나 이벤트를 통해 액션 사용을 촉진하고,
 사이트의 디자인과 동선 등도 함께 검토해야 함.

 각 액션에 대한 사용자와 비사용자의 다음날 지속률을 한꺼번에 계산하려면,
 모든 사용자와 모든 액션의 조합을 만든 뒤 사용자의 액션 실행 여부를 0과 1로 나타내는 테이블을 만들어 집계하는 것이 좋음.
 */

-- 코드 12-13 모든 사용자와 액션의 조합을 도출하는 쿼리

with
    repeat_interval(index_name, interval_begin_date, interval_end_date) as (
        values
        ('07 day retention', 1, 7)
             , ('14 day retention', 8, 14)
             , ('21 day retention', 15, 21)
             , ('28 day retention', 22, 28)
    ), action_log_with_index_date as (
    select
        u.user_id
         , u.register_date
         , cast(a.stamp as date) as action_date
         , max(cast(a.stamp as date)) over() as latest_date
         , r.index_name
         -- 지표의 대상 기간 시작일과 종료일 계산하기
         , cast(u.register_date::date + '1day'::interval * r.interval_begin_date as date) as index_begin_date
         , cast(u.register_date::date + '1day'::interval * r.interval_end_date as date) as index_end_date
    from mst_users as u
             left outer join action_log as a
                             on u.user_id = a.user_id
             cross join repeat_interval as r
)
   , user_action_flag as (
    select
        user_id
         , register_date
         , index_name
         -- 지표의 대상 기간에 액션을 했는지 플래그로 나타내기
         , sign(
        -- 사용자 별로 대상 기간에 한 액션의 합계 구하기
            sum(
                -- 대상 기간의 종료일이 로그의 최신 날짜 이전인지 확인하기
                    case when index_end_date <= latest_date then
                             -- 지표의 대상 기간에 액션을 했다면 1, 안 했다면 0 지정하기
                             case when action_date between index_begin_date and index_end_date then 1 else 0 end
                        end
            )
           ) as index_date_action
    from action_log_with_index_date
    group by user_id, register_date, index_name, index_begin_date, index_end_date
)
    , mst_actions as (
    select 'view' as action
    union all select 'comment' as action
    union all select 'follow' as action
)
    , mst_user_actions as (
    select
        u.user_id
        , u.register_date
        , a.action
    from mst_users as u
    cross join mst_actions as a
)
select *
from mst_user_actions
order by user_id, action;

-- 코드 12-14 사용자의 액션 로그를 0, 1의 플래그를 표현하는 쿼리
with
    repeat_interval(index_name, interval_begin_date, interval_end_date) as (
        values
        ('07 day retention', 1, 7)
             , ('14 day retention', 8, 14)
             , ('21 day retention', 15, 21)
             , ('28 day retention', 22, 28)
    ), action_log_with_index_date as (
    select
        u.user_id
         , u.register_date
         , cast(a.stamp as date) as action_date
         , max(cast(a.stamp as date)) over() as latest_date
         , r.index_name
         -- 지표의 대상 기간 시작일과 종료일 계산하기
         , cast(u.register_date::date + '1day'::interval * r.interval_begin_date as date) as index_begin_date
         , cast(u.register_date::date + '1day'::interval * r.interval_end_date as date) as index_end_date
    from mst_users as u
             left outer join action_log as a
                             on u.user_id = a.user_id
             cross join repeat_interval as r
)
   , user_action_flag as (
    select
        user_id
         , register_date
         , index_name
         -- 지표의 대상 기간에 액션을 했는지 플래그로 나타내기
         , sign(
        -- 사용자 별로 대상 기간에 한 액션의 합계 구하기
            sum(
                -- 대상 기간의 종료일이 로그의 최신 날짜 이전인지 확인하기
                    case when index_end_date <= latest_date then
                             -- 지표의 대상 기간에 액션을 했다면 1, 안 했다면 0 지정하기
                             case when action_date between index_begin_date and index_end_date then 1 else 0 end
                        end
            )
           ) as index_date_action
    from action_log_with_index_date
    group by user_id, register_date, index_name, index_begin_date, index_end_date
)
   , mst_actions as (
    select 'view' as action
    union all select 'comment' as action
    union all select 'follow' as action
)
   , mst_user_actions as (
    select
        u.user_id
         , u.register_date
         , a.action
    from mst_users as u
             cross join mst_actions as a
)
, register_action_flag as (
    select distinct
        m.user_id
        , m.register_date
        , m.action
        , case
            when a.action is not null then 1 else 0
            end as do_action
        , index_name
        , index_date_action
    from mst_user_actions as m
    left join action_log as a
    on m.user_id = a.user_id
    and cast(m.register_date as date) = cast(a.stamp as date)
    and m.action = a.action
    left join
        user_action_flag as f
        on m.user_id = f.user_id
    where
        f.index_date_action is not null
)
select * from register_action_flag
order by user_id, index_name, action;

/*
 do_action : 등록일에 follow, view 등의 액션 실행 여부
 index_date_action : 다음날 지속률 판정 기간(n일) 동안의 해당 액션 실행 여부
 */

 -- 코드 12-15 액션에 따른 지속률과 정착률을 집계하는 쿼리
with
    repeat_interval(index_name, interval_begin_date, interval_end_date) as (
        values
        ('07 day retention', 1, 7)
             , ('14 day retention', 8, 14)
             , ('21 day retention', 15, 21)
             , ('28 day retention', 22, 28)
    ), action_log_with_index_date as (
    select
        u.user_id
         , u.register_date
         , cast(a.stamp as date) as action_date
         , max(cast(a.stamp as date)) over() as latest_date
         , r.index_name
         -- 지표의 대상 기간 시작일과 종료일 계산하기
         , cast(u.register_date::date + '1day'::interval * r.interval_begin_date as date) as index_begin_date
         , cast(u.register_date::date + '1day'::interval * r.interval_end_date as date) as index_end_date
    from mst_users as u
             left outer join action_log as a
                             on u.user_id = a.user_id
             cross join repeat_interval as r
)
   , user_action_flag as (
    select
        user_id
         , register_date
         , index_name
         -- 지표의 대상 기간에 액션을 했는지 플래그로 나타내기
         , sign(
        -- 사용자 별로 대상 기간에 한 액션의 합계 구하기
            sum(
                -- 대상 기간의 종료일이 로그의 최신 날짜 이전인지 확인하기
                    case when index_end_date <= latest_date then
                             -- 지표의 대상 기간에 액션을 했다면 1, 안 했다면 0 지정하기
                             case when action_date between index_begin_date and index_end_date then 1 else 0 end
                        end
            )
           ) as index_date_action
    from action_log_with_index_date
    group by user_id, register_date, index_name, index_begin_date, index_end_date
)
   , mst_actions as (
    select 'view' as action
    union all select 'comment' as action
    union all select 'follow' as action
)
   , mst_user_actions as (
    select
        u.user_id
         , u.register_date
         , a.action
    from mst_users as u
             cross join mst_actions as a
)
   , register_action_flag as (
    select distinct
        m.user_id
                  , m.register_date
                  , m.action
                  , case
                        when a.action is not null then 1 else 0
        end as do_action
                  , index_name
                  , index_date_action
    from mst_user_actions as m
             left join action_log as a
                       on m.user_id = a.user_id
                           and cast(m.register_date as date) = cast(a.stamp as date)
                           and m.action = a.action
             left join
         user_action_flag as f
         on m.user_id = f.user_id
    where
        f.index_date_action is not null
)
select
    action
    , count(1) users
    , avg(100.0 * do_action) as usage_rate
    , index_name
    , avg(case do_action when 1 then 100.0 * index_date_action end) as idx_rate
    , avg(case do_action when 0 then 100.0 * index_date_action end) as no_action_idx_rate
from register_action_flag
group by index_name, action
order by index_name, action;

-- 4. 액션 수에 따른 정착률 집계하기
/* 등록일과 이후 7일 동안(7일 정착률 기간)에 실행한 액션 수에 따라
   14일 정착률이 어떻게 변화하는지 살펴보기
 */

-- 코드 12-16 액션의 계급 마스터와 사용자 액션 플래그의 조합을 산출하는 쿼리
with
    repeat_interval(index_name, interval_begin_date, interval_end_date) as (
        values
             ('14 day retention', 8, 14)

    ), action_log_with_index_date as (
    select
        u.user_id
         , u.register_date
         , cast(a.stamp as date) as action_date
         , max(cast(a.stamp as date)) over() as latest_date
         , r.index_name
         -- 지표의 대상 기간 시작일과 종료일 계산하기
         , cast(u.register_date::date + '1day'::interval * r.interval_begin_date as date) as index_begin_date
         , cast(u.register_date::date + '1day'::interval * r.interval_end_date as date) as index_end_date
    from mst_users as u
             left outer join action_log as a
                             on u.user_id = a.user_id
             cross join repeat_interval as r
)
   , user_action_flag as (
    select
        user_id
         , register_date
         , index_name
         -- 지표의 대상 기간에 액션을 했는지 플래그로 나타내기
         , sign(
        -- 사용자 별로 대상 기간에 한 액션의 합계 구하기
            sum(
                -- 대상 기간의 종료일이 로그의 최신 날짜 이전인지 확인하기
                    case when index_end_date <= latest_date then
                             -- 지표의 대상 기간에 액션을 했다면 1, 안 했다면 0 지정하기
                             case when action_date between index_begin_date and index_end_date then 1 else 0 end
                        end
            )
           ) as index_date_action
    from action_log_with_index_date
    group by user_id, register_date, index_name, index_begin_date, index_end_date
)
, mst_action_bucket(action, min_count, max_count) as (
    -- 액션 단계 마스터
    values
        ('comment', 0, 0)
        , ('comment', 1, 5)
         , ('comment', 6, 10)
         , ('comment', 11, 9999)
        , ('follow', 0, 0)
        , ('follow', 1, 5)
         , ('follow', 6, 10)
         , ('follow', 11, 9999)
)
, mst_user_action_bucket as (
    -- 사용자 마스터와 액션 단계 마스터 조합하기
    select u.user_id
         , u.register_date
         , a.action
         , a.min_count
         , a.max_count
    from mst_users as u
             cross join mst_action_bucket as a)
    select *
from mst_user_action_bucket
    order by user_id, action, min_count;

-- 코드 12-17 등록 후 7일 동안의 액션 수를 집계하는 쿼리
with
    repeat_interval(index_name, interval_begin_date, interval_end_date) as (
        values
            ('14 day retention', 8, 14)

    ), action_log_with_index_date as (
    select
        u.user_id
         , u.register_date
         , cast(a.stamp as date) as action_date
         , max(cast(a.stamp as date)) over() as latest_date
         , r.index_name
         -- 지표의 대상 기간 시작일과 종료일 계산하기
         , cast(u.register_date::date + '1day'::interval * r.interval_begin_date as date) as index_begin_date
         , cast(u.register_date::date + '1day'::interval * r.interval_end_date as date) as index_end_date
    from mst_users as u
             left outer join action_log as a
                             on u.user_id = a.user_id
             cross join repeat_interval as r
)
   , user_action_flag as (
    select
        user_id
         , register_date
         , index_name
         -- 지표의 대상 기간에 액션을 했는지 플래그로 나타내기
         , sign(
        -- 사용자 별로 대상 기간에 한 액션의 합계 구하기
            sum(
                -- 대상 기간의 종료일이 로그의 최신 날짜 이전인지 확인하기
                    case when index_end_date <= latest_date then
                             -- 지표의 대상 기간에 액션을 했다면 1, 안 했다면 0 지정하기
                             case when action_date between index_begin_date and index_end_date then 1 else 0 end
                        end
            )
           ) as index_date_action
    from action_log_with_index_date
    group by user_id, register_date, index_name, index_begin_date, index_end_date
)
   , mst_action_bucket(action, min_count, max_count) as (
    -- 액션 단계 마스터
    values
    ('comment', 0, 0)
         , ('comment', 1, 5)
         , ('comment', 6, 10)
         , ('comment', 11, 9999)
         , ('follow', 0, 0)
         , ('follow', 1, 5)
         , ('follow', 6, 10)
         , ('follow', 11, 9999)
)
   , mst_user_action_bucket as (
    -- 사용자 마스터와 액션 단계 마스터 조합하기
    select u.user_id
         , u.register_date
         , a.action
         , a.min_count
         , a.max_count
    from mst_users as u
             cross join mst_action_bucket as a)
    , register_action_flag as (
        -- 등록일에서 7일 후 까지의 액션 수를 세고,
        -- 액션 단계와 14일 정착 달성 플래그 계산하기
        select
            m.user_id
            , m.action
            , m.min_count
            , m.max_count
            , count(a.action) as action_count
            , case
                when count(a.action) between m.min_count and m.max_count then 1
                else 0
            end as achieve
            , index_name
            , index_date_action
        from mst_user_action_bucket as m
        left join action_log as a
        on m.user_id = a.user_id
        and cast(a.stamp as date)
            between cast(m.register_date as date)
            and cast(m.register_date as date) + interval '7 days'
        and m.action = a.action
        left join user_action_flag as f
        on m.user_id = f.user_id
        where
            f.index_date_action is not null
        group by
            m.user_id
            , m.action
            , m.min_count
            , m.max_count
            , f.index_name
            , f.index_date_action
)
select *
from register_action_flag
order by user_id, action, min_count;

-- 코드 12-18 등록 후 7일 동안의 액션 횟수별로 14일 정착률을 집계하는 쿼리
with
    repeat_interval(index_name, interval_begin_date, interval_end_date) as (
        values
            ('14 day retention', 8, 14)

    ), action_log_with_index_date as (
    select
        u.user_id
         , u.register_date
         , cast(a.stamp as date) as action_date
         , max(cast(a.stamp as date)) over() as latest_date
         , r.index_name
         -- 지표의 대상 기간 시작일과 종료일 계산하기
         , cast(u.register_date::date + '1day'::interval * r.interval_begin_date as date) as index_begin_date
         , cast(u.register_date::date + '1day'::interval * r.interval_end_date as date) as index_end_date
    from mst_users as u
             left outer join action_log as a
                             on u.user_id = a.user_id
             cross join repeat_interval as r
)
   , user_action_flag as (
    select
        user_id
         , register_date
         , index_name
         -- 지표의 대상 기간에 액션을 했는지 플래그로 나타내기
         , sign(
        -- 사용자 별로 대상 기간에 한 액션의 합계 구하기
            sum(
                -- 대상 기간의 종료일이 로그의 최신 날짜 이전인지 확인하기
                    case when index_end_date <= latest_date then
                             -- 지표의 대상 기간에 액션을 했다면 1, 안 했다면 0 지정하기
                             case when action_date between index_begin_date and index_end_date then 1 else 0 end
                        end
            )
           ) as index_date_action
    from action_log_with_index_date
    group by user_id, register_date, index_name, index_begin_date, index_end_date
)
   , mst_action_bucket(action, min_count, max_count) as (
    -- 액션 단계 마스터
    values
    ('comment', 0, 0)
         , ('comment', 1, 5)
         , ('comment', 6, 10)
         , ('comment', 11, 9999)
         , ('follow', 0, 0)
         , ('follow', 1, 5)
         , ('follow', 6, 10)
         , ('follow', 11, 9999)
)
   , mst_user_action_bucket as (
    -- 사용자 마스터와 액션 단계 마스터 조합하기
    select u.user_id
         , u.register_date
         , a.action
         , a.min_count
         , a.max_count
    from mst_users as u
             cross join mst_action_bucket as a)
   , register_action_flag as (
    -- 등록일에서 7일 후 까지의 액션 수를 세고,
    -- 액션 단계와 14일 정착 달성 플래그 계산하기
    select
        m.user_id
         , m.action
         , m.min_count
         , m.max_count
         , count(a.action) as action_count
         , case
               when count(a.action) between m.min_count and m.max_count then 1
               else 0
        end as achieve
         , index_name
         , index_date_action
    from mst_user_action_bucket as m
             left join action_log as a
                       on m.user_id = a.user_id
                           and cast(a.stamp as date)
                              between cast(m.register_date as date)
                              and cast(m.register_date as date) + interval '7 days'
                           and m.action = a.action
             left join user_action_flag as f
                       on m.user_id = f.user_id
    where
        f.index_date_action is not null
    group by
        m.user_id
           , m.action
           , m.min_count
           , m.max_count
           , f.index_name
           , f.index_date_action
)
select
    action
    , min_count || ' ~ ' || max_count as count_range
    , sum(case achieve when 1 then 1 else 0 end) as achieve
    , index_name
    , avg(case achieve when 1 then 100.0 * index_date_action end) as achieve_index_rate
from register_action_flag
group by index_name, action, min_count, max_count
order by index_name, action, min_count;


-- 5. 사용 일수에 따른 정착률 집계하기
/*
 7일 정착 기간 동안 사용자가 며칠 사용했는지가 이후 정착률에 어떠한 영향을 주는지 확인하는 방버
 리포트 예시
 - 약 70%의 사용자가 7일 정착 판정 기간(등록 다음날부터 7일 이내)에 1~4일밖에 사용하지 않았다.
 - 7일 정착 판정 기간 동안 1일밖에 사용하지 않은 사용자의 28일 정착률은 20.8%이다.
 - 5일 동안 사용한 사용자의 28일 정착률은 45%이다.
 - 그런데 6일 동안 사용한 사용자의 28일 정착률은 55.5%로, 5일 동안 사용자와 비교해서 10.5% 높다는 것을 알 수 있다.
 => 등록 후 7일 동안 사용자가 계속해서 사용하게 만드는 대책 등을 세울 수 있음.
 예를 들어, 소셜 게임이라면, 등록 직후 사용자에게 1~5일 동안 연속 접속 로그인 보상 등을 제공하고
 6일이 되었을 때는 굉장히 큰 보너스를 주어서 어떻게든 6일간 계속해서 사용하도록 만드는 대책을 세울 수 있음.
 */

-- 6. 사용자의 잔존율 집계하기
/*
 서비스 등록 수개월 후에 어느 정도 비율의 사용자가 서비스를 지속해서 사용하는지 대략적으로라도 파악해두면,
 서비스에 어떤 문제가 있는지 찾아내거나, 과거와 현재를 비교하고 미래 목표에 대한 전망을 검토할 수 있음
 */

-- 표 12-11 사용자의 잔존율 예시
/*
        | 2025.01 | 02 | 03 | 04 | 05 | 06
 2015.01|  100%   |
      02|  90%    |100%|
      03|   75%   | 80%|100%|
      ...

- 이전과 비교해 n개월 후의 잔존율이 내려갔다면?
  . 신규 등록자가 서비스를 사용하기 위한 장벽이 높아지지는 않았는지 확인하기
- n개월 후에 잔존율이 갑자기 낮아지는 경향이 있다면?
  . 서비스의 사용 목적을 달성하는 기간이 예상보다 너무 짧지는 않은지 확인하기
- 오래 사용하던 사용자인데도 특정 월을 기준으로 사용하지 않게 되었다면?
  . 사용자가 서비스 내부에서의 경쟁 등으로 빨리 지친 것은 아닌지 확인하기
 */


-- 코드 12-21 12개월 후까지의 월을 도출하기 위한 보조 테이블을 만드는 쿼리
with
    mst_intervals(interval_month) as (
        values (1), (2), (3), (4), (5), (6), (7)
        , (8), (9), (10), (11), (12)
    )
, mst_users_with_index_month as (
    -- 사용자 마스터에 등록 월부터 12개월 후까지의 월을 추가하기
    select
        u.user_id
        , u.register_date
        , cast(u.register_date::date + i.interval_month * '1 month'::interval as date) as index_date
        , substring(u.register_date, 1, 7) as register_month
        , substring(cast(u.register_date::date + i.interval_month * '1 month'::interval as text), 1, 7) as index_month
    from mst_users as u
    cross join mst_intervals as i
)
, action_log_in_month as (
    -- 액션 로그의 날짜에서 월 부분만 추출하기
    select distinct
        user_id
        , substring(stamp, 1, 7) as action_month
    from action_log
)
select
    -- 사용자 마스터와 액션 로그를 결합한 뒤, 월별로 잔존율 집계하기
    u.register_month
    , u.index_month
    , sum(case when a.action_month is not null then 1 else 0 end) as users
    , avg(case when a.action_month is not null then 100.0 else 0.0 end) as retention_rate
from mst_users_with_index_month as u
left join action_log_in_month as a
on u.user_id = a.user_id
and u.index_month = a.action_month
group by u.register_month, u.index_month
order by u.register_month, u.index_month;

-- 7. 방문 빈도를 기반으로 사용자 속성을 정의하고 집계하기

-- MAU
/*
 특정 월에 서비스를 사용한 사용자 수를 MAU(Monthly Active Users)라고 부름.
 MAU를 3개로 나누어 분석하기
 - 신규 사용자 : 이번 달에 등록한 사용자
 - 리피트 사용자 : 이전 달에도 사용했던 사용자
 - 컴백 사용자 : 이번 달의 신규 등록자가 아니고, 이전 달에도 사용하지 않았던, 한동안 사용하지 않았다가 돌아온 사용자

 리피트 사용자를 3가지로 분류하기
 - 신규 리피트 사용자 : 이전 달에는 신규 사용자로 분류되었으며, 이번 달에도 사용한 사용자
 - 기존 리피트 사용자 : 이전 달도 리피트 사용자로 분류되었으며, 이번 달에도 사용한 사용자
 - 컴백 리피트 사용자 : 이전 달에 컴백 사용자로 분류되었으며, 이번 달에도 사용한 사용자
 */

-- MAU 속성별 반복률 계산하기
/*
 반복률 :
 - 신규 반복 MAU 반복률 : 이전 달에 신규 사용자이면서 해당 월에 신규 리피트 사용자인 사용자의 비율
 - 기존 반복 MAU 반복률 : 이전 달에 기존 사용자이면서 해당 월에 기존 리피트 사용자인 사용자의 비율
 - 컴백 반복 MAU 반복률 : 이전 달에 컴백 사용자이면서 해당 월에 컴백 리피트 사용자인 사용자의 비율

 */


-- 8. 방문 종류를 기반으로 성장지수 집계하기
/*
 서비스를 운영할 때는 사용자 등록을 포함해 사용자의 지속 사용, 리텐션 등을 높일 수 있는 대책과 서비스 성장을 가속시키기 위한 팀 존재
 일반적으로 이러한 팀을 그로스 해킹(Growth Hacking) 팀이라고 부름
 */

-- 성장 지수
/*
 성장지수는 사용자의 서비스 사용과 관련한 상태 변화를 수치화해서 서비스가 성장하는지 알려주는 지표
 성장지수가 1이상이라면 서비스가 성장한다는 뜻이며, 0보다 낮다면 서비스가 퇴보중이라는 뜻
 */

-- 표 12-13 서비스 사용과 관련한 상태 변화 패턴
/*
 Signup : 회원가입
 Deactivation : 액티브 유저가 비액티브 유저가 되었음
 Reactivation : 비액티브 유저가 액티브 유저로 돌아옴
 Exit : 서비스를 탈퇴하거나 사용을 중지함.
 */

-- 성장지수 계산 방법 예시
-- 성장지수 : Signup + Reactivation - Deactivation - Exit

/*
 성장지수 집계하기
 신규 등록인가(is_new)
 탈퇴 회원인가(is_exit)
 특정 날짜에 서비스에 접근했는가? (is_access)
 전날 서비스에 접근했는가? (was_access)
 */


