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
            "idType": "1",  # 证件类型  1身份证  2护照 3港澳台居民身份证 Z其他   -------------
            "id": "",  # 证件号码
            "sex": "F",  # 性别 F女M男            -----------------
            "dbBankCode": "0022",  # 放款银行代码           ---------------
            "dbAcct": "",  # 放款卡号
            "dbAcctName": "",  # 放款银行卡账户名
            "loanDate": "",  # 放款申请时间  YYYY-MM-DD HH24:MI:SS
            "loanAmt": "10000",  # 放款金额         500-30000  ----------------------
            "lnTerm": "6",  # 期数    3/6/12/18/24       -------------------
            "creditAmt": "30000",  # 授信额度              -------------
            "loanPurpose": "08",  # 贷款用途    08装修房屋09购置大宗消费品10支付教育支出11支付医疗支出12支付旅游支出13支付其他消费款   ----
            "feeRate": "0.00065452",  # 费率          ---------------
            "yearRate": "0.2389",  # 年化利率        -----------
            "mobileNo": "",  # 注册手机号       -------------------
            "idValidDateStart": "2020-12-20",  # 身份证有效期起始日    ---------------------
            "idValidDateEnd": "2030-12-20",  # 身份证有效期结束日  YYYY-MM-DD --------------------
            "idAddress": "四川省成都市高新区天府三街",  # 身份证地址   -----------------
            "agency": "成都高新派出所",  # 身份证签发机关        ---------------
            "cardMobileNo": "13855139654",  # 银行卡绑定手机号  ---------------
            "creditCardSts": "N",  # 是否客户名下任一张信用卡状态为呆帐、核销 ------------
            "loanAcctSts": "Y",  # 是否贷款账户状态为呆帐、核销 -------------
            "creditCardOverdueDays": "Y",  # 是否客户名下任一张信用卡在过去2年内有超过120天、150天、180天以上的逾期 ----------
            "loanOverDays": "Y",  # 是否客户有过贷款在过去2年内有超过120天、150天、180天以上的逾期 -----------
            "thirdPartyBlackList": "N",  # 是否命中同盾、百融、前海、汇法黑名单 ----------
            "idVerifyRisk": "A",  # 核身风险等级  --------------
            "idCert": "Y",  # 是否有身份证或身份证明 ----------
            "ageCheck": "Y",  # 满足年龄18至55岁       --------------
            "policeInfoNotExist": "N",  # 公安信息不存在            -------------------
            "policeInfoNotMatch": "N",  # 公安信息不匹配        ------------------
            "overdueHisMaxDays": "100",  # 360平台上历史最大逾期天数  ---------
            "overdueHisMaxAmt": "5678.34",  # 360平台上历史最大逾期金额 ------------
            "ascore": "1000",  # A卡分  0-1000       -------------
            "bscore": "100",  # B卡分  0-1000    -------------
            "occupation": "2",        # 职业 1 党的机关、国家机关、群众团体和社会组织、企事业单位负责人2 专业技术人员3 办事人员和有关人员4 社会生产服务和生活服务人员5 农、林、牧、渔业生产及辅助人员6 生产制造及有关人员7 军人8 不便分类的其他从业人员 ----
            "rpyType": "01",            # 还款方式 01等额本息  ------
            "creditDataNo": "346291876879586557952",
            "directlyDataFlag": "N",
            "ocr1": "/upload/ocr/test/idcard_front.jpg",   # 身份证人像面
            "ocr2": "/upload/ocr/test/idcard_back.jpg",    # 身份证国徽面
            "face": "/upload/ocr/test/idcard_face.jpg"      # 人脸

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
        'interface': '/api/v1/jietiao/withhold/apply',
        'payload': {
            "sourceCode": "QH",  ##请求方代码
            "tranNo": "",  # 代扣申请流水号
            "totalAmt": "",  # 扣款金额
            "repayBankAcct": "",  # 还款方银行卡号
            "repayCstname": "",  # 客户姓名
            "repayBankNo": "0007",  # 银行编码
            "repayRelcard": "",  # 还款方身份证号
            "repayRelphone": "",  # 还款方手机号
            "remark": "代扣",  # 备注
            "channelId": "kq_xy",  # 通道代码 通联协议: tl_xy通联:tl快钱协议: kq_xy快钱:kq
            "agreementNo": "8888,99999"  # 协议号 如果是快钱协议付，则协议号包含快钱客户号，格式为客户号,协议号
        }
    },
    # 代扣申请结果查询
    'payment_query': {
        'interface': '/api/v1/jietiao/withhold/query',
        'payload': {
            "sourceCode": "QH",  # 请求方代码  QH
            "tranNo": ""  # 代扣申请流水号
        }
    },
    # 还款通知接口
    'repay_notice': {
        'interface': '/api/v1/jietiao/repay/apply',
        'payload': {
            "ifEnough":"0",  #0:非足额 1:足额
            "loanReqNo":"346177553668492058625",
            "rpyChannel":"1",  #0线下 1线上
            "rpyDate":"2022-07-13",
            "rpyDeductAmt":0, #营销减免金额
            "rpyIntAmt":0.66000000,
            "rpyOintAmt":0,
            "rpyPrinAmt":1000,
            "rpyRedLineAmt":0,  #红线减免
            "rpyReqNo":"346242956052115002121615678",
            "rpyShareAmt":1, #返费
            "rpyShareAmtFour":2,
            "rpyShareAmtOne":3,
            "rpyShareAmtThree":4,
            "rpyShareAmtTwo":5,
            # "rpyTerm":7,
            "rpyType":"01",   #提前还款:01(提前结清) 期供还款:02 (按指定期数进行还款，包含部分还款、提前还当期)   逾期还款：03（逾期还部分、逾期足额按期还）
            "sourceCode":"QH",
            "tranNo":"repayReqNo16576826171401"
        }
    },
    # 还款查询接口
    'repay_query': {
        'interface': '/api/v1/jietiao/repay/query',
        'payload': {
            "loanReqNo": "",  # 放款请求流水号
            "sourceCode": "QH",  # 请求方代码QH
            "rpyReqNo": ""  # 还款请求流水号

        }
    }

}
