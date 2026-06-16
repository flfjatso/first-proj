# 数据库表结构：员工归属机构历史

CREATE TABLE ldm.emp_blng_org_h (
  emp_id varchar(50)  NOT NULL,
  blng_inner_org_id varchar(50) ,
  pos_seq_cd varchar ,
  part_time_flg char(1) ,
  s_dt_date varchar(8) ,
  e_dt_date varchar(8)  NOT NULL,
  eff_dt date,
  post_categ_cd varchar(8) ,
  job_classification_cd varchar(10) ,
  CONSTRAINT emp_blng_org_h_pkey PRIMARY KEY (emp_id, e_dt_date)
)
;

ALTER TABLE ldm.emp_blng_org_h 
  OWNER TO ietl_operator;

CREATE INDEX emp_blng_org_h_emp_id_idx ON ldm.emp_blng_org_h USING btree (
  emp_id  pg_catalog.text_ops ASC NULLS LAST,
  s_dt_date  pg_catalog.text_ops ASC NULLS LAST,
  e_dt_date  pg_catalog.text_ops ASC NULLS LAST
);

CREATE INDEX emp_blng_org_h_s_dt_date_idx ON ldm.emp_blng_org_h USING btree (
  (s_dt_date::integer) pg_catalog.int4_ops ASC NULLS LAST,
  (e_dt_date::integer) pg_catalog.int4_ops ASC NULLS LAST
);

COMMENT ON COLUMN ldm.emp_blng_org_h.emp_id IS '员工编号';
COMMENT ON COLUMN ldm.emp_blng_org_h.blng_inner_org_id IS '归属内部机构编号';
COMMENT ON COLUMN ldm.emp_blng_org_h.pos_seq_cd IS '职务序列代码';
COMMENT ON COLUMN ldm.emp_blng_org_h.part_time_flg IS '兼职标志(Y:主职；N:兼职)';
COMMENT ON COLUMN ldm.emp_blng_org_h.s_dt_date IS '开始日期';
COMMENT ON COLUMN ldm.emp_blng_org_h.e_dt_date IS '结束日期';
COMMENT ON COLUMN ldm.emp_blng_org_h.eff_dt IS '生效日期';
COMMENT ON COLUMN ldm.emp_blng_org_h.post_categ_cd IS '岗位类别代码';
COMMENT ON COLUMN ldm.emp_blng_org_h.job_classification_cd IS '职务分类代码';
COMMENT ON TABLE ldm.emp_blng_org_h IS '员工归属机构历史';

# 查询语句：查询全表所有字段：
select 
a.emp_id, -- -- -- -- -- -- -- -- -- -- 员工编号
a.blng_inner_org_id, -- -- -- -- -- -- -归属内部机构编号
a.pos_seq_cd, -- -- -- -- -- -- -- -- --职务序列代码
a.part_time_flg, -- -- -- -- -- -- -- --兼职标志(Y:主职；N:兼职)
a.s_dt_date, -- -- -- -- -- -- -- -- -- 开始日期
a.e_dt_date, -- -- -- -- -- -- -- -- -- 结束日期
a.eff_dt, -- -- -- -- -- -- -- -- -- -- 生效日期
a.eff_dt, -- -- -- -- -- -- -- -- -- -- 生效日期
a.post_categ_cd, -- -- -- -- -- -- -- --岗位类别代码
a.job_classification_cd-- -- -- -- -- 职务分类代码
from ldm.emp_blng_org_h a 
where a.s_dt_date <= '20260317' and a.e_st_date > '20260317';




#该只能使用拉链形式查询：
drop table if exists emp_blng_org_h_temp;
create temp table emp_blng_org_h_temp as 
select emp_id,blng_inner_org_id
from  ldm.emp_blng_org_h a 
where a..s_dt_date <= '20240508' and a.e_dt_date > '20240508'; 
create index emp_blng_org_h_temp_idx1 on emp_blng_org_h_temp(emp_id);


