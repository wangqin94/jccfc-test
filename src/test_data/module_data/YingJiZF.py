# # ---------------------------------------------------------
# # - 项目特性配置文件
# # - created time: 2021-03-06
# # - version: 1.1
# # ---------------------------------------------------------

# -----------------------------------------------------------
# 应急支付项目配置
# -----------------------------------------------------------
YingJiZF = {
    'queryChannel': {
        'interface': '/api/v1/emergency/queryChannel',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "channelName": "度",
            }
        }

    },
    'queryInvoiceListByPage': {
        'interface': '/api/v1/emergency/queryInvoiceListByPage',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "bankType": "",  # 开户行总行号 中国工商：0102 中国农业：0103 中国银行：0104 建设银行：0105
                "certificateNo": "",  # 身份证号
                "channelNo": "F21C02BAID",  # 渠道号
                "loanStatus": "1",  # EnumLoanInvoiceStatus 借据状态 枚举类型NORMAL("1", "正常"),OVERDUE("2", "逾期"),SETTLE(
                # "3", "结清");
                "noticeType": "0",  # 通知类型（0-无条件、1-账单日通知、2-逾期通知）
                "userIdList": [],  # 客户ID集合 list
                "pageNum": 1,
                "pageSize": 20,
                "settleFlag": "0",  # 结清标识 EnumBool 0-否，1-是
                "userTel": "",  # 电话号码
            }
        }

    },
    'loan_bill': {
        'interface': '/api/v1/loan/bill',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "idNo": "140431198406286402",  # 身份证号
                "applyNo": "000LI5538514397462145161272",  # 借据号
                "billType": "1",  # 1-正常账单，2-提前结清
            }
        }
    },
    'payment_query': {
        'interface': '/api/v1/payment/query',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "idNo": "140431198406286402",  # 身份证号
                "applyNo": "000LI5538514397462145161272",  # 借据号
                "channelCode": "F21C02BAID",  # 渠道号
            }
        }

    },
    'loan_query': {
        'interface': '/api/v1/loan/query',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "idNo": "140431198406286402",  # 身份证号
                "channelCode": "F21C02BAID",  # 渠道号
            }
        }
    },
    'loan_details': {
        'interface': '/api/v1/loan/details',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "applyNo": "000LI5538514397462145161272",  # 借据号
            }
        }
    },

    'repay_query': {
        'interface': '/api/v1/repay/query',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "applyNo": "000LI5538514397462145161272",  # 借据号
            }
        }
    },

    'plan_query': {
        'interface': '/api/v1/replay/plan/query',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "applyNo": "000LA2021060000004557",  # 支用申请号：000LA2021050000000020
                "channelCodes": ["F20B02XIEC"]
            }
        }
    },

    'payment_result': {
        'interface': '/api/v1/payment/result',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "appOrderNo": "appOrderNo000LA2021060000004557",  # 订单流水号：000LA2021050000000020
            }
        }
    },

    'bankcard_bind': {
        'interface': '/api/v1/bankCard/bind',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "certificateNo": "140431198406286402",  # 身份证号
                "mobileNo": "14983105967",  # 手机号
                "accountNo": "6212269404480619920",  # 新银行卡号
                "accountBankName": "",  # 新银行卡所属银行名称
                "accountBin": "",  # 新银行卡所属银行卡bin
                "bankCode": "",  # 新银行总行号
                "branchBankCode": "",  # 新银行支行联号
            }
        }
    },

    'bankcard_modify': {
        'interface': '/api/v1/bankCard/modify',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "invoiceId": "000LI5538514397462145161272",  # 借据号
                "certificateNo": "140431198406286402",  # 身份证号
                "mobileNo": "14983105967",  # 手机号
                "oldAccountNo": "6212269404480619920",  # 新银行卡号
                "newAccountNo": "6212269404480612920",  # 旧银行卡号
                "newAccountBankName": "",  # 新银行卡所属银行名称
                "newAccountBin": "",  # 新银行卡所属银行卡bin
                "newBankCode": "",  # 新银行总行号
                "newBranchBankCode": "",  # 新银行支行联号
            }
        }
    },

    'payment': {
        'interface': '/api/v1/payment',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "loanInvoiceId": "000LI5538514397462145161272",  # 借据号
                "channelNo": "2",  # 主动还款渠道
                "repayType": "0",  # 还款方式 0-按期还款   1-提前还款
                "paymentType": "5",  # 支付类型1-支付宝-主动还款 2-支付宝-代扣 3-微信-主动还款 4-微信-代扣 5-银行卡-主动还款 6-银行卡-代扣   7-云闪付-主动还款
                "periods": "1",  # 还款期数 多期以,分隔
                "repayAmt": 212.46,  # 还款金额
                "appOrderNo": "",  # 还款订单流水号
                "settleStatus": "1",  # 结清标识 EnumBool 0 未结清  1 结清
                "payPlatformCode": "zhifubianhao",  # 支付平台编号
                "aliPayViewUrl": "https://www.baidu.com/",  # 支付平台编号
                "idNo": "451123198311190587",  # 身份证号（银行卡还款必须）
                "phoneNum": "18908989867",  # 用户银行卡绑定手机号（银行卡还款必须）
                "bankAcctName": "楚东进",  # 还款人姓名（银行卡还款必须）
                "bankName": "0102",  # 银行编号（银行卡还款必须）
                "bankAcctNo": "6212810833868379081",  # 还款人银行卡卡号（银行卡还款必须）
                "deviceInfo": "设备信息1.21sxf",  # 设备信息（微信还款必须）
                "wxPayViewUrl": "https://www.baidu.com/",  # 传值外网可以访问的地址（微信还款必须）
                "createIp": "10.12.255.0",  # ip（微信还款必须）
            }
        }
    },
}