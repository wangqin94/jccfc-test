# # ---------------------------------------------------------
# # - 项目特性配置文件
# # - created time: 2021-03-06
# # - version: 1.1
# # ---------------------------------------------------------

# -----------------------------------------------------------
# 360借条2期项目配置
# -----------------------------------------------------------
JieTiao = {
    # 放款请求接口
    'loan': {
        'interface': '/api/v1/jietiao/loan/apply',
        'payload': {
            "loanReqNo": "",  # 放款请求流水号
            "sourceCode": "QH",  # 请求方代码  QH
            "custName": "",  # 客户名称
            "idType": "1",  # 证件类型  1身份证  2护照 3港澳台居民身份证 Z其他
            "id": "",  # 证件号码
            "sex": "F",  # 性别 F女M男
            "dbBankCode": "0001",  # 放款银行代码
            "dbAcct": "",  # 放款卡号
            "dbAcctName": "",  # 放款银行卡账户名
            "loanDate": "",  # 放款申请时间  YYYY-MM-DD HH24:MI:SS
            "loanAmt": "",  # 放款金额
            "lnTerm": "",  # 期数
            "creditAmt": "",  # 授信额度
            "loanPurpose": "08",  # 贷款用途    08装修房屋09购置大宗消费品10支付教育支出11支付医疗支出12支付旅游支出13支付其他消费款
            "feeRate": "",  # 费率
            "yearRate": "",  # 年化利率
            "mobileNo": "",  # 注册手机号
            "idValidDateStart": "",  # 身份证有效期起始日
            "idValidDateEnd": "",  # 身份证有效期结束日  YYYY-MM-DD
            "idAddress": "四川省成都市高新区天府三街",  # 身份证地址
            "agency": "成都高新派出所",  # 身份证签发机关
            "cardMobileNo": "13855139654",  # 银行卡绑定手机号
            "creditCardSts": "1",  # 是否客户名下任一张信用卡状态为呆帐、核销
            "loanAcctSts": "1",  # 是否贷款账户状态为呆帐、核销
            "creditCardOverdueDays": "1",  # 是否客户名下任一张信用卡在过去2年内有超过120天、150天、180天以上的逾期
            "loanOverDays": "1",  # 是否客户有过贷款在过去2年内有超过120天、150天、180天以上的逾期
            "thirdPartyBlackList": "1",  # 是否命中同盾、百融、前海、汇法黑名单
            "idVerifyRisk": "A",  # 核身风险等级
            "idCert": "1",  # 是否有身份证或身份证明
            "ageCheck": "1",  # 满足年龄18至55岁
            "policeInfoNotExist": "1",  # 公安信息不存在
            "policeInfoNotMatch": "1",  # 公安信息不匹配
            "overdueHisMaxDays": "100",  # 360平台上历史最大逾期天数
            "overdueHisMaxAmt": "20000",  # 360平台上历史最大逾期金额
            "ascore": "1000",  # A卡分  0-1000
            "bscore": "1000"  # B卡分  0-1000
        }
    },
    # 放款结果查询接口
    'loan_query': {
        'interface': '/api/v1/jietiao/loan/query',
        'payload': {
            "loanReqNo": "",  # 放款请求流水号
            "sourceCode": "QH"  # 请求方代码QH
        }
    },
    # 代扣申请接口
    'payment': {
        'interface': '/api/v1/welab/common/queryBindCardResult',
        'payload': {
            "sourceCode": "QH",  ##请求方代码
            "tranNo": "",  # 代扣申请流水号
            "totalAmt": "",  # 扣款金额
            "repayBankAcct": "",  # 还款方银行卡号
            "repayCstname": "",  # 客户姓名
            "repayBankNo": "0001",  # 银行编码
            "repayRelcard": "",  # 还款方身份证号
            "repayRelphone": "13854692564",  # 还款方手机号
            "remark": "代扣",  # 备注
            "channelId": "tl",  # 通道代码 通联协议: tl_xy通联:tl快钱协议: kq_xy快钱:kq
            "agreementNo": "123456789"  # 协议号 如果是快钱协议付，则协议号包含快钱客户号，格式为客户号,协议号
        }
    },
    # 代扣申请结果查询
    'payment_query': {
        'interface': '/api/v1/welab/common/updateWithholdCard',
        'payload': {
            "sourceCode": "QH",  # 请求方代码  QH
            "tranNo": ""  # 代扣申请流水号
        }
    },
    # 还款通知接口
    'repay_notice': {
        'interface': '/api/v1/welab/credit/apply',
        'payload': {
            "loanReqNo": "",  # 放款请求流水号
            "sourceCode": "QH",  # 请求方代码  QH
            "rpyType": "",  # 还款类别  提前还款:01(提前结清) 期供还款:02 (按指定期数进行还款，包含部分还款、提前还当期) 逾期还款：03（逾期还部分、逾期足额按期还)
            "rpyTerm": "",  # 还款期数  期供还款该字段必填 提前结清期数为空
            "rpyReqNo": "",  # 还款请求流水号
            "tranNo": "",  # 代扣申请流水号
            "rpyDate": "",  # 还款日期
            "rpyPrinAmt": "",  # 还款本金
            "rpyIntAmt": "",  # 还款利息
            "rpyOintAmt": "",  # 还款罚息
            "rpyShareAmt": "30%",  # 分润金额
            "rpyDeductAmt": "",  # 营销减免金额
            "rpyRedLineAmt": "",  # 红线减免金额
            "ifEnough": "",  # 是否足额 0:非足额 1:足额
            "rpyShareAmtOne": "12%",  # 分润金额1
            "rpyShareAmtTwo": "2%",  # 分润金额2
            "rpyShareAmtThree": "3%",  # 分润金额3
            "rpyShareAmtFour": "4%",  # 分润金额4
            "rpyChannel": ""  # 还款渠道  0线下1线上
        }
    },
    # 还款查询接口
    'repay_query': {
        'interface': '/api/v1/welab/credit/queryResult',
        'payload': {
            "loanReqNo": "",  # 放款请求流水号
            "sourceCode": "QH",  # 请求方代码QH
            "rpyReqNo": ""  # 还款请求流水号

        }
    }

}
