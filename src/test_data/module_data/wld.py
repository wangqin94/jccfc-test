# # ---------------------------------------------------------
# # - 项目特性配置文件
# # - created time: 2021-03-06
# # - version: 1.1
# # ---------------------------------------------------------

# -----------------------------------------------------------
# 我来贷5期项目配置
# -----------------------------------------------------------
wld = {
    # 发起代扣签约
    'bind_card': {
        'interface': '/api/v1/welab/common/getCardRealNameMessage',
        'payload': {
            "head": {
                "tenantId": "000",
                "channelNo": "01",
                "merchantId": "F21E03WOLD",
                "requestSerialNo": "${requestSerialNo}",
                "requestTime": "${requestTime}",
            },
            "body": {
                "payer": "${姓名}",
                "payerIdNum": "${身份证号}",
                "payerPhoneNum": "${手机号}",
                "payerBankCardNum": "${银行卡号}",
                "payerBankCode": "0102"
            }
        }
    },
    # 确认代扣签约
    'confirm_bind_card': {
        'interface': '/api/v1/welab/common/bindCardRealName',
        'payload': {
            "head": {
                "tenantId": "000",
                "channelNo": "01",
                "merchantId": "F21E03WOLD",
                "requestSerialNo": "${requestSerialNo}",
                "requestTime": "${requestTime}",
            },
            "body": {
                "tradeSerialNo": "${tradeSerialNo}",
                "smsCode": "111111"
            }
        }
    },
    # 代扣签约结果查询
    'query_bind_card': {
        'interface': '/api/v1/welab/common/queryBindCardResult',
        'payload': {
            "head": {
                "tenantId": "000",
                "channelNo": "01",
                "merchantId": "F21E03WOLD",
                "requestSerialNo": "${requestSerialNo}",
                "requestTime": "${requestTime}",
            },
            "body": {
                "tradeSerialNo": "${tradeSerialNo}",
                "userId": "${userId}"
            }
        }
    },
    # 换卡申请
    'update_card': {
        'interface': '/api/v1/welab/common/updateWithholdCard',
        'payload': {
            "head": {
                "tenantId": "000",
                "channelNo": "01",
                "merchantId": "F21E03WOLD",
                "requestSerialNo": "${requestSerialNo}",
                "requestTime": "${requestTime}",
            },
            "body": {
                "loanInvoiceId": "${loanInvoiceId}",
                "idNo": "${idNo}",
                "repaymentAccountNo": "${repaymentAccountNo}"
            }
        }
    },
    # 授信申请
    'credit': {
        'interface': '/api/v1/welab/credit/apply',
        'payload': {
            "head": {
                "tenantId": "000",
                "channelNo": "01",
                "merchantId": "F21E03WOLD",
                "requestSerialNo": "${requestSerialNo}",
                "requestTime": "${requestTime}",
            },
            "body": {
                "thirdApplyId": "${thirdApplyId}",  # 授信申请编号
                "repayType": "1",  # 还款方式 EnumRepayMethod
                "orderType": "1",  # 订单类型 EnumOrderType
                "goodsName": "取现借款",  # 商品名称
                "interestRate": "35.5",  # 年化利率
                "applyAmount": "1000",  # 申请金额
                "monthIncome": "10000",  # 月收入
                "userBankCardNo": "${银行卡号}",  # 用户银行卡号
                "bankCode": "0102",  # 银行编码
                "reserveMobile": "${手机号}",  # 银行预留手机号
                "loanTerm": "3",  # 贷款期数
                "name": "${姓名}",  # 借款人姓名
                "idNo": "${身份证号}",  # 证件号码
                "sex": "1",  # 性别
                "mobileNo": "${手机号}",  # 手机号码
                "education": "4",  # 学历 EnumEduLevel
                "maritalStatus": "10",  # 婚姻状态 EnumMarriageStatus
                "nation": "汉族",  # 民族
                "idExpiryDate": "2020.12.30-2030.12.30",  # 证件有效期
                "issuingAuth": "成都市公安局天府新区分局",  # 发证机关
                "idCardAddr": "成都市天府新区华阳街道天府大道南段892号",  # 身份证地址
                "loanPurpose": "5",  # 贷款用途 EnumLoanPurpose
                "compName": "蜗牛文化传媒有限公司",   # 单位名称
                "compPhone": "028-6868-6688",  # 单位电话
                "workTime": "2",  # 在现工作单位时间
                "userOccupation": "1",  # 职业 EnumVocationType
                "duties": "B",  # 职务 EnumPost
                "companyNature": "B",  # 单位性质
                "industryCategory": "B",  # 行业类别
                "workAddrAddress": "四川省成都市高新区泰和二街123号",  # 工作详细地址
                "workAddrProvinceCode": "510000",  # 工作地址省份代码
                "workAddrProvinceName": "四川省",  # 工作地址省份名称
                "workAddrCityCode": "510100",  # 工作地址市级代码
                "workAddrCityName": "成都市",  # 工作地址市级名称
                "workAddrAreaCode": "510107",  # 工作地址区代码
                "workAddrAreaName": "武侯区",  # 工作地址区名称
                "liveAddress": "四川省成都市高新区泰和二街125号",  # 居住详细地址
                "liveProvinceCode": "510000",  # 居住地址省份代码
                "liveProvinceName": "四川省",  # 居住地址省份名称
                "liveCityCode": "510100",  # 居住地址市级代码
                "liveCityName": "成都市",  # 居住地址市级名称
                "liveAreaCode": "510107",  # 居住地址区代码
                "liveAreaName": "武侯区",  # 居住地址区名称
                "contactRelationList": [
                    {
                        "contactName": "何奕阳",
                        "contactMobile": "18380446001",
                        "contactRel": "2"  # 配偶
                    },
                    {
                        "contactName": "王羲之",
                        "contactMobile": "18380446002",
                        "contactRel": "1"  # 父母
                    }
                ],
                "fileInfos": [
                    {
                        "fileType": "1",
                        "fileName": "idz-1.jpg",
                        "fileUrl": "http://jccfc-hpre.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/hj/wld/credit/test/idz-1.jpg"
                    },
                    {
                        "fileType": "2",
                        "fileName": "idz-1.jpg",
                        "fileUrl": "http://jccfc-hpre.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/hj/wld/credit/test/idz-1.jpg"
                    },
                    {
                        "fileType": "3",
                        "fileName": "face_distinguish.jpg",
                        "fileUrl": "http://jccfc-hpre.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/hj/wld/credit/test/face_distinguish.jpg"
                    },
                    {
                        "fileType": "4",
                        "fileName": "授权书.pdf",
                        "fileUrl": "http://jccfc-hpre.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/hj/wld/credit/test/授权书.pdf"
                    },
                    {
                        "fileType": "6",
                        "fileName": "JC_third_auth_202110120000099.pdf",
                        "fileUrl": "http://jccfc-huat.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/hj/wld/credit/test/JC_third_auth_202110120000099.pdf"
                    },
                    {
                        "fileType": "7",
                        "fileName": "JC_userauth_202000000948071999.pdf",
                        "fileUrl": "http://jccfc-hpre.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/hj/wld/credit/test/JC_userauth_202000000948071999.pdf"
                    }
                ]
            }
        }
    },
    # 授信查询
    'credit_query': {
        'interface': '/api/v1/welab/credit/queryResult',
        'payload': {
            "head": {
                "tenantId": "000",
                "channelNo": "01",
                "merchantId": "F21E03WOLD",
                "requestSerialNo": "${requestSerialNo}",
                "requestTime": "${requestTime}",
            },
            "body": {
                "thirdApplyId": "${thirdApplyId}",
            }
        }
    },
    # 放款申请
    'loan': {
        'interface': '/api/v1/welab/loan/apply',
        'payload': {
            "head": {
                "tenantId": "000",
                "channelNo": "01",
                "merchantId": "F21E03WOLD",
                "requestSerialNo": "${requestSerialNo}",
                "requestTime": "${requestTime}",
            },
            "body": {
                "thirdApplyId": "${thirdApplyId}",
                "loanAmt": "1000",  # 借款金额
                "firstRepayDate": "2021-07-11",  # 首期还款日期yyyy-MM-dd
                "fixedRepayDay": "11",  # 固定还款日
                "loanTerm": "3",  # 贷款期数
                "name": "${姓名}",  # 借款人姓名
                "idNo": "${身份证号}",  # 证件号码
                "mobileNo": "${手机号}",  # 手机号码
                "orderType": "1",  # 订单类型 EnumOrderType
                "interestRate": "35.5",  # 年利率
                "repayType": "1",  # 还款方式 EnumRepayMethod
                "loanPurpose": "5",  # 贷款用途 EnumLoanPurpose
                "accountNo": "${银行卡号}",  # 放款/还款银行卡号
                "bankName": "中国工商银行",  # 中国工商银行
            }
        }
    },
    # 放款查询
    'loan_query': {
        'interface': '/api/v1/welab/loan/queryResult',
        'payload': {
            "head": {
                "tenantId": "000",
                "channelNo": "01",
                "merchantId": "F21E03WOLD",
                "requestSerialNo": "${requestSerialNo}",
                "requestTime": "${requestTime}",
            },
            "body": {
                "thirdApplyId": "${thirdApplyId}",
            }
        }
    },
    # 还款计划查询
    'repay_plan_query': {
        'interface': '/api/v1/welab/loan/queryRepayPlan',
        'payload': {
            "head": {
                "tenantId": "000",
                "channelNo": "01",
                "merchantId": "F21E03WOLD",
                "requestSerialNo": "${requestSerialNo}",
                "requestTime": "${requestTime}",
            },
            "body": {
                "loanInvoiceId": "${loanInvoiceId}",
            }
        }
    },
    # 还款
    'repay': {
        'interface': '/api/v1/welab/repay/withhold',
        'payload': {
            "head": {
                "tenantId": "000",
                "channelNo": "01",
                "merchantId": "F21E03WOLD",
                "requestSerialNo": "${requestSerialNo}",
                "requestTime": "${requestTime}",
            },
            "body": {
                "repayApplyList": [
                    {
                        "repayApplySerialNo": "${repayApplySerialNo}",  # 还款申请流水号
                        "loanInvoiceId": "${loanInvoiceId}",  # 资金方放款编号
                        "repaymentAccountNo": "${repaymentAccountNo}",  # 还款账号
                        "repayType": "1",  # 还款类型 EnumTrialRepayType
                        "repayScene": "01",  # 还款场景 EnumRepayScene
                        "repayNum": "1",  # 期数
                        "repayAmount": "256.62",  # 还款总金额
                        "repayPrincipal": "200.62",  # 还款总本金
                        "repayInterest": "56",  # 还款总利息
                        "repayFee": "0",  # 还款总费用
                        "repayOverdueFee": "0",  # 还款总罚息
                        "repayCompoundInterest": "0",  # 还款总复利
                    }
                ]
            }
        }
    },
    # 还款结果查询
    'repay_result_query': {
        'interface': '/api/v1/welab/repay/queryWithholdResult',
        'payload': {
            "head": {
                "tenantId": "000",
                "channelNo": "01",
                "merchantId": "F21E03WOLD",
                "requestSerialNo": "${requestSerialNo}",
                "requestTime": "${requestTime}",
            },
            "body": {
                "repayApplySerialNo": "${repayApplySerialNo}",
            }
        }
    },

}