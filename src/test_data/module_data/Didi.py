Didi = {
    # 加密接口-滴滴
    'encrypt': {
        'interface': '/api/didi/encrypt',
    },

    # 解密接口
    'decrypt': {
        'interface': '/api/didi/decrypt',
    },
    # 授信申请数据结构
    "credit_apply": {
        "interface": "/api/v1/didi/credit/creditApply",
        "payload": {
            "sftpDir": "/hj/xdgl/didi/credit",
            "userInfo": {
                "name": "张三",  # ⽤户姓名
                "idNo": "411023199909011011",  # 身份证号
                "phone": "17633336333",  # 银⾏卡绑定⼿机号
                "bankCardNo": "",  # 银⾏卡号
                "bankName": "中国银行",  # 银行名称
                "bankAddr": "BOC",  # 银行编码
                "jobType": "1",
                # 职业 0:机关、党群组织、企事业单位负责⼈， 1:专业技术⼈员， 3:办事⼈员和有关⼈员， 4:商业、服务业⼈员，
                # 5:农林牧渔⽔利业⽣产⼈员， 6 ⽣产、运输设备操作相关⼈员， X: 军⼈ Y：其他从业⼈员
                "province": "四川",  # 省
                "city": "成都",  # 市
                "county": "高新",  # 区
                "address": "中航城市广场",  # 客户详细地址
                "nationality": "中国",  # 国籍
                "certificateType": "身份证",  # 证件类型 默认身份证
            },
            "ocrInfo": {
                "name": "张三",
                "gender": "⼥",
                "race": "汉",
                "birthday": "1995-03-09",
                "address": "贵州市六盘⽔市⽔调⽔个",
                "idNo": "411023199909011011",
                "validDate": "2015.10.08-2035.10.08",
                "authority": "六盘⽔公安局"
            },
            "userScoreInfo": {
                "scoreOne": 650,
                "scoreTwo": 19500,
                "scoreThree": 1690000,
                "endDate": "2024-05-20 22:16:54"
            },
            "applicationId": "DC00003080202309231729191413d8",  # 授信申请单号  64位
            "callbackUrl": "http://manhattanloantest.xiaojukeji.com/manhattan/loan/openfin/superpartner/standard/creditResult"
            # 接收异步通知回调的地址
        }
    },
    # 授信查询数据结构
    "credit_query": {
        'interface': '/api/v1/didi/credit/creditQuery',
        "payload": {
            "applicationId": ""  # 授信申请单号
        }
    },
    # 支用风控审核
    "loan_risk_check": {
        'interface': '/api/v1/didi/loan/loanRiskCheck',
        "payload": {
            "applicationId": "",  # 授信申请单号
            "loanOrderId": "",  # 贷款ID
            "loanAmount": "",  # 贷款⾦额，单位分
            "interestType": 2,  # 还款类型： 1 等额本⾦； 2 等额本息； 3 先息后本
            "totalInstallment": 0,  # 贷款总期数
            "interestRate": 0,  # ⽇利率
            "interestPenaltyRate": 0,  # ⽇罚息率
            "loanUsage": "1",  # 1：⽇常消费、 2：汽⻋加油 3：修⻋保养、 5：医疗⽀出、 6：教育深造、 7：房屋装修  8：旅游出⾏ 28: 其他消费⽤款  默认⽇常消费
            "sftpDir": "/hj/xdgl/didi/credit",  # 必须设置，与活体、 OCR及合同路径相关
            "callbackUrl": "",  # 接收异步通知回调的地址
            "finProductType": "",  # 产品类型: 1.随借随还， 2.固定期限
            "rateType": "0",  # 是否涉及营销定价优惠；默认为【0】否  1 是
            "preAbsId": '',  # 信托计划编号
            "guaranteeOrgCode": '',  # 融担机构标识
            "guaranteeOrgName": '',  # 融担机构名称
            "userInfo": {
                "name": "张三",  # ⽤户姓名
                "idNo": "411023199909011011",  # 身份证号
                "phone": "17633336333",  # 银⾏卡绑定⼿机号
                "bankCardNo": "",  # 银⾏卡号
                "bankName": "中国银行",  # 银行名称
                "bankAddr": "BOC",  # 银行编码
                "jobType": "1",
                # 职业 0:机关、党群组织、企事业单位负责⼈， 1:专业技术⼈员， 3:办事⼈员和有关⼈员， 4:商业、服务业⼈员，
                # 5:农林牧渔⽔利业⽣产⼈员， 6 ⽣产、运输设备操作相关⼈员， X: 军⼈ Y：其他从业⼈员
                "province": "四川",  # 省
                "city": "成都",  # 市
                "county": "高新",  # 区
                "address": "中航城市广场",  # 客户详细地址
                "nationality": "中国",  # 国籍
                "certificateType": "1",  # 证件类型 默认身份证
            },
            "ocrInfo": {
                "name": "张三",
                "gender": "⼥",
                "race": "汉",
                "birthday": "1995-03-09",
                "address": "贵州市六盘⽔市⽔调⽔个",
                "idNo": "411023199909011011",
                "validDate": "2015.12.24-2035.12.24",
                "authority": "六盘⽔公安局"
            }
        }
    },
    # 支用风控审核查询
    "query_loan_risk_check": {
        'interface': '/api/v1/didi//loan/queryLoanRiskCheck',
        'payload': {
            "applicationId": "",  # 授信申请单号
            "loanOrderId": "",  # 贷款ID
        }
    },

    # 提交借款申请接口
    "loan_apply": {
        'interface': '/api/v1/didi/loan/loanApply',
        "payload": {
            "applicationId": "",  # 授信申请单号
            "loanOrderId": "",  # 贷款ID
            "loanAmount": "",  # 贷款⾦额，单位分
            "userInfo": {
                "name": "张三",  # ⽤户姓名
                "idNo": "411023199909011011",  # 身份证号
                "phone": "17633336333",  # 银⾏卡绑定⼿机号
                "bankCardNo": "",  # 银⾏卡号
                "bankName": "中国银行",  # 银行名称
                "bankAddr": "BOC",  # 银行编码
                "jobType": "1",
                # 职业 0:机关、党群组织、企事业单位负责⼈， 1:专业技术⼈员， 3:办事⼈员和有关⼈员， 4:商业、服务业⼈员，
                # 5:农林牧渔⽔利业⽣产⼈员， 6 ⽣产、运输设备操作相关⼈员， X: 军⼈ Y：其他从业⼈员
                "province": "四川",  # 省
                "city": "成都",  # 市
                "county": "高新",  # 区
                "address": "中航城市广场",  # 客户详细地址
                "nationality": "中国",  # 国籍
                "certificateType": "1",  # 证件类型 默认身份证
            },
        },
        "repayDay": "",  # 还款⽇，滴滴侧计算⽣成
        "callbackUrl": "",  # 接收异步通知回调的地址
        "guaranteeOrgCode": '',  # 融担机构标识
        "guaranteeOrgName": '',  # 融担机构名称
    },
    # 查询借款结果接口
    "query_loan_result": {
        'interface': '/api/v1/didi/loan/queryLoanResult',
        'payload': {
            "loanOrderId": "",  # 贷款ID
        }
    },
    # 主动还款
    "repay": {
        'interface': 'api/v1/didi/repay/repay',
        "payload": {
            "userInfo": {
                "address": "浙江省杭州市上城区御景湾3栋4303号",
                "bankCardNo": "6221821289128562",
                "city": "杭州市",
                "county": "上城区",
                "bankName": "工商银行",
                "bankAddr": "ICBC",
                "idNo": "330102200906279097",
                "province": "浙江省",
                "nationality": "中国",
                "phone": "14967765224",
                "name": "玥彩",
                "jobType": "1",
                "certificateType": "身份证"
            },
            "loanNumbers": "1,2,3,4,5,6,7,8,9,10,11,12",
            "repayType": 2,
            "loanOrderId": "DC0000308020230923180538978b52",
            "payType": 1,
            "subAccStatus": 0,
            "repayAmountInfo": {
                "principal": 0,
                "interestPenalty": 0,
                "advanceClearFee": 0,
                "totalAmount": 100000,
                "guaranteeFee": 0,
                "insuranceFee": 0,
                "interest": 0,
                "ratedInterest": 0,
                "principalPenalty": 0,
                "guaranteeConsultFee": 0
            },
            "agreementNo": "00000000000991392065",
            "callbackUrl": "http://manhattanloantest.xiaojukeji.com/manhattan/loan/openfin/superpartner/standard/activeRepayResult",
            "subAcctList": [],
            "payId": "202309231805380002150ff9df670b0l",
            "applicationId": "DC0000308020230923180538979cf73"
        }
    },


    # 渠道还款通知
    "initiate_Repay": {
        'interface': '/api/v1/didi/repay/initiateRepay',
        'payload': {
            "applicationId": "",  # 授信申请单号
            "loanOrderId": "",  # 贷款ID
            "payId": "",  # 还款⽀付流⽔单号，幂等字段
            "payType": "",  # 还款⽀付⽅式： 1 ⽤户主动还款； 2 合作⽅发起代扣还款； 3 滴滴发起代扣还款； 4 滴滴发起的线下还款； 9 代偿； 10 ⽀付宝还
            "repayType": "",  # 1.当期还款， 2.结清全部
            "loanNumbers": "",  # 还款期数：多期还款时还款期数之间通过英⽂逗号","隔开；
            "callbackUrl": "",  # 接收异步通知回调的地址
            "agreementNo": "",  # 中⾦绑卡协议流⽔号
            "repayAmountInfo": "",  # 应还⾦额信息
            "repayDate": "",  # 还款时间, ⾮必填, 格式: yyyy-MM-dd,默认当前⽇期
            "subAccStatus": 0,  # 0:不分账 1:分账
            "subAcctList": [
                {
                    'subAcctNo': '',  # 分账账号
                    'subAmount': ''  # 分账⾦额
                }
            ],  # 分账列表
            "userInfo": {
                "name": "",
                "idNo": "",
                "bankCardNo": "",
                "phone": ""
            },
        }
    },
    # 查询还款结果
    "query_repay_result": {
        'interface': '/api/v1/didi/repay/queryRepayResult',
        'payload': {
            "loanOrderId": "",  # 贷款ID
            "payId": "",  # 还款⽀付流⽔单号，幂等字段
        }
    }

}
