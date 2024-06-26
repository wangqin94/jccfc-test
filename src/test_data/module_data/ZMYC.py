# # ---------------------------------------------------------
# # - 项目特性配置文件
# # - created time: 2021-03-06
# # - version: 1.1
# # ---------------------------------------------------------

# -----------------------------------------------------------
# 极融项目配置
# -----------------------------------------------------------
ZMYC = {
    # 加密接口
    'encrypt': {
        'interface': '/api/v1/yinliu/secret/thirdEncryptData/{}',
    },

    # 解密接口
    'decrypt': {
        'interface': '/api/v1/yinliu/secret/thirdDecryptData',
    },
    # 协议共享申请接口
    'sharedWithholdingAgreement': {
        'interface': '/api/v1/yl/common/sharedWithholdingAgreement',
        'payload': {
            "head": {
                "merchantId": "G22E02JIKE",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "payer": "QH",  # 付款方姓名
                "mobileNo": "",  # 注册手机号
                "payerPhoneNum": "",  # 付款方银行卡预留手机号
                "payerIdNum": "",  # 付款方身份证号
                "payerBankCardNum": "",  # 付款方银行卡号
                "payerBankCode": "0102",  # 付款方银行编号
                "aggrementNum": "",  # 代扣协议号
                "payChannel": "1001",  # 支付通道1035  极融宝付
            }
        }
    },
    # 代扣签约申请接口
    'getCardRealNameMessage': {
        'interface': '/api/v1/yl/common/getCardRealNameMessage',
        'payload': {
            "head": {
                "merchantId": "G24E011",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "payer": "QH",  # 付款方姓名
                "mobileNo": "",  # 注册手机号
                "payerPhoneNum": "",  # 付款方银行卡预留手机号
                "payerIdNum": "",  # 付款方身份证号
                "payerBankCardNum": "",  # 付款方银行卡号
                "payerBankCode": "",  # 付款方银行编号
                "paymentChannel": "1001",  # 支付通道
                "aggrementNum":""
            }
        }
    },
    # 确认代扣签约接口
    'bindCardRealName': {
        'interface': '/api/v1/yl/common/bindCardRealName',
        'payload': {
            "head": {
                "merchantId": "G24E011",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "tradeSerialNo": "",  # 同发起代扣签约返回的交易流水号
                "mobileNo": "",  # 注册手机号
                "payerPhoneNum": "",  # 付款方银行卡预留手机号
                "userId": "",  # 锦程用户编号
                "smsCode": "111111",  # 验证码
            }
        }
    },
    # 代扣申请结果查询
    'queryWithholdingAgreement': {
        'interface': '/api/v1/yl/common/queryWithholdingAgreement',
        'payload': {
            "head": {
                "merchantId": "G24E011",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "payer": "付款方姓名",  # 付款方姓名
                "payerIdNum": "",  # 付款方身份证号
                "payerBankCardNum": "",  # 付款方银行卡号
                "payerPhoneNum": ""  # 付款方银行卡预留手机号
            }
        }
    },
    # 授信请求接口
    'credit_apply': {
        'interface': '/api/v1/yl/common/credit/apply',
        'payload': {
            "head": {
                "merchantId": "G24E011",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "thirdApplyId": "",  # 三方授信申请编号  与放款申请编号保持一致
                "thirdApplyTime": "",  # 客户三方申请时间  yyyyMMddHHmmss
                "repayType": "1",  # 还款方式  EnumRepayMethod
                "orderType": "1",  # 订单类型  固定传1-取现
                "goodsName": "装修",  # 商品名称  取现为：取现借款、分期购物为：商品名称
                "userBankCardNo": "0102",  # 用户银行卡号
                "bankCode": "0102",  # 银行编码
                "reserveMobile": "",  # 银行预留手机号
                "loanTerm": 6,  # 贷款期数
                "name": "",  # 借款人姓名
                "idNo": "",  # 证件号码
                "sex": "1",  # 性别  UNKNOWN("0", "未知的性别"),MALE("1", "男"),FEMALE("2", "女"),NOT_EXPLAINED("9", "未说明的性别");
                "mobileNo": "手机号码",  # 手机号码
                "education": "11",  # 学历 EnumEduLevel
                "degree": "0",  # 最高学位 EnumCreditDegree
                "maritalStatus": "20",  # 婚姻状态 EnumMarriageStatus，若已婚，则联系人需含配偶
                "nation": "汉",  # 民族
                "idExpiryDate": "1990.1.1-2053.06.25",  # 身份证有效期 1990.1.1-2099.12.31（长期传2099.12.31）
                "issuingAuth": "成都高新派出所",  # 发证机关
                "idCardAddrAddress": "天府四街OCG写字楼A座",  # 身份证地址
                "idCardAddrProvinceCode": "510000",  # 身份证地址省份代码
                "idCardAddrProvinceName": "四川省",  # 身份证地址省份名称
                "idCardAddrCityCode": "510100",  # 身份证地址市级代码
                "idCardAddrCityName": "成都市",  # 身份证地址市级名称
                "idCardAddrAreaCode": "510107",  # 身份证地址区代码
                "idCardAddrAreaName": "武侯区",  # 身份证地址区名称
                "idCardAddr": "四川省成都市高新区天府四街OCG写字楼A座",  # 身份证完整地址
                "loanPurpose": "4",  # 贷款用途 EnumLoanPurpose
                "compName": "单位名称",  # 单位名称
                "compPhone": "13812345689",  # 单位电话
                "workTime": 1000,  # 在现工作单位时间 单位：月
                "workStatus": 'F',  # 工作状态 EnumWorkStatus
                "userOccupation": "0",  # 职业 EnumVocationType
                "duties": "A",  # 职务 EnumPost
                "companyNature": "A",  # 单位性质 EnumUnitProperty
                "industryCategory": "A",  # 行业类别 EnumIndustryType
                "workAddrAddress": "金融街119号",  # 工作详细地址
                "workAddrProvinceName": "安徽省",  # 工作地址省份名称
                "workAddrProvinceCode": "",  # 工作地址省份代码
                "workAddrCityName": "合肥市",  # 工作地址市级名称
                "workAddrCityCode": "",  # 工作地址市级代码
                "workAddrAreaName": "蜀山区",  # 工作地址区名称
                "workAddrAreaCode": "",  # 工作地址区代码
                "liveAddress": "金融街119号",  # 工作详细地址
                "liveProvinceName": "安徽省",  # 居住地址省份名称
                "liveProvinceCode": "",  # 居住地址省份代码
                "liveCityName": "合肥市",  # 居住地址市级名称
                "liveCityCode": "",  # 居住地址市级代码
                "liveAreaName": "蜀山区",  # 居住地址区名称
                "liveAreaCode": "",  # 居住地址区代码
                "applyAmount": 1000,  # 申请金额 元
                "monthIncome": 1000,  # 月收入  元
                "familyMonthIncome": 2000,  # 家庭月收入  元
                # "liabilities": "0",  # EnumLiabilities，可传多个枚举，码值间以英文逗号“,”分隔；0-无贷款时，不支持多个枚举
                "guaranteeMerchantId": "",
                "contactRelationList": [
                    {
                        "contactName": "配偶姓名",  # 联系人姓名
                        "contactMobile": "13912345689",  # 联系人电话
                        "contactRel": "2",  # 联系人关系 EnumRelationType
                    },
                ],
                "fileInfos": [
                    {
                        "fileType": "1",  # 身份证正面
                        "fileUrl": "xdgl/jike/test/front.jpg",
                        "fileName": "front.png"
                    },
                    {
                        "fileType": "2",  # 身份证反面
                        "fileUrl": "xdgl/jike/test/back.jpg",
                        "fileName": "back.png"
                    },
                    {
                        "fileType": "3",  # 人脸
                        "fileUrl": "xdgl/jike/test/face.jpg",
                        "fileName": "face.png"
                    },
                    {
                        "fileType": "4",  # 征信查询授权书
                        "fileUrl": "xdgl/jike/test/credit.pdf",
                        "fileName": "credit.pdf"
                    },
                    {
                        "fileType": "6",
                        "fileUrl": "xdgl/jike/test/C20JIKEloancontract.pdf",
                        "fileName": "JC_non_student_202000000948071964.pdf"
                    },
                    {
                        "fileType": "7",  # 三方查询授权书
                        "fileUrl": "xdgl/jike/test/third.pdf",
                        "fileName": "third.pdf"
                    },
                    {
                        "fileType": "10",
                        "fileUrl": "xdgl/jike/test/C20JIKEloancontract.pdf",
                        "fileName": "JC_third_auth_202000000948071964.pdf"
                    }
                ],
            }
        }

    },
    # 授信申请结果查询
    'credit_query': {
        'interface': '/api/v1/yl/common/credit/queryResult',
        'payload': {
            "head": {
                "merchantId": "G24E011",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "thirdApplyId": "",  # 授信申请编号 与授信申请编号保持一致(同一thirdApplyId间隔不小于30秒)
            }
        }
    },
    # 还款计划试算
    'repayPlanTrial': {
        'interface': '/api/v1/yl/common/loan/repayPlanTrial',
        'payload': {
            "head": {
                "merchantId": "G24E011",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "productId": "G24E011",  # 产品编号  固定传G24E011
                "applyAmount": "1000",  # 申请金额
                "term": "12",  # 申请总期次
                "loanDate": "",  # 放款日期 yyyy-MM-dd
            }
        }
    },
    # 放款请求接口
    'loan_apply': {
        'interface': '/api/v1/yl/common/loan/apply',
        'payload': {
            "head": {
                "merchantId": "G24E011",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "thirdApplyId": "",  # 放款申请编号  与授信申请编号保持一致
                "loanAmt": 1000,  # 借款金额
                "loanTerm": 6,  # 贷款期数
                "name": "",  # 借款人姓名
                "idNo": "",  # 证件号码
                "mobileNo": "0102",  # 手机号码
                "reserveMobile": "",  # 银行预留手机号
                "orderType": "1",  # 订单类型  固定传1-取现
                "repayType": "1",  # 还款方式  EnumRepayMethod
                "accountNo": "",  # 放款/还款银行卡号
                "bankName": "工商银行",  # 还款银行名称
                "loanPurpose": "1",  # 贷款用途 EnumLoanPurpose
                "guaranteeContractNo": "",  # 担保合同号
                "fileInfos": [
                    {
                        "fileType": "9",
                        "fileUrl": "xdgl/jike/test/C20JIKEloancontract.pdf",
                        "fileName": "C20JIKEloancontract.pdf"
                    }
                ],
                "repaymentPlans": [
                    {
                        "period": "1",  # 期数
                        "billDate": "2022-02-03",  # 账单日
                        "principalAmt": 1,  # 本金金额
                        "interestAmt": 1,  # 利息金额
                        "guaranteeAmt": 1,  # 担保费金额
                    }
                ],
            }
        }

    },
    # 放款申请结果查询
    'loan_query': {
        'interface': '/api/v1/yl/common/loan/queryResult',
        'payload': {
            "head": {
                "merchantId": "G24E01JUZI",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "thirdApplyId": "",  # 授信申请编号 与授信申请编号保持一致(同一thirdApplyId间隔不小于30秒)
            }
        }
    },

    # 还款计划查询
    'repayPlan_query': {
        'interface': '/api/v1/yl/common/loan/queryRepayPlan',
        'payload': {
            "head": {
                "merchantId": "G24E01JUZI",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "loanInvoiceId": "",  # 资金方放款编号 放款成功后返回的资金方借据编号
            }
        }
    },

    # 借款合同查询
    'loanContract_query': {
        'interface': '/api/v1/yl/common/loan/queryLoanContract',
        'payload': {
            "head": {
                "merchantId": "G24E01JUZI",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "loanInvoiceId": "",  # 资金方放款编号 放款成功后返回的资金方借据编号
                "contractType": "6",  # 合同类型 EnumFileType,固定传6-借款合同
            }
        }
    },

    # 担保费同步
    'syncGuaranteePlan': {
        'interface': '/api/v1/yl/common/loan/syncGuaranteePlan',
        'payload': {
            "head": {
                "merchantId": "",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "loanInvoiceId": "",  # 资金方放款编号 放款成功后返回的资金方借据编号
                "flag": "",
                "guaranteePlans": [
                    {
                        "period": 3,
                        "guaranteeAmt": 20,
                    }
                ],  # 担保费计划列表

            }
        }
    },
    # 还款试算
    'repayTrial': {
        'interface': '/api/v1/yl/common/repay/repayTrial',
        'payload': {
            "head": {
                "merchantId": "G24E01JUZI",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "loanInvoiceId": "",  # 资金方放款编号
                "repayTerm": "",  # 期次 提前结清传起始期次
                "repayDate": "",  # 还款日期 yyyy-MM-dd
                "repayType": "",  # 还款类型  EnumTrialRepayType
            }
        }
    },
    # 还款通知接口
    'repay_apply': {
        'interface': '/api/v1/yl/common/repay/uniteRepay',
        'payload': {
            "head": {
                "merchantId": "G24E01JUZI",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "repayScene": "01",  # 还款场景 EnumRepayScene REPAY_ONLINE("01", "线上还款"),REPAY_OFFLINE("02", "线下还款"),ALIPAY_NOTICE（"04","支付宝还款通知"）OVERDUE_NOTICE（"05","逾期（代偿、回购后）还款通知"）
                "repayApplySerialNo": "6",  # 还款申请流水号 每笔还款申请流水号唯一，支付宝还款传支付宝扣款订单号
                "thirdWithholdId": "",  # 三方代扣编号 线下还款、逾期还款通知：传机构代扣编号；支付宝还款通知：传支付宝扣款订单号；其他还款场景不传
                "appAuthToken": "6",  # 支付宝授权令牌 支付宝还款通知必传
                "loanInvoiceId": "",  # 资金方放款编号 放款成功后返回的资金方借据编号
                "thirdRepayTime": "",  # 线下还款、支付宝还款必传，客户实际还款时间
                "thirdRepayAccountType": "中国工商银行",  # 线下还款、支付宝还款必传，银行卡还款传开户行名称，微信、支付宝还款传支付平台名称，如：微信、支付宝、中国工商银行 等；
                "repaymentAccountNo": "6",  # 还款账号 线上还款、线下还款、支付宝还款必传
                "repayType": "1",  # 还款类型 EnumTrialRepayType
                "repayNum": 1,  # 期数 前结清，将各期金额合并，期数传开始期次
                "repayAmount": 0,  # 资还款总金额
                "repayPrincipal": 0,  # 还款总本金
                "repayInterest": 0,  # 还款总利息
                "repayGuaranteeFee": 0,  # 还款总担保费
                "repayFee": 0,  # 还款总费用
                "repayOverdueFee": 0,  # 还款总罚息
                "repayCompoundInterest": 0,  # 还款总复利
            }
        }
    },
    # 还款结果查询
    'repay_query': {
        'interface': '/api/v1/yl/common/repay/queryWithholdResult',
        'payload': {
            "head": {
                "merchantId": "G24E01JUZI",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "repayApplySerialNo": "",  # 还款申请流水号
            }
        }
    },


    # 附件补录
    'supplementAttachment': {
        'interface': '/api/v1/yl/common/supplementAttachment',
        'payload': {
            "head": {
                "merchantId": "G24E01JUZI",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "thirdApplyId": "",  # 渠道申请编号  贷前附件上传时不传，贷后附件补录必传
                "fileInfos": [
                    {
                        "fileType": "1",
                        "file": "文件Base64字符串",
                        "fileName": "idcard_front_202000000948071964.jpg"
                    },
                    {
                        "fileType": "2",
                        "file": "文件Base64字符串",
                        "fileName": "idcard_back_202000000948071964.jpg"
                    },
                    {
                        "fileType": "3",
                        "file": "文件Base64字符串",
                        "fileName": "face_distinguish_202000000948071964.jpg"
                    },
                    {
                        "fileType": "4",
                        "file": "文件Base64字符串",
                        "fileName": "JC_userauth_202000000948071964.pdf"
                    },
                    {
                        "fileType": "6",
                        "file": "文件Base64字符串",
                        "fileName": "JC_non_student_202000000948071964.pdf"
                    },
                    {
                        "fileType": "7",
                        "file": "文件Base64字符串",
                        "fileName": "JC_third_auth_202000000948071964.pdf"
                    }
                ],
            }
        }
    },

    # 省市区地址获取
    'getAllAreaInfo': {
        'interface': '/api/v1/yl/common/getAllAreaInfo',
        'payload': {
            "head": {
                "merchantId": "G24E01JUZI",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
            }
        }
    },

    # LPR查询
    'queryLprInfo': {
        'interface': '/api/v1/yl/common/queryLprInfo',
        'payload': {
            "head": {
                "merchantId": "G24E01JUZI",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "thirdApplyId": "",
                "queryFlag": "loan"
            }
        }
    },

    # 授信额度取消
    'cancelCreditLine': {
        'interface': '/api/v1/yl/common/cancellationCreditLine',
        'payload': {
            "head": {
                "merchantId": "G24E01JUZI",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "thirdApplyId": "",
                "reason": "授信额度取消-测试"
            }
        }
    },

    # 代偿结果查询
    'queryAccountResult': {
        'interface': '/api/v1/yl/common/compensation/queryAccountResult',
        'payload': {
            "head": {
                "merchantId": "G24E01JUZI",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "thirdApplyId": "",
                "loanInvoiceId": "",  # 与三方申请号二选一必传
                "term": ""
            }
        }
    },

    # 结清证明申请
    'applySettlementCer': {
        'interface': '/api/v1/yl/common/applySettlementCer',
        'payload': {
            "head": {
                "merchantId": "G24E01JUZI",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "name": "",  # 用户姓名
                "idNo": "",  # 用户身份证
                "mobileNo": "",  # 用户手机号
                "loanApplyIdList": []  # 放款申请编号List<String>
            }
        }
    },

    # 结清证明下载
    'settlementCerDownload': {
        'interface': '/api/v1/yl/common/settlementCerDownload',
        'payload': {
            "head": {
                "merchantId": "G24E01JUZI",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "name": "",  # 用户姓名
                "idNo": "",  # 用户身份证
                "applyId": ""  # 结清证明编号
            }
        }
    },
    # 代偿确认
    'compensationConfirm': {
        'interface': '/api/v1/yl/common/compensationConfirm',
        'payload': {
            "head": {
                "merchantId": "G24E01JUZI",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "confirmList": [
                    {
                    "compensationNo":""  # 代偿、回购清单内的流水号
                }
                ]
            }
        }
    },

    # 自牧云创理赔文件 键值对字典数据模板
    "ZMYCClaimTemple": {
        'loan_no': '',  # 借据号
        'name': '',  # 姓名
        'cer_no': '',  # 身份证号
        'current_period': '',  # 期次
        'repay_amt': '',  # 代偿总额
        'repay_date': '',  # 代偿日期
        'business_no': '',  # 流水号
        'product_id': '',  # 产品号
        'type_flag': '1',  # 类型标志
        'loan_amt': '',  # 贷款总金额
        'loan_period': '',  # 贷款总期次
        'loan_date': '',  # 放款时间
        'paid_prin_amt': '',  # 本金
        'paid_int_amt': '',  # 利息
        'left_repay_amt': '',  # 在贷余额
        'compensationOverdueFee': '',  # 代偿罚息
        'guaranteeMerchantId': '',  # 担保商户号
    },

    # 自牧云创回购文件 键值对字典数据模板
    "ZMYCBuyBackTemple": {
        'loan_no': '',  # 借据号
        'name': '',  # 姓名
        'cer_no': '',  # 身份证号
        'current_period': '',  # 期次
        'repay_amt': '',  # 代偿总额
        'repay_date': '',  # 代偿日期
        'business_no': '',  # 流水号
        'product_id': '',  # 产品号
        'type_flag': '1',  # 类型标志
        'loan_amt': '',  # 贷款总金额
        'loan_period': '',  # 贷款总期次
        'loan_date': '',  # 放款时间
        'paid_prin_amt': '',  # 本金
        'paid_int_amt': '',  # 利息
        'left_repay_amt': '',  # 在贷余额
        'compensationOverdueFee': '',  # 代偿罚息
        'guaranteeMerchantId': '',  # 担保商户号
    },
    # H5还款
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
                "loanInvoiceId": "",  # 借据号
                "channelNo": "6",  # 主动还款渠道
                "repayType": "0",  # 还款方式 0-按期还款   1-提前还款
                "paymentType": "5",  # 支付类型1-支付宝-主动还款 2-支付宝-代扣 3-微信-主动还款 4-微信-代扣 5-银行卡-主动还款 6-银行卡-代扣   7-云闪付-主动还款
                "periods": "1",  # 还款期数 多期以,分隔
                "repayAmt": 212.46,  # 还款金额
                "appOrderNo": "",  # 还款订单流水号
                "settleStatus": "0",  # 结清标识 EnumBool 0 未结清  1 结清
                "payPlatformCode": "zhifubianhao",  # 支付平台编号
                "aliPayViewUrl": "https://www.baidu.com/",  # 支付平台编号
                "idNo": "451123198311190587",  # 身份证号（银行卡还款必须）
                "phoneNum": "18908989867",  # 用户银行卡绑定手机号（银行卡还款必须）
                "bankAcctName": "楚东进",  # 还款人姓名（银行卡还款必须）
                "bankName": "0102",  # 银行编号（银行卡还款必须）
                "bankAcctNo": "6212810833868379081",  # 还款人银行卡卡号（银行卡还款必须）
                "deviceInfo": "设备信息1.21sxf",  # 设备信息（微信还款必须）
                "wxPayViewUrl": "https://www.baidu.com/",  # 传值外网可以访问的地址（微信还款必须）
                "createIp": "10.12.255.0",  # ip（微信还款必须）,
                "paymentOrderNo": ""  # H5订单号 H5还款必传
            }
        }
    }
}
