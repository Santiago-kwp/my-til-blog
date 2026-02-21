set search_path to sql_receipt;

-- 8강 여러 개의 테이블 조작하기
/*
 * 여러 개의 테이블을 조작할 때는 SQL이 복잡해지기 쉬움. 이러한 SQL을 간단하고 가독성 높게 작성하는 방법과 부족한 데이터를 보완하는 방법 소
 */

/* 업무 데이터를 사용하는 경우
 * 예를 들어 SNS 사이트를 생각해보자. '댓글','좋아요','팔로우'라는 각각의 테이블에 저장된 정보를 기반으로 '사용자가 어떤 행동을 하는가'를 분석하고 싶으면 이런 테이블들을 하나로 합쳐서 다루어야 합니다.
 *
 */

-- 로그 데이터를 사용하는 경우
/* 다양한 행동을 기록하는 하나의 거대한 로그 파일이 하나의 테이블에 저장된 경우에도
   여러 처리를 실행하려면 여러 개의 select 구문을 조합하거나 자기 결합해서 레코드들을 비교해야 한다.
   이처럼 테이블이 하나라도 여러 테이블을 다루는 것처럼 처리해야 하는 경우도 있다.
 */

-- 1. 여러 개의 테이블을 세로로 결합하기
-- 데이터 8-1 애플리케이션1의 사용자 마스터(app1_mst_users) 테이블
create table app1_mst_users(
    user_id varchar(10),
    name varchar(20),
    email varchar(50)
);

insert into app1_mst_users(user_id, name, email) values
                                                     ('U001','Sato','sato@example.com'),
                                                     ('U002','Suzuki','suzuki@example.com');

-- 데이터 8-2 애플리케이션2의 사용자 마스터(app2_mst_users) 테이블
create table app2_mst_users(
                               user_id varchar(10),
                               name varchar(20),
                               phone varchar(15)
);

insert into app2_mst_users(user_id, name, phone) values
                                                     ('U001','Ito','080-xxxx-xxxx'),
                                                     ('U002','Tanaka','070-xxxx-xxxx');

/*
 비슷한 구조를 가지는 테이블의 데이터를 일괄 처리하고 싶은 경우, 다음 코드처럼 UNION ALL 구문을 사용해 여러 개의 테이블을 세로로 결합하면 좋음.
 결합할 때는 테이블의 컬럼이 완전히 일치해야 하므로, 한쪽 테이블에만 존재하는 컬럼은 phone 컬럼처럼 select 구문으로 제외하거나 email 컬럼처럼 디폴트 값을 줘야 함.
 */

-- 코드 8-1 UNION ALL 구문을 사용해 테이블을 세로로 결합하는 쿼리
select 'app1' as app_name, user_id, name, email from app1_mst_users
union all
select 'app2' as app_name, user_id, name, null as email from app2_mst_users;


-- 2. 여러 개의 테이블을 가로로 정렬하기
/*
 카테고리별 마스터 테이블에 카테고리별 매출 또는 카테고리별 상품 매출 순위를 기반으로
 카테고리 내부에서 가장 잘 팔리는 상품ID를 모아 테이블로 한 번에 보고 싶다고 하자.
 */

-- 데이터 8-3 카테고리 마스터 테이블
create table mst_categories(
    category_id bigint primary key,
    name varchar(50)
);

insert into mst_categories(category_id, name) values
                                                  (1, 'dvd'),
                                                  (2, 'cd'),
                                                  (3, 'book');

-- 데이터 8-4 카테고리별 매출 테이블
create table category_sales(
    category_id bigint,
    sales bigint
);

insert into category_sales(category_id, sales) values
                                                   (1, 850000),
                                                   (2, 500000);

-- 데이터 8-5 카테고리별 상품 매출 순위(product_sale_ranking) 테이블
create table product_sale_ranking(
    category_id bigint,
    rank int,
    product_id varchar(10),
    sales bigint
);

insert into product_sale_ranking values
                                     (1,1,'D001',50000),
                                     (1,2,'D002',20000),
                                     (1,3,'D003',10000),
                                     (2,1,'C001',30000),
                                     (2,2,'C002',20000),
                                     (2,3,'C003',10000);

/* 여러 개의 테이블을 가로 정렬할 때 가장 일반적인 방법은 JOIN을 사용하는 것.
   다만 마스터 테이블에 JOIN을 사용하면 결합하지 못한 데이터가 사라지거나, 반대로 중복된 데이터가 발생할 수 있음.

   다음 코드 예의 출력 결과는 테이블을 카테고리 ID로 단순하게 결합한 결과.
   그런데 카테고리 마스터에 존재하는 book 카테고리가 결합하지 못해서 여러 개의 상품 데이터가 사라졌으며,
   여러 개의 상품 ID가 부여된 DVD/CD 카테고리는 가격이 중복되어 출력됨
 */

select
    m.category_id
, m.name
, s.sales
, r.product_id AS sale_product
from mst_categories as m
join
    -- 카테고리별로 매출액 결합하기
    category_sales as s
    on m.category_id = s.category_id
join
    -- 카테고리별로 상품 결합하기
    product_sale_ranking as r
    on m.category_id = r.category_id;

/*
 마스터 테이블의 행 수를 변경하지 않고 데이터를 가로 정렬하려면,
 LEFT JOIN을 사용해 결합하지 못한 레코드를 유지한 상태로,
 결합할 레코드가 반드시 1개 이하가 되게 하는 조건을 사용해야 합니다.
 */

-- 코드 8-3 마스터 테이블의 행 수를 변경하지 않고 여러 개의 테이블을 가로로 정렬하는 쿼리
select
    m.category_id
    , m.name
    , s.sales
    , r.product_id as top_sale_product
from
    mst_categories as m
    -- left join을 사용해서 결합한 레코드를 남김
    left join
    -- 카테고리별 매출액 결합하기
    category_sales as s
    on m.category_id = s.category_id
    -- left join을 사용해서 결합하지 못한 레코드를 남김
    left join
    -- 카테고리별 최고 매출 상품 하나만 추출해서 결합하기
    product_sale_ranking as r
    on m.category_id = r.category_id
    and r.rank=1;

/*
 select 구문 내부에서 상관 서브 쿼리를 사용할 수 있는 미들웨어의 경우,
 JOIN을 사용하지 않고 여러 테이블 값을 가로로 정렬할 수 있음
 */

 -- 코드 8-4 상관 서브쿼리로 여러 개의 테이블을 가로로 정렬하는 쿼리
select
    m.category_id
    , m.name
    -- 상관 서브쿼리를 사용해 카테고리별로 매출액 추출하기
    , (select s.sales
       from category_sales as s
       where m.category_id = s.category_id
       ) as sales
    -- 상관 서브쿼리를 사용해 카테고리별로 최고 매출 상품을
    -- 하나 추출하기(순위로 따로 압축하지 않아도 됨)
    , (select r.product_id
       from product_sale_ranking as r
       where m.category_id = r.category_id
       order by sales desc
       limit 1
       ) as top_sale_product
from mst_categories as m;



-- 3. 조건 플래그를 0과 1로 표현하기
/* 마스터 테이블에 다양한 데이터를 집약하고, 마스터 테이블의 속성 조건을 0또는 1이라는 플래그로 표현하는 방법
   신용카드 번호를 포함한 마스터 테이블에 구매 로그 테이블을 결합해서 사용자들의 '신용카드 번호 등록 여부',
   '구매 이력 여부'라는 두 가지 조건을 0과 1로 표현하는 방법
 */

-- 데이터 8-6 신용카드 번호를 포함한 사용자 마스터(mst_users_with_card_number) 테이블
create table mst_users_with_card_number(
    user_id varchar(10),
    card_number varchar(50)
);

insert into mst_users_with_card_number values
                                           ('U001','1234-xxxx-xxxx-xxxx'),
                                           ('U002',null),
                                           ('U003','5678-xxxx-xxxx-xxxx');

-- 데이터 8-7 구매 로그(purchase_log) 테이블
drop table if exists purchase_log;
create table purchase_log(
    purchase_id bigint,
    user_id varchar(10),
    amount int,
    stamp timestamp
);

insert into purchase_log values
                             (10001, 'U001', 200, '2017-01-30 10:00:00'),
                             (10002, 'U001', 500, '2017-02-10 10:00:00'),
                             (10003, 'U001', 200, '2017-02-12 10:00:00'),
                             (10004, 'U002', 800, '2017-03-01 10:00:00'),
                             (10005, 'U002', 400, '2017-03-02 10:00:00');

/*
 case 식과 sign 함수로 신용카드 등록과 구매 이력 유무를 0과 1이라는 플래그로 나타내는 쿼리
 신용 카드 번호를 등록하지 않은 경우 card_number 컬럼의 값이 null이므로, case 식을 사용해서
 null이 아닐 경우에는 1, null이라면 0으로 변환
 */

 -- 코드 8-5 신용 카드 등록과 구매 이력 유무를 0과 1이라는 플래그로 나타내는 쿼리
select
    m.user_id
    , m.card_number
    , count(p.user_id) as purchase_count
    -- 신용 카드 번호를 등록한 경우 1, 등록하지 않은 경우 0으로 표현하기
    , case when m.card_number is not null then 1 else 0 end as has_card
    -- 구매 이력이 있는 경우 1, 없는 경우 0으로 표현하기
    , sign(count(p.user_id)) as has_purchased
from
    mst_users_with_card_number as m
    left join
        purchase_log as p
    on m.user_id = p.user_id
group by m.user_id, m.card_number;


-- 4. 계산한 테이블에 이름 붙여 재사용하기
/*
 복잡한 처리를 하는 sql문을 작성할 때는 서브 쿼리의 중첩이 많아짐. 비슷한 처리를 여러번 하는 경우도 있음.
 이렇게 되면 쿼리의 가독성이 굉장히 낮아짐.
 이때 SQL99에서 도입된 공통 테이블 식(CTE: Common Table Expression)을 사용하면 일시적인 테이블에 이름을 붙여 재사용할 수 있음.
 */

-- 데이터 8-8 카테고리별 상품 매출(product_sales) 테이블
create table product_sales(
    category_name varchar(10),
    product_id varchar(20),
    sales int
);

insert into product_sales values
                              ('dvd', 'D001',50000),
                              ('dvd','D002',20000),
                              ('dvd','D003',10000),
                              ('cd', 'C001',30000),
                              ('cd', 'C002',20000),
                              ('cd', 'C003',10000),
                              ('book', 'B001',20000),
                              ('book', 'B002',15000),
                              ('book', 'B003',10000),
                              ('book', 'B004',5000);

-- 코드 8-6 카테고리별 순위를 추가한 테이블에 이름 붙이기
/*
 일단 row_number 함수를 사용해 카테고리별로 순위를 붙임.
 그리고 CTE 구문을 사용해 만들어진 테이블에 product_sale_ranking이라는 이름을 붙임.
 CTE 구문은 WITH 구문을 사용해 'WITH <테이블 이름> AS (select ~)' 형태로 사용
 */

with
    product_sale_ranking as (
        select
            category_name
            , product_id
            , sales
            , row_number() over (partition by category_name order by sales desc) as rank
        from product_sales
    )
select *
from product_sale_ranking;

-- 코드 8-7 카테고리들의 순위에서 유니크한 순위 목록을 계산하는 쿼리
with
    product_sale_ranking as (
        select
            category_name
             , product_id
             , sales
             , row_number() over (partition by category_name order by sales desc) as rank
        from product_sales
    )
    , mst_rank as (select distinct rank
                   from product_sale_ranking)
    select * from mst_rank;

-- 코드 8-8 카테고리들의 순위를 횡단적으로 출력하는 쿼리
with
    product_sale_ranking as (
        select
            category_name
             , product_id
             , sales
             , row_number() over (partition by category_name order by sales desc) as rank
        from product_sales
    )
   , mst_rank as (select distinct rank
                  from product_sale_ranking)
    select
        m.rank
        , r1.product_id as dvd
        , r1.sales as dvd_sales
        , r2.product_id as cd
        , r2.sales as cd_sales
        , r3.product_id as book
        , r3.sales as book_sales
    from
        mst_rank as m
    left join
        product_sale_ranking as r1
        on m.rank = r1.rank
        and r1.category_name = 'dvd'
    left join
        product_sale_ranking as r2
        on m.rank = r2.rank
            and r2.category_name = 'cd'
    left join
        product_sale_ranking as r3
        on m.rank = r3.rank
            and r3.category_name = 'book'
    order by m.rank;

/*
 만약 CTE를 사용하지 않고 이러한 처리를 하려면 ROW_NUMBER()로 순위를 계산하는 처리를 여러번 작성해야 하므로,
 가독성이 굉장히 떨어짐.
 참고로, 많이 사용되는 일시 테이블은 아예 물리적인 테이블로 저장하는 것이 재사용 측면과 성능 측면에서 모두 좋음.
 하지만 분석 담당자가 테이블을 생성할 수 있는 권한이 없는 경우가 꽤 있음.
 */

-- 5. 유사 테이블 만들기

-- 임의의 레코드를 가진 유사 테이블 만들기

-- 코드 8-9 디바이스 ID와 이름의 마스터 테이블을 만드는 쿼리
with
    mst_devices as (
            select 1 as device_id, 'PC' as device_name
        union all select 2 as device_id, 'SP' as device_name
        union all select 3 as device_id, '애플리케이션' as device_name
    )
select *
from mst_devices;


create table users(
                      user_id varchar(10),
                      regist_device int
);

insert into users values
                      ('U001',1),
                      ('U002',2),
                      ('U003',3);

-- 코드 8-10 의사 테이블을 사용해 코드를 레이블로 변환하는 쿼리
with
    mst_devices as (
        select 1 as device_id, 'PC' as device_name
        union all select 2 as device_id, 'SP' as device_name
        union all select 3 as device_id, '애플리케이션' as device_name
    )
select
    u.user_id
    , d.device_name
from
    users as u
    left join
        mst_devices as d
        on u.regist_device = d.device_id;

/*
 앞의 코드 예는 표준 SQL을 준수하고 있으며 대부분의 미들웨어에서 작동함.
 다만 UNION ALL은 처리가 비교적 무거우므로 레코드 수가 많아지면 성능 문제가 발생할 수 있음.
 */

 -- VALUES 구문을 사용한 유사 테이블 만들기
/*
 각 미들웨어에서 구현하고 있는 확장 기능을 사용하면 앞의 쿼리의 성능을 개선할 수 있음.
 PostgreSQL에서는 INSERT 구문 이외에도 VALUES 구문을 사용해 레코드를 만들 수 있으므로 다음과 같이 작성 가능
 성능적으로 좋을 뿐만 아니라 코드도 굉장히 간단해짐
 */

-- 코드 8-11 VALUES 구문을 사용해 동적으로 테이블을 만드는 쿼리
with
    mst_devices(device_id, device_name) as (
        values
            (1, 'PC')
        , (2, 'SP')
        , (3, '애플리케이션')
    )
select *
from mst_devices;

-- 배열형 테이블 함수를 사용한 유사 테이블 만들기
/*
 VALUES 구문을 사용할 수 없는 미들웨어의 경우에는 구조화된 데이터를 테이블에 전개하는 함수를 사용해
 동적으로 테이블을 만들 수 있음. 예를 들어 Hive에서는 구조화된 array 자료형을 사용해서 데이터를 정의하고,
 explode 함수를 사용해 테이블로 전개할 수 있음.
 array 자료형과 explode 함수를 사용해 작성하면 다음과 같음
 */
-- 코드 8-12 배열과 explode 함수를 사용해 동적으로 테이블을 만드는 쿼리
with
    mst_devices as (
        select
            -- 배열을 열로 전개하기
        d[0] as device_id
        , d[1] as device_name
        from
            -- 배열을 테이블로 전개하기
        (select explode(
                array(
                array('1', 'PC')
                , array('2', 'SP')
                , array('3', '애플리케이션')
                )) d
                ) as t
    )
    select *
    from  mst_devices;


-- 순번을 사용해 테이블 작성하기
/*
 일부 미들웨어에는 순번을 자동 생성하는 테이블 함수가 구현되어 있음.
 generate_series 함수는 PostgreSQL에서만 지원.
 Redshift에서도 리더 노드로 실행될 경우 동작하기도 함
 */

-- 코드 8-14 순번을 가진 유사 테이블을 작성하는 쿼리
with
    series as (
        -- 1부터 5까지의 순선 생성하기
        select generate_series(1, 5) as idx
        -- BigQuery의 경우 generate_array 사용하기
        -- select idx from unnest(generate_array(1, 5)) as idx
    )
select *
from series;

/*
 Hive, SparkSQL에서는 generate_series 함수가 구현되어 있지 않으므로 앞의 쿼리가 동작하지 않음
 지정 문자열을 n번 반복하는 repeat 함수를 응용해서, split 함수와 조합해서 임의의 길이를 가진 배열을 생성하고,
 explode 함수로 행으로 전개한 후 row_number 함수로 순번을 붙임
 */

 -- 코드 8-15 repeat 함수를 응용해서 순번을 작성하는 쿼리
select
    row_number() over (order by x) as idx
from
    -- repeat 함수와 split 함수를 조합해서 임의의 길이를 가진 배열을 생성하고
    -- explode로 전개하기
    (select explode(split(repeat('x', 5 -1),'x')) as x) as t;





