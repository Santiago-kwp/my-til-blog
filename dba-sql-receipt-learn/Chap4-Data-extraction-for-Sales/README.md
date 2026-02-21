# Chapter 4: 매출을 파악하기 위한 데이터 추출

---

# 9강. 시계열 기반으로 데이터 집계하기

시계열 데이터를 다양한 관점에서 집계하여 매출 추이를 분석하는 방법

---

## 1. 날짜별 매출 집계하기

매출 집계의 기본: 날짜별 매출과 평균 구매액 집계

```sql
SELECT
    dt,
    COUNT(*) AS purchase_count,
    SUM(purchase_amount) AS total_amount,
    AVG(purchase_amount) AS avg_amount
FROM purchase_log
GROUP BY dt
ORDER BY dt;
```

---

## 2. 이동평균을 사용한 날짜별 추이 보기

일별 변동이 심할 때 7일 이동평균으로 트렌드 파악

### 7일 이동평균 계산
```sql
SELECT
    dt,
    SUM(purchase_amount) AS total_amount,
    -- 최근 최대 7일 동안의 평균 (데이터가 7일 미만이어도 계산)
    AVG(SUM(purchase_amount))
        OVER(ORDER BY dt ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
        AS seven_day_avg,
    -- 최근 7일 데이터가 있을 때만 계산 (엄격한 7일 이동평균)
    CASE
        WHEN 7 = COUNT(*)
            OVER(ORDER BY dt ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
        THEN AVG(SUM(purchase_amount))
            OVER(ORDER BY dt ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
    END AS seven_day_avg_strict
FROM purchase_log
GROUP BY dt
ORDER BY dt;
```

### 이동평균 포인트
- `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`: 현재 행 포함 최근 7일
- 엄격한 이동평균: 7일 데이터가 모두 있을 때만 계산 (CASE + COUNT 활용)

---

## 3. 당월 매출 누계 구하기

월별로 파티션을 나누어 누적 매출 계산

### 기본 방법
```sql
SELECT
    dt,
    SUBSTRING(dt, 1, 7) AS year_month,
    SUM(purchase_amount) AS total_amount,
    SUM(SUM(purchase_amount))
        OVER(PARTITION BY SUBSTRING(dt, 1, 7) ORDER BY dt ROWS UNBOUNDED PRECEDING)
        AS agg_amount
FROM purchase_log
GROUP BY dt
ORDER BY dt;
```

### CTE로 가독성 향상
```sql
WITH daily_purchase AS (
    SELECT
        dt,
        SUBSTRING(dt, 1, 4) AS year,
        SUBSTRING(dt, 6, 2) AS month,
        SUBSTRING(dt, 9, 2) AS date,
        SUM(purchase_amount) AS purchase_amount
    FROM purchase_log
    GROUP BY dt
)
SELECT
    dt,
    CONCAT(year, '-', month) AS year_month,
    purchase_amount,
    SUM(purchase_amount)
        OVER(PARTITION BY year, month ORDER BY dt ROWS UNBOUNDED PRECEDING)
        AS agg_amount
FROM daily_purchase
ORDER BY dt;
```

### 핵심 패턴
```sql
SUM(SUM(purchase_amount)) OVER(...)
```
- 안쪽 `SUM()`: GROUP BY로 집계한 날짜별 합계
- 바깥 `SUM()`: 윈도우 함수로 누적합 계산

---

## 4. 월별 매출의 작대비 구하기

JOIN 없이 CASE 문으로 연도별 매출을 피벗하여 작대비 계산

```sql
WITH daily_purchase AS (
    SELECT
        dt,
        SUBSTRING(dt, 1, 4) AS year,
        SUBSTRING(dt, 6, 2) AS month,
        SUBSTRING(dt, 9, 2) AS date,
        SUM(purchase_amount) AS purchase_amount
    FROM purchase_log
    GROUP BY dt
)
SELECT
    month,
    SUM(CASE year WHEN '2014' THEN purchase_amount END) AS amount_2014,
    SUM(CASE year WHEN '2015' THEN purchase_amount END) AS amount_2015,
    100.0
        * SUM(CASE year WHEN '2015' THEN purchase_amount END)
        / SUM(CASE year WHEN '2014' THEN purchase_amount END)
        AS rate
FROM daily_purchase
GROUP BY month
ORDER BY month;
```

### 작대비 계산 포인트
- CASE 문으로 연도별 매출을 각각 집계
- 비율 계산: `올해 매출 / 작년 매출 * 100`

---

## 5. Z 차트로 업적의 추이 확인하기

계절 변동을 배제하고 트렌드를 분석하는 방법

### Z 차트의 3가지 지표
| 지표 | 설명 | 의미 |
|------|------|------|
| **월차매출** | 해당 월의 매출 | 월별 실적 |
| **매출누계** | 해당 연도 1월부터의 누적 매출 | 연간 목표 달성도 |
| **이동년계** | 해당 월 + 과거 11개월 매출 합계 | 계절 변동 제거한 트렌드 |

### Z 차트 해석
- **매출누계가 직선**: 월차매출이 일정
- **매출누계 기울기 증가**: 최근 매출 상승
- **이동년계가 우상향**: 매출 성장 트렌드

### Z 차트 쿼리
```sql
WITH daily_purchase AS (
    SELECT
        dt,
        SUBSTRING(dt, 1, 4) AS year,
        SUBSTRING(dt, 6, 2) AS month,
        SUBSTRING(dt, 9, 2) AS date,
        SUM(purchase_amount) AS purchase_amount
    FROM purchase_log
    GROUP BY dt
),
monthly_purchase AS (
    SELECT
        year,
        month,
        SUM(purchase_amount) AS amount
    FROM daily_purchase
    GROUP BY year, month
),
calc_index AS (
    SELECT
        year,
        month,
        amount,
        -- 2015년 누계 매출
        SUM(CASE WHEN year = '2015' THEN amount END)
            OVER(ORDER BY year, month ROWS UNBOUNDED PRECEDING)
            AS agg_amount,
        -- 이동년계 (당월 + 과거 11개월)
        SUM(amount)
            OVER(ORDER BY year, month ROWS BETWEEN 11 PRECEDING AND CURRENT ROW)
            AS year_avg_amount
    FROM monthly_purchase
    ORDER BY year, month
)
SELECT
    CONCAT(year, '-', month) AS year_month,
    amount,
    agg_amount,
    year_avg_amount
FROM calc_index
WHERE year = '2015'
ORDER BY year_month;
```

---

## 6. 매출과 관련된 지표 함께 집계하기

매출의 '원인'을 파악하기 위해 구매 횟수, 구매 단가 등 주변 데이터도 함께 분석

```sql
WITH daily_purchase AS (
    SELECT
        dt,
        SUBSTRING(dt, 1, 4) AS year,
        SUBSTRING(dt, 6, 2) AS month,
        SUBSTRING(dt, 9, 2) AS date,
        SUM(purchase_amount) AS purchase_amount,
        COUNT(order_id) AS orders
    FROM purchase_log
    GROUP BY dt
),
monthly_purchase AS (
    SELECT
        year,
        month,
        SUM(orders) AS orders,
        AVG(purchase_amount) AS avg_amount,
        SUM(purchase_amount) AS monthly
    FROM daily_purchase
    GROUP BY year, month
)
SELECT
    CONCAT(year, '-', month) AS year_month,
    orders,
    avg_amount,
    monthly,
    -- 당해 연도 누계 매출
    SUM(monthly)
        OVER(PARTITION BY year ORDER BY month ROWS UNBOUNDED PRECEDING)
        AS agg_amount,
    -- 12개월 전 매출
    LAG(monthly, 12)
        OVER(ORDER BY year, month)
        AS last_year,
    -- 작대비
    100.0 * monthly / LAG(monthly, 12) OVER(ORDER BY year, month)
        AS rate
FROM monthly_purchase
ORDER BY year_month;
```

### 매출 분석 시 주요 지표
| 지표 | 설명 |
|------|------|
| `orders` | 주문 건수 |
| `avg_amount` | 평균 구매 금액 |
| `monthly` | 월별 매출 |
| `agg_amount` | 연간 누계 매출 |
| `last_year` | 작년 동월 매출 |
| `rate` | 작대비 (%) |

---

# 10강. 다면적인 축을 사용해 데이터 집약하기

매출의 시계열뿐만 아니라 상품의 카테고리, 가격 등을 조합해서 데이터의 특징을 추출하는 방법

---

## 1. 카테고리별 매출과 소계 계산하기

### UNION ALL 방식 (기본)
소카테고리, 대카테고리, 전체 매출을 각각 집계 후 결합

```sql
WITH
    sub_category_amount AS (
        -- 소카테고리별 매출
        SELECT category, sub_category, SUM(price) AS amount
        FROM purchase_detail_log
        GROUP BY category, sub_category
    ),
    category_amount AS (
        -- 대카테고리별 매출
        SELECT category, 'all' AS sub_category, SUM(price) AS amount
        FROM purchase_detail_log
        GROUP BY category
    ),
    total_amount AS (
        -- 전체 매출
        SELECT 'all' AS category, 'all' AS sub_category, SUM(price) AS amount
        FROM purchase_detail_log
    )
SELECT * FROM sub_category_amount
UNION ALL SELECT * FROM category_amount
UNION ALL SELECT * FROM total_amount;
```

### ROLLUP 방식 (권장)
SQL99 표준, 성능이 더 좋고 간결함

```sql
SELECT
    COALESCE(category, 'all') AS category,
    COALESCE(sub_category, 'all') AS sub_category,
    SUM(price) AS amount
FROM purchase_detail_log
GROUP BY ROLLUP(category, sub_category);
```

### ROLLUP 동작 원리
`ROLLUP(category, sub_category)` 는 다음을 자동 생성:
1. 소카테고리별 합계 (category, sub_category)
2. 대카테고리별 합계 (category, NULL)
3. 전체 합계 (NULL, NULL)

---

## 2. ABC 분석으로 잘 팔리는 상품 판별하기

매출 중요도에 따라 상품을 등급으로 분류하는 재고 관리 기법

### ABC 등급 기준
| 등급 | 구성비 누계 | 설명 |
|------|------------|------|
| A | 0% ~ 70% | 매출 상위 (핵심 상품) |
| B | 70% ~ 90% | 매출 중위 |
| C | 90% ~ 100% | 매출 하위 |

### ABC 분석 쿼리
```sql
WITH
    monthly_sales AS (
        SELECT
            category,
            SUM(price) AS amount
        FROM purchase_detail_log
        WHERE dt BETWEEN '2017-01-01' AND '2017-01-31'
        GROUP BY category
    ),
    sales_composition_ratio AS (
        SELECT
            category,
            amount,
            -- 구성비: 항목별 매출 / 전체 매출
            100.0 * amount / SUM(amount) OVER() AS composition_ratio,
            -- 구성비 누계: 항목별 누계 매출 / 전체 매출
            100.0 * SUM(amount) OVER(ORDER BY amount DESC)
                / SUM(amount) OVER() AS cumulative_ratio
        FROM monthly_sales
    )
SELECT
    *,
    CASE
        WHEN cumulative_ratio BETWEEN 0 AND 70 THEN 'A'
        WHEN cumulative_ratio BETWEEN 70 AND 90 THEN 'B'
        WHEN cumulative_ratio BETWEEN 90 AND 100 THEN 'C'
    END AS abc_rank
FROM sales_composition_ratio
ORDER BY amount DESC;
```

### ABC 분석 포인트
- `SUM(amount) OVER()`: 전체 매출 (파티션 없음)
- `SUM(amount) OVER(ORDER BY amount DESC)`: 매출 높은 순으로 누적합
- 등급 분류는 SQL보다 리포트 툴에서 하는 것이 유연함

---

## 3. 팬 차트로 상품의 매출 증가율 확인하기

기준 시점을 100%로 두고 이후의 변동률을 확인하는 그래프

### 팬 차트의 용도
- 매출 금액이 작은 카테고리의 성장률도 파악 가능
- 트렌드 변화와 성장 분야 발견에 유용

### 팬 차트 쿼리
```sql
WITH
    daily_category_amount AS (
        SELECT
            dt,
            category,
            SUBSTRING(dt, 1, 4) AS year,
            SUBSTRING(dt, 6, 2) AS month,
            SUM(price) AS amount
        FROM purchase_detail_log
        GROUP BY dt, category
    ),
    monthly_category_amount AS (
        SELECT
            CONCAT(year, '-', month) AS year_month,
            category,
            SUM(amount) AS amount
        FROM daily_category_amount
        GROUP BY year, month, category
    )
SELECT
    year_month,
    category,
    amount,
    -- 기준 시점(첫 달) 매출
    FIRST_VALUE(amount)
        OVER(PARTITION BY category ORDER BY year_month ROWS UNBOUNDED PRECEDING)
        AS base_amount,
    -- 기준 대비 비율
    100.0 * amount
        / FIRST_VALUE(amount)
            OVER(PARTITION BY category ORDER BY year_month ROWS UNBOUNDED PRECEDING)
        AS rate
FROM monthly_category_amount
ORDER BY year_month, category;
```

### 팬 차트 포인트
- `FIRST_VALUE()`: 각 카테고리의 첫 번째(기준) 매출 추출
- 기준 시점 선택에 명확한 근거 필요

---

## 4. 히스토그램으로 구매 가격대 집계하기

가격 분포를 시각화하기 위한 도수분포표 작성

### 히스토그램 작성 단계
1. 최댓값, 최솟값, 범위 구하기
2. 계급 수 결정 및 계급 범위 계산
3. 각 데이터의 계급 판정
4. 계급별 도수(개수)와 합계 집계

### 자동 계급 히스토그램
```sql
WITH
    stats AS (
        SELECT
            MAX(price) + 1 AS max_price,  -- +1로 최댓값도 범위 내 포함
            MIN(price) AS min_price,
            MAX(price) + 1 - MIN(price) AS range_price,
            10 AS bucket_num  -- 계급 수
        FROM purchase_detail_log
    ),
    purchase_log_with_bucket AS (
        SELECT
            price,
            min_price,
            1.0 * range_price / bucket_num AS bucket_range,
            -- 계급 판정
            FLOOR(
                1.0 * (price - min_price)
                / (1.0 * range_price / bucket_num)
            ) + 1 AS bucket
        FROM purchase_detail_log, stats
    )
SELECT
    bucket,
    min_price + bucket_range * (bucket - 1) AS lower_limit,
    min_price + bucket_range * bucket AS upper_limit,
    COUNT(price) AS num_purchase,
    SUM(price) AS total_amount
FROM purchase_log_with_bucket
GROUP BY bucket, min_price, bucket_range
ORDER BY bucket;
```

### 수동 계급 히스토그램 (권장)
리포트의 직관성을 위해 계급 범위를 수동 설정

```sql
WITH
    stats AS (
        SELECT
            100000 AS max_price,   -- 수동 설정
            0 AS min_price,        -- 수동 설정
            100000 AS range_price,
            10 AS bucket_num       -- 10000원 단위
    ),
    purchase_log_with_bucket AS (
        SELECT
            p.price,
            s.min_price,
            1.0 * s.range_price / s.bucket_num AS bucket_range,
            FLOOR(
                1.0 * (p.price - s.min_price)
                / (1.0 * s.range_price / s.bucket_num)
            ) + 1 AS bucket
        FROM purchase_detail_log p
        CROSS JOIN stats s
    )
SELECT
    bucket,
    min_price + bucket_range * (bucket - 1) AS lower_limit,
    min_price + bucket_range * bucket AS upper_limit,
    COUNT(*) AS num_purchase,
    SUM(price) AS total_amount
FROM purchase_log_with_bucket
GROUP BY bucket, min_price, bucket_range
ORDER BY bucket;
```

### 히스토그램 해석 팁
- **산이 2개인 경우**: 서로 다른 모집단이 섞여 있을 가능성
- PostgreSQL: `width_bucket()` 함수로 간단히 계급 판정 가능

---

# 핵심 함수 요약

## 9강 함수/구문
| 함수/구문 | 용도 |
|----------|------|
| `SUM() OVER()` | 윈도우 함수로 누적합 계산 |
| `AVG() OVER()` | 윈도우 함수로 이동평균 계산 |
| `ROWS BETWEEN n PRECEDING AND CURRENT ROW` | 이동 윈도우 프레임 (n+1개 행) |
| `ROWS UNBOUNDED PRECEDING` | 처음부터 현재 행까지 누적 |
| `PARTITION BY` | 그룹별로 윈도우 분리 |
| `LAG(컬럼, n)` | n행 이전 값 참조 (작대비 계산) |
| `SUBSTRING()` | 문자열에서 연/월/일 추출 |
| `CONCAT()` | 문자열 결합 |
| `WITH (CTE)` | 중간 계산 결과에 이름 붙여 가독성 향상 |

## 주요 패턴

### 누적합 패턴
```sql
SUM(SUM(amount)) OVER(PARTITION BY month ORDER BY dt ROWS UNBOUNDED PRECEDING)
```

### 이동평균 패턴
```sql
AVG(SUM(amount)) OVER(ORDER BY dt ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
```

### 작대비 패턴
```sql
100.0 * 올해매출 / LAG(올해매출, 12) OVER(ORDER BY year, month)
```

## 10강 함수/구문
| 함수/구문 | 용도 |
|----------|------|
| `ROLLUP(col1, col2)` | 소계/총계 자동 계산 (GROUP BY 확장) |
| `COALESCE()` | ROLLUP의 NULL을 'all' 등으로 치환 |
| `SUM() OVER()` | 전체 합계 (파티션 없음) |
| `SUM() OVER(ORDER BY col)` | 누적합 (구성비 누계) |
| `FIRST_VALUE()` | 기준 시점 값 추출 (팬 차트) |
| `FLOOR()` | 소수점 버림 (계급 판정) |
| `width_bucket()` | 히스토그램 계급 판정 (PostgreSQL) |

## 10강 주요 패턴

### ROLLUP 소계/총계 패턴
```sql
GROUP BY ROLLUP(category, sub_category)
```

### ABC 분석 구성비 누계 패턴
```sql
100.0 * SUM(amount) OVER(ORDER BY amount DESC) / SUM(amount) OVER()
```

### 팬 차트 기준 대비 비율 패턴
```sql
100.0 * amount / FIRST_VALUE(amount) OVER(PARTITION BY category ORDER BY year_month)
```

### 히스토그램 계급 판정 패턴
```sql
FLOOR((price - min_price) / bucket_range) + 1
```
