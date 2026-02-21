# Chapter 5: 사용자를 파악하기 위한 데이터 추출

---

# 11강. 사용자 전체의 특징과 경향 찾기

사용자 속성과 행동 패턴을 분석하여 서비스 개선에 활용하는 방법

---

## 1. 사용자의 액션 수 집계하기

### 액션과 관련된 지표 집계

- **UU (Unique Users)**: 중복 없이 집계된 사용자 수
- **사용률 (usage_rate)**: 특정 액션 UU / 전체 UU
- **1인당 액션 수**: 액션 수 / 액션 UU

```sql
WITH stats AS (
    SELECT COUNT(DISTINCT session) AS total_uu
    FROM action_log
)
SELECT
    l.action,
    COUNT(DISTINCT l.session) AS action_uu,
    COUNT(1) AS action_count,
    s.total_uu,
    100.0 * COUNT(DISTINCT l.session) / s.total_uu AS usage_rate,
    1.0 * COUNT(1) / COUNT(DISTINCT l.session) AS count_per_user
FROM action_log AS l
CROSS JOIN stats AS s
GROUP BY l.action, s.total_uu;
```

### 로그인/비로그인 사용자 구분 집계

```sql
WITH action_log_with_status AS (
    SELECT
        session,
        user_id,
        action,
        CASE WHEN COALESCE(user_id, '') <> '' THEN 'login' ELSE 'guest' END
            AS login_status
    FROM action_log
)
SELECT
    COALESCE(action, 'all') AS action,
    COALESCE(login_status, 'all') AS login_status,
    COUNT(DISTINCT session) AS action_uu,
    COUNT(1) AS action_count
FROM action_log_with_status
GROUP BY ROLLUP(action, login_status);
```

### 회원/비회원 구분 (세션 내 로그인 이력 기반)

```sql
WITH action_log_with_status AS (
    SELECT
        session,
        user_id,
        action,
        CASE
            WHEN COALESCE(
                MAX(user_id) OVER(
                    PARTITION BY session
                    ORDER BY stamp
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                ), '') <> ''
            THEN 'member'
            ELSE 'none'
        END AS member_status,
        stamp
    FROM action_log
)
SELECT * FROM action_log_with_status;
```

### 회원 판별 핵심 기법

- `MAX(user_id) OVER(...)`: 세션 내에서 한 번이라도 로그인하면 user_id가 전파됨
- `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`: 시간 순서대로 누적

---

## 2. 연령별 구분 집계하기

### 생년월일로 나이 계산

```sql
WITH mst_users_with_age AS (
    SELECT
        *,
        FLOOR(
            (20170101 - CAST(REPLACE(SUBSTRING(birth_date, 1, 10), '-', '') AS INTEGER))
            / 10000
        ) AS age
    FROM mst_users
)
SELECT user_id, sex, birth_date, age FROM mst_users_with_age;
```

### 성별 + 연령대 카테고리 분류

| 카테고리 | 설명                |
| -------- | ------------------- |
| C        | 4~12세 (Child)      |
| T        | 13~19세 (Teen)      |
| M1/F1    | 20~34세 남성/여성   |
| M2/F2    | 35~49세 남성/여성   |
| M3/F3    | 50세 이상 남성/여성 |

```sql
WITH mst_users_with_category AS (
    SELECT
        user_id,
        sex,
        age,
        CONCAT(
            CASE WHEN 20 <= age THEN sex ELSE '' END,
            CASE
                WHEN age BETWEEN 4 AND 12 THEN 'C'
                WHEN age BETWEEN 13 AND 19 THEN 'T'
                WHEN age BETWEEN 20 AND 34 THEN '1'
                WHEN age BETWEEN 35 AND 49 THEN '2'
                WHEN age >= 50 THEN '3'
            END
        ) AS category
    FROM mst_users_with_age
)
SELECT category, COUNT(1) AS user_count
FROM mst_users_with_category
GROUP BY category;
```

---

## 3. 연령별 구분의 특징 추출하기

연령대별로 어떤 카테고리 상품을 구매하는지 분석

```sql
SELECT
    p.category AS product_category,
    u.category AS user_category,
    COUNT(*) AS purchase_count
FROM action_log AS p
JOIN mst_users_with_category AS u
    ON p.user_id = u.user_id
WHERE action = 'purchase'
GROUP BY p.category, u.category
ORDER BY p.category, u.category;
```

---

## 4. 사용자의 방문 빈도 집계하기

한 주 동안 며칠 서비스를 사용하는지 분석

```sql
WITH action_day_count_per_user AS (
    SELECT
        user_id,
        COUNT(DISTINCT SUBSTRING(stamp, 1, 10)) AS action_day_count
    FROM action_log
    WHERE SUBSTRING(stamp, 1, 10) BETWEEN '2016-11-01' AND '2016-11-07'
    GROUP BY user_id
)
SELECT
    action_day_count,
    COUNT(DISTINCT user_id) AS user_count
FROM action_day_count_per_user
GROUP BY action_day_count
ORDER BY action_day_count;
```

---

## 5. 벤 다이어그램으로 사용자 액션 집계하기

### 액션 플래그 생성

```sql
WITH user_action_flag AS (
    SELECT
        user_id,
        SIGN(SUM(CASE WHEN action = 'purchase' THEN 1 ELSE 0 END)) AS has_purchase,
        SIGN(SUM(CASE WHEN action = 'review' THEN 1 ELSE 0 END)) AS has_review,
        SIGN(SUM(CASE WHEN action = 'favorite' THEN 1 ELSE 0 END)) AS has_favorite
    FROM action_log
    GROUP BY user_id
)
SELECT * FROM user_action_flag;
```

### CUBE로 모든 액션 조합 집계

```sql
WITH user_action_flag AS (
    SELECT
        user_id,
        SIGN(SUM(CASE WHEN action = 'purchase' THEN 1 ELSE 0 END)) AS has_purchase,
        SIGN(SUM(CASE WHEN action = 'review' THEN 1 ELSE 0 END)) AS has_review,
        SIGN(SUM(CASE WHEN action = 'favorite' THEN 1 ELSE 0 END)) AS has_favorite
    FROM action_log
    GROUP BY user_id
),
action_venn_diagram AS (
    SELECT
        has_purchase,
        has_review,
        has_favorite,
        COUNT(1) AS users
    FROM user_action_flag
    GROUP BY CUBE(has_purchase, has_review, has_favorite)
)
SELECT
    CASE has_purchase WHEN 1 THEN 'purchase' WHEN 0 THEN 'not purchase' ELSE 'any' END AS has_purchase,
    CASE has_review WHEN 1 THEN 'review' WHEN 0 THEN 'not review' ELSE 'any' END AS has_review,
    CASE has_favorite WHEN 1 THEN 'favorite' WHEN 0 THEN 'not favorite' ELSE 'any' END AS has_favorite,
    users,
    100.0 * users / NULLIF(
        SUM(CASE WHEN has_purchase IS NULL AND has_review IS NULL AND has_favorite IS NULL
            THEN users ELSE 0 END) OVER(), 0
    ) AS ratio
FROM action_venn_diagram
ORDER BY has_purchase, has_review, has_favorite;
```

### CUBE vs ROLLUP

- `ROLLUP`: 계층적 소계 (A > B > 전체)
- `CUBE`: 모든 조합의 소계 (A, B, A+B, 전체)

---

## 6. Decile 분석으로 사용자를 10단계 그룹으로 나누기

구매 금액 기준으로 사용자를 10등분하여 분석

### Decile 분석 과정

1. 구매 금액 순으로 정렬
2. 상위 10%씩 Decile 1~10 할당 (NTILE 함수)
3. 그룹별 구매 금액 합계/평균 집계
4. 구성비, 구성비누계 계산

```sql
WITH user_purchase_amount AS (
    SELECT user_id, SUM(amount) AS purchase_amount
    FROM action_log
    WHERE action = 'purchase'
    GROUP BY user_id
),
users_with_decile AS (
    SELECT
        user_id,
        purchase_amount,
        NTILE(10) OVER(ORDER BY purchase_amount DESC) AS decile
    FROM user_purchase_amount
),
decile_with_purchase_amount AS (
    SELECT
        decile,
        SUM(purchase_amount) AS amount,
        AVG(purchase_amount) AS avg_amount,
        SUM(SUM(purchase_amount)) OVER(ORDER BY decile) AS cumulative_amount,
        SUM(SUM(purchase_amount)) OVER() AS total_amount
    FROM users_with_decile
    GROUP BY decile
)
SELECT
    decile,
    amount,
    avg_amount,
    100.0 * amount / total_amount AS total_ratio,
    100.0 * cumulative_amount / total_amount AS cumulative_ratio
FROM decile_with_purchase_amount;
```

### NTILE 함수

- `NTILE(n)`: 데이터를 n개의 동일한 크기 그룹으로 분할
- 정렬 후 순번 기반으로 그룹 할당

---

## 7. RFM 분석으로 사용자를 3가지 관점의 그룹으로 나누기

Decile 분석의 한계(기간 의존성)를 보완하는 다차원 분석

### RFM 3가지 지표

| 지표              | 설명           | 우량 고객 기준 |
| ----------------- | -------------- | -------------- |
| **R (Recency)**   | 최근 구매일    | 최근에 구매    |
| **F (Frequency)** | 구매 횟수      | 자주 구매      |
| **M (Monetary)**  | 구매 금액 합계 | 많이 구매      |

### RFM 지표 집계

```sql
WITH purchase_log AS (
    SELECT
        user_id,
        amount,
        SUBSTRING(stamp, 1, 10) AS dt
    FROM action_log
    WHERE action = 'purchase'
),
user_rfm AS (
    SELECT
        user_id,
        MAX(dt) AS recent_date,
        CURRENT_DATE - MAX(dt::date) AS recency,
        COUNT(dt) AS frequency,
        SUM(amount) AS monetary
    FROM purchase_log
    GROUP BY user_id
)
SELECT * FROM user_rfm;
```

### RFM 랭크 부여 (각 지표 1~5점)

```sql
WITH user_rfm_rank AS (
    SELECT
        user_id,
        recency,
        frequency,
        monetary,
        CASE
            WHEN recency < 14 THEN 5
            WHEN recency < 28 THEN 4
            WHEN recency < 60 THEN 3
            WHEN recency < 90 THEN 2
            ELSE 1
        END AS r,
        CASE
            WHEN 20 <= frequency THEN 5
            WHEN 10 <= frequency THEN 4
            WHEN 5 <= frequency THEN 3
            WHEN 2 <= frequency THEN 2
            ELSE 1
        END AS f,
        CASE
            WHEN 300000 <= monetary THEN 5
            WHEN 100000 <= monetary THEN 4
            WHEN 30000 <= monetary THEN 3
            WHEN 5000 <= monetary THEN 2
            ELSE 1
        END AS m
    FROM user_rfm
)
SELECT * FROM user_rfm_rank;
```

### RFM 활용 방법

#### 1차원: 통합 랭크 (R+F+M)

```sql
SELECT
    r + f + m AS total_rank,
    COUNT(user_id)
FROM user_rfm_rank
GROUP BY r + f + m
ORDER BY total_rank DESC;
```

#### 2차원: R x F 매트릭스

```sql
SELECT
    CONCAT('r_', r) AS r_rank,
    COUNT(CASE WHEN f = 5 THEN 1 END) AS f_5,
    COUNT(CASE WHEN f = 4 THEN 1 END) AS f_4,
    COUNT(CASE WHEN f = 3 THEN 1 END) AS f_3,
    COUNT(CASE WHEN f = 2 THEN 1 END) AS f_2,
    COUNT(CASE WHEN f = 1 THEN 1 END) AS f_1
FROM user_rfm_rank
GROUP BY r
ORDER BY r_rank DESC;
```

### RFM 기반 마케팅 전략

| 사용자 상태    | 대책                             |
| -------------- | -------------------------------- |
| 신규 → 단골    | 신규 배송 무료 쿠폰              |
| 안정 → 단골    | SNS 팔로우 유도                  |
| 단골 이탈 전조 | 포인트 잔고 통지, 신규 상품 메일 |
| 신규 이탈 전조 | 신규 배송 무료 쿠폰              |

---

# 12강. 사용자 전체의 시계열 변화 찾기

사용자의 서비스 사용을 시계열로 수치화하고 변화를 시각화하는 방법

---

## 1. 등록 수의 추이와 경향 보기

### 날짜별 등록 수 추이

```sql
SELECT
    register_date,
    COUNT(DISTINCT user_id) AS register_count
FROM mst_users
GROUP BY register_date
ORDER BY register_date;
```

### 월별 등록 수와 전월비 계산

```sql
WITH mst_users_with_year_month AS (
    SELECT
        *,
        SUBSTRING(register_date, 1, 7) AS year_month
    FROM mst_users
)
SELECT
    year_month,
    COUNT(DISTINCT user_id) AS register_count,
    LAG(COUNT(DISTINCT user_id)) OVER(ORDER BY year_month) AS last_month_count,
    1.0 * COUNT(DISTINCT user_id)
        / LAG(COUNT(DISTINCT user_id)) OVER(ORDER BY year_month)
        AS month_over_month_ratio
FROM mst_users_with_year_month
GROUP BY year_month;
```

---

## 2. 지속률과 정착률 산출하기

### 지속률과 정착률의 정의

| 지표       | 정의                                         | 사용 서비스 예시                                    |
| ---------- | -------------------------------------------- | --------------------------------------------------- |
| **지속률** | 등록일 기준 이후 지정일에 서비스 사용 여부   | 뉴스 사이트, 소셜 게임, SNS (매일 사용)             |
| **정착률** | 등록일 기준 이후 7일간 한 번이라도 사용 여부 | EC 사이트, 리뷰 사이트, Q&A 사이트 (목적 기반 사용) |

### 다음날 지속률 계산

```sql
WITH action_log_with_mst_users AS (
    SELECT
        u.user_id,
        u.register_date,
        CAST(a.stamp AS date) AS action_date,
        MAX(CAST(a.stamp AS date)) OVER() AS latest_date,
        CAST(u.register_date::date + '1 day'::interval AS date) AS next_day_1
    FROM mst_users u
    LEFT OUTER JOIN action_log AS a
        ON u.user_id = a.user_id
),
user_action_flag AS (
    SELECT
        user_id,
        register_date,
        SIGN(
            SUM(
                CASE WHEN next_day_1 <= latest_date THEN
                    CASE WHEN next_day_1 = action_date THEN 1 ELSE 0 END
                END
            )
        ) AS next_1_day_action
    FROM action_log_with_mst_users
    GROUP BY user_id, register_date
)
SELECT
    register_date,
    AVG(100.0 * next_1_day_action) AS repeat_rate_1_day
FROM user_action_flag
GROUP BY register_date
ORDER BY register_date;
```

### 핵심 기법: latest_date 체크의 필요성

```sql
CASE WHEN next_day_1 <= latest_date THEN
    CASE WHEN next_day_1 = action_date THEN 1 ELSE 0 END
END
```

- **문제**: 로그 데이터가 없는 미래 날짜에 대해 "사용하지 않음"으로 잘못 판정될 수 있음
- **해결**: `latest_date` 이전인 경우에만 판정 → 아직 관찰하지 못한 기간은 NULL 처리

### 지속률 지표 마스터 테이블 (VALUES 구문)

```sql
WITH repeat_interval(index_name, interval_date) AS (
    VALUES
        ('01 day repeat', 1),
        ('02 day repeat', 2),
        ('03 day repeat', 3),
        ('04 day repeat', 4),
        ('05 day repeat', 5),
        ('06 day repeat', 6),
        ('07 day repeat', 7)
)
SELECT * FROM repeat_interval;
```

### n일 지속률 집계 (세로 기반)

```sql
WITH repeat_interval(index_name, interval_date) AS (
    VALUES ('01 day repeat', 1), ('02 day repeat', 2), ...
),
action_log_with_index_date AS (
    SELECT
        u.user_id,
        u.register_date,
        CAST(a.stamp AS date) AS action_date,
        MAX(CAST(a.stamp AS date)) OVER() AS latest_date,
        r.index_name,
        CAST(u.register_date::date + interval '1 day' * r.interval_date AS date) AS index_date
    FROM mst_users AS u
    LEFT OUTER JOIN action_log AS a ON u.user_id = a.user_id
    CROSS JOIN repeat_interval AS r
),
user_action_flag AS (
    SELECT
        user_id, register_date, index_name,
        SIGN(
            SUM(
                CASE WHEN index_date <= latest_date THEN
                    CASE WHEN index_date = action_date THEN 1 ELSE 0 END
                END
            )
        ) AS index_date_action
    FROM action_log_with_index_date
    GROUP BY user_id, register_date, index_name, index_date
)
SELECT
    register_date, index_name,
    AVG(100.0 * index_date_action) AS repeat_rate
FROM user_action_flag
GROUP BY register_date, index_name
ORDER BY register_date, index_name;
```

### 정착률 지표 마스터 (기간 범위)

```sql
WITH repeat_interval(index_name, interval_begin_date, interval_end_date) AS (
    VALUES
        ('07 day retention', 1, 7),
        ('14 day retention', 8, 14),
        ('21 day retention', 15, 21),
        ('28 day retention', 22, 28)
)
SELECT * FROM repeat_interval;
```

### 정착률 계산

```sql
-- 지표 대상 기간 시작일/종료일 계산
CAST(u.register_date::date + '1day'::interval * r.interval_begin_date AS date) AS index_begin_date,
CAST(u.register_date::date + '1day'::interval * r.interval_end_date AS date) AS index_end_date

-- 기간 내 액션 여부 판정
CASE WHEN action_date BETWEEN index_begin_date AND index_end_date THEN 1 ELSE 0 END
```

---

## 3. 지속과 정착에 영향을 주는 액션 집계하기

### 분석 목적

- 1일 지속률 개선 → 등록 당일 사용자 행동 분석
- 14일 정착률 개선 → 7일 정착률 기간 동안의 행동 분석

### 모든 사용자-액션 조합 생성

```sql
WITH mst_actions AS (
    SELECT 'view' AS action
    UNION ALL SELECT 'comment' AS action
    UNION ALL SELECT 'follow' AS action
),
mst_user_actions AS (
    SELECT
        u.user_id,
        u.register_date,
        a.action
    FROM mst_users AS u
    CROSS JOIN mst_actions AS a
)
SELECT * FROM mst_user_actions;
```

### 등록일 액션 실행 여부 플래그

```sql
SELECT DISTINCT
    m.user_id,
    m.register_date,
    m.action,
    CASE WHEN a.action IS NOT NULL THEN 1 ELSE 0 END AS do_action,
    index_name,
    index_date_action
FROM mst_user_actions AS m
LEFT JOIN action_log AS a
    ON m.user_id = a.user_id
    AND CAST(m.register_date AS date) = CAST(a.stamp AS date)
    AND m.action = a.action
LEFT JOIN user_action_flag AS f
    ON m.user_id = f.user_id;
```

### 액션별 지속률/정착률 비교

```sql
SELECT
    action,
    COUNT(1) AS users,
    AVG(100.0 * do_action) AS usage_rate,
    index_name,
    AVG(CASE do_action WHEN 1 THEN 100.0 * index_date_action END) AS idx_rate,
    AVG(CASE do_action WHEN 0 THEN 100.0 * index_date_action END) AS no_action_idx_rate
FROM register_action_flag
GROUP BY index_name, action
ORDER BY index_name, action;
```

---

## 4. 액션 수에 따른 정착률 집계하기

### 액션 단계 마스터 (버킷)

```sql
WITH mst_action_bucket(action, min_count, max_count) AS (
    VALUES
        ('comment', 0, 0),
        ('comment', 1, 5),
        ('comment', 6, 10),
        ('comment', 11, 9999),
        ('follow', 0, 0),
        ('follow', 1, 5),
        ('follow', 6, 10),
        ('follow', 11, 9999)
)
SELECT * FROM mst_action_bucket;
```

### 등록 후 7일간 액션 횟수별 14일 정착률

```sql
SELECT
    action,
    min_count || ' ~ ' || max_count AS count_range,
    SUM(CASE achieve WHEN 1 THEN 1 ELSE 0 END) AS achieve,
    index_name,
    AVG(CASE achieve WHEN 1 THEN 100.0 * index_date_action END) AS achieve_index_rate
FROM register_action_flag
GROUP BY index_name, action, min_count, max_count
ORDER BY index_name, action, min_count;
```

---

## 5. 사용 일수에 따른 정착률 집계하기

### 분석 인사이트 예시

- 7일 정착 기간 중 1~4일만 사용한 사용자가 약 70%
- 1일 사용자의 28일 정착률: 20.8%
- 5일 사용자의 28일 정착률: 45%
- 6일 사용자의 28일 정착률: 55.5% (5일 대비 +10.5%)

### 대책 예시

- 소셜 게임: 1~5일 연속 접속 보상 + 6일차 대형 보너스

---

## 6. 사용자의 잔존율 집계하기

### 잔존율 분석 목적

- 등록 수개월 후 서비스 지속 사용 비율 파악
- 과거/현재 비교 및 미래 전망 검토

### 12개월 후까지 월별 잔존율 계산

```sql
WITH mst_intervals(interval_month) AS (
    VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9), (10), (11), (12)
),
mst_users_with_index_month AS (
    SELECT
        u.user_id,
        u.register_date,
        CAST(u.register_date::date + i.interval_month * '1 month'::interval AS date) AS index_date,
        SUBSTRING(u.register_date, 1, 7) AS register_month,
        SUBSTRING(CAST(u.register_date::date + i.interval_month * '1 month'::interval AS text), 1, 7) AS index_month
    FROM mst_users AS u
    CROSS JOIN mst_intervals AS i
),
action_log_in_month AS (
    SELECT DISTINCT
        user_id,
        SUBSTRING(stamp, 1, 7) AS action_month
    FROM action_log
)
SELECT
    u.register_month,
    u.index_month,
    SUM(CASE WHEN a.action_month IS NOT NULL THEN 1 ELSE 0 END) AS users,
    AVG(CASE WHEN a.action_month IS NOT NULL THEN 100.0 ELSE 0.0 END) AS retention_rate
FROM mst_users_with_index_month AS u
LEFT JOIN action_log_in_month AS a
    ON u.user_id = a.user_id
    AND u.index_month = a.action_month
GROUP BY u.register_month, u.index_month
ORDER BY u.register_month, u.index_month;
```

### 잔존율 분석 포인트

| 현상                 | 확인 사항                                          |
| -------------------- | -------------------------------------------------- |
| n개월 후 잔존율 하락 | 신규 등록자의 서비스 사용 장벽이 높아지지 않았는지 |
| 특정 n개월 후 급락   | 서비스 사용 목적 달성 기간이 너무 짧지 않은지      |
| 장기 사용자 이탈     | 서비스 내부 경쟁으로 지친 것은 아닌지              |

---

## 7. MAU (Monthly Active Users) 분석

### MAU 사용자 분류

| 분류              | 정의                                           |
| ----------------- | ---------------------------------------------- |
| **신규 사용자**   | 이번 달에 등록한 사용자                        |
| **리피트 사용자** | 이전 달에도 사용했던 사용자                    |
| **컴백 사용자**   | 신규가 아니고, 이전 달 미사용 후 돌아온 사용자 |

### 리피트 사용자 세분화

| 분류            | 정의                                   |
| --------------- | -------------------------------------- |
| **신규 리피트** | 이전 달 신규 사용자 → 이번 달도 사용   |
| **기존 리피트** | 이전 달 리피트 사용자 → 이번 달도 사용 |
| **컴백 리피트** | 이전 달 컴백 사용자 → 이번 달도 사용   |

### MAU 반복률

- **신규 반복 MAU 반복률**: 이전 달 신규 → 이번 달 신규 리피트 비율
- **기존 반복 MAU 반복률**: 이전 달 기존 → 이번 달 기존 리피트 비율
- **컴백 반복 MAU 반복률**: 이전 달 컴백 → 이번 달 컴백 리피트 비율

---

## 8. 성장지수 집계하기

### 성장지수 정의

서비스 사용 관련 상태 변화를 수치화한 지표

- **성장지수 > 1**: 서비스 성장 중
- **성장지수 < 0**: 서비스 퇴보 중

### 상태 변화 패턴

| 패턴             | 설명                   |
| ---------------- | ---------------------- |
| **Signup**       | 회원가입               |
| **Deactivation** | 액티브 → 비액티브      |
| **Reactivation** | 비액티브 → 액티브 복귀 |
| **Exit**         | 서비스 탈퇴/사용 중지  |

### 성장지수 계산 공식

```
성장지수 = Signup + Reactivation - Deactivation - Exit
```

### 성장지수 집계를 위한 플래그

| 플래그       | 의미                          |
| ------------ | ----------------------------- |
| `is_new`     | 신규 등록인가                 |
| `is_exit`    | 탈퇴 회원인가                 |
| `is_access`  | 특정 날짜에 서비스 접근했는가 |
| `was_access` | 전날 서비스에 접근했는가      |

---

# 핵심 함수 요약

## 11강 함수/구문

| 함수/구문                                   | 용도                             |
| ------------------------------------------- | -------------------------------- |
| `COUNT(DISTINCT col)`                       | 중복 제거 카운트 (UU 계산)       |
| `COALESCE(col, '')`                         | NULL 처리 (로그인 판별)          |
| `MAX() OVER(PARTITION BY ... ORDER BY ...)` | 세션 내 로그인 이력 전파         |
| `ROLLUP(col1, col2)`                        | 계층적 소계/총계                 |
| `CUBE(col1, col2, col3)`                    | 모든 조합의 소계 (벤 다이어그램) |
| `SIGN()`                                    | 0/1 플래그 생성                  |
| `NTILE(n)`                                  | n등분 그룹 할당 (Decile)         |
| `SUM(SUM()) OVER()`                         | 집계 후 누적합 (구성비누계)      |
| `generate_series(1, n)`                     | 순번 테이블 생성 (PostgreSQL)    |

## 주요 분석 패턴

### 사용률 패턴

```sql
100.0 * COUNT(DISTINCT session) / total_uu AS usage_rate
```

### 연령대 분류 패턴

```sql
FLOOR((기준일정수 - 생년월일정수) / 10000) AS age
```

### Decile 분석 패턴

```sql
NTILE(10) OVER(ORDER BY purchase_amount DESC) AS decile
```

### RFM 분석 패턴

```sql
CURRENT_DATE - MAX(dt::date) AS recency  -- R
COUNT(dt) AS frequency                    -- F
SUM(amount) AS monetary                   -- M
```

## 12강 함수/구문

| 함수/구문                       | 용도                             |
| ------------------------------- | -------------------------------- |
| `VALUES (val1), (val2), ...`    | 임시 테이블 생성 (인터벌 마스터) |
| `LAG() OVER(ORDER BY ...)`      | 이전 행 값 참조 (전월비 계산)    |
| `INTERVAL '1 day' * n`          | 날짜 연산 (n일 후 계산)          |
| `CAST(date + interval AS date)` | TIMESTAMP → DATE 변환            |
| `SIGN(SUM(...))`                | 액션 실행 여부 0/1 플래그        |
| `LEFT OUTER JOIN`               | 사용자-액션 로그 결합            |
| `CROSS JOIN`                    | 사용자-인터벌 모든 조합 생성     |
| `BETWEEN begin AND end`         | 기간 내 액션 판정                |
| `SUBSTRING(date, 1, 7)`         | 월 단위 추출                     |

### 지속률/정착률 핵심 패턴

```sql
-- 관찰 가능 기간 체크 (미래 데이터 오판정 방지)
CASE WHEN index_date <= latest_date THEN
    CASE WHEN index_date = action_date THEN 1 ELSE 0 END
END
```

### 날짜 연산 패턴 (PostgreSQL)

```sql
-- n일 후 계산
CAST(register_date::date + '1 day'::interval * n AS date) AS index_date

-- n개월 후 계산
CAST(register_date::date + interval_month * '1 month'::interval AS date) AS index_date
```

### 잔존율 패턴

```sql
-- 월별 잔존율 (등록월 기준 n개월 후)
AVG(CASE WHEN a.action_month IS NOT NULL THEN 100.0 ELSE 0.0 END) AS retention_rate
```

### 성장지수 패턴

```sql
-- 성장지수 = Signup + Reactivation - Deactivation - Exit
성장지수 = (신규등록) + (복귀) - (비활성화) - (탈퇴)
```
