set search_path to sql_receipt;

drop table if exists mst_users;
create table mst_users (
    user_id varchar(10),
    sex char(1),
    birth_date varchar(10),
    register_date varchar(10),
    register_device varchar(5),
    withdraw_date varchar(10)
);

insert into mst_users values
('U001', 'M', '1977-06-17', '2025-10-01', 'pc', null),
('U002', 'F', '1953-06-12', '2025-10-01', 'sp', '2025-10-10'),
('U003', 'F', '1950-07-18', '2025-10-10', 'app', null),
('U004', 'M', '1982-11-05', '2025-10-11', 'pc', null),
('U005', 'F', '1990-03-20', '2025-10-11', 'sp', null),
('U006', 'M', '1985-08-30', '2025-10-12', 'app', '2025-10-20'),
('U007', 'F', '1992-01-15', '2025-10-12', 'pc', null),
('U008', 'M', '1979-12-01', '2025-10-13', 'sp', null),
('U009', 'F', '1995-05-10', '2025-10-13', 'app', null),
('U010', 'M', '1988-09-22', '2025-10-14', 'pc', '2025-10-25'),
('U011', 'F', '1998-07-07', '2025-10-14', 'sp', null),
('U012', 'M', '1975-04-14', '2025-10-15', 'app', null),
('U013', 'F', '1983-10-02', '2025-10-15', 'pc', null),
('U014', 'M', '1991-02-28', '2025-10-16', 'sp', null),
('U015', 'F', '1980-06-09', '2025-10-16', 'app', '2025-10-30'),
('U016', 'M', '1993-11-11', '2025-10-17', 'pc', null),
('U017', 'F', '1987-01-23', '2025-10-17', 'sp', null),
('U018', 'M', '1996-08-18', '2025-10-18', 'app', null),
('U019', 'F', '1984-09-03', '2025-10-18', 'pc', null),
('U020', 'M', '1999-12-25', '2025-10-19', 'sp', '2025-11-01'),
('U021', 'F', '1978-02-19', '2025-10-19', 'app', null),
('U022', 'M', '1986-05-29', '2025-10-20', 'pc', null),
('U023', 'F', '1994-04-01', '2025-10-20', 'sp', null),
('U024', 'M', '1988-12-10', '2025-01-05', 'pc', null),
('U025', 'F', '1991-03-15', '2025-01-15', 'sp', null),
('U026', 'M', '1985-07-20', '2025-02-03', 'app', null),
('U027', 'F', '1993-11-25', '2025-02-12', 'pc', null),
('U028', 'M', '1980-01-30', '2025-03-01', 'sp', '2025-03-10'),
('U029', 'F', '1996-05-05', '2025-03-11', 'app', null),
('U030', 'M', '1982-09-14', '2025-04-02', 'pc', null),
('U031', 'F', '1998-02-19', '2025-04-14', 'sp', null),
('U032', 'M', '1976-08-08', '2025-05-03', 'app', null),
('U033', 'F', '1984-10-21', '2025-05-18', 'pc', null),
('U034', 'M', '1990-06-28', '2025-06-05', 'sp', null),
('U035', 'F', '1981-04-12', '2025-06-20', 'app', '2025-06-30'),
('U036', 'M', '1995-02-11', '2025-07-07', 'pc', null),
('U037', 'F', '1989-09-01', '2025-07-19', 'sp', null),
('U038', 'M', '1999-12-31', '2025-08-01', 'app', null),
('U039', 'F', '1983-03-03', '2025-08-16', 'pc', null),
('U040', 'M', '1979-05-27', '2025-09-04', 'sp', null),
('U041', 'F', '1992-10-09', '2025-09-19', 'app', null),
('U042', 'M', '1987-06-18', '2025-10-08', 'pc', null),
('U043', 'F', '1994-01-23', '2025-10-22', 'sp', null),
('U044', 'M', '1986-11-13', '2025-11-06', 'app', null),
('U045', 'F', '1997-07-07', '2025-11-24', 'pc', '2025-12-01'),
('U046', 'M', '1981-02-02', '2025-12-09', 'sp', null),
('U047', 'F', '1990-08-11', '2025-12-25', 'app', null),
('U048', 'M', '1988-04-04', '2026-01-10', 'pc', null);




drop table if exists action_log;
create table action_log(
    session varchar(20),
    user_id varchar(10),
    action varchar(10),
    category varchar(10),
    products text,
    amount int,
    stamp varchar(30)
);

insert into action_log values
                           ('989004ea','U001','view',null,null,null,'2026-01-25 18:00:00'),
                           ('989004ea','U001','favorite','drama','D001',null,'2026-01-25 18:05:31'),
                           ('989004ea','U001','add_cart','drama','D001',null,'2026-01-25 18:07:34'),
                           ('989004ea','U001','add_cart','drama','D002',null,'2026-01-25 18:09:51'),
                           ('989004ea','U001','purchase','drama','D001,D002',2000,'2026-01-25 18:19:09'),
                           ('989004ea','U001','review','drama','D003',2000,'2026-01-25 18:23:09'),
                           ('762afcd3',null,'view',null,null,null,'2026-01-25 18:31:29'),
                           ('5503dc73','U004','view',null,null,null,'2025-07-15 10:00:00'),
                           ('5503dc73','U004','add_cart','movie','M001',null,'2025-07-15 10:05:00'),
                           ('01a2de89','U005','view',null,null,null,'2026-01-10 11:00:00'),
                           ('01a2de89','U005','favorite','music','MU001',null,'2026-01-10 11:02:00'),
                           ('38372e68','U006','view',null,null,null,'2026-01-10 12:00:00'),
                           ('a1d2345e','U007','view',null,null,null,'2026-01-30 13:00:00'),
                           ('b3f21b9c','U008','view',null,null,null,'2026-01-10 14:00:00'),
                           ('c4a1de84','U009','view',null,null,null,'2025-12-15 15:00:00'),
                           ('c4a1de84','U009','review','movie','M002',1500,'2025-12-15 15:20:00'),
                           ('d8e5c4a1',null,'view',null,null,null,'2025-12-15 16:00:00'),
                           ('d8e5c4a1',null,'add_cart','book','B005',null,'2025-12-15 16:05:00'),
                           ('f1b2c3d4','U010','view',null,null,null,'2026-01-12 09:00:00'),
                           ('2f8a6b3d','U011','view',null,null,null,'2026-01-12 10:00:00'),
                           ('2f8a6b3d','U011','add_cart','drama','D003',null,'2026-01-12 10:05:00'),
                           ('e4b5c6d7','U012','view',null,null,null,'2026-01-12 11:00:00'),
                           ('8a7b6c5d','U013','view',null,null,null,'2025-07-20 12:00:00'),
                           ('8a7b6c5d','U013','favorite','book','B003',null,'2025-07-20 12:01:00'),
                           ('1a2b3c4d',null,'view',null,null,null,'2025-07-20 12:30:00'),
                           ('9f8e7d6c','U014','view',null,null,null,'2025-08-20 13:00:00'),
                           ('5c6d7e8f','U015','view',null,null,null,'2025-10-20 14:00:00'),
                           ('7d8e9f0a','U016','view',null,null,null,'2026-01-15 10:00:00'),
                           ('b1c2d3e4',null,'view',null,null,null,'2026-01-15 10:45:00'),
                           ('b1c2d3e4',null,'favorite','movie','M006',null,'2026-01-15 10:50:00'),
                           ('f5e6d7c8','U017','view',null,null,null,'2026-01-15 11:00:00'),
                           ('f5e6d7c8','U017','add_cart','movie','M003',null,'2026-01-15 11:05:00'),
                           ('f5e6d7c8','U017','add_cart','movie','M004',null,'2026-01-15 11:07:00'),
                           ('a9b8c7d6','U018','view',null,null,null,'2026-01-15 12:00:00'),
                           ('e5f4a3b2','U019','view',null,null,null,'2026-01-15 13:00:00'),
                           ('e5f4a3b2','U019','review','book','B004',1200,'2026-01-15 13:25:00'),
                           ('1d2c3b4a','U020','view',null,null,null,'2026-01-28 14:00:00'),
                           ('8c7b6a5f','U021','view',null,null,null,'2025-12-01 15:00:00'),
                           ('8c7b6a5f','U021','favorite','drama','D004',null,'2025-12-01 15:03:00'),
                           ('3f4e5d6c',null,'view',null,null,null,'2025-12-01 15:30:00'),
                           ('6a5b4c3d','U022','view',null,null,null,'2025-09-20 16:00:00'),
                           ('b2a1f8e9','U023','view',null,null,null,'2025-11-01 17:00:00'),
                           ('c3b2a1f8',null,'view',null,null,null,'2025-11-01 17:45:00'),
                           ('d4c3b2a1','U002','view',null,null,null,'2026-01-18 10:00:00'),
                           ('d4c3b2a1','U002','add_cart','book','B001',null,'2026-01-18 10:05:00'),
                           ('e5d4c3b2','U003','view',null,null,null,'2025-12-10 11:00:00'),
                           ('e5d4c3b2','U003','add_cart','drama','D004',null,'2025-12-10 11:05:00'),
                           ('f6e5d4c3','U005','add_cart','movie','M002',null,'2026-01-10 12:05:00'),
                           ('a7f6e5d4','U006','add_cart','music','MU004',null,'2026-01-10 13:05:00'),
                           ('b8a7f6e5','U008','add_cart','book','B002',null,'2026-01-10 14:05:00'),
                           ('c9b8a7f6','U010','add_cart','drama','D005',null,'2026-01-12 09:05:00'),
                           ('e2d1c9b8','U012','add_cart','book','B003',null,'2026-01-12 11:05:00'),
                           ('b5a4f3e2','U016','add_cart','movie','M004',null,'2026-01-15 10:05:00'),
                           ('d7c6b5a4','U018','add_cart','music','MU001',null,'2026-01-15 12:05:00'),
                           ('f9e8d7c6','U020','add_cart','movie','M005',null,'2026-01-28 14:05:00'),
                           ('5c6d7e8f','U015','purchase','music','MU002,MU003',2000,'2025-10-20 14:10:00'),
                           ('6a5b4c3d','U022','purchase','movie','M005',1800,'2025-09-20 16:12:00'),
                           ('a4f3e2d1','U014','purchase','drama','D006',2100,'2025-08-20 13:10:00'),
                           ('f3e2d1c9','U013','purchase','music','MU005',600,'2025-07-20 12:20:00'),
                           ('11111111','U001','purchase','book','B001',15000,'2026-01-30 10:00:00'),
                           ('11111112','U001','purchase','book','B002',15000,'2026-01-29 10:00:00'),
                           ('11111113','U001','purchase','book','B003',15000,'2026-01-28 10:00:00'),
                           ('11111114','U001','purchase','book','B004',15000,'2026-01-27 10:00:00'),
                           ('11111115','U001','purchase','book','B005',15000,'2026-01-26 10:00:00'),
                           ('11111116','U001','purchase','book','B006',15000,'2026-01-23 10:00:00'),
                           ('11111117','U001','purchase','book','B007',15000,'2026-01-22 10:00:00'),
                           ('11111118','U001','purchase','book','B008',15000,'2026-01-21 10:00:00'),
                           ('11111119','U001','purchase','book','B009',15000,'2026-01-20 10:00:00'),
                           ('11111120','U001','purchase','book','B010',15000,'2026-01-19 10:00:00'),
                           ('11111121','U001','purchase','book','B011',15000,'2026-01-16 10:00:00'),
                           ('11111122','U001','purchase','book','B012',15000,'2026-01-15 10:00:00'),
                           ('11111123','U001','purchase','book','B013',15000,'2026-01-14 10:00:00'),
                           ('11111124','U001','purchase','book','B014',15000,'2026-01-13 10:00:00'),
                           ('11111125','U001','purchase','book','B015',15000,'2026-01-12 10:00:00'),
                           ('11111126','U001','purchase','book','B016',15000,'2026-01-09 10:00:00'),
                           ('11111127','U001','purchase','book','B017',15000,'2026-01-08 10:00:00'),
                           ('11111128','U001','purchase','book','B018',15000,'2026-01-07 10:00:00'),
                           ('11111129','U001','purchase','book','B019',15000,'2026-01-06 10:00:00'),
                           ('11111130','U001','purchase','book','B020',15000,'2026-01-05 10:00:00'),
                           ('22222221','U002','purchase','movie','M001',10000,'2026-01-18 11:00:00'),
                           ('22222222','U002','purchase','movie','M002',10000,'2026-01-02 11:00:00'),
                           ('22222223','U002','purchase','movie','M003',10000,'2025-12-15 11:00:00'),
                           ('22222224','U002','purchase','movie','M004',10000,'2025-12-01 11:00:00'),
                           ('22222225','U002','purchase','movie','M005',10000,'2025-11-20 11:00:00'),
                           ('22222226','U002','purchase','movie','M006',10000,'2025-11-10 11:00:00'),
                           ('22222227','U002','purchase','movie','M007',10000,'2025-11-01 11:00:00'),
                           ('22222228','U002','purchase','movie','M008',10000,'2025-10-20 11:00:00'),
                           ('22222229','U002','purchase','movie','M009',10000,'2025-10-10 11:00:00'),
                           ('22222230','U002','purchase','movie','M010',10000,'2025-10-01 11:00:00'),
                           ('33333331','U003','purchase','drama','D001',6000,'2025-12-20 12:00:00'),
                           ('33333332','U003','purchase','drama','D002',6000,'2025-11-20 12:00:00'),
                           ('33333333','U003','purchase','drama','D003',6000,'2025-10-20 12:00:00'),
                           ('33333334','U003','purchase','drama','D004',6000,'2025-09-20 12:00:00'),
                           ('33333335','U003','purchase','drama','D005',6000,'2025-08-20 12:00:00'),
                           ('44444441','U004','purchase','music','MU001',2500,'2025-07-15 13:00:00'),
                           ('55555551','U007','purchase','book','B010',2500,'2026-01-30 14:00:00'),
                           ('d4c3b2a1','U002','purchase','book','B001',1200,'2026-01-18 10:10:00'),
                           ('e5d4c3b2','U003','purchase','drama','D004',2200,'2025-12-10 11:10:00'),
                           ('f6e5d4c3','U005','purchase','movie','M002',1600,'2026-01-10 12:10:00'),
                           ('a7f6e5d4','U006','purchase','music','MU004',500,'2026-01-10 13:10:00'),
                           ('b8a7f6e5','U008','purchase','book','B002',1800,'2026-01-10 14:10:00'),
                           ('c9b8a7f6','U010','purchase','drama','D005',2500,'2026-01-12 09:10:00'),
                           ('d1c9b8a7','U011','purchase','movie','M003',1700,'2026-01-12 10:15:00'),
                           ('e2d1c9b8','U012','purchase','book','B003',1300,'2026-01-12 11:10:00'),
                           ('b5a4f3e2','U016','purchase','movie','M004',1900,'2026-01-15 10:10:00'),
                           ('c6b5a4f3','U017','purchase','book','B004,B005',3200,'2026-01-15 11:20:00'),
                           ('d7c6b5a4','U018','purchase','music','MU001',400,'2026-01-15 12:10:00'),
                           ('e8d7c6b5','U019','purchase','drama','D007',2300,'2026-01-15 13:30:00'),
                           ('f9e8d7c6','U020','purchase','movie','M005',1800,'2026-01-28 14:10:00'),
                           ('1a2b3c4d','U024','view',null,null,null,'2025-01-06 10:00:00'),
                           ('1a2b3c4d','U024','purchase','book','B001',1500,'2025-01-06 10:10:00'),
                           ('2b3c4d5e','U025','view',null,null,null,'2025-01-16 11:00:00'),
                           ('3c4d5e6f','U026','view',null,null,null,'2025-02-04 12:00:00'),
                           ('3c4d5e6f','U026','purchase','drama','D002',2200,'2025-02-04 12:15:00'),
                           ('4d5e6f7g','U027','view',null,null,null,'2025-02-13 13:00:00'),
                           ('5e6f7g8h','U028','view',null,null,null,'2025-03-02 14:00:00'),
                           ('5e6f7g8h','U028','purchase','movie','M003',1800,'2025-03-02 14:05:00'),
                           ('6f7g8h9i','U029','view',null,null,null,'2025-03-12 15:00:00'),
                           ('7g8h9i0j','U030','view',null,null,null,'2025-04-03 16:00:00'),
                           ('7g8h9i0j','U030','purchase','book','B002',2000,'2025-04-03 16:10:00'),
                           ('8h9i0j1k','U031','view',null,null,null,'2025-04-15 17:00:00'),
                           ('9i0j1k2l','U032','view',null,null,null,'2025-05-04 18:00:00'),
                           ('9i0j1k2l','U032','purchase','music','MU001',1000,'2025-05-04 18:05:00'),
                           ('0j1k2l3m','U033','view',null,null,null,'2025-05-19 19:00:00'),
                           ('1k2l3m4n','U034','view',null,null,null,'2025-06-06 20:00:00'),
                           ('1k2l3m4n','U034','purchase','drama','D003',2100,'2025-06-06 20:15:00'),
                           ('2l3m4n5o','U035','view',null,null,null,'2025-06-21 21:00:00'),
                           ('3m4n5o6p','U036','view',null,null,null,'2025-07-08 22:00:00'),
                           ('3m4n5o6p','U036','purchase','movie','M004',1600,'2025-07-08 22:05:00'),
                           ('4n5o6p7q','U037','view',null,null,null,'2025-07-20 09:00:00'),
                           ('5o6p7q8r','U038','view',null,null,null,'2025-08-02 10:00:00'),
                           ('5o6p7q8r','U038','purchase','book','B003',1300,'2025-08-02 10:20:00'),
                           ('6p7q8r9s','U039','view',null,null,null,'2025-08-17 11:00:00'),
                           ('7q8r9s0t','U040','view',null,null,null,'2025-09-05 12:00:00'),
                           ('7q8r9s0t','U040','purchase','music','MU002',800,'2025-09-05 12:10:00'),
                           ('8r9s0t1u','U041','view',null,null,null,'2025-09-20 13:00:00'),
                           ('9s0t1u2v','U042','view',null,null,null,'2025-10-09 14:00:00'),
                           ('9s0t1u2v','U042','purchase','drama','D004',2400,'2025-10-09 14:05:00'),
                           ('0t1u2v3w','U043','view',null,null,null,'2025-10-23 15:00:00'),
                           ('1u2v3w4x','U044','view',null,null,null,'2025-11-07 16:00:00'),
                           ('1u2v3w4x','U044','purchase','movie','M005',1700,'2025-11-07 16:15:00'),
                           ('2v3w4x5y','U045','view',null,null,null,'2025-11-25 17:00:00'),
                           ('3w4x5y6z','U046','view',null,null,null,'2025-12-10 18:00:00'),
                           ('3w4x5y6z','U046','purchase','book','B004',1100,'2025-12-10 18:05:00'),
                           ('4x5y6z7a','U047','view',null,null,null,'2025-12-26 19:00:00'),
                           ('5y6z7a8b','U048','view',null,null,null,'2026-01-11 20:00:00'),
                           ('5y6z7a8b','U048','purchase','music','MU003',900,'2026-01-11 20:10:00');



-- 1. 사용자의 액션 수 집계하기

-- 액션과 관련된 지표 집계하기
/*
 특정 액션 UU를 전체 액션 UU로 나눈 것을 '사용률(usage_rate)', 이를 사용하면 특정 액션을 얼마나 자주 사용하는지 확인할 수 있음
 사용자가 평균적으로 액션을 몇 번이나 사용했는지 확인할 수 있게 '1명 당 액션 수(count_per_user)'도 함께 구하자

 * UU는 Unique Users를 나타내는 중복 없이 집계된 사용자 수를 나타내는 말.
 페이지 열람 UU라고 하면, 페이지를 열었던 사용자 수를 중복 없이 집계한 것
 */

-- 코드 11-1 액션 수와 비율을 계산하는 쿼리
with
    stats as (
        -- 로그 전체의 유니크 사용자 수 구하기
        select count(distinct session) as total_uu
        from action_log
    )
select
    l.action
-- 액션 UU : 해당 행동을 한 중복 없는 사용자 수 (Unique Users)
    , count(distinct l.session) as action_uu
-- 액션의 수
    , count(1) as action_count
-- 전체 UU
    , s.total_uu
-- 사용률: <액션 UU> / <전체 UU>
    , 100.0 * count(distinct l.session) / s.total_uu as usage_rate
-- 1인당 액션 수 : <액션 수> / <액션 UU>
    , 1.0 * count(1) / count(distinct l.session) as count_per_user
from action_log as l
-- 로그 전체의 유니크 사용자 수를 모든 레코드에 결합하기
cross join
    stats as s
group by
    l.action, s.total_uu;

-- 로그인 사용자와 비로그인 사용자를 구분해서 집계하기
/*
 로그인하지 않아도 서비스 일부를 사용할 수 있는 사이트의 경우, 회원과 비회원을 따로 나누어 집계하는 것이 좋음
 로그인, 비로그인, 회원, 비회원을 판별할 때는 로그 데이터에 session 정보가 있어야 함.
 */

-- 코드 11-2 로그인 상태를 판별하는 쿼리
with
    action_log_with_status as (
        select
            session
            , user_id
            , action
            -- user_id가 NULL 또는 빈 문자가 아닌 경우 login이라고 판정하기 // <> : 같지 않다.
            , case when coalesce(user_id, '') <> '' then 'login' else 'guest' end
            as login_status
        from action_log
        )
select *
from action_log_with_status;

-- 코드 11-3 로그인 상태에 따라 액션 수 등을 따로 집계하는 쿼리
with
    action_log_with_status as (
        select
            session
             , user_id
             , action
             -- user_id가 NULL 또는 빈 문자가 아닌 경우 login이라고 판정하기 // <> : 같지 않다.
             , case when coalesce(user_id, '') <> '' then 'login' else 'guest' end
            as login_status
        from action_log
    )
select
    coalesce(action, 'all') as action
    , coalesce(login_status, 'all') as login_status
    , count(distinct session) as action_uu
    , count(1) as action_count
from action_log_with_status
group by rollup(action, login_status);

/*
 group by rollup(action, login_status): 이 쿼리의 가장 중요한 부분입니다.
GROUP BY는 특정 열을 기준으로 데이터를 그룹화하여 집계 함수(예: COUNT, SUM)를 적용합니다.
ROLLUP은 GROUP BY의 확장 기능으로, 그룹별 집계 결과와 함께 소계(subtotal)와 총계(grand total)를 자동으로 추가해 줍니다.
rollup(action, login_status)는 다음과 같은 3가지 수준(Level)으로 그룹화를 진행합니다.
Level 1: action과 login_status 두 컬럼 모두로 그룹화 (e.g., 'purchase'이면서 'login'인 그룹)
Level 2: action 컬럼만으로 그룹화하여 login_status의 소계를 계산 (e.g., 'purchase' 전체 그룹)
Level 3: 전체 데이터의 총계를 계산
coalesce(action, 'all') as action 와 coalesce(login_status, 'all') as login_status:
ROLLUP이 소계나 총계를 만들 때, 그룹화되지 않은 컬럼의 값은 NULL이 됩니다.
예를 들어, 'purchase'의 소계를 계산할 때 action은 'purchase'이지만 login_status는 NULL이 됩니다.
coalesce 함수는 이 NULL 값을 사람이 보기 좋게 'all'이라는 문자로 바꿔주는 역할을 합니다.
count(distinct session) as action_uu: 그룹화된 범위 내에서 중복을 제외한 session의 개수를 셉니다. 이는 곧 순수 사용자 수(UU)를 의미합니다.
count(1) as action_count: 그룹화된 범위 내의 모든 행(row)의 개수를 셉니다. 이는 곧 액션의 총 발생 횟수를 의미합니다.
 */


 -- 회원과 비회원을 구분해서 집계하기
/*
 로그인하지 않은 상태라도, 이전에 한 번이라도 로그인했다면 회원으로 계산하고 싶을 수 있음.
 */

-- 코드 11-4 회원 상태를 판별하는 쿼리
with
    action_log_with_status as (
        select
            session
            , user_id
            , action
            -- 로그를 타임스탬프 순서로 나열하고, 한 번이라도 로그인한 사용자일 경우,
            -- 이후의 모든 로그 상태를 member로 설정
            , case
                when
                    coalesce(max(user_id)
                        over(partition by session order by stamp
                            rows between unbounded preceding and current row)
                    , '') <> ''
                    then 'member'
                else 'none'
            end as member_status
            , stamp
        from action_log
    )
select *
from action_log_with_status;

/*
 윈도 함수에서 session 별로 파티션을 설명하면, 해당 session에서 한 번이라도 로그인했다면
 MAX(user_id)로 사용자 ID를 추출할 수 있음.

 코드 분석: max(user_id) over(partition by session ...)
over(...): 이 부분이 바로 윈도우 함수를 사용하겠다는 선언입니다.
partition by session: session ID가 같은 것끼리 그룹을 나눕니다. 즉, 모든 계산은 각각의 세션 안에서만 독립적으로 이루어집니다.
order by stamp: 각 세션 내에서 데이터를 시간(stamp) 순서대로 정렬합니다.
rows between unbounded preceding and current row: 이 부분이 핵심입니다. "현재 처리 중인 행을 기준으로, 파티션(세션)의 맨 처음부터 현재 행까지"를 계산 범위로 지정합니다. 즉, 시간이 흐름에 따라 계산 범위가 점점 누적됩니다.
max(user_id): 위에서 지정된 누적 범위 안에서 user_id의 최댓값을 찾습니다.
MAX 함수의 동작 원리
SQL에서 문자열에 MAX 함수를 적용하면 알파벳순으로 가장 뒤에 있는 값을 반환합니다. 하지만 더 중요한 특징은 MAX 함수는 NULL 값을 무시한다는 것입니다.

 결론 : 시간 순서대로 누적되는 데이터 범위 내에서, user_id 값이 한번이라도 나타나면 (NULL이 아니면) 그 값을 계속해서 다음 행으로 "전파(propagate)"시키기 위함입니다.
 */

 -- 2. 연령별 구분 집계하기
/*
 회원 정보를 저장하는 서비스는, 해당 서비스의 사용자를 파악하고 의도한대로 서비스가 사용되는지 확인해야 할 경우가 많음
 또한 광고 디자인과 캐치 프레이즈를 검토하려면 사용자 속성을 집계해야 함.
 사용자 속성을 정의하고 집계하면 다양한 리포트를 만들 수 있음.
 */

-- 코드 11-5 사용자의 생일을 계산하는 쿼리
with
    mst_users_with_int_birth_date as (
        select
            *
        -- 특정 날짜(2017년 1월 1일)의 정수 표현
        , 20170101 as int_specific_date
        , cast(replace(substring(birth_date, 1, 10), '-', '') as integer) as int_birth_date
        from mst_users
    )
, mst_users_with_age as (
    select
        *
        -- 특정 날짜(2017년 1월 1일)의 나이
        , floor((int_specific_date - int_birth_date) / 10000) as age
        from mst_users_with_int_birth_date
)
select
    user_id, sex, birth_date, age
from mst_users_with_age;

-- 코드 11-6 성별과 연령별 구분을 계산하는 쿼리
with
    mst_users_with_int_birth_date as (
        select
            *
             -- 특정 날짜(2017년 1월 1일)의 정수 표현
             , 20170101 as int_specific_date
             , cast(replace(substring(birth_date, 1, 10), '-', '') as integer) as int_birth_date
        from mst_users
    )
   , mst_users_with_age as (
    select
        *
         -- 특정 날짜(2017년 1월 1일)의 나이
         , floor((int_specific_date - int_birth_date) / 10000) as age
    from mst_users_with_int_birth_date
)
, mst_users_with_category as (
    select user_id
            , sex
            , age
            , concat(
                case
                    when 20 <= age then sex
                    else ''
                end
                , case
                      when age between 4 and 12 then 'C'
                      when age between 13 and 19 then 'T'
                      when age between 20 and 34 then '1'
                      when age between 35 and 49 then '2'
                      when age >= 50 then '3'
                end
            ) as category
    from mst_users_with_age
)
select *
from mst_users_with_category


-- 코드 11-7 연령별 구분의 사람 수를 계산하는 쿼리
with
    mst_users_with_int_birth_date as (
        select
            *
             -- 특정 날짜(2017년 1월 1일)의 정수 표현
             , 20170101 as int_specific_date
             , cast(replace(substring(birth_date, 1, 10), '-', '') as integer) as int_birth_date
        from mst_users
    )
   , mst_users_with_age as (
    select
        *
         -- 특정 날짜(2017년 1월 1일)의 나이
         , floor((int_specific_date - int_birth_date) / 10000) as age
    from mst_users_with_int_birth_date
)
   , mst_users_with_category as (
    select user_id
         , sex
         , age
         , concat(
            case
                when 20 <= age then sex
                else ''
                end
        , case
              when age between 4 and 12 then 'C'
              when age between 13 and 19 then 'T'
              when age between 20 and 34 then '1'
              when age between 35 and 49 then '2'
              when age >= 50 then '3'
                end
           ) as category
    from mst_users_with_age
)
select
    category
    , count(1) as user_count
from mst_users_with_category
group by category;

-- 3. 연령별 구분의 특징 추출하기
/*
 서비스의 사용 형태가 사용자 속성에 따라 다르다는 것을 확인하면 상품 또는 기사를 사용자 속성에 맞게 추천할 수 있음.
 */

-- 코드 11-8 연령별 구분과 카테고리를 집계하는 쿼리
with
    mst_users_with_int_birth_date as (
        select
            *
             -- 특정 날짜(2017년 1월 1일)의 정수 표현
             , 20170101 as int_specific_date
             , cast(replace(substring(birth_date, 1, 10), '-', '') as integer) as int_birth_date
        from mst_users
    )
   , mst_users_with_age as (
    select
        *
         -- 특정 날짜(2017년 1월 1일)의 나이
         , floor((int_specific_date - int_birth_date) / 10000) as age
    from mst_users_with_int_birth_date
)
   , mst_users_with_category as (
    select user_id
         , sex
         , age
         , concat(
            case
                when 20 <= age then sex
                else ''
                end
        , case
              when age between 4 and 12 then 'C'
              when age between 13 and 19 then 'T'
              when age between 20 and 34 then '1'
              when age between 35 and 49 then '2'
              when age >= 50 then '3'
                end
           ) as category
    from mst_users_with_age
)
select
    p.category as product_category
    , u.category as user_category
    , count(*) as purchase_count
from action_log as p
    join mst_users_with_category as u
    on p.user_id = u.user_id
where
    -- 구매 로그만 선택하기
    action = 'purchase'
group by
    p.category, u.category
order by
    p.category, u.category;


-- 4. 사용자의 방문 빈도 집계하기
/*
 사용자가 일주일 또는 한 달 동안 서비스를 얼마나 쓰는지 알면 업무 분석에 큰 도움이 됨.
 서비스를 한 주 동안 며칠 사용하는 사용자가 몇 명인지 집계
 */

-- 코드 11-9 한 주에 며칠 사용되었는지를 집계하는 쿼리
with
    action_log_with_dt as (
        select *
        , substring(stamp, 1, 10) as dt
        from action_log
    )
    , action_day_count_per_user as (
        select
            user_id
            , count(distinct dt) as action_day_count
        from action_log_with_dt
        where
            -- 한 주 동안을 대상으로 지정
            dt between '2016-11-01' and '2016-11-07'
        group by user_id
)
select
    action_day_count
    , count(distinct user_id) as user_count
from action_day_count_per_user
group by action_day_count
order by action_day_count;

-- 5. 벤 다이어그램으로 사용자 액션 집계하기

-- 코드 11-11 사용자들의 액션 플래그를 집계하는 쿼리
with
    user_action_flag as (
        -- 사용자가 액션을 했으면 1, 안 했으면 0으로 플래그 붙이기
        select
            user_id
            , sign(sum(case when action = 'purchase' then 1 else 0 end)) as has_purchase
            , sign(sum(case when action = 'review' then 1 else 0 end)) as has_review
            , sign(sum(case when action = 'favorite' then 1 else 0 end)) as has_favorite
        from action_log
        group by user_id
    )
select *
from user_action_flag;

/*
 벤 다이어그램을 그리려면 '구매 액션만 한 사용자 수' 또는 '구매와 리뷰 액션을 한 사용자 수' 처럼
 하나의 액션 또는 두 개의 액션을 한 사용자가 몇 명인지 계산해야 함.
 표준 SQL에 정의되어 있는 CUBE 구문을 사용하면 이러한 수를 쉽게 계산할 수 있음.

 */

 -- 코드 11-12 모든 액션 조합에 대한 사용자 수 계산하기
with
    user_action_flag as (
        -- 사용자가 액션을 했으면 1, 안 했으면 0으로 플래그 붙이기
        select
            user_id
             , sign(sum(case when action = 'purchase' then 1 else 0 end)) as has_purchase
             , sign(sum(case when action = 'review' then 1 else 0 end)) as has_review
             , sign(sum(case when action = 'favorite' then 1 else 0 end)) as has_favorite
        from action_log
        group by user_id
    )
, action_venn_diagram as (
    -- cube를 사용해서 모든 액션 조합 구하기
    select has_purchase
         , has_review
         , has_favorite
         , count(1) as users
    from user_action_flag
    group by cube (has_purchase, has_review, has_favorite))
select *
from action_venn_diagram
order by has_purchase, has_review, has_favorite;

/*
 출력 결과에서 has_purchase, has_review, has_favorite 컬럼의 값이 없는(null)
 레코드는 해당 액션을 했는지 안 했는지 모르는 경우를 의미함.
 */

 -- 코드 11-15 벤 다이어그램을 만들기 위해 데이터를 가공하는 쿼리
with
    user_action_flag as (
        -- 사용자가 액션을 했으면 1, 안 했으면 0으로 플래그 붙이기
        select
            user_id
             , sign(sum(case when action = 'purchase' then 1 else 0 end)) as has_purchase
             , sign(sum(case when action = 'review' then 1 else 0 end)) as has_review
             , sign(sum(case when action = 'favorite' then 1 else 0 end)) as has_favorite
        from action_log
        group by user_id
    )
   , action_venn_diagram as (
    -- cube를 사용해서 모든 액션 조합 구하기
    select has_purchase
         , has_review
         , has_favorite
         , count(1) as users
    from user_action_flag
    group by cube (has_purchase, has_review, has_favorite)
    )
select
    -- 0, 1 플래그를 문자열로 가공하기
    case has_purchase
        when 1 then 'purchase' when 0 then 'not purchase' else 'any'
    end as has_purchase
    , case has_review
          when 1 then 'review' when 0 then 'not review' else 'any'
    end as has_review
    , case has_favorite
          when 1 then 'favorite' when 0 then 'not favorite' else 'any'
    end as has_favorite
    , users
    -- 전체 사용자 수를 기반으로 비율 구하기
    , 100.0 * users
        / nullif(
          -- 모든 액션이 NULL인 사용자 수가 전체 사용자 수를 나타내므로
          -- 해당 레코드의 사용자 수를 Window 함수로 구하기
          sum(case when has_purchase is null
                and has_review is null
                and has_favorite is null
                then users else 0 end) over()
          , 0)
    as ratio
from action_venn_diagram
order by has_purchase, has_review, has_favorite;

/*
 이번 절의 예는 EC 사이트를 기준으로 했지만, SNS 등의 사이트도 다음과 같은 형태로 적용할 수 있음.
 - 글을 작성하지 않고 다른 사람의 글만 확인하는 사용자
 - 글을 많이 작성하는 사용자
 - 글을 거의 작성하지 않지만 댓글을 많이 작성하는 사용자
 - 글과 댓글 모두 적극적으로 작성하는 사용자
 어떠한 대책을 수행했을 때, 해당 대책으로 효과가 발생한 사용자가 얼마나 되는지 벤다이어그램으로 확인하면,
 대책을 제대로 세웠는지 확인할 수 있음
 */

 -- 6. Decile 분석을 사용해 사용자를 10단계 그룹으로 나누기
/*
 Decile 분석 과정
 1. 사용자를 구매 금액이 많은 순으로 정렬
 2. 정렬된 사용자 상위부터 10%씩 Decile1 부터 10까지의 그룹을 할당
 3. 각 그룹의 구매 금액 합계를 집계
 4. 전체 구매 금액에 대해 각 Decile의 구매 금액 비율(구성비)를 계산
 5. 상위에서 누적으로 어느 정도의 비율을 차지하는지 구성비누계를 집계

 사용자를 구매 금액이 많은 순서로 정렬하고, 정렬된 사용자의 상위에서 10%씩 decile 할당
 같은 수로 데이터 그룹을 만들 때는 NTILE 함수 사용
 */

-- 코드 11-16 구매액이 많은 순서로 사용자 그룹을 10등분하는 쿼리
with
    user_purchase_amount as (
        select
            user_id
            , sum(amount) as purchase_amount
        from action_log
        where action = 'purchase'
        group by user_id
    )
    , users_with_decile as (
        select
            user_id
            , purchase_amount
            , ntile(10) over (order by purchase_amount desc) as decile
        from user_purchase_amount
)
select *
from users_with_decile;


-- 코드 11-17 10분할한 Decile들을 집계하는 쿼리
with
    user_purchase_amount as (
        select
            user_id
             , sum(amount) as purchase_amount
        from action_log
        where action = 'purchase'
        group by user_id
    )
   , users_with_decile as (
    select
        user_id
         , purchase_amount
         , ntile(10) over (order by purchase_amount desc) as decile
    from user_purchase_amount
)
, decile_with_purchase_amount as (
    select
        decile
        , sum(purchase_amount) as amount
        , avg(purchase_amount) as avg_amount
        , sum(sum(purchase_amount)) over (order by decile) as cumulative_amount
        , sum(sum(purchase_amount)) over () as total_amount
    from users_with_decile
    group by decile
)
select *
from decile_with_purchase_amount;

/*
 sum(sum(...)) over (...) 구문은 다음과 같이 작동합니다.
Inner SUM: GROUP BY와 함께 작동하여 그룹별 소계(subtotal)를 먼저 계산합니다.
Outer SUM (Window Function): GROUP BY로 계산된 소계 값들을 대상으로, 누적 합계나 전체 합계 같은 추가적인 계산을 수행합니다.
이 패턴은 **"집계된 결과에 대해 다시 집계"**를 하고 싶을 때 사용하는 매우 강력하고 효율적인 SQL 기법입니다.
 */

 -- 코드 11-18 구매액이 많은 Decile 순서로 구성비와 구성비누계를 계산하는 쿼리

with
    user_purchase_amount as (
        select
            user_id
             , sum(amount) as purchase_amount
        from action_log
        where action = 'purchase'
        group by user_id
    )
   , users_with_decile as (
    select
        user_id
         , purchase_amount
         , ntile(10) over (order by purchase_amount desc) as decile
    from user_purchase_amount
)
   , decile_with_purchase_amount as (
    select
        decile
         , sum(purchase_amount) as amount
         , avg(purchase_amount) as avg_amount
         , sum(sum(purchase_amount)) over (order by decile) as cumulative_amount
         , sum(sum(purchase_amount)) over () as total_amount
    from users_with_decile
    group by decile
)
select
    decile
    , amount
    , avg_amount
    , 100.0 * amount / total_amount as total_ratio
    , 100.0 * cumulative_amount / total_amount as cumulative_ratio
from decile_with_purchase_amount;


-- 7. RFM 분석으로 사용자를 3가지 관점의 그룹으로 나누기
/*
 Decile 분석은 데이터 검색 기간에 따라 문제가 있음.
 예를 들어 검색 기간이 너무 장기간이면 과거에는 우수 고객이었어도,
 현재는 다른 서비스를 사용하는 휴면 고객이 포함될 가능성이 있음.
 반대로 검색 대상이 단기간이라면 정기적으로 구매하는 안정 고객이 포함되지 않고,
 해당 기간 동안에만 일시적으로 많이 구매한 사용자가 우수 고객으로 취급될 수 있음.
 */

-- RFM 분석의 3가지 지표 집계하기
/*
 - Recency : 최근 구매일
    최근 무언가를 구매한 사용자를 우량 고객으로 취급
 - Frequency : 구매 횟수
    사용자가 구매한 횟수를 세고, 많을수록 우량 고객으로 취급
 - Monetary : 구매 금액 합계
    사용자의 구매 금액 합계를 집계하고, 금액이 높을수록 우량 고객으로 취급
 */

-- 코드 11-19 사용자별로 RFM을 집계하는 쿼리
with
    purchase_log as (
        select
            user_id
            , amount
        -- 타임스탬프를 기반으로 날짜 추출하기
            , substring(stamp, 1, 10) as dt
        from action_log
        where action = 'purchase'
    )
, user_rfm as (
    select
        user_id
        , max(dt) as recent_date
        , current_date - max(dt::date) as recency
        , count(dt) as frequency
        , sum(amount) as monetary
    from purchase_log
    group by user_id
)
select *
from user_rfm;

-- RFM 랭크 정의하기
/*
 RFM 분석에서는 3개의 지표를 각각 5개의 그룹으로 나누는 것이 일반적입니다.
 이렇게 하면 125개의 그룹으로 사용자를 나눠 파악할 수 있습니다.
 */

-- 코드 11-20 사용자들의 RFM 랭크를 계산하는 쿼리
with
    purchase_log as (
        select
            user_id
             , amount
             -- 타임스탬프를 기반으로 날짜 추출하기
             , substring(stamp, 1, 10) as dt
        from action_log
        where action = 'purchase'
    )
   , user_rfm as (
    select
        user_id
         , max(dt) as recent_date
         , current_date - max(dt::date) as recency
         , count(dt) as frequency
         , sum(amount) as monetary
    from purchase_log
    group by user_id
)
, user_rfm_rank as (
    select
        user_id
        , recent_date
        , recency
        , frequency
        , monetary
        , case
            when recency < 14 then 5
            when recency < 28 then 4
            when recency < 60 then 3
            when recency < 90 then 2
            else 1
        end as r
        , case
            when 20 <= frequency then 5
            when 10 <= frequency then 4
            when 5 <= frequency then 3
            when 2 <= frequency then 2
            when 1 <= frequency then 1
        end as f
        , case
            when 300000 <= monetary then 5
            when 100000 <= monetary then 4
            when 30000 <= monetary then 3
            when 5000 <= monetary then 2
            else 1
        end as m
    from user_rfm
)
select *
from user_rfm_rank;

-- 코드 11-21 각 그룹의 사람 수를 확인하는 쿼리

with
    purchase_log as (
        select
            user_id
             , amount
             -- 타임스탬프를 기반으로 날짜 추출하기
             , substring(stamp, 1, 10) as dt
        from action_log
        where action = 'purchase'
    )
   , user_rfm as (
    select
        user_id
         , max(dt) as recent_date
         , current_date - max(dt::date) as recency
         , count(dt) as frequency
         , sum(amount) as monetary
    from purchase_log
    group by user_id
)
   , user_rfm_rank as (
    select
        user_id
         , recent_date
         , recency
         , frequency
         , monetary
         , case
               when recency < 14 then 5
               when recency < 28 then 4
               when recency < 60 then 3
               when recency < 90 then 2
               else 1
        end as r
         , case
               when 20 <= frequency then 5
               when 10 <= frequency then 4
               when 5 <= frequency then 3
               when 2 <= frequency then 2
               when 1 <= frequency then 1
        end as f
         , case
               when 300000 <= monetary then 5
               when 100000 <= monetary then 4
               when 30000 <= monetary then 3
               when 5000 <= monetary then 2
               else 1
        end as m
    from user_rfm
)
, mst_rfm_index as (
    --  1부터 5까지의 숫자를 가지는 테이블 만들기
    select generate_series as rfm_index from generate_series(1, 5)
)
, rfm_flag as (
    select
        m.rfm_index
        , case when m.rfm_index = r.r then 1 else 0 end as r_flag
        , case when m.rfm_index = r.f then 1 else 0 end as f_flag
        , case when m.rfm_index = r.m then 1 else 0 end as m_flag
    from mst_rfm_index as m
    cross join
        user_rfm_rank as r
)
select
    rfm_index
    , sum(r_flag) as r
    , sum(f_flag) as f
    , sum(m_flag) as m
from rfm_flag
group by rfm_index
order by rfm_index desc;

-- 사용자를 1차원으로 구분하기
/*
 RFM 분석을 3차원으로 표현하면 125개의 그룹이 발생하므로 굉장히 관리하기 어려움.
 RFM의 각 랭크 합계를 기반으로 13개 그룹으로 나누어 관리하는 방법
 */

-- 코드 11-22 통합 랭크를 계산하는 쿼리
with
    purchase_log as (
        select
            user_id
             , amount
             -- 타임스탬프를 기반으로 날짜 추출하기
             , substring(stamp, 1, 10) as dt
        from action_log
        where action = 'purchase'
    )
   , user_rfm as (
    select
        user_id
         , max(dt) as recent_date
         , current_date - max(dt::date) as recency
         , count(dt) as frequency
         , sum(amount) as monetary
    from purchase_log
    group by user_id
)
   , user_rfm_rank as (
    select
        user_id
         , recent_date
         , recency
         , frequency
         , monetary
         , case
               when recency < 14 then 5
               when recency < 28 then 4
               when recency < 60 then 3
               when recency < 90 then 2
               else 1
        end as r
         , case
               when 20 <= frequency then 5
               when 10 <= frequency then 4
               when 5 <= frequency then 3
               when 2 <= frequency then 2
               when 1 <= frequency then 1
        end as f
         , case
               when 300000 <= monetary then 5
               when 100000 <= monetary then 4
               when 30000 <= monetary then 3
               when 5000 <= monetary then 2
               else 1
        end as m
    from user_rfm
)
select
    r + f + m as total_rank
    , r, f, m
    , count(user_id)
from user_rfm_rank
group by r, f, m
order by total_rank desc, r desc, f desc, m desc;

-- 코드 11-23 종합 랭크별로 사용자 수를 집계하는 쿼리
with
    purchase_log as (
        select
            user_id
             , amount
             -- 타임스탬프를 기반으로 날짜 추출하기
             , substring(stamp, 1, 10) as dt
        from action_log
        where action = 'purchase'
    )
   , user_rfm as (
    select
        user_id
         , max(dt) as recent_date
         , current_date - max(dt::date) as recency
         , count(dt) as frequency
         , sum(amount) as monetary
    from purchase_log
    group by user_id
)
   , user_rfm_rank as (
    select
        user_id
         , recent_date
         , recency
         , frequency
         , monetary
         , case
               when recency < 14 then 5
               when recency < 28 then 4
               when recency < 60 then 3
               when recency < 90 then 2
               else 1
        end as r
         , case
               when 20 <= frequency then 5
               when 10 <= frequency then 4
               when 5 <= frequency then 3
               when 2 <= frequency then 2
               when 1 <= frequency then 1
        end as f
         , case
               when 300000 <= monetary then 5
               when 100000 <= monetary then 4
               when 30000 <= monetary then 3
               when 5000 <= monetary then 2
               else 1
        end as m
    from user_rfm
)
select
    r+f+m as total_rank
    , count(user_id)
from user_rfm_rank
group by total_rank
order by total_rank desc;

-- 2차원으로 사용자 인식하기

-- 코드 11-24 R과 F를 사용해 2차원 사용자 층의 사용자 수를 집계하는 쿼리
with
    purchase_log as (
        select
            user_id
             , amount
             -- 타임스탬프를 기반으로 날짜 추출하기
             , substring(stamp, 1, 10) as dt
        from action_log
        where action = 'purchase'
    )
   , user_rfm as (
    select
        user_id
         , max(dt) as recent_date
         , current_date - max(dt::date) as recency
         , count(dt) as frequency
         , sum(amount) as monetary
    from purchase_log
    group by user_id
)
   , user_rfm_rank as (
    select
        user_id
         , recent_date
         , recency
         , frequency
         , monetary
         , case
               when recency < 14 then 5
               when recency < 28 then 4
               when recency < 60 then 3
               when recency < 90 then 2
               else 1
        end as r
         , case
               when 20 <= frequency then 5
               when 10 <= frequency then 4
               when 5 <= frequency then 3
               when 2 <= frequency then 2
               when 1 <= frequency then 1
        end as f
         , case
               when 300000 <= monetary then 5
               when 100000 <= monetary then 4
               when 30000 <= monetary then 3
               when 5000 <= monetary then 2
               else 1
        end as m
    from user_rfm
)
select
    concat('r_', r) as r_rank
    , count(case when f=5 then 1 end) as f_5
    , count(case when f=4 then 1 end) as f_4
    , count(case when f=3 then 1 end) as f_3
    , count(case when f=2 then 1 end) as f_2
    , count(case when f=1 then 1 end) as f_1
from user_rfm_rank
group by r
order by r_rank desc;

/*
 어떤 대책을 실시할지 생각해보기
 신규 -> 단골 : 신규 배송 무료 쿠폰
 안정 -> 단골 : 페이스북 페이지 좋아요
 단골 이탈 전조 -> 단골 : 포인트 잔고 통지, 신규 상품 입고 메일
 신규 이탈 전조 -> 안정 : 신규 배송 무료 쿠폰
 */