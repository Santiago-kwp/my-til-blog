# Chapter 3: 데이터 가공을 위한 SQL

---

# 6강. 여러 개의 값에 대한 조작

## 1. 여러 값 비교하기

### 분기별 매출 증감 판정
- `CASE` 문을 사용해 분기별 매출 증감을 '+', '-', ' '로 표시
- `SIGN()` 함수: 양수(1), 0, 음수(-1) 반환

```sql
SELECT year, q1, q2,
    CASE
        WHEN q1 < q2 THEN '+'
        WHEN q1 = q2 THEN ' '
        ELSE '-'
    END AS judge_q1_q2,
    SIGN(q2-q1) AS sign_q2_q1
FROM quarterly_sales;
```

### NULL을 포함한 연산
- `COALESCE(값, 기본값)`: NULL일 경우 기본값 반환
- `NULLIF(값1, 값2)`: 값1과 값2가 같으면 NULL 반환 (0으로 나누기 방지에 유용)

```sql
-- 연간 평균 계산 (NULL 제외)
SELECT year,
    (COALESCE(q1,0) + COALESCE(q2,0) + COALESCE(q3,0) + COALESCE(q4,0))
    / NULLIF(SIGN(COALESCE(q1,0)) + SIGN(COALESCE(q2,0)) + SIGN(COALESCE(q3,0)) + SIGN(COALESCE(q4,0)), 0)
    AS average
FROM quarterly_sales;
```

---

## 2. CTR(클릭률) 계산
- 하나하나 구할 때 `ctr_as_percent` 컬럼처럼 click에 `100.0`을 곱해 계산하면,
  자료형 변환이 자동으로 이루어지므로 쿼리가 간단해짐
### 0으로 나누기 방지
```sql
SELECT dt, ad_id,
    -- CASE 문 사용
    CASE WHEN impressions > 0 THEN 100.0 * clicks / impressions END AS ctr_by_case,
    -- NULLIF 사용
    100.0 * clicks / NULLIF(impressions, 0) AS ctr_by_nullif
FROM advertising_stats;
```

---

## 3. 거리 계산

### 1차원 거리
- `ABS()`: 절대값
- `SQRT()`, `POWER()`: 제곱근과 거듭제곱

```sql
SELECT ABS(x1-x2) AS abs,
       SQRT(POWER(x1-x2, 2)) AS rms
FROM location_1d;
```

### 2차원 거리 (유클리드 거리)
- PostgreSQL의 `POINT` 자료형과 `<->` 연산자 활용

```sql
SELECT SQRT(POWER(x1-x2,2) + POWER(y1-y2,2)) AS dist,
       POINT(x1,y1) <-> POINT(x2,y2) AS dist_point
FROM location_2d;
```

---

## 4. 날짜/시간 다루기

### 날짜 연산
- `INTERVAL`: 시간 간격 더하기/빼기

```sql
SELECT
    register_stamp + INTERVAL '1 hour' AS after_1_hour,
    register_stamp - INTERVAL '30 minutes' AS before_30_minutes,
    (register_stamp::date + INTERVAL '1 day')::date AS after_1_day
FROM mst_users_with_dates;
```

### 날짜 차이 계산
```sql
SELECT
    CURRENT_DATE - register_stamp::date AS diff_days
FROM mst_users_with_dates;
```

### 나이 계산
```sql
-- AGE 함수 사용
SELECT
    EXTRACT(YEAR FROM AGE(birth_date::date)) AS current_age,
    EXTRACT(YEAR FROM AGE(register_stamp::date, birth_date::date)) AS register_age
FROM mst_users_with_dates;

-- 문자열 연산으로 계산 (이식성 높음)
SELECT
    FLOOR((CAST(REPLACE(CAST(CURRENT_DATE AS TEXT), '-', '') AS INTEGER)
         - CAST(REPLACE(birth_date, '-', '') AS INTEGER)) / 10000) AS current_age
FROM mst_users_with_dates;
```

---

## 5. IP 주소 다루기

### inet 자료형 (PostgreSQL 전용)
```sql
-- IP 주소 비교
SELECT CAST('127.0.0.1' AS inet) < CAST('127.0.0.2' AS inet) AS lt;

-- 네트워크 범위 포함 여부 (<<, >> 연산자)
SELECT CAST('127.10.22.1' AS inet) << CAST('127.0.0.0/8' AS inet) AS is_contained;
```

### 문자열로 IP 주소 다루기
- `SPLIT_PART()`: 구분자로 문자열 분리
- `LPAD()`: 문자열 왼쪽 채우기

```sql
-- IP를 정수로 변환
SELECT ip,
    CAST(SPLIT_PART(ip, '.', 1) AS INTEGER) * 2^24
  + CAST(SPLIT_PART(ip, '.', 2) AS INTEGER) * 2^16
  + CAST(SPLIT_PART(ip, '.', 3) AS INTEGER) * 2^8
  + CAST(SPLIT_PART(ip, '.', 4) AS INTEGER) AS ip_integer
FROM (SELECT '192.168.0.1' AS ip) AS t;

-- IP를 0으로 패딩
SELECT ip,
    LPAD(SPLIT_PART(ip, '.', 1), 3, '0')
 || LPAD(SPLIT_PART(ip, '.', 2), 3, '0')
 || LPAD(SPLIT_PART(ip, '.', 3), 3, '0')
 || LPAD(SPLIT_PART(ip, '.', 4), 3, '0') AS ip_padding
FROM (SELECT '192.168.0.1' AS ip) AS t;
```

---

# 7강. 하나의 테이블에 대한 조작

## 1. 윈도우 함수

### 순위 함수
| 함수 | 설명 |
|------|------|
| `ROW_NUMBER()` | 유일한 순위 부여 |
| `RANK()` | 동일 값에 같은 순위, 다음 순위 건너뜀 |
| `DENSE_RANK()` | 동일 값에 같은 순위, 다음 순위 이어감 |

### 이전/다음 행 참조
- `LAG(컬럼, n)`: n행 이전 값
- `LEAD(컬럼, n)`: n행 이후 값

```sql
SELECT product_id, score,
    ROW_NUMBER() OVER(ORDER BY score DESC) AS row,
    RANK() OVER(ORDER BY score DESC) AS rank,
    DENSE_RANK() OVER(ORDER BY score DESC) AS dense_rank,
    LAG(product_id) OVER(ORDER BY score DESC) AS lag1,
    LEAD(product_id) OVER(ORDER BY score DESC) AS lead1
FROM popular_products;
```

### 윈도우 프레임과 집계 함수
- `ROWS BETWEEN ... AND ...`: 윈도우 프레임 지정

| 프레임 옵션 | 설명 |
|------------|------|
| `UNBOUNDED PRECEDING` | 파티션의 첫 번째 행 |
| `CURRENT ROW` | 현재 행 |
| `UNBOUNDED FOLLOWING` | 파티션의 마지막 행 |
| `n PRECEDING` | 현재 행 기준 n행 이전 |
| `n FOLLOWING` | 현재 행 기준 n행 이후 |

```sql
SELECT product_id, score,
    -- 누계 점수
    SUM(score) OVER(ORDER BY score DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cum_score,
    -- 이동 평균 (앞뒤 1행 포함)
    AVG(score) OVER(ORDER BY score DESC
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS local_avg,
    -- 최고/최저 순위 상품
    FIRST_VALUE(product_id) OVER(ORDER BY score DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS first_value,
    LAST_VALUE(product_id) OVER(ORDER BY score DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_value
FROM popular_products;
```

---

## 2. PARTITION BY - 그룹별 윈도우 함수

```sql
SELECT category, product_id, score,
    ROW_NUMBER() OVER(PARTITION BY category ORDER BY score DESC) AS row,
    RANK() OVER(PARTITION BY category ORDER BY score DESC) AS rank,
    DENSE_RANK() OVER(PARTITION BY category ORDER BY score DESC) AS dense_rank
FROM popular_products;
```

### 카테고리별 상위 N개 추출
```sql
SELECT * FROM (
    SELECT category, product_id, score,
        ROW_NUMBER() OVER(PARTITION BY category ORDER BY score DESC) AS rank
    FROM popular_products
) AS ranked
WHERE rank <= 2;
```

### DISTINCT + FIRST_VALUE로 카테고리별 최상위 추출
```sql
SELECT DISTINCT category,
    FIRST_VALUE(product_id) OVER(
        PARTITION BY category ORDER BY score DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS product_id
FROM popular_products;
```

---

## 3. 행을 열로 변환 (Pivot)

### 행을 열로 변환
```sql
SELECT dt,
    MAX(CASE WHEN indicator='impressions' THEN val END) AS impressions,
    MAX(CASE WHEN indicator='sessions' THEN val END) AS sessions,
    MAX(CASE WHEN indicator='users' THEN val END) AS users
FROM daily_kpi
GROUP BY dt;
```

### 행을 쉼표로 구분된 문자열로 집약
```sql
SELECT purchase_id,
    STRING_AGG(product_id, ',') AS product_ids,
    SUM(price) AS amount
FROM purchase_detail_log
GROUP BY purchase_id;
```

---

## 4. 열을 행으로 변환 (Unpivot)

가로 기반 데이터(컬럼)를 세로 기반 데이터(행)로 전환하는 기법

### 고정 길이 데이터: 피벗 테이블 + CROSS JOIN
- 데이터 수가 고정되어 있을 때 사용
- 전개할 데이터 수만큼의 일련 번호를 가진 피벗 테이블을 만들어 CROSS JOIN

```sql
SELECT
    q.year,
    -- Q1~Q4 레이블 출력
    CASE
        WHEN p.idx = 1 THEN 'q1'
        WHEN p.idx = 2 THEN 'q2'
        WHEN p.idx = 3 THEN 'q3'
        WHEN p.idx = 4 THEN 'q4'
    END AS quarter,
    -- Q1~Q4 매출 출력
    CASE
        WHEN p.idx = 1 THEN q.q1
        WHEN p.idx = 2 THEN q.q2
        WHEN p.idx = 3 THEN q.q3
        WHEN p.idx = 4 THEN q.q4
    END AS sales
FROM quarterly_sales AS q
CROSS JOIN (
    -- 행으로 전개할 열의 수만큼 순번 테이블 생성
              SELECT 1 AS idx
    UNION ALL SELECT 2 AS idx
    UNION ALL SELECT 3 AS idx
    UNION ALL SELECT 4 AS idx
) AS p;
```

---

## 5. 배열을 행으로 전개하기

데이터 길이가 가변적일 때 테이블 함수를 사용하여 배열을 행으로 전개

### 테이블 함수란?
- 리턴값이 테이블인 함수
- 배열을 매개변수로 받아 레코드로 분할하여 리턴

| 미들웨어 | 함수 |
|---------|------|
| PostgreSQL, BigQuery | `UNNEST()` |
| Hive, SparkSQL | `EXPLODE()` |

### UNNEST 기본 사용법
```sql
SELECT UNNEST(ARRAY['A001', 'A002', 'A003']) AS product_id;
```

### 쉼표로 구분된 문자열을 행으로 전개
```sql
-- 방법 1: STRING_TO_ARRAY + UNNEST + CROSS JOIN
SELECT
    purchase_id,
    product_id
FROM purchase_log AS p
CROSS JOIN UNNEST(STRING_TO_ARRAY(product_ids, ',')) AS product_id;

-- 방법 2: REGEXP_SPLIT_TO_TABLE (PostgreSQL 전용, 더 간단)
SELECT
    purchase_id,
    REGEXP_SPLIT_TO_TABLE(product_ids, ',') AS product_id
FROM purchase_log;
```

### 관련 함수 비교
| 함수 | 용도 |
|------|------|
| `STRING_TO_ARRAY(문자열, 구분자)` | 문자열을 배열로 변환 |
| `UNNEST(배열)` | 배열을 행으로 전개 |
| `REGEXP_SPLIT_TO_TABLE(문자열, 패턴)` | 정규식으로 분리하여 바로 행으로 전개 |

---

# 8강. 여러 개의 테이블 조작하기

여러 개의 테이블을 조작할 때 SQL을 간단하고 가독성 높게 작성하는 방법

---

## 1. 여러 개의 테이블을 세로로 결합하기 (UNION ALL)

비슷한 구조의 테이블을 하나로 합칠 때 사용

### 주의사항
- 결합할 테이블의 컬럼이 완전히 일치해야 함
- 한쪽에만 있는 컬럼은 제외하거나 기본값(NULL 등)을 지정

```sql
-- 두 앱의 사용자 테이블을 세로로 결합
SELECT 'app1' AS app_name, user_id, name, email
FROM app1_mst_users
UNION ALL
SELECT 'app2' AS app_name, user_id, name, NULL AS email
FROM app2_mst_users;
```

---

## 2. 여러 개의 테이블을 가로로 정렬하기 (JOIN)

### JOIN 사용 시 주의사항
- 단순 JOIN은 결합하지 못한 데이터가 사라지거나 중복 발생 가능
- 마스터 테이블의 행 수를 유지하려면 `LEFT JOIN` 사용
- 결합 레코드가 1개 이하가 되는 조건 필요

### LEFT JOIN으로 마스터 행 수 유지
```sql
SELECT
    m.category_id,
    m.name,
    s.sales,
    r.product_id AS top_sale_product
FROM mst_categories AS m
LEFT JOIN category_sales AS s
    ON m.category_id = s.category_id
LEFT JOIN product_sale_ranking AS r
    ON m.category_id = r.category_id
    AND r.rank = 1;  -- 1위 상품만 결합
```

### 상관 서브쿼리로 가로 정렬
JOIN 없이 SELECT 절 내에서 서브쿼리로 값 추출

```sql
SELECT
    m.category_id,
    m.name,
    -- 상관 서브쿼리로 매출액 추출
    (SELECT s.sales
     FROM category_sales AS s
     WHERE m.category_id = s.category_id) AS sales,
    -- 상관 서브쿼리로 최고 매출 상품 추출
    (SELECT r.product_id
     FROM product_sale_ranking AS r
     WHERE m.category_id = r.category_id
     ORDER BY sales DESC
     LIMIT 1) AS top_sale_product
FROM mst_categories AS m;
```

---

## 3. 조건 플래그를 0과 1로 표현하기

마스터 테이블에 다양한 조건을 플래그로 표현

```sql
SELECT
    m.user_id,
    m.card_number,
    COUNT(p.user_id) AS purchase_count,
    -- 신용카드 등록 여부 (NULL이 아니면 1)
    CASE WHEN m.card_number IS NOT NULL THEN 1 ELSE 0 END AS has_card,
    -- 구매 이력 여부 (COUNT > 0이면 1)
    SIGN(COUNT(p.user_id)) AS has_purchased
FROM mst_users_with_card_number AS m
LEFT JOIN purchase_log AS p
    ON m.user_id = p.user_id
GROUP BY m.user_id, m.card_number;
```

---

## 4. CTE (Common Table Expression) - 계산 테이블에 이름 붙이기

SQL99에서 도입된 공통 테이블 식으로 일시 테이블에 이름을 붙여 재사용

### 기본 문법
```sql
WITH 테이블명 AS (
    SELECT ...
)
SELECT * FROM 테이블명;
```

### CTE 기본 예제
```sql
WITH product_sale_ranking AS (
    SELECT
        category_name,
        product_id,
        sales,
        ROW_NUMBER() OVER(PARTITION BY category_name ORDER BY sales DESC) AS rank
    FROM product_sales
)
SELECT * FROM product_sale_ranking;
```

### 여러 CTE 연결하기
```sql
WITH
    product_sale_ranking AS (
        SELECT
            category_name,
            product_id,
            sales,
            ROW_NUMBER() OVER(PARTITION BY category_name ORDER BY sales DESC) AS rank
        FROM product_sales
    ),
    mst_rank AS (
        SELECT DISTINCT rank FROM product_sale_ranking
    )
SELECT * FROM mst_rank;
```

### CTE 활용: 카테고리별 순위를 횡단적으로 출력
```sql
WITH
    product_sale_ranking AS (
        SELECT
            category_name, product_id, sales,
            ROW_NUMBER() OVER(PARTITION BY category_name ORDER BY sales DESC) AS rank
        FROM product_sales
    ),
    mst_rank AS (
        SELECT DISTINCT rank FROM product_sale_ranking
    )
SELECT
    m.rank,
    r1.product_id AS dvd,
    r1.sales AS dvd_sales,
    r2.product_id AS cd,
    r2.sales AS cd_sales,
    r3.product_id AS book,
    r3.sales AS book_sales
FROM mst_rank AS m
LEFT JOIN product_sale_ranking AS r1
    ON m.rank = r1.rank AND r1.category_name = 'dvd'
LEFT JOIN product_sale_ranking AS r2
    ON m.rank = r2.rank AND r2.category_name = 'cd'
LEFT JOIN product_sale_ranking AS r3
    ON m.rank = r3.rank AND r3.category_name = 'book'
ORDER BY m.rank;
```

---

## 5. 유사 테이블 만들기

실제 테이블 없이 임시로 데이터를 생성하는 방법

### 방법 1: UNION ALL (표준 SQL)
```sql
WITH mst_devices AS (
        SELECT 1 AS device_id, 'PC' AS device_name
    UNION ALL SELECT 2 AS device_id, 'SP' AS device_name
    UNION ALL SELECT 3 AS device_id, '애플리케이션' AS device_name
)
SELECT * FROM mst_devices;
```

### 방법 2: VALUES 구문 (PostgreSQL)
성능이 더 좋고 코드가 간결함

```sql
WITH mst_devices(device_id, device_name) AS (
    VALUES
        (1, 'PC'),
        (2, 'SP'),
        (3, '애플리케이션')
)
SELECT * FROM mst_devices;
```

### 방법 3: 배열 + EXPLODE (Hive, SparkSQL)
```sql
WITH mst_devices AS (
    SELECT
        d[0] AS device_id,
        d[1] AS device_name
    FROM (
        SELECT EXPLODE(
            ARRAY(
                ARRAY('1', 'PC'),
                ARRAY('2', 'SP'),
                ARRAY('3', '애플리케이션')
            )
        ) d
    ) AS t
)
SELECT * FROM mst_devices;
```

### 순번 테이블 생성

#### PostgreSQL: generate_series
```sql
WITH series AS (
    SELECT generate_series(1, 5) AS idx
)
SELECT * FROM series;
```

#### BigQuery: generate_array + unnest
```sql
SELECT idx FROM UNNEST(generate_array(1, 5)) AS idx;
```

#### Hive/SparkSQL: repeat + split + explode
```sql
SELECT
    ROW_NUMBER() OVER(ORDER BY x) AS idx
FROM (
    SELECT EXPLODE(SPLIT(REPEAT('x', 5-1), 'x')) AS x
) AS t;
```

---

# 핵심 함수 요약

## 6강 함수
| 함수 | 용도 |
|------|------|
| `COALESCE()` | NULL 대체값 지정 |
| `NULLIF()` | 조건부 NULL 반환 |
| `SIGN()` | 부호 반환 (-1, 0, 1) |
| `ABS()`, `SQRT()`, `POWER()` | 수학 연산 |
| `INTERVAL` | 날짜/시간 연산 |
| `AGE()` | 날짜 차이 계산 |
| `SPLIT_PART()` | 문자열 분리 |
| `LPAD()` | 문자열 왼쪽 채우기 |

## 7강 함수
| 함수 | 용도 |
|------|------|
| `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()` | 순위 부여 |
| `LAG()`, `LEAD()` | 이전/다음 행 참조 |
| `FIRST_VALUE()`, `LAST_VALUE()` | 프레임 내 첫/마지막 값 |
| `STRING_AGG()` | 문자열 집약 |
| `UNNEST()` | 배열을 행으로 전개 |
| `STRING_TO_ARRAY()` | 문자열을 배열로 변환 |
| `REGEXP_SPLIT_TO_TABLE()` | 정규식으로 분리하여 행으로 전개 |

## 8강 함수/구문
| 함수/구문 | 용도 |
|----------|------|
| `UNION ALL` | 테이블 세로 결합 |
| `LEFT JOIN` | 마스터 행 유지하며 가로 결합 |
| 상관 서브쿼리 | SELECT 절에서 다른 테이블 값 참조 |
| `WITH ... AS (CTE)` | 일시 테이블에 이름 붙여 재사용 |
| `VALUES` | 유사 테이블 생성 (PostgreSQL) |
| `generate_series()` | 순번 생성 (PostgreSQL) |
| `EXPLODE()` | 배열을 행으로 전개 (Hive/SparkSQL) |
