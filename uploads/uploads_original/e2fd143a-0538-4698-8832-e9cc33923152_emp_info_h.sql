
# 数据库表结构：员工信息历史

CREATE TABLE ldm.emp_info_h (
  emp_id varchar(50)  NOT NULL,
  emp_lob_num varchar(50) ,
  emp_name varchar ,
  identity_no varchar ,
  birth_dt date,
  gen_cd varchar ,
  natn_cd varchar ,
  ethn_cd varchar ,
  political_outlook_cd varchar ,
  disability_flg char(1) ,
  marg_status_cd varchar(10) ,
  children_qtty numeric(10,0),
  cont_tel varchar(50) ,
  family_address varchar(500) ,
  common_addr varchar(2048) ,
  residence_type_cd varchar ,
  residence_loc_provin_cd varchar(10) ,
  dom_rgst_addr varchar(500) ,
  join_work_dt date,
  entry_dt date,
  probation_per_start_dt date,
  probation_per_plan_closing_dt date,
  probation_per_actl_closing_dt date,
  probation_per_assess_rslt_cd varchar ,
  lp_entity_id varchar ,
  mgmt_blng_loc_cntry_cd varchar ,
  mgmt_blng_loc_provin_cd varchar ,
  mgmt_blng_loc_city_cd varchar ,
  work_loc_cntry_cd varchar ,
  work_loc_provin_cd varchar ,
  work_loc_city_cd varchar ,
  tax_loc_cntry_cd varchar ,
  tax_loc_provin_cd varchar ,
  tax_loc_city_cd varchar ,
  soc_sec_pay_loc_cntry_cd varchar ,
  soc_sec_pay_loc_provin_cd varchar ,
  soc_sec_pay_loc_city_cd varchar ,
  emp_type_cd varchar ,
  comp_mailbox varchar(500) ,
  indv_mailbox varchar(500) ,
  graduating_stu_flg char(1) ,
  labor_contract_due_dt date,
  leave_dt date,
  leave_type_cd varchar ,
  leave_rsn_cd varchar ,
  s_dt_date varchar(8) ,
  e_dt_date varchar(8)  NOT NULL,
  key_flg char(1) ,
  input_delay_date date,
  leave_update_delay_date date,
  skill_mark char(1) ,
  leave_category varchar ,
  certificate_type_cd varchar ,
  emp_type_oper_cd varchar ,
  comp_mailbox_encrypt varchar(2000) ,
  identity_no_encrypt varchar(2000) ,
  cont_tel_encrypt varchar(2000) ,
  common_addr_encrypt varchar(2000) ,
  family_address_encrypt varchar(2000) ,
  indv_mailbox_encrypt varchar(2000) ,
  CONSTRAINT emp_info_h_pkey PRIMARY KEY (emp_id, e_dt_date)
)
;
ALTER TABLE ldm.emp_info_h 
  OWNER TO ietl_operator;
CREATE INDEX emp_info_h_emp_lob_num_idx ON ldm.emp_info_h USING btree (
  emp_lob_num  pg_catalog.text_ops ASC NULLS LAST
);
CREATE UNIQUE INDEX emp_info_h_emp_lob_num_unidx ON ldm.emp_info_h USING btree (
  emp_lob_num  pg_catalog.text_ops ASC NULLS LAST,
  e_dt_date  pg_catalog.text_ops ASC NULLS LAST
);
CREATE INDEX emp_info_h_identity_no_idx ON ldm.emp_info_h USING btree (
  identity_no  pg_catalog.text_ops ASC NULLS LAST
);
CREATE INDEX emp_info_h_s_dt_date_brin_idx ON ldm.emp_info_h USING brin (
  s_dt_date  pg_catalog.text_minmax_ops
);
CREATE INDEX emp_info_h_s_dt_date_idx ON ldm.emp_info_h USING btree (
  s_dt_date  pg_catalog.text_ops ASC NULLS LAST,
  e_dt_date  pg_catalog.text_ops ASC NULLS LAST
);
COMMENT ON COLUMN ldm.emp_info_h.emp_id IS '员工编号';
COMMENT ON COLUMN ldm.emp_info_h.emp_lob_num IS '员工工号';
COMMENT ON COLUMN ldm.emp_info_h.emp_name IS '员工姓名';
COMMENT ON COLUMN ldm.emp_info_h.identity_no IS '证件号码';
COMMENT ON COLUMN ldm.emp_info_h.birth_dt IS '出生日期';
COMMENT ON COLUMN ldm.emp_info_h.gen_cd IS '性别代码';
COMMENT ON COLUMN ldm.emp_info_h.natn_cd IS '国籍（地区）代码';
COMMENT ON COLUMN ldm.emp_info_h.ethn_cd IS '民族代码';
COMMENT ON COLUMN ldm.emp_info_h.political_outlook_cd IS '政治面貌代码';
COMMENT ON COLUMN ldm.emp_info_h.disability_flg IS '残疾标志';
COMMENT ON COLUMN ldm.emp_info_h.marg_status_cd IS '婚姻状况代码';
COMMENT ON COLUMN ldm.emp_info_h.children_qtty IS '子女数量';
COMMENT ON COLUMN ldm.emp_info_h.cont_tel IS '联系电话';
COMMENT ON COLUMN ldm.emp_info_h.family_address IS '家庭住址';
COMMENT ON COLUMN ldm.emp_info_h.common_addr IS '常用住址';
COMMENT ON COLUMN ldm.emp_info_h.residence_type_cd IS '户口类型代码';
COMMENT ON COLUMN ldm.emp_info_h.residence_loc_provin_cd IS '户口所在省份代码';
COMMENT ON COLUMN ldm.emp_info_h.dom_rgst_addr IS '户籍地址';
COMMENT ON COLUMN ldm.emp_info_h.join_work_dt IS '参加工作日期';
COMMENT ON COLUMN ldm.emp_info_h.entry_dt IS '入职日期';
COMMENT ON COLUMN ldm.emp_info_h.probation_per_start_dt IS '试用期开始日期';
COMMENT ON COLUMN ldm.emp_info_h.probation_per_plan_closing_dt IS '试用期计划截止日期';
COMMENT ON COLUMN ldm.emp_info_h.probation_per_actl_closing_dt IS '试用期实际截止日期';
COMMENT ON COLUMN ldm.emp_info_h.probation_per_assess_rslt_cd IS '试用期考核结果代码';
COMMENT ON COLUMN ldm.emp_info_h.lp_entity_id IS '法人实体编号';
COMMENT ON COLUMN ldm.emp_info_h.mgmt_blng_loc_cntry_cd IS '管理归属地国家代码';
COMMENT ON COLUMN ldm.emp_info_h.mgmt_blng_loc_provin_cd IS '管理归属地省份代码';
COMMENT ON COLUMN ldm.emp_info_h.mgmt_blng_loc_city_cd IS '管理归属地城市代码';
COMMENT ON COLUMN ldm.emp_info_h.work_loc_cntry_cd IS '工作地国家代码';
COMMENT ON COLUMN ldm.emp_info_h.work_loc_provin_cd IS '工作地省份代码';
COMMENT ON COLUMN ldm.emp_info_h.work_loc_city_cd IS '工作地城市代码';
COMMENT ON COLUMN ldm.emp_info_h.tax_loc_cntry_cd IS '纳税地国家代码';
COMMENT ON COLUMN ldm.emp_info_h.tax_loc_provin_cd IS '纳税地省份代码';
COMMENT ON COLUMN ldm.emp_info_h.tax_loc_city_cd IS '纳税地城市代码';
COMMENT ON COLUMN ldm.emp_info_h.soc_sec_pay_loc_cntry_cd IS '社保缴纳地国家代码';
COMMENT ON COLUMN ldm.emp_info_h.soc_sec_pay_loc_provin_cd IS '社保缴纳地省份代码';
COMMENT ON COLUMN ldm.emp_info_h.soc_sec_pay_loc_city_cd IS '社保缴纳地城市代码';
COMMENT ON COLUMN ldm.emp_info_h.emp_type_cd IS '员工类型代码';
COMMENT ON COLUMN ldm.emp_info_h.comp_mailbox IS '公司邮箱';
COMMENT ON COLUMN ldm.emp_info_h.indv_mailbox IS '个人邮箱';
COMMENT ON COLUMN ldm.emp_info_h.graduating_stu_flg IS '应届生标志';
COMMENT ON COLUMN ldm.emp_info_h.labor_contract_due_dt IS '劳动合同到期日期';
COMMENT ON COLUMN ldm.emp_info_h.leave_dt IS '离职日期';
COMMENT ON COLUMN ldm.emp_info_h.leave_type_cd IS '离职类型代码';
COMMENT ON COLUMN ldm.emp_info_h.leave_rsn_cd IS '离职原因代码';
COMMENT ON COLUMN ldm.emp_info_h.s_dt_date IS '开始日期';
COMMENT ON COLUMN ldm.emp_info_h.e_dt_date IS '结束日期';
COMMENT ON COLUMN ldm.emp_info_h.key_flg IS '骨干标志';
COMMENT ON COLUMN ldm.emp_info_h.input_delay_date IS '员工录入日期';
COMMENT ON COLUMN ldm.emp_info_h.leave_update_delay_date IS '员工离职日期录入日期';
COMMENT ON COLUMN ldm.emp_info_h.skill_mark IS '技术人员标识';
COMMENT ON COLUMN ldm.emp_info_h.leave_category IS '离职分类';
COMMENT ON COLUMN ldm.emp_info_h.certificate_type_cd IS '证件类型代码';
COMMENT ON COLUMN ldm.emp_info_h.emp_type_oper_cd IS '员工类型（运营）代码';
COMMENT ON COLUMN ldm.emp_info_h.comp_mailbox_encrypt IS '公司邮箱(加密)';
COMMENT ON COLUMN ldm.emp_info_h.identity_no_encrypt IS '证件号码(加密)';
COMMENT ON COLUMN ldm.emp_info_h.cont_tel_encrypt IS '手机号(加密)';
COMMENT ON COLUMN ldm.emp_info_h.common_addr_encrypt IS '常用住址(加密)';
COMMENT ON COLUMN ldm.emp_info_h.family_address_encrypt IS '家庭住址(加密)';
COMMENT ON COLUMN ldm.emp_info_h.indv_mailbox_encrypt IS '个人邮箱(加密)';
COMMENT ON TABLE ldm.emp_info_h IS '员工信息历史';

# 查询语句：查询全表所有字段：
select 
a.emp_id, -- -- -- -- -- -- -- -- -- -- 员工编号
a.emp_lob_num, -- -- -- -- -- -- -- -- -员工工号
a.emp_name, -- -- -- -- -- -- -- -- -- -员工姓名
a.identity_no, -- -- -- -- -- -- -- -- -证件号码
a.birth_dt, -- -- -- -- -- -- -- -- -- -出生日期
a.gen_cd, -- -- -- -- -- -- -- -- -- -- 性别代码
a.natn_cd, -- -- -- -- -- -- -- -- -- --国籍（地区）代码
a.ethn_cd, -- -- -- -- -- -- -- -- -- --民族代码
a.political_outlook_cd, -- -- -- -- -- -政治面貌代码
a.disability_flg, -- -- -- -- -- -- -- -残疾标志
a.marg_status_cd, -- -- -- -- -- -- -- -婚姻状况代码
a.children_qtty, -- -- -- -- -- -- -- --子女数量
a.cont_tel, -- -- -- -- -- -- -- -- -- -联系电话
a.family_address, -- -- -- -- -- -- -- -家庭住址
a.common_addr, -- -- -- -- -- -- -- -- -常用住址
a.residence_type_cd, -- -- -- -- -- -- -户口类型代码
a.residence_loc_provin_cd, -- -- -- -- -户口所在省份代码
a.dom_rgst_addr, -- -- -- -- -- -- -- --户籍地址
a.join_work_dt, -- -- -- -- -- -- -- -- 参加工作日期
a.entry_dt, -- -- -- -- -- -- -- -- -- -入职日期
a.probation_per_start_dt, -- -- -- -- --试用期开始日期
a.probation_per_plan_closing_dt, -- -- -试用期计划截止日期
a.probation_per_actl_closing_dt, -- -- -试用期实际截止日期
a.probation_per_assess_rslt_cd, -- -- --试用期考核结果代码
a.lp_entity_id, -- -- -- -- -- -- -- -- 法人实体编号
a.mgmt_blng_loc_cntry_cd, -- -- -- -- --管理归属地国家代码
a.mgmt_blng_loc_provin_cd, -- -- -- -- -管理归属地省份代码
a.mgmt_blng_loc_city_cd, -- -- -- -- -- 管理归属地城市代码
a.work_loc_cntry_cd, -- -- -- -- -- -- -工作地国家代码
a.work_loc_provin_cd, -- -- -- -- -- -- 工作地省份代码
a.work_loc_city_cd, -- -- -- -- -- -- --工作地城市代码
a.tax_loc_cntry_cd, -- -- -- -- -- -- --纳税地国家代码
a.tax_loc_provin_cd, -- -- -- -- -- -- -纳税地省份代码
a.tax_loc_city_cd, -- -- -- -- -- -- -- 纳税地城市代码
a.soc_sec_pay_loc_cntry_cd, -- -- -- -- 社保缴纳地国家代码
a.soc_sec_pay_loc_provin_cd, -- -- -- --社保缴纳地省份代码
a.soc_sec_pay_loc_city_cd, -- -- -- -- -社保缴纳地城市代码
a.emp_type_cd, -- -- -- -- -- -- -- -- -员工类型代码
a.comp_mailbox, -- -- -- -- -- -- -- -- 公司邮箱
a.indv_mailbox, -- -- -- -- -- -- -- -- 个人邮箱
a.graduating_stu_flg, -- -- -- -- -- -- 应届生标志
a.labor_contract_due_dt, -- -- -- -- -- 劳动合同到期日期
a.leave_dt, -- -- -- -- -- -- -- -- -- -离职日期
a.leave_type_cd, -- -- -- -- -- -- -- --离职类型代码
a.leave_rsn_cd, -- -- -- -- -- -- -- -- 离职原因代码
a.s_dt_date, -- -- -- -- -- -- -- -- -- 开始日期
a.e_dt_date, -- -- -- -- -- -- -- -- -- 结束日期
a.key_flg, -- -- -- -- -- -- -- -- -- --骨干标志
a.input_delay_date, -- -- -- -- -- -- --员工录入日期
a.leave_update_delay_date, -- -- -- -- -员工离职日期录入日期
a.skill_mark, -- -- -- -- -- -- -- -- --技术人员标识
a.leave_category, -- -- -- -- -- -- -- -离职分类
a.certificate_type_cd, -- -- -- -- -- --证件类型代码
a.emp_type_oper_cd, -- -- -- -- -- -- --员工类型（运营）代码
a.comp_mailbox_encrypt, -- -- -- -- -- -公司邮箱(加密)
a.identity_no_encrypt, -- -- -- -- -- --证件号码(加密)
a.cont_tel_encrypt, -- -- -- -- -- -- --手机号(加密)
a.common_addr_encrypt, -- -- -- -- -- --常用住址(加密)
a.family_address_encrypt, -- -- -- -- --家庭住址(加密)
a.indv_mailbox_encrypt  -- -- -- -- -- -个人邮箱(加密)
from ldm.emp_info_h a 
where a.e_dt_date = '29991231';

#用户信息最新数据查询
select * from ldm.emp_info_h where e_dt_date = '29991231' ;

#用户信息历史拉链查询
select * from ldm.emp_info_h where s_dt_date >= '20250131' and e_dt_date > '20250131';

#随机查询2条数据
select * from ldm.emp_info_h where e_dt_date = '29991231' limit 2

emp_id	emp_lob_num	emp_name	identity_no	birth_dt	gen_cd	natn_cd	ethn_cd	political_outlook_cd	disability_flg	marg_status_cd	children_qtty	cont_tel	family_address	common_addr	residence_type_cd	residence_loc_provin_cd	dom_rgst_addr	join_work_dt	entry_dt	probation_per_start_dt	probation_per_plan_closing_dt	probation_per_actl_closing_dt	probation_per_assess_rslt_cd	lp_entity_id	mgmt_blng_loc_cntry_cd	mgmt_blng_loc_provin_cd	mgmt_blng_loc_city_cd	work_loc_cntry_cd	work_loc_provin_cd	work_loc_city_cd	tax_loc_cntry_cd	tax_loc_provin_cd	tax_loc_city_cd	soc_sec_pay_loc_cntry_cd	soc_sec_pay_loc_provin_cd	soc_sec_pay_loc_city_cd	emp_type_cd	comp_mailbox	indv_mailbox	graduating_stu_flg	labor_contract_due_dt	leave_dt	leave_type_cd	leave_rsn_cd	s_dt_date	e_dt_date	key_flg	input_delay_date	leave_update_delay_date	skill_mark	leave_category	certificate_type_cd	emp_type_oper_cd	comp_mailbox_encrypt	identity_no_encrypt	cont_tel_encrypt	common_addr_encrypt	family_address_encrypt	indv_mailbox_encrypt
E100101275	0090131159	李*	370923197112010058	1991-02-03	1	CHN	01	03	0	10		15100000000		北京市******************	04	370000	山东省	2014-09-01	2016-11-03			2017-02-02		300000	CHN	310000	310100	CHN	110000	110100	CHN	110000	110100	CHN	110000	110100	1	Li******@chinasofti.com	15*********@163.com	0	2019-11-02	2017-10-18	A	A2(1)	20240815	29991231	0	2016-11-18	2017-10-23	1	0100	C01	STC03	QimMK6O4hXMxu+A5tXd6IJWoGwNqz/c6eiqChYQxvMI=	6vE/jc0rdw6GEX0NWb69KHW96UboGr7UZAAY7v5nmCs=	TfwPxcDQiU+cwKFqwI5+nA==	6/TB7VL4dEZxJ/yDnzffWDHewjaDanYTZqrgibLXS11c+NEWsS8BNGBGPSalNdhmm/y7kehRDTzVYbyIC+aKjg==		ADMofafybDK8C39xB6OaDiFe4h9NhvR4bb9LJbF5+jY=
E200302980	0000044242	丁**	372925197112016734	1989-07-02	1	CHN	01	13	0	10		18500000008	山东省****************		04	370000	山东省	2010-04-27	2015-05-25	2015-05-25	2015-08-24			503000	CHN	110000	110100	CHN	110000	110100	CHN	110000	110100	CHN	110000	110100	1	di**********@chinasoftinc.com	di**********@chinasoftinc.com	0	2018-05-25	2017-07-04	A	ORG2	20240815	29991231	0	2016-11-18	2017-06-27	0	0100	C01		/xQvKMCJ+jalmwN++UHO0Q9rmBkd+0CqNCCVmly+fCw=	KpNDvtUdebIpxzFSKoj09LvPHcfpW8usLy6O5kwueXk=	kkSa6KJJDpdi2mfKihlbnw==		/qc4hlZJVTEOgmM8OfTxTEBu67DxArdFXAG0w1WkC9/5aP+Zhv/Kd//1hh3pcqdjxg661YKtXHkbB8gfDpwclg==	/xQvKMCJ+jalmwN++UHO0Q9rmBkd+0CqNCCVmly+fCw=


# 查询人员所在部门信息 ：
 select a.emp_id,c.*
 from ldm.emp_info_h a 
 left join ldm.emp_blng_org_h b on a.emp_id = b.emp_id and b.s_dt_date <= '20250401' and b.e_dt_date > '20250401' 
 left join sum.sum_org_all_summary_h c on b.blng_inner_org_id = c.inner_org_id and c.e_dt_date = '29991231'
 where a.e_dt_date = '29991231' and emp_lob_num = '0000003144' 
 
# 员工归属机构历史
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

# 部门信息 

CREATE TABLE sum.sum_org_all_summary_h (
  inner_org_id varchar(50) COLLATE pg_catalog.default NOT NULL,
  inner_org_nam varchar(50) COLLATE pg_catalog.default,
  super_inner_org_id text COLLATE pg_catalog.default,
  parent_ids text COLLATE pg_catalog.default,
  parent_ids_spare text COLLATE pg_catalog.default,
  org_arr text[] COLLATE pg_catalog.default,
  inner_org_type text COLLATE pg_catalog.default,
  inner_org_hirc_cd text COLLATE pg_catalog.default,
  gp_nam varchar(50) COLLATE pg_catalog.default,
  lob_group_nam varchar(50) COLLATE pg_catalog.default,
  lob_nam varchar(50) COLLATE pg_catalog.default,
  budu_nam varchar(50) COLLATE pg_catalog.default,
  dd_nam varchar(50) COLLATE pg_catalog.default,
  ds_nam varchar(50) COLLATE pg_catalog.default,
  is_valid varchar(2) COLLATE pg_catalog.default,
  s_dt_date varchar(8) COLLATE pg_catalog.default,
  e_dt_date varchar(8) COLLATE pg_catalog.default NOT NULL,
  management_dep_cd int4,
  org_attr_cd varchar(10) COLLATE pg_catalog.default,
  vir_attr_cd varchar(10) COLLATE pg_catalog.default,
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
  org_arr COLLATE pg_catalog.default pg_catalog.array_ops
);
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
 
 
 
