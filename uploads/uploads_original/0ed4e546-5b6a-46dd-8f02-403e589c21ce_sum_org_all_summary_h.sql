# 数据库表结构：部门机构表
CREATE TABLE sum.sum_org_all_summary_h (
  inner_org_id varchar(50)  NOT NULL,
  inner_org_nam varchar(50) ,
  super_inner_org_id text ,
  parent_ids text ,
  parent_ids_spare text ,
  org_arr text[] ,
  inner_org_type text ,
  inner_org_hirc_cd text ,
  gp_nam varchar(50) ,
  lob_group_nam varchar(50) ,
  lob_nam varchar(50) ,
  budu_nam varchar(50) ,
  dd_nam varchar(50) ,
  ds_nam varchar(50) ,
  is_valid varchar(2) ,
  s_dt_date varchar(8) ,
  e_dt_date varchar(8)  NOT NULL,
  management_dep_cd int4,
  org_attr_cd varchar(10) ,
  vir_attr_cd varchar(10) ,
  CONSTRAINT sum_org_all_summary_pkey PRIMARY KEY (inner_org_id, e_dt_date)
)
;

ALTER TABLE sum.sum_org_all_summary_h 
  OWNER TO ietl_operator;
CREATE INDEX sum_org_all_summary_h_e_dt_date_idx ON sum.sum_org_all_summary_h USING btree (
  (e_dt_date::integer) pg_catalog.int4_ops ASC NULLS LAST,
  (s_dt_date::integer) pg_catalog.int4_ops ASC NULLS LAST
);
CREATE INDEX sum_org_all_summary_h_org_arr_idx ON sum.sum_org_all_summary_h USING gin (
  org_arr  pg_catalog.array_ops
COMMENT ON COLUMN sum.sum_org_all_summary_h.inner_org_id IS '机构coa';
COMMENT ON COLUMN sum.sum_org_all_summary_h.inner_org_nam IS '机构名称';
COMMENT ON COLUMN sum.sum_org_all_summary_h.super_inner_org_id IS '父级coa';
COMMENT ON COLUMN sum.sum_org_all_summary_h.parent_ids IS '所有父级coa[ ]格式';
COMMENT ON COLUMN sum.sum_org_all_summary_h.parent_ids_spare IS '所有父级coa - 格式';
COMMENT ON COLUMN sum.sum_org_all_summary_h.org_arr IS '所有父级coa数组';
COMMENT ON COLUMN sum.sum_org_all_summary_h.inner_org_type IS '机构层级类型';
COMMENT ON COLUMN sum.sum_org_all_summary_h.inner_org_hirc_cd IS '机构层级';
COMMENT ON COLUMN sum.sum_org_all_summary_h.gp_nam IS '集团';
COMMENT ON COLUMN sum.sum_org_all_summary_h.lob_group_nam IS '业务群';
COMMENT ON COLUMN sum.sum_org_all_summary_h.lob_nam IS '业务线';
COMMENT ON COLUMN sum.sum_org_all_summary_h.budu_nam IS '事业部';
COMMENT ON COLUMN sum.sum_org_all_summary_h.dd_nam IS '交付部';
COMMENT ON COLUMN sum.sum_org_all_summary_h.ds_nam IS '交付分部';
COMMENT ON COLUMN sum.sum_org_all_summary_h.is_valid IS '是否有效：1有效，0失效';
COMMENT ON COLUMN sum.sum_org_all_summary_h.s_dt_date IS '开始日期';
COMMENT ON COLUMN sum.sum_org_all_summary_h.e_dt_date IS '结束日期';
COMMENT ON COLUMN sum.sum_org_all_summary_h.management_dep_cd IS '管理类型';
COMMENT ON COLUMN sum.sum_org_all_summary_h.org_attr_cd IS '部门属性代码';
COMMENT ON COLUMN sum.sum_org_all_summary_h.vir_attr_cd IS '虚实属性代码';

# 查询语句：查询全表所有字段：
select 
a.inner_org_id, -- -- -- -- -- -- -- -- 机构coa
a.inner_org_nam, -- -- -- -- -- -- -- --机构名称
a.super_inner_org_id, -- -- -- -- -- -- 父级coa
a.parent_ids, -- -- -- -- -- -- -- -- --所有父级coa[ ]格式
a.parent_ids_spare, -- -- -- -- -- -- --所有父级coa - 格式
a.org_arr, -- -- -- -- -- -- -- -- -- --所有父级coa数组
a.inner_org_type, -- -- -- -- -- -- -- -机构层级类型
a.inner_org_hirc_cd, -- -- -- -- -- -- -机构层级
a.gp_nam, -- -- -- -- -- -- -- -- -- -- 集团
a.lob_group_nam, -- -- -- -- -- -- -- --业务群
a.lob_nam, -- -- -- -- -- -- -- -- -- --业务线
a.budu_nam, -- -- -- -- -- -- -- -- -- -事业部
a.dd_nam, -- -- -- -- -- -- -- -- -- -- 交付部
a.ds_nam, -- -- -- -- -- -- -- -- -- -- 交付分部
a.is_valid, -- -- -- -- -- -- -- -- -- -是否有效：1有效，0失效
a.s_dt_date, -- -- -- -- -- -- -- -- -- 开始日期
a.e_dt_date, -- -- -- -- -- -- -- -- -- 结束日期
a.management_dep_cd, -- -- -- -- -- -- -管理类型
a.org_attr_cd, -- -- -- -- -- -- -- -- -部门属性代码
a.vir_attr_cd -- -- -- -- -- -- -- -- -虚实属性代码 
where sum.sum_org_all_summary_h a 
where a.e_dt_date = '29991231';

 
#常用关联查
drop table if exists sum_org_all_summary_h_temp;
create temp table sum_org_all_summary_h_temp as 
select inner_org_id,inner_org_nam,super_inner_org_id,org_arr, 
gp_nam,lob_group_nam,lob_nam,budu_nam,dd_nam,inner_org_hirc_cd,is_valid 
from sum.sum_org_all_summary_h a where e_dt_date = '29991231';
create index sum_org_all_summary_h_temp_idx1 on sum_org_all_summary_h_temp(inner_org_id);
