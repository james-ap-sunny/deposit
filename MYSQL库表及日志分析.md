索引

1. 活期账户存款表（rb_acct）结构说明 ............................................. 第2行
2. 活期账户余额表（rb_acct_balance）结构说明 ................................. 约第120行
3. 账户余额历史表（rb_acct_balance_hist）结构说明 .......................... 约第150行
4. 总账核算流水表（rb_gl_hist）结构说明 ........................................ 约第182行
5. 日间TAE流水表（rb_tae_info）结构说明 ........................................ 约第350行
6. 原始交易报文表（fw_tran_info）结构说明 ....................................... 约第400行
7. In_msg报文字段值格式化展示（多组） ........................................... 约第500行及以后
8. 核心系统生产日志信息分析 ..................................................... 约第600行
9. 核心系统生产日志原始内容示例 ................................................ 约第630行
10. 慢SQL分析与业务推断 ........................................................ 约第650行

注：行号为估算，实际查阅请结合全文搜索章节标题。


活期账户存款表（rb_acct）结构说明
1. 表名与用途
表名：rb_acct
用途：记录银行客户活期账户的基础信息，包括账户属性、客户信息、账户状态、开户销户、利息、币种、分支机构等。


字段名	类型	说明
INTERNAL_KEY	bigint	账户内部键值，主键
CLIENT_NO	varchar(20)	客户号
BASE_ACCT_NO	varchar(50)	账户号/卡号
CLIENT_TYPE	varchar(6)	客户类型（如个人、公司）
INDIVIDUAL_FLAG	char(1)	是否个人客户标志
DOCUMENT_ID	varchar(50)	证件号码
DOCUMENT_TYPE	varchar(4)	证件类型
ISS_COUNTRY	varchar(3)	证件签发国家
ACCT_CLASS	char(1)	账户分类
CARD_NO	varchar(50)	卡号
PROD_TYPE	varchar(20)	产品类型
ACCT_CCY	varchar(3)	币种
ACCT_SEQ_NO	varchar(5)	账户序号
PROFIT_CENTER	varchar(20)	利润中心
ACCT_NAME	varchar(200)	账户名称
ACCT_NAME_PREFIX	varchar(50)	账户名称前缀
ACCT_NAME_SUFFIX	varchar(50)	账户名称后缀
ALT_ACCT_NAME	varchar(200)	账户别名
ACCT_BRANCH	varchar(20)	开户网点
ACCT_DESC	varchar(200)	账户描述
SOURCE_TYPE	varchar(10)	来源类型
ACCT_OPEN_DATE	datetime	开户日期
EFFECT_DATE	datetime	生效日期
OPEN_TRAN_DATE	datetime	开户交易日期
ACCT_STATUS	char(1)	账户状态
ACCT_STATUS_PREV	char(1)	账户上一次状态
ACCT_STATUS_UPD_DATE	datetime	账户状态变更日期
ACCT_CLOSE_DATE	datetime	销户日期
ACCT_CLOSE_USER_ID	varchar(30)	销户柜员
ACCT_CLOSE_REASON	varchar(30)	销户原因
ACCT_TYPE	varchar(3)	账户类型
TERM	varchar(10)	期限类型
TERM_TYPE	char(10)	期限类型，Q-季，Y-年，Q-季，M-月，W-周，D-日
MATURITY_DATE	datetime	到期日，定期到期/通知到期/大额存单到期
ORI_MATURITY_DATE	datetime	原始到期日，账户首次开立时的到期日，未进行期限变更时的到期日
ORIG_ACCT_OPEN_DATE	datetime	原始开户日期，账户首次开立日期，未进行过转存的首次开立日期
ACCT_NATURE	varchar(10)	账户性质
ACCT_DUE_DATE	datetime	账户到期日
ACCT_REAL_FLAG	char(1)	账户是否虚实标志，Y-实账户，N-虚账户
ACCT_RES_STATUS	char(2)	账户限额状态，Y-限额，N-不限额
ACCT_STOP_PAY	char(1)	账户止付状态，Y-止付，N-可付
ALL_DEP_IND	char(1)	是否全额存款，Y-是，N-否
ALL_DRA_IND	char(1)	是否全额支取，Y-是，N-否
FIXED_ACCT_CLASS	char(1)	定期账户分类，A-协议存款，B-一定期一本通，C-通知存款，D-定活两便，E-教育储蓄，F-整存整取，L-零存整取，M-大额存单
LEAD_ACCT_FLAG	char(1)	主账户标志，Y-是，N-否
ACCT_LICENSE_DATE	datetime	账户许可证签发日期
ACCT_LICENSE_NO	varchar(50)	账户许可证号
MAIN_PROD_TYPE	varchar(20)	主账户产品类型
MAIN_BAL_FLAG	char(1)	主账户是否带余额，Y-是，N-否
MAIN_INT_FLAG	char(1)	主账户是否带利息，Y-是，N-否
PARENT_INTERNAL_KEY	bigint	上级账户内部识别号
REASON_CODE	varchar(10)	原因代码
ACCOUNTING_STATUS_UPD_DATE	datetime	账户状态变更日期
APPROVAL_DATE	datetime	复核日期
AUTO_RENEW_ROLLOVER	char(1)	是否自动转存，N-不自动转存，Y-本金自动转存，O-本息自动转存
PARTIAL_RENEW_ROLL	char(1)	是否部分转存，Y-是，N-否
TIMES_RENEWED	int	已续存次数
RENEW_NO	int	本条续存序号
ROLLOVER_IND	int	是否转存，Y-是，N-否
TIMES_ROLLEDOVER	int	已转存次数
LAST_MVMT_STATUS	char(1)	上一次更改状态，I-利息支出，O-本息转存，P-部分提前支取，R-到期支取，W-部分选择支取
ADULT_PRINCIPAL	char(1)	是否允许增加本金，Y-是，N-否
DOMINANT_DATE	datetime	主导日期
FINAL_TRAN_DATE	datetime	最后交易日期
SETTLE_DATE	datetime	结算日期
BATCH_APPLY_BRANCH	varchar(20)	申请机构编号
HOME_BRANCH	varchar(20)	客户归属机构编号
DOC_TYPE	varchar(10)	凭证类型
PREFIX	varchar(10)	凭证起始号码
VOUCHER_START_NO	varchar(50)	凭证起始号码
VOUCHER_STATUS	varchar(3)	凭证状态（INUS-未使用, WAY-待销毁, WDE-待销毁在途, DES-销毁, LCB-丢失, CAN-已作废, LO-C-已退回, SOL-空头支票, ACP-已承兑, VER-已核销, USE-已使用, FOB-已冻结）
APPR_LETTER_NO	varchar(30)	审批函编号
INT_IND_FLAG	char(1)	复核标志，Y-复核，N-未复核
XRATE	decimal(15,4)	汇率
FLAG	char(1)	标志
AUTO_SETTLE_FLAG	char(1)	自动结清标志，Y-是，N-否
BAL_TYPE	char(2)	余额类型，CA-客户账户，GL-总账账户，R-客户监管账户
GL_TYPE	char(1)	总账类型，内账-在账，外账-监管账户
MULTI_BAL_TYPE_FLAG	char(5)	多余额类型标志
NOTICE_PERIOD	varchar(20)	通知期限
NO_TRAN_FLAG	char(1)	16个月无交易标志，Y-是，N-否
OSA_FLAG	char(1)	OSA账户标志
OWNERSHIP_TYPE	char(2)	账户归属类型，IAS-多币种联合, SG-独立账户, SU-继承账户
REGION_FLAG	char(1)	区域账户标志，I-In region, O-offshore(离岸)
ACCOUNTING_STATUS	char(3)	上次核算状态，ZHC-正常, YUQ-逾期, FYJ-非应计, FY-手工转非应计, WRN-核销, TER-终止
ACCOUNTING_STATUS_PREV	char(3)	上次核算状态
ACCT_EXEC	varchar(30)	客户经理
CHECKED_FLAG	char(1)	是否已核查，Y-是，N-否
MANAGEMENT_FREE_FLAG	char(1)	对私免收管理费标志，Y-是，N-否
XRATE1	char(1)	汇率1
OLD_PROD_TYPE	varchar(20)	原产品类型
IMPOUND_FAD	char(1)	是否已冻结，Y-是，N-否
BUSINESS_UNIT	varchar(50)	业务单元
CUR_STAGE_NO	varchar(30)	当前阶段编号
SETTLE	char(1)	结算标志
SETTLE_USER_ID	varchar(30)	结算柜员
MM_REF_NO	varchar(50)	MM参考号
DAC_VALUE	varchar(30)	DAC值
SOURCE_MODULE	varchar(30)	来源模块
TELLER_ID	varchar(30)	交易柜员号
APPR_USER_ID	varchar(30)	审批柜员号
USER_ID	varchar(30)	交易柜员号
LAST_CHANGE_DATE	datetime	最后变更日期
LAST_CHANGE_USER_ID	varchar(30)	最后修改柜员号
TRAN_TIMESTAMP	varchar(26)	交易时间戳
COMPANY	varchar(20)	公司
ACCT_PROPERTY2	varchar(10)	账户性质2（1-账户开立使用，J-结算类，T-投融资类）
JOINT_ACCT_FLAG	char(1)	联名账户标志，Y-是，N-否
AGREEMENT_ID	varchar(50)	协议编号
RECOVER_FLAG	char(1)	实付追缴标志，Y-是，N-否
AGRE_PROD_TYPE	varchar(20)	协议产品类型
VOF_RATE	decimal(15,8)	资金收益利率
REMAIN_TERM	varchar(2)	剩余期限，标识定期账户剩余期限或者通知情况（如A-0D, B-7D, C-1M, D-2M, E-3M, F-6M, G-1Y, H-2Y, I-3Y, J-999Y, P-999P, Q-001P, R-003F, S-006P, T-998P, X-999Y）
REMAIN_TERM_PRE	varchar(2)	上一账户剩余期限
TRF_OPEN_FALG	char(1)	大额存单账户信息，是否转让开户，Y-大额存单转让开户，N-非转让开户
ACCT_NAME_EN	varchar(200)	账户英文名
AMEND_DATE	datetime	变更日期
OPEN_USER_ID	varchar(10)	开户柜员编号
CATEGORY_TYPE	varchar(6)	客户细分类型
CREATE_TIMESTAMP	varchar(26)	数据创建时间戳
CLIENT_ACCOUNTING_FLAG	char(1)	客户细账是否参与核算，Y-参与核算，N-不参与核算


活期账户余额表（rb_acct_balance）结构说明
1. 表名与用途
表名：rb_acct_balance
用途：记录银行客户活期账户的余额信息，包括账户内部键值、汇总金额、历史余额等。

字段名	类型	说明
INTERNAL_KEY	bigint	账户内部键值，主键
TOTAL_AMOUNT	decimal(20,2)	汇总金额
TOTAL_AMOUNT_PREV	decimal(20,2)	上日总金额
TOTAL_AMOUNT_LAST_PREV	decimal(20,2)	上上日汇总余额（分分核对用）
FLD_AMOUNT	decimal(20,2)	转账复核登记薄金额
FINREG_AMOUNT	decimal(20,2)	理财登记薄账户金额
DOS_AMOUNT	decimal(20,2)	欠息金额
OD_AMOUNT	decimal(20,2)	透支金额
ODD_AMOUNT	decimal(20,2)	透支总金额
LAST_BAL_UPD_DATE	datetime	上次余额日期
LAST_CHANGE_DATE	datetime	最后修改日期
LAST_CHANGE_USER_ID	varchar(30)	最后修改柜员号
CLIENT_NO	varchar(20)	客户号
DAC_VALUE	varchar(20)	DAC值防篡改加密
TRAN_TIMESTAMP	varchar(26)	交易时间戳
COMPANY	varchar(20)	法人
LCY_TOTAL_AMOUNT	decimal(20,2)	本币余额
CREATE_TIMESTAMP	varchar(26)	数据创建时间戳


账户余额历史表（rb_acct_balance_hist）结构说明
1. 表名与用途
表名：rb_acct_balance_hist
用途：记录银行客户活期账户的余额历史信息，包括账户内部键值、交易日期、汇总金额、历史余额等。

字段名	类型	说明
INTERNAL_KEY	bigint	账户内部键值，主键
TRAN_DATE	datetime	交易日期
TOTAL_AMOUNT	decimal(20,2)	汇总金额
TOTAL_AMOUNT_PREV	decimal(20,2)	上日总金额
TOTAL_AMOUNT_LAST_PREV	decimal(20,2)	上上日汇总余额（分分核对用）
FLD_AMOUNT	decimal(20,2)	冻结金额
FINREG_AMOUNT	decimal(20,2)	理财登记薄账户金额
DOS_AMOUNT	decimal(20,2)	欠息金额
OD_AMOUNT	decimal(20,2)	透支金额
ODD_AMOUNT	decimal(20,2)	透支总金额
CLIENT_NO	varchar(20)	客户号
DAC_VALUE	varchar(200)	DAC值防篡改加密
LAST_CHANGE_DATE	datetime	最后修改日期
LAST_CHANGE_USER_ID	varchar(30)	最后修改柜员号
TRAN_TIMESTAMP	varchar(26)	交易时间戳
COMPANY	varchar(20)	法人
CREATE_TIMESTAMP	varchar(26)	数据创建时间戳


总账核算流水表（rb_gl_hist）结构说明
1. 表名与用途
表名：rb_gl_hist
用途：记录银行客户账户的总账核算流水信息，包括账户、交易、金额、产品、科目等详细信息。

字段名	类型	说明
GL_SEQ_NO	varchar(50)	总账序号
CHANNEL_SEQ_NO	varchar(50)	渠道流水号
INTERNAL_KEY	bigint	账户内部键值
PROD_TYPE	varchar(20)	账户类型
BASE_ACCT_NO	varchar(50)	账户号/卡号
ACCT_CCY	varchar(3)	账户币种
ACCT_SEQ_NO	varchar(5)	账户序列号
ACCT_BRANCH	varchar(20)	账户开户机构
CLIENT_NO	varchar(20)	客户号
CLIENT_TYPE	varchar(6)	客户类型
CHANNEL_DATE	datetime	渠道日期
EFFECT_DATE	datetime	生效日期
TRAN_DATE	datetime	交易日期
TRAN_BRANCH	varchar(20)	交易机构
TRAN_TYPE	varchar(10)	交易类型
CR_DR_IND	char(1)	借贷标志（C-贷，D-借）
EVENT_TYPE	varchar(20)	事件类型
CCY	varchar(3)	币种
GL_CODE	varchar(20)	科目代码
MARKETING_PROD	varchar(20)	营销产品
MARKETING_PROD_DESC	varchar(200)	营销产品名称
FLAT_RATE	decimal(15,8)	业务流水号
SUB_SEQ_NO	varchar(10)	子流水号
REFERENCE	varchar(50)	系统流水号/交易参考号
AMOUNT	decimal(20,2)	交易金额
AMT_TYPE	varchar(20)	金额类型（BAL-余额，DDA-发放金额，INFP-逾期利息，LIM-额度金额，OD-透支金额，ODIP-逾期复利，ODPP-逾期罚息）
INT_AMT	decimal(20,2)	利息金额
ODI_AMT	decimal(20,2)	逾期利息金额
PRI_AMT	decimal(20,2)	本金金额
TAX_AMT	decimal(20,2)	税金金额
CONTRA_EQUITY_AMT	decimal(20,2)	他行管值金额
ODP_AMT	decimal(20,2)	罚息金额
CROSS_RATE	decimal(15,8)	交叉汇率
SPREAD_PERCENT	decimal(15,8)	浮动百分比/贴现百分比
GL_POSTED_FLAG	char(1)	过账标记，Y-是，N-否
IN_STATUS	char(1)	批量插入状态，B-批量插入，O-流水插入
REVERSAL_FLAG	char(1)	是否冲正，Y-是，N-否
ACCOUNTING_STATUS	varchar(3)	核算状态，ZHC-正常，YUQ-逾期，FYJ-非应计，FY-手工转非应计，WRN-核销，TER-终止
BANK_SEQ_NO	varchar(50)	银行交易序号
BUSINESS_UNIT	varchar(50)	业务单元
TRAN_CATEGORY	varchar(50)	交易类别
TRAN_PROFIT_CENTER	varchar(20)	交易利润中心
PROFIT_CENTER	varchar(20)	利润中心
SEND_SYSTEM	varchar(20)	发起系统
SOURCE_TYPE	varchar(10)	来源类型
SOURCE_MODULE	varchar(10)	来源模块
SYSTEM_ID	varchar(20)	系统编号
UN_REAL	char(1)	是否未实现，Y-是，N-否
RESERVE1	varchar(50)	保留字段1
NARRATIVE	varchar(500)	摘要
TRAN_TIMESTAMP	varchar(26)	交易时间戳
COMPANY	varchar(20)	法人
USER_ID	varchar(30)	交易柜员号
RULE_NO	varchar(20)	规则编号
BALANCE_CHANGE_TYPE	varchar(5)	余额变化类型，up-增加，down-减少
DEAL_FLAG	char(1)	是否处理，Y-是，N-否
REMAIN_TERM	varchar(2)	剩余期限，标识定期账户剩余期限或者通知情况（如A-0D, B-7D, C-1M, D-2M, E-3M, F-6M, G-1Y, H-2Y, I-3Y, J-999Y, P-999P, Q-001P, R-003F, S-006P, T-998P, X-999Y）
CUST_RATE	decimal(15,8)	客户汇率
LOCAL_CCY	varchar(3)	当地币种
LCY_TRAN_AMT	decimal(20,2)	本地币种交易金额
CAPTURE_TERMINAL_ID	varchar(30)	终端ID
PROGRAM_ID	varchar(20)	作业编号
INPUT_MEDIUM_ID	varchar(30)	入账媒介ID
UNION_REF	varchar(50)	会计平账联合参考号
MANUAL_ACCOUNT_FLAG	char(1)	手工记账标志，Y-是，N-否
INLAND_OFFSHORE	char(1)	境内外标志，I-境内，O-境外
INDUSTRY	varchar(20)	行业代码
PURPOSE_CODE	varchar(10)	用途代码
GUARANTY_STYLE	varchar(5)	担保方式
OVERDUE_FLAG	char(1)	逾期标志，Y-存在，N-不存在
CENTRAL_BANK_CUSTOMER_CLASS	char(5)	央行客户分类
CR_RATING	char(3)	客户信用等级
VOUCHER_NO	varchar(50)	凭证号
NARRATIVE1	varchar(500)	摘要1
NARRATIVE2	varchar(500)	摘要2
NARRATIVE3	varchar(500)	摘要3
NARRATIVE4	varchar(500)	摘要4
TREATS_CHANNEL_NO	varchar(20)	渠道任务编号
TREATS_REFERENCE	varchar(50)	Trea系统交易流水号
PRODUCT_RELATED_INDICATOR	char(1)	是否产品相关，Y-是，N-否
GIMIS_CUSTOMER_INDICATOR	char(1)	GIMIS客户标识
GIMIS_ATTRIBUTE2	varchar(3)	GIMIS属性2
GIMIS_ATTRIBUTE1	varchar(3)	GIMIS属性1
ORDER_NO	varchar(50)	订单号
DEAL_NO	varchar(50)	交易流水号
COUNTRY_LOC	varchar(3)	国家地区
BASE_CCY_AMOUNT_ONE	decimal(20,2)	基础币种金额1
BASE_CCY_AMOUNT_TWO	decimal(20,2)	基础币种金额2
SEQ	varchar(20)	HUB系统交易顺序号
BASE_CENTER	varchar(20)	成本中心
USER_LANG	varchar(10)	用户语言
GROUP_CLIENT	varchar(30)	集团客户资料编号
SUM_BOOK_FLAG	char(1)	汇总账标志，Y-汇总流水，N-非汇总流水
BELONG_SYSTEM	varchar(20)	归属系统
BOOK_TYPE	varchar(20)	账本类型
ACCT_TYPE	char(1)	账户类型，A-AIO账户，C-结算账户，D-基准账户，E-委托贷款，L-转让贷款，M-普通贷款，S-储蓄账户，T-定期账户，U-贴现账户
ACCT_COMPANY	varchar(10)	账户法人
PROD_GROUP	varchar(20)	产品群组
CLIENT_GROUP	varchar(20)	客户群组
TERM_GROUP	varchar(20)	将剩余期限组别
COST_GROUP	varchar(20)	成本中心组别
CREDIT_GROUP	varchar(20)	信用等级组别
PRODUCT_RE	char(1)	账务处理标识
CORP_SIZE	varchar(5)	企业规模（9-其他，CS01-大型企业，CS02-中型企业，CS03-小型企业，CS04-微型企业）
GHO_CUSTOMER_CLASS	varchar(5)	集团客户分类
AMOUNT_NATURE	varchar(10)	金额性质
OLD_BRANCH	varchar(20)	变更前机构
BUS_SEQ_NO	varchar(50)	项目使用的业务流水号字段
INT_IND_FLAG	char(1)	是否正利率计息，Y-是，N-否，F-是，负利率计息
LOAN_PROD_TYPE	varchar(20)	贷款产品类型
TERM	varchar(10)	期限
ASSET_TYPE_CODE	varchar(10)	资产三分类
REASON_CODE	varchar(10)	用途
ACCT_STATUS	char(1)	账户状态，N-新建，H-待激活，A-活动，D-睡眠，S-久悬，O-转营业外，P-逾期，C-关闭，I-预开户，R-预销户
CHANNEL	varchar(10)	渠道编号
BUSI_TYPE	varchar(20)	业务品种
BATCH_NO	varchar(50)	批次号
BUSI_PROD	varchar(20)	业务产品代码
CATEGORY_TYPE	varchar(6)	客户细分类型
REVERSAL_DATE	datetime	冲正日期
REVERSAL_ORIGINAL_SEQ_NO	varchar(50)	冲正原交易流水号
REVERSAL_SEQ_NO	varchar(50)	冲正流水号
SEGMENT_SEQ_NO	varchar(50)	分段序列号
CREATE_TIMESTAMP	varchar(26)	数据创建时间戳


日间TAE流水表（rb_tae_info）结构说明
1. 表名与用途
表名：rb_tae_info
用途：记录日间分布式交易流水信息，包括账户、交易、金额、渠道、卡号等详细信息。

字段名	类型	说明
SEQ_NO	varchar(50)	序号
MAIN_SEQ_NO	varchar(50)	主流水号
SUB_SEQ_NO	varchar(100)	子流水号
CHANNEL_DATE	datetime	渠道日期
CHANNEL_SEQ_NO	varchar(50)	渠道流水号
TRAN_CHANNEL	varchar(20)	交易渠道
REFERENCE	varchar(50)	系统流水号/交易参考号
DR_CR_FLAG	char(1)	借贷标志（D-借，C-贷）
BASE_ACCT_NO	varchar(50)	账户号/卡号
CCY	varchar(3)	币种
PROD_TYPE	varchar(20)	产品代码
ACCT_SEQ_NO	varchar(5)	账户序列号
CARD_NO	varchar(50)	卡号
INTERNAL_KEY	bigint	账户内部键值
CLIENT_NO	varchar(20)	客户号
AMOUNT	decimal(20,2)	交易金额
REVERSAL	char(1)	冲正标志，Y-是，N-否
TRAN_DATE	datetime	交易日期
SESSION_ID	varchar(20)	场次/场次号
NARRATIVE	varchar(500)	摘要/开户时的账户用途，销户时的销户原因
COMPANY	varchar(20)	法人
TRAN_TIMESTAMP	varchar(26)	交易时间戳
CREATE_TIMESTAMP	varchar(26)	数据创建时间戳


原始交易报文表（fw_tran_info）结构说明
1. 表名与用途
表名：fw_tran_info
用途：以垂直表形式记录每类业务的原始交易报文及相关信息，包括服务、交易、报文、流水、状态等。

字段名	类型	说明
SERVICE_ID	varchar(100)	服务ID
SERVICE_NAME	varchar(200)	服务名称
SERVICE_NO	varchar(200)	服务唯一识别号
TRAN_DATE	varchar(20)	交易日期
TRAN_TIME	varchar(20)	交易时间
IN_MSG	longblob	输入报文
OUT_MSG	longblob	输出报文
RESPONSE_TYPE	varchar(100)	输出响应类型
START_TIME	varchar(30)	交易开始时间
END_TIME	varchar(30)	交易完成时间
SOURCE_TYPE	varchar(50)	渠道类型
SEQ_NO	varchar(50)	渠道流水号
SUB_SEQ_NO	varchar(50)	子流水号
BUS_SEQ_NO	varchar(50)	业务流水号
PROGRAM_ID	varchar(20)	调用方程序标识
STATUS	varchar(1)	状态
REFERENCE	varchar(50)	业务参考号
PLATFORM_ID	varchar(32)	平台流水号
USER_ID	varchar(30)	操作柜员
IP_ADDRESS	varchar(30)	IP地址
BRANCH_ID	varchar(20)	网点
COMPENSATE_SERVICE_NO	varchar(200)	待补偿原交易唯一识别号
WEEK_DAY	decimal(1,0)	星期
CREATE_DATE	datetime	数据创建时间
CNSM_SOURCE_TYPE	varchar(10)	调用方渠道类型
CNSM_TRAN_DATE	varchar(8)	调用方交易日期
CNSM_TRAN_TIMESTAMP	varchar(26)	调用方交易时间戳
CNSM_SYS_MAC	varchar(200)	调用方终端地址
CNSM_SYS_ID	varchar(30)	调用方系统编号
CNSM_SYS_MAC	varchar(200)	调用方终端地址
TMI_ID	varchar(20)	调用方服务标识
CREATE_TIMESTAMP	varchar(26)	数据创建时间戳


示例In_msg报文字段值格式化展示：
tranDate：20250620
origServiceNo：SHN07B1XZ02506201593468044054467
seqNo：GHN07B1XZ02506201593468044054467
branchId：010001
userId：HN0711
sourceType：HN07
userLang：CHINESE
tranTimestamp：130043
messageType：ONLINE
messageCode：2101
serviceCode：MbsdCore
reference：CBS1125062000000030216
fileFlg：0
subSeqNo：SHN07B1XZ02506201593468044054467
reqTimeout：0
busSeqNo：GHN07B1XZ02506201593468044054467
cnsmTranDate：20250620
cnsmTranTimestamp：130043
onlineBatchType：0
appHead：null
totalNum：-1
pgupOrPgdn：0
totalRows：0
totalFlag：E
currentNum：0
loanAmt：500000.00
prodType：Y16
clientNo：1044631848
ccy：CNY
origLoanAmt：500000.00
schedMode：17
signDate：20250620
odEndDate：20260619
marketingProd：000000000000000000000000000000000000
applyBranch：050200
acctDesc：null
acctExec：null
amtType：ALL
settleAcctCcy：CNY
settleAcctClass：PAY
settleBaseAcctNo：6231501089177347
settleClient：1044631848
settleAcctSeqNo：00001
payRecInd：PAY
settleProdType：R
settleAcctName：某某某
othBaseAcctNo：6231501089179577
othRealTranName：马加源
scheduleArray：[]
creditSource：XYD
endDate：20260619
totalAmt：250000
intDealDay：21
rollRateArray：[]
...（其余字段略）

注：如需全部字段详细格式化，请提供完整JSON文本或指定需要展示的字段范围。


示例In_msg报文字段值格式化展示：
origServiceNo：SHN07B1XZ02506201643260041937916
seqNo：GHN07B1XZ02506201643260041937916
branchId：HN0761
userId：HN0761
sourceType：HN07
userLang：CHINESE
filePath：null
tranTimestamp：125105
messageType：ONLINE
messageCode：2101
serviceCode：MbsdCore
company：C006
reference：CBS11250620000000302135
subSeqNo：SHN07B1XZ02506201643260041937916
branchPermissionsFlag：N
cnsmTranDate：20250620
cnsmTranTimestamp：125105
onlineBatchType：O
appHead：null
totalNum：-1
pgupOrPgdn：0
totalRows：0
totalFlag：E
currentNum：0
loanAmt：500000.00
prodType：Y16
clientNo：1045390402
lender：0193
ccy：CNY
origLoanAmt：500000.00
schedMode：17
signDate：20250619
odEndDate：20260619
marketingProd：020034
marketingProdDesc：快乐贷
homeBranch：546701
openBranch：546701
autoRecFlag：N
loanClass：C
purpose：正常
gearProdFlag：N
effectDate：20250620
maturityDate：20260619
team：null
termType：null
applyBranch：54
acctDesc：null
acctExec：O1983
isOneOffFlag：N
graceChargeIntFlag：null
graceChargeOdiFlag：null
acctChangeFlag：N
trnOutBank：null
paySeqRef：null
guarantyStyle：20
fiveCategory：10
creditNo：null
sofCountry：null
sofState：null
analysis1：null
analysis2：null
analysis3：null
tfLoanType：null
tfRefNo：null
autoSettleSodIntFlag：N
clientEconType：null
accountingPeriodFlag：null
schedAssembleFlag：null
mainBorrowerRelation：null
beforeIncomeFlag：N
reviewedFlag：N
supplementDate：null
econDepartmentType：null
amountNature：N
recoverFlag：N
isIndividualBus：N
autoRecDaytimeFlag：N
loanAmtControl：null
remark：null
intArray：[{'intClass':'INT','intType':'L1','spreadType':'F','realRate':-6.00,'actualRate':3.00,'calcByInt':'N','intIndFlag':'Y','rateEffectType':'N','intApplType':'N','monthBasis':'ACT','yearBasis':'360','acctFixedRate':'N','finalRate':4.00,'actualRate':3.00,'calcByInt':'N','intIndFlag':'Y','rateEffectType':'N','intApplType':'N','monthBasis':'ACT','yearBasis':'360','acctFixedRate':'N'}]
cycleFreq：null
nextCycleDate：20250621
intDay：21
intClass：INT
payRecInd：PAY
settleMethod：R
amtType：ALL
settleAcctCcy：CNY
settleAcctClass：PAY
settleBaseAcctNo：621059051472001126
settleClient：1045390402
settleAcctSeqNo：00001
settleProdType：2100006
settleAcctName：曾启狄
settleAmt：400000
othBaseAcctNo：621059051472001126
othRealTranName：曾启狄
...（其余字段略）

注：如需全部字段详细格式化，请提供完整JSON文本或指定需要展示的字段范围。


核心系统生产日志信息分析

【日志片段示例】
UPDATE rb_acct_int_detail SET INT_ACCRUED=..., TAX_ACCRUED=..., INT_POSTED=..., TAX_POSTED=..., CYCLE_DATE='2025-06-21', LAST_CYCLE_DATE='2025-06-20', TRAN_TIMESTAMP=... WHERE INTERNAL_KEY=... AND CLIENT_NO=... AND INT_CLASS=...;
-- clientIP=... @prepareSql=... ...

【结构说明】
- 日志主要为批量UPDATE语句，针对账户利息、税金等表进行数据更新。
- WHERE条件精确定位账户、客户、利息类别，确保数据准确。
- 日志包含执行环境信息（如clientIP、prepareSql、request等），反映系统分布式、参数化执行特性。

【业务流程与系统特性推断】
- 日志反映批量计息/结息处理，通常在日终或定时批量作业窗口执行。
- 支持多节点并发处理，具备分布式或集群架构。
- 使用参数化SQL和详细审计日志，提升安全性和可追溯性。
- 日志详尽，有助于数据一致性校验和问题追溯。

【合理推断与建议】
- 当前系统运行健康，批量作业顺畅。
- 建议持续优化批量窗口和SQL性能，防范高并发下的超时或锁等待。
- 日志为合规审计和数据追溯提供坚实基础，建议定期归档备份。

如需展示完整日志内容或分析特定SQL/异常，请补充相关信息。


【核心系统生产日志原始内容示例】
```
UPDATE rb_acct_int_detail SET INT_ACCRUED=..., TAX_ACCRUED=..., INT_POSTED=..., TAX_POSTED=..., CYCLE_DATE='2025-06-21', LAST_CYCLE_DATE='2025-06-20', TRAN_TIMESTAMP=... WHERE INTERNAL_KEY=... AND CLIENT_NO=... AND INT_CLASS=...;
-- clientIP=10.6.101.243:2988484 @prepareSql=UPDATE rb_acct_int_detail SET INT_ACCRUED=..., TAX_ACCRUED=..., ... WHERE INTERNAL_KEY=1001341547 AND CLIENT_NO=1011816148 AND INT_CLASS='X3D' ...
UPDATE rb_acct_int_detail SET INT_ACCRUED=..., TAX_ACCRUED=..., INT_POSTED=..., TAX_POSTED=..., CYCLE_DATE='2025-06-21', LAST_CYCLE_DATE='2025-06-20', TRAN_TIMESTAMP=... WHERE INTERNAL_KEY=... AND CLIENT_NO=... AND INT_CLASS=...;
-- clientIP=10.6.101.230:1934892 @prepareSql=UPDATE rb_acct_int_detail SET INT_ACCRUED=..., TAX_ACCRUED=..., ... WHERE INTERNAL_KEY=1001341546 AND CLIENT_NO=1011569643 AND INT_CLASS='X3D' ...
...（其余日志略，详见原始系统日志）
```

注：如需全量日志内容或指定时间段、账户的日志，请提供具体范围或原始文件。


示例In_msg报文字段值格式化展示：
tranDate：20250712
origServiceNo：TA0040xx20250712ZJ20250712166994141
seqNo：GA0040xx202507120010852209
branchId：010003
userId：HN0111
sourceType：HN01
userLang：CHINESE
tranTimestamp：101626
messageType：1000
serviceCode：MbsdCore
company：C001
reference：CBS15250712000000000230
runDate：null
cnsmSysId：A00044
srcSysSvrId：null
subSeqNo：TA0040xx202507120010852209
reqTimeout：0
busSeqNo：BA0040xx202507120010852209
msgVer：null
innerServiceFlag：true
finalInnerflag：true
branchPermissionsFlag：N
cnsmTranDate：20250620
cnsmTranTimestamp：101539
cnsmSysMac：null
srcSysId：A00044
srcSysMac：null
totalNum：-1
pgupOrPgdn：0
currentNum：0
body：sceneInfo:[{tranType:4189,tranAmt:120000.00,tranCcy:CNY,amtType:BAL,tranBranch:010003,sceneCode:GLZ91340301,reversalFlag:N,remark:comstar本币系统科目记账,dcFlag:MD,settlementDate:20250712,batchNo:null,narrativeCode:MDM}]
retStatus：null
retCode：CORERBxx6FRB6T
retMsg：[GL13210301]科目代码不允许记账
...（其余字段略）

注：如需全部字段详细格式化，请提供完整JSON文本或指定需要展示的字段范围。

一、日志内容结构解析【结息日】
日志来源与命令
日志显示通过 grep 命令筛选了包含 update rb_acct_int_detail 和 ifnull 及 int_adj_prev 的慢SQL日志。
日志文件路径如 /data/dtsql_run/15014/gateway/log/interf_instance_...，表明这是分布式SQL网关或数据库中间件的执行日志。
SQL语句结构
主要为 UPDATE rb_acct_int_detail SET ... WHERE ... 语句，涉及字段有：
INT_ACCRUED_LAST_PREV、INT_ACCRUED_PREV、INT_ADJ_PREV、DISCNT_INT_PREV、DISCNT_INT_LAST_PREV、ADJ_UPD_LAST_DATE 等。
SQL中大量使用 ifnull() 函数，目的是在字段为NULL时赋默认值，保证数据更新的健壮性。
WHERE条件通常包含 INTERNAL_KEY 范围、ADJ_UPD_LAST_DATE、INT_ADJ_PREV 等，确保批量更新的精确性。
执行环境与耗时
日志中包含 clientIP（如86.0.101.240:23752）、prepareSql（预编译SQL）、event_timecost（事件耗时）、select_resultcode 等信息。
例如：event_timecost=0.27、timecost=3774.145，表示SQL执行耗时，单位为秒或毫秒。
慢SQL特征
日志中有多条SQL执行耗时较长（如3秒以上），属于慢SQL范畴。
可能涉及大范围数据更新、索引不佳或并发冲突等问题。

二、慢SQL业务分析与合理推断
业务场景
该慢SQL主要用于批量调整账户利息、贴现利息等历史数据，常见于日终批量、利息调整、数据修复等场景。
涉及的表为 rb_acct_int_detail，是银行核心系统中记录账户利息明细的关键表。
慢SQL成因分析
数据量大：WHERE条件为范围查询（BETWEEN ? AND ?），每次更新可能涉及成千上万条记录。
索引优化不足：如WHERE条件未命中合适索引，或涉及多个字段联合索引失效，导致全表扫描。
函数使用：大量使用 ifnull()，可能影响SQL优化器选择索引，增加CPU消耗。
并发冲突：批量作业高并发执行，可能导致锁等待、资源竞争，进一步拉长SQL执行时间。
硬件瓶颈：磁盘IO、网络带宽、数据库节点负载等也可能影响SQL响应速度。
风险与建议
风险：慢SQL会拖慢批量作业进度，影响日终结算、对账、利息结息等关键业务流程，严重时可能导致业务中断或数据不一致。
建议：
优化SQL语句，减少不必要的函数嵌套，提升索引利用率。
针对WHERE条件建立合适的联合索引。
分批处理大数据量更新，避免单次SQL影响过大。
定期监控慢SQL日志，及时调整批量窗口和作业调度策略。
升级硬件或扩展数据库节点，提升整体处理能力。

三、总结
本次慢SQL日志反映出银行核心系统在批量利息调整、历史数据修复等场景下，存在SQL执行耗时较长的问题。建议从SQL优化、索引设计、批量调度、硬件扩容等多方面入手，持续提升系统批量处理效率，保障核心业务稳定运行。
如需进一步分析具体SQL、表结构或执行计划，请补充相关信息！


子账户转入转出登记表（rb_transfer_acct）结构说明
1. 表名与用途
表名：rb_transfer_acct
用途：记录子账户转入转出登记信息，包含客户号、账户号、交易日期、转入转出类型、前后账户等。

字段名	类型	说明
CLIENT_NO	varchar(20)	客户号
CLIENT_NAME	varchar(200)	客户名称
BASE_ACCT_NO	varchar(50)	账户号
TRAN_DATE	datetime	交易日期
TRAN_BRANCH	varchar(20)	交易机构
ID_INOUT_OPERATE_TYPE	varchar(20)	定期账户转入转出操作类型（01-转入，02-互转，03-转出）
TRANSFER_IN_AFTER_ACCT	varchar(50)	转入后账号
TRANSFER_IN_BEFORE_ACCT	varchar(50)	转入前账号
TRANSFER_OUT_AFTER_ACCT	varchar(50)	转出后账号
TRANSFER_OUT_BEFORE_ACCT	varchar(50)	转出前账号
OPER_USER_ID	varchar(30)	操作柜员号
TRAN_TIMESTAMP	varchar(26)	交易时间戳
COMPANY	varchar(20)	法人
TRANSFER_OUT_AFTER_SEQ_NO	varchar(5)	转出后账户序号
TRANSFER_OUT_BEFORE_SEQ_NO	varchar(5)	转出前账户序号
TRANSFER_IN_AFTER_SEQ_NO	varchar(5)	转入后账户序号
TRANSFER_IN_BEFORE_SEQ_NO	varchar(5)	转入前账户序号
IN_SEQ_NO	varchar(5)	转入账户序号
OUT_SEQ_NO	varchar(5)	转出账户序号
SEQ_NO	varchar(50)	序号
CREATE_TIMESTAMP	varchar(26)	数据创建时间戳


交易流水表（rb_tran_hist）结构说明
1. 表名与用途
表名：rb_tran_hist
用途：记录银行账户的交易流水信息，包括序号、渠道流水号、账户、金额、交易类型、币种、事件类型等。

字段名	类型	说明
SEQ_NO	varchar(50)	序号/序号
CHANNEL_SEQ_NO	varchar(50)	渠道流水号
SUB_SEQ_NO	varchar(100)	业务流水号
TAE_SUB_NO	varchar(200)	TAE子流水序号
SOURCE_TYPE	varchar(10)	渠道类型
REFERENCE	varchar(50)	交易参考号
CLIENT_NO	varchar(20)	客户号
INTERNAL_KEY	bigint	账户内部键值
BASE_ACCT_NO	varchar(50)	账户号
PROD_TYPE	varchar(20)	产品类型
ACCT_CCY	varchar(3)	币种
ACCT_SEQ_NO	varchar(5)	账户序列号
SUB_ACCT_NO	varchar(50)	子账户号
ACCT_CLASS	char(1)	账户分类
ACCT_STATUS	char(1)	账户状态
ACCT_REAL_FLAG	char(1)	账户是否虚实标志
ACCT_TRAN_FLAG	char(1)	账户交易标志
ACCT_DESC	varchar(200)	账户描述
ACCT_BRANCH	varchar(20)	开户机构
EVENT_TYPE	varchar(20)	事件类型
TRAN_DATE	datetime	交易日期
TRAN_BRANCH	varchar(20)	交易机构
CR_DR_IND	char(1)	借贷标志（C-贷，D-借）
CCY	varchar(3)	币种
TRAN_TYPE	varchar(10)	交易类型
TRAN_DESC	varchar(200)	交易描述
PREVIOUS_BAL_AMT	decimal(20,2)	交易前余额
TRAN_AMT	decimal(20,2)	交易金额
ACTUAL_BAL	decimal(20,2)	交易后余额
TRAN_CATEGORY	varchar(5)	交易类别
GL_CODE	varchar(20)	科目代码
OTH_REFERENCE	varchar(50)	对方系统流水号/对方交易参考号
OTH_INTERNAL_KEY	bigint	对手账户内部键值
OTH_BASE_ACCT_NO	varchar(50)	对方账号/卡号
OTH_ACCT_CCY	varchar(3)	对方账户币种
OTH_ACCT_SEQ_NO	varchar(5)	对方账户序列号
FH_SEQ_NO	varchar(50)	记账系统编号信息
OTH_PROD_TYPE	varchar(20)	对方产品代码
OTH_ACCT_DESC	varchar(200)	对方账户描述
OTH_BANK_CODE	varchar(20)	对方银行代码
OTH_BANK_NAME	varchar(200)	对方银行名称
OTH_BRANCH	varchar(20)	对方开户机构
OTH_REAL_BANK_CODE	varchar(20)	真实对方金融机构代码
OTH_REAL_BANK_NAME	varchar(200)	真实对方金融机构名称
OTH_REAL_PROD_TYPE	varchar(20)	真实对方金融产品类型
OTH_REAL_BASE_ACCT_NO	varchar(50)	真实对方账号
CONTRA_ACCT_CCY	varchar(3)	他行币种
FROM_CCY	varchar(3)	转出币种
OTH_SEQ_NO	varchar(50)	对方交易流水号
PRIMARY_TRAN_SEQ_NO	varchar(50)	主交易序号
TO_CCY	varchar(3)	转入币种
FROM_AMOUNT	decimal(20,2)	转出金额
TO_AMOUNT	decimal(20,2)	转入金额
DOC_TYPE	varchar(10)	凭证类型
PREFIX	varchar(100)	凭证起始号码
VOUCHER_NO	varchar(50)	凭证号
DOCUMENT_ID	varchar(50)	证件号码
DOCUMENT_TYPE	varchar(4)	证件类型
CLIENT_NAME	varchar(200)	客户名称
CLIENT_TYPE	varchar(6)	客户类型
BILL_NO	varchar(50)	票据号码
BUSINESS_UNIT	varchar(50)	业务单元
CASH_ITEM	varchar(10)	现金标志
TRAN_NOTE	varchar(600)	业务处理标志
TRAN_STATUS	char(1)	交易状态
AUTO_REVERSAL_FLAG	char(1)	自动冲正标志
AMT_CALC_TYPE	varchar(2)	金额计算类型
CHANNEL	varchar(10)	渠道编号
AMT_TYPE	varchar(10)	金额类型
BAL_TYPE	varchar(2)	余额类型
CONTRA_EQUIV_AMT	decimal(20,2)	他行等值金额
ACTUAL_BAL_AMT_FIN	decimal(20,2)	实际后余额
BASE_EQUIV_AMT	decimal(20,2)	基础等值金额
FLAT_RATE	decimal(15,8)	平盘汇率
OV_TO_AMOUNT	decimal(20,2)	跨境交易时修改交叉汇率计算的金额
CROSS_RATE	decimal(15,8)	交叉汇率
FROM_RATE_FLAG	char(1)	买方交汇率标志
FROM_XRATE	decimal(15,8)	买方汇率
OV_CROSS_RATE	decimal(15,8)	实际交易时修改交叉汇率
TO_RATE_FLAG	char(1)	卖方交汇率标志
TO_XRATE	decimal(15,8)	卖方汇率
BIZ_TYPE	varchar(10)	业务类型
FIN_TYPE	varchar(3)	金融类型
QUOTE_TYPE	char(1)	报价类型
MEDIUM_FLAG	char(1)	介质标志
MEDIUM_TYPE	char(1)	介质类型
ORIG_SYSTEM	varchar(50)	原系统
OTH_DOCUMENT_TYPE	varchar(4)	对方证件类型
PBK_UPD_FLAG	char(1)	是否补记事件
PRIMARY_EVENT_TYPE	varchar(10)	主事件类型
RATE_TYPE	varchar(10)	汇率类型
TRAN_METHOD	varchar(20)	交易方式
WITHDRAWAL_TYPE	char(1)	支取方式
BATCH_NO	varchar(50)	批次号
BANK_SEQ_NO	varchar(50)	银行交易序号
COMMISSION_CLIENT_TEL	varchar(20)	代理人电话
LENDER	varchar(100)	贷款人
LIMIT_REF	varchar(500)	额度编号
OTH_BRANCH_REGIONALISM_CODE	varchar(20)	对方金融机构行政区划代码
USER_ID	varchar(30)	操作柜员号
COMPANY	varchar(20)	法人
CHEQUE_DATE	date	支票日期
REMARK	varchar(200)	备注
CASH_USE_PLACE_CODE	varchar(20)	现钞去向国家/地区代码
CASH_USE_REMARK	varchar(200)	现钞去向说明
CASH_SOURCE_COUNTRY	varchar(20)	现钞来源国家/地区代码
CASH_SOURCE_REMARK	varchar(200)	现钞来源说明
IS_TAE	char(1)	是否TAE流水
TRAN_CODE	varchar(50)	交易代码
DEAL_NO	varchar(50)	交易流水号
DEAL_CODE	varchar(50)	交易代码
INPUT_MEDIUM_ID	varchar(30)	输入媒介ID
TELLER_TERMINAL_TYPE	varchar(20)	柜员终端类型
APPR_INDICATOR	char(1)	是否需要审批
APPR_TERMINAL_ID	varchar(10)	审批终端ID
PRINT_INDICATOR	char(1)	是否打印标志
REMAIN_TERM	varchar(2)	剩余期限
INPUT_MEDIUM_TYPE	varchar(2)	输入媒介类型
TRAN_COUNTRY	varchar(3)	交易国家/地区
LCY_TRAN_AMT	decimal(20,2)	本币交易金额
CUST_RATE	decimal(15,8)	客户汇率
AUTO_TRADE_FLAG	char(1)	自动交易标志
TREATS_CHANNEL_NO	varchar(20)	Treats渠道流水号
TREATS_REFERENCE	varchar(50)	Treats系统交易流水号
TACK_OVER_CCY_RATE	decimal(15,8)	承接汇率
TACK_OVER_CCY_RATE_UNIT	varchar(10)	承接汇率单位
MATURITY_NARRATIVE1	varchar(200)	到期说明1
MATURITY_NARRATIVE2	varchar(200)	到期说明2
MATURITY_NARRATIVE3	varchar(200)	到期说明3
MATURITY_NARRATIVE4	varchar(200)	到期说明4
...（其余字段略）


补偿表（taa_compensation）结构说明
1. 表名与用途
表名：taa_compensation
用途：记录补偿相关信息，包括主表ID、补偿状态、补偿次数、决策状态、渠道信息、响应码、响应信息、创建和修改时间等。

字段名	类型	说明
MAIN_ID	varchar(160)	主表ID，主键
COMPENSAT_STATUS	bigint	补偿状态
COMPENSAT_NUM	int	补偿次数
DECISION_STAT	varchar(10)	决策状态
CHNL_ID	varchar(20)	渠道ID
CHNL_SEQ	varchar(50)	渠道流水号
CHNL_DATE	date	渠道日期
RSP_CODE	varchar(50)	处理码
RSP_MSG	varchar(500)	处理信息
CREAT_TIME	datetime	创建时间
MODIFY_TIME	datetime	最后修改时间


进度状态表（taa_progress_status）结构说明
1. 表名与用途
表名：taa_progress_status
用途：记录补偿或流程的进度状态，包括主表ID、状态码、状态信息、序号、类型、渠道信息、创建时间等。

字段名	类型	说明
ID	bigint	主键，自增ID
MAIN_ID	varchar(160)	主表ID
STATUS_CODE	varchar(50)	状态码
STATUS_MSG	varchar(1000)	状态信息
ID_SEQ	bigint	子序号/批次号
TYPE	varchar(500)	类型（M主S子）
CREAT_TIME	datetime	创建时间
CHNL_ID	varchar(20)	渠道ID
CHNL_SEQ	varchar(50)	渠道流水号
CHNL_DATE	date	渠道日期


TAE交易信息表（taa_tran_info）结构说明
1. 表名与用途
表名：taa_tran_info
用途：记录TAE相关交易信息，包括主表ID、渠道信息、流水号、子流水号、参考号、类型、结果、返回JSON等。

字段名	类型	说明
MAIN_ID	varchar(160)	主表ID，主键
CHNL_ID	varchar(20)	渠道ID
CHNL_SEQ	varchar(50)	渠道流水号
SUB_SEQ_NO	varchar(50)	渠道子流水号
CHNL_DATE	date	渠道日期
REFERENCE	varchar(50)	参考号
TYPE	varchar(8)	类型（account记账/Reversal冲正）
RESULT	varchar(1)	结果（S成功/F失败）
RET_JSON	longtext	返回报文


核心系统生产日志分析补充（TAE分布式交易与子账户流水）
一、日志内容结构与业务场景
日志类型与SQL操作
日志主要为INSERT INTO TAE_ACCT_SUBTRADES等SQL语句，涉及分布式交易子账户流水的批量插入。
典型SQL结构：
INSERT INTO TAE_ACCT_SUBTRADES (MAIN_ID, ID_SEQ, TRN_BRAN_NO, ...) VALUES (?, ?, ?, ...)
伴随有clientIP、proxyHost、sql_size、event_timecost等执行环境与性能信息。
关键字段与业务含义
MAIN_ID：主表ID，关联主交易或补偿主表。
ID_SEQ：子流水序号，标识分布式事务内的子操作。
TRN_BRAN_NO：交易机构号。
BASE_ACCT_NO、CCY、DC_FLAG、TXN_AMT等：账户、币种、借贷标志、金额等核心流水信息。
TRADE_STAT、RSP_MSG：交易状态、响应信息，便于后续补偿与问题追溯。
CREATE_TIME、MODIFY_TIME：创建、修改时间，支持全流程审计。
执行环境与性能监控
日志中包含clientIP=86.0.101.239、proxyHost=86.0.89.13等分布式节点信息，反映系统多节点并发处理特性。
event_timecost、sql_size等字段用于监控SQL执行耗时与数据量，便于性能分析和瓶颈定位。

