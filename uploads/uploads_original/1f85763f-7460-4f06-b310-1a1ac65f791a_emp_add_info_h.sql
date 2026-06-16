# 数据库表结构：员工信息附加表
CREATE TABLE ldm.emp_add_info_h (
  emp_id varchar(50)  NOT NULL,
  emp_lob_num varchar(50) ,
  engage_it_work_dt date,
  serv_duration_start_dt date,
  trainee_flg char(1) ,
  recruit_channel_cd varchar(50) ,
  health_stat_cd varchar(10) ,
  s_dt_date varchar(8) ,
  e_dt_date varchar(8)  NOT NULL,
  emp_post_class_cd varchar(10) ,
  cont_tel_two varchar(100) ,
  regular_dt date,
  direct_director_id varchar(50) ,
  duty_hrbp_lob_num varchar(50) ,
  onshore_ehs_labor_no varchar(50) ,
  pay_commercial_insurance_flg char(1) ,
  emp_type_eff_dt date,
  lp_entity_eff_dt date,
  post_categ_eff_dt date,
  mgmt_blng_loc_eff_dt date,
  marg_status_eff_dt date,
  work_loc_eff_dt date,
  soc_sec_pay_loc_eff_dt date,
  pos_seq_eff_dt date,
  tax_loc_eff_dt date,
  emp_post_class_eff_dt date,
  director_id varchar(50) ,
  original_plan_regular_dt date,
  probation_perform varchar(100) ,
  onshore_ehs_labor_name varchar(50) ,
  entry_abnormal_material_supply_cd varchar(10) ,
  cust_per_id varchar(50) ,
  cust_per_name varchar(50) ,
  certif_due_dt date,
  certif_addr varchar(1000) ,
  tax_loc_county_cd varchar(100) ,
  tax_loc_town_cd varchar(100) ,
  soc_sec_pay_loc_county_cd varchar(100) ,
  mgmt_blng_loc_county_cd varchar(100) ,
  work_loc_county_cd varchar(100) ,
  post_cd varchar(20) ,
  bas_pos_cd varchar(20) ,
  reach_post_dt date,
  em_create_dt date,
  em_update_dt date,
  inter_viewer_flag char(1) ,
  more_entry_flg char(1) ,
  entry_num int2,
  first_entry_emp_id varchar(10) ,
  mid_sch_loc_provin_cd varchar(100) ,
  mid_sch_loc_city_cd varchar(100) ,
  grade_cd varchar(50) ,
  cont_tel_one varchar(100) ,
  post_rank_cd varchar(10) ,
  cont_tel_one_encrypt varchar(2000) ,
  cont_tel_two_encrypt varchar(2000) ,
  cust_per_id_encrypt varchar(2000) ,
  cust_per_name_encrypt varchar(2000) ,
  certif_addr_encrypt varchar(2000) ,
  CONSTRAINT emp_add_info_h_pkey PRIMARY KEY (emp_id, e_dt_date)
)
;
ALTER TABLE ldm.emp_add_info_h 
  OWNER TO ietl_operator;
COMMENT ON COLUMN ldm.emp_add_info_h.emp_id IS '员工编号';
COMMENT ON COLUMN ldm.emp_add_info_h.emp_lob_num IS '员工工号';
COMMENT ON COLUMN ldm.emp_add_info_h.engage_it_work_dt IS '从事IT工作日期';
COMMENT ON COLUMN ldm.emp_add_info_h.serv_duration_start_dt IS '司龄开始日期';
COMMENT ON COLUMN ldm.emp_add_info_h.trainee_flg IS '实习生标志';
COMMENT ON COLUMN ldm.emp_add_info_h.recruit_channel_cd IS '招聘渠道代码';
COMMENT ON COLUMN ldm.emp_add_info_h.health_stat_cd IS '健康状态代码';
COMMENT ON COLUMN ldm.emp_add_info_h.s_dt_date IS '开始日期';
COMMENT ON COLUMN ldm.emp_add_info_h.e_dt_date IS '结束日期';
COMMENT ON COLUMN ldm.emp_add_info_h.emp_post_class_cd IS '员工岗位分类代码';
COMMENT ON COLUMN ldm.emp_add_info_h.cont_tel_two IS '联系电话二';
COMMENT ON COLUMN ldm.emp_add_info_h.regular_dt IS '转正日期';
COMMENT ON COLUMN ldm.emp_add_info_h.direct_director_id IS '直接主管工号-EHS';
COMMENT ON COLUMN ldm.emp_add_info_h.duty_hrbp_lob_num IS '责任HRBP工号';
COMMENT ON COLUMN ldm.emp_add_info_h.onshore_ehs_labor_no IS '中软在岸EHS接口人工号';
COMMENT ON COLUMN ldm.emp_add_info_h.pay_commercial_insurance_flg IS '缴纳商业保险标志';
COMMENT ON COLUMN ldm.emp_add_info_h.emp_type_eff_dt IS '员工类型生效日期';
COMMENT ON COLUMN ldm.emp_add_info_h.lp_entity_eff_dt IS '法人实体生效日期';
COMMENT ON COLUMN ldm.emp_add_info_h.post_categ_eff_dt IS '岗位类别生效日期';
COMMENT ON COLUMN ldm.emp_add_info_h.mgmt_blng_loc_eff_dt IS '管理归属地生效日期';
COMMENT ON COLUMN ldm.emp_add_info_h.marg_status_eff_dt IS '婚姻状况生效日期';
COMMENT ON COLUMN ldm.emp_add_info_h.work_loc_eff_dt IS '工作地生效日期';
COMMENT ON COLUMN ldm.emp_add_info_h.soc_sec_pay_loc_eff_dt IS '社保缴纳地生效日期';
COMMENT ON COLUMN ldm.emp_add_info_h.pos_seq_eff_dt IS '职务序列生效日期';
COMMENT ON COLUMN ldm.emp_add_info_h.tax_loc_eff_dt IS '纳税地生效日期';
COMMENT ON COLUMN ldm.emp_add_info_h.emp_post_class_eff_dt IS '员工岗位分类生效日期';
COMMENT ON COLUMN ldm.emp_add_info_h.director_id IS '直属部门主管编号';
COMMENT ON COLUMN ldm.emp_add_info_h.original_plan_regular_dt IS '原计划转正日期';
COMMENT ON COLUMN ldm.emp_add_info_h.probation_perform IS '试用期绩效';
COMMENT ON COLUMN ldm.emp_add_info_h.onshore_ehs_labor_name IS '中软在岸EHS接口人姓名';
COMMENT ON COLUMN ldm.emp_add_info_h.entry_abnormal_material_supply_cd IS '入职异常材料补齐代码';
COMMENT ON COLUMN ldm.emp_add_info_h.cust_per_id IS '客户方接口人编号';
COMMENT ON COLUMN ldm.emp_add_info_h.cust_per_name IS '客户方接口人姓名';
COMMENT ON COLUMN ldm.emp_add_info_h.certif_due_dt IS '证件到期日期';
COMMENT ON COLUMN ldm.emp_add_info_h.certif_addr IS '证件地址';
COMMENT ON COLUMN ldm.emp_add_info_h.tax_loc_county_cd IS '纳税地区县代码';
COMMENT ON COLUMN ldm.emp_add_info_h.tax_loc_town_cd IS '纳税地乡镇代码';
COMMENT ON COLUMN ldm.emp_add_info_h.soc_sec_pay_loc_county_cd IS '社保缴纳地区县代码';
COMMENT ON COLUMN ldm.emp_add_info_h.mgmt_blng_loc_county_cd IS '管理归属地区县代码';
COMMENT ON COLUMN ldm.emp_add_info_h.work_loc_county_cd IS '工作地区县代码';
COMMENT ON COLUMN ldm.emp_add_info_h.post_cd IS '岗位代码';
COMMENT ON COLUMN ldm.emp_add_info_h.bas_pos_cd IS '基准职位代码';
COMMENT ON COLUMN ldm.emp_add_info_h.reach_post_dt IS '到岗日期';
COMMENT ON COLUMN ldm.emp_add_info_h.em_create_dt IS '档案系统数据创建日期';
COMMENT ON COLUMN ldm.emp_add_info_h.em_update_dt IS '档案系统数据更新日期';
COMMENT ON COLUMN ldm.emp_add_info_h.inter_viewer_flag IS '面试官人员标志';
COMMENT ON COLUMN ldm.emp_add_info_h.more_entry_flg IS '多次入职标志';
COMMENT ON COLUMN ldm.emp_add_info_h.entry_num IS '入职次数';
COMMENT ON COLUMN ldm.emp_add_info_h.first_entry_emp_id IS '首次入职员工编号';
COMMENT ON COLUMN ldm.emp_add_info_h.mid_sch_loc_provin_cd IS '中学所在地省份代码';
COMMENT ON COLUMN ldm.emp_add_info_h.mid_sch_loc_city_cd IS '中学所在地城市代码';
COMMENT ON COLUMN ldm.emp_add_info_h.grade_cd IS '岗级代码';
COMMENT ON COLUMN ldm.emp_add_info_h.cont_tel_one IS '联系电话一';
COMMENT ON COLUMN ldm.emp_add_info_h.post_rank_cd IS '岗位职级代码';
COMMENT ON COLUMN ldm.emp_add_info_h.cont_tel_one_encrypt IS '联系电话一(加密)';
COMMENT ON COLUMN ldm.emp_add_info_h.cont_tel_two_encrypt IS '联系电话二(加密)';
COMMENT ON COLUMN ldm.emp_add_info_h.cust_per_id_encrypt IS '客户方接口人编号(加密)';
COMMENT ON COLUMN ldm.emp_add_info_h.cust_per_name_encrypt IS '客户方接口人姓名(加密)';
COMMENT ON COLUMN ldm.emp_add_info_h.certif_addr_encrypt IS '证件地址(加密)';



# 查询语句：查询全表所有字段：
select 
a.emp_id, -- -- -- -- -- -- -- -- -- -- 员工编号
a.emp_lob_num, -- -- -- -- -- -- -- -- -员工工号
a.engage_it_work_dt, -- -- -- -- -- -- -从事IT工作日期
a.serv_duration_start_dt, -- -- -- -- --司龄开始日期
a.trainee_flg, -- -- -- -- -- -- -- -- -实习生标志
a.recruit_channel_cd, -- -- -- -- -- -- 招聘渠道代码
a.health_stat_cd, -- -- -- -- -- -- -- -健康状态代码
a.s_dt_date, -- -- -- -- -- -- -- -- -- 开始日期
a.e_dt_date, -- -- -- -- -- -- -- -- -- 结束日期
a.emp_post_class_cd, -- -- -- -- -- -- -员工岗位分类代码
a.cont_tel_two, -- -- -- -- -- -- -- -- 联系电话二
a.regular_dt, -- -- -- -- -- -- -- -- --转正日期
a.direct_director_id, -- -- -- -- -- -- 直接主管工号-EHS
a.duty_hrbp_lob_num, -- -- -- -- -- -- -责任HRBP工号
a.onshore_ehs_labor_no, -- -- -- -- -- -中软在岸EHS接口人工号
a.pay_commercial_insurance_flg, -- -- --缴纳商业保险标志
a.emp_type_eff_dt, -- -- -- -- -- -- -- 员工类型生效日期
a.lp_entity_eff_dt, -- -- -- -- -- -- --法人实体生效日期
a.post_categ_eff_dt, -- -- -- -- -- -- -岗位类别生效日期
a.mgmt_blng_loc_eff_dt, -- -- -- -- -- -管理归属地生效日期
a.marg_status_eff_dt, -- -- -- -- -- -- 婚姻状况生效日期
a.work_loc_eff_dt, -- -- -- -- -- -- -- 工作地生效日期
a.soc_sec_pay_loc_eff_dt, -- -- -- -- --社保缴纳地生效日期
a.pos_seq_eff_dt, -- -- -- -- -- -- -- -职务序列生效日期
a.tax_loc_eff_dt, -- -- -- -- -- -- -- -纳税地生效日期
a.emp_post_class_eff_dt, -- -- -- -- -- 员工岗位分类生效日期
a.director_id, -- -- -- -- -- -- -- -- -直属部门主管编号
a.original_plan_regular_dt, -- -- -- -- 原计划转正日期
a.probation_perform, -- -- -- -- -- -- -试用期绩效
a.onshore_ehs_labor_name, -- -- -- -- --中软在岸EHS接口人姓名
a.entry_abnormal_material_supply_cd, -- 入职异常材料补齐代码
a.cust_per_id, -- -- -- -- -- -- -- -- -客户方接口人编号
a.cust_per_name, -- -- -- -- -- -- -- --客户方接口人姓名
a.certif_due_dt, -- -- -- -- -- -- -- --证件到期日期
a.certif_addr, -- -- -- -- -- -- -- -- -证件地址
a.tax_loc_county_cd, -- -- -- -- -- -- -纳税地区县代码
a.tax_loc_town_cd, -- -- -- -- -- -- -- 纳税地乡镇代码
a.soc_sec_pay_loc_county_cd, -- -- -- --社保缴纳地区县代码
a.mgmt_blng_loc_county_cd, -- -- -- -- -管理归属地区县代码
a.work_loc_county_cd, -- -- -- -- -- -- 工作地区县代码
a.post_cd, -- -- -- -- -- -- -- -- -- --岗位代码
a.bas_pos_cd, -- -- -- -- -- -- -- -- --基准职位代码
a.reach_post_dt, -- -- -- -- -- -- -- --到岗日期
a.em_create_dt, -- -- -- -- -- -- -- -- 档案系统数据创建日期
a.em_update_dt, -- -- -- -- -- -- -- -- 档案系统数据更新日期
a.inter_viewer_flag, -- -- -- -- -- -- -面试官人员标志
a.more_entry_flg, -- -- -- -- -- -- -- -多次入职标志
a.entry_num, -- -- -- -- -- -- -- -- -- 入职次数
a.first_entry_emp_id, -- -- -- -- -- -- 首次入职员工编号
a.mid_sch_loc_provin_cd, -- -- -- -- -- 中学所在地省份代码
a.mid_sch_loc_city_cd, -- -- -- -- -- --中学所在地城市代码
a.grade_cd, -- -- -- -- -- -- -- -- -- -岗级代码
a.cont_tel_one, -- -- -- -- -- -- -- -- 联系电话一
a.post_rank_cd, -- -- -- -- -- -- -- -- 岗位职级代码
a.cont_tel_one_encrypt, -- -- -- -- -- -联系电话一(加密)
a.cont_tel_two_encrypt, -- -- -- -- -- -联系电话二(加密)
a.cust_per_id_encrypt, -- -- -- -- -- --客户方接口人编号(加密)
a.cust_per_name_encrypt, -- -- -- -- -- 客户方接口人姓名(加密)
a.certif_addr_encrypt -- -- -- -- -- --证件地址(加密)
from ldm.emp_add_info_h a 
where a.e_dt_date = '29991231';
