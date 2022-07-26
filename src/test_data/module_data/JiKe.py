# # ---------------------------------------------------------
# # - 项目特性配置文件
# # - created time: 2021-03-06
# # - version: 1.1
# # ---------------------------------------------------------

# -----------------------------------------------------------
# 即科项目配置
# -----------------------------------------------------------
JiKe = {
    # 加密接口
    'encrypt': {
        'interface': '/api/v1/yinliu/secret/thirdEncryptData/G22E02JIKE',
    },

    # 解密接口
    'decrypt': {
        'interface': '/api/v1/yinliu/secret/thirdDecryptData',
    },
    # 代扣申请接口
    'sharedWithholdingAgreement': {
        'interface': '/api/v1/jike/common/sharedWithholdingAgreement',
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
                "payerPhoneNum": "",  # 付款方银行卡预留手机号
                "payerIdNum": "",  # 付款方身份证号
                "payerBankCardNum": "",  # 付款方银行卡号
                "payerBankCode": "0102",  # 付款方银行编号
                "aggrementNum": "",  # 代扣协议号
                "payChannel": "1010",  # 支付通道  固定传1010-宝付协议支付渠道
            }
        }
    },
    # 代扣申请结果查询
    'queryWithholdingAgreement': {
        'interface': '/api/v1/jike/common/queryWithholdingAgreement',
        'payload': {
            "head": {
                "merchantId": "G22E02JIKE",
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
    # 换卡通知接口
    'updateWithholdCard': {
        'interface': '/api/v1/jike/common/queryWithholdingAgreement',
        'payload': {
            "head": {
                "merchantId": "G22E02JIKE",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "loanInvoiceId": "",  # 资金方放款编号
                "idNo": "",  # 证件号码
                "repaymentAccountNo": ""  # 新银行卡号
            }
        }
    },
    # 授信请求接口
    'credit_apply': {
        'interface': '/api/v1/jike/credit/apply',
        'payload': {
            "head": {
                "merchantId": "G22E02JIKE",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "thirdApplyId": "",  # 三方授信申请编号  与放款申请编号保持一致
                "repayType": "1",  # 还款方式  EnumRepayMethod
                "orderType": "2",  # 订单类型  固定传2-赊销(分期购物)
                "goodsName": "美容贷",  # 商品名称  取现为：取现借款、分期购物为：商品名称
                "interestRate": 23.4,  # 年化利率(百分比，比如 17.56 表示 17.56%)
                "custInterestRate": 24.00,  # 对客实际利率 (百分比，比如 17.56 表示 17.56%)
                "userBankCardNo": "0102",  # 用户银行卡号
                "bankCode": "0102",  # 银行编码
                "reserveMobile": "",  # 银行预留手机号
                "loanTerm": 12,  # 贷款期数
                "name": "",  # 借款人姓名
                "idNo": "",  # 证件号码
                "sex": "1",  # 性别  UNKNOWN("0", "未知的性别"),MALE("1", "男"),FEMALE("2", "女"),NOT_EXPLAINED("9", "未说明的性别");
                "mobileNo": "手机号码",  # 手机号码
                "education": "11",  # 学历 EnumEduLevel
                "maritalStatus": "20",  # 婚姻状态 EnumMarriageStatus，若已婚，则联系人需含配偶
                "nation": "汉",  # 民族
                "idExpiryDate": "1990.1.1-2099.12.31",  # 身份证有效期 1990.1.1-2099.12.31（长期传2099.12.31）
                "idCardAddr": "四川省成都市高新区天府三街",  # 身份证地址
                "issuingAuth": "成都高新派出所",  # 发证机关
                "loanPurpose": "4",  # 贷款用途 EnumLoanPurpose
                "compName": "单位名称",  # 单位名称
                "compPhone": "13812345689",  # 单位电话
                "workTime": 1000,  # 在现工作单位时间 单位：月
                "workStatus": 'F',  # 工作状态 EnumWorkStatus
                "userOccupation": "0",  # 职业 EnumVocationType
                "duties": "A",  # 职务 EnumPost
                "companyNature": "A",  # 单位性质 EnumUnitProperty
                "industryCategory": "A",  # 行业类别 EnumIndustryType
                "workAddrAddress": "工作单位地址成都市武侯区中航城市广场",  # 工作详细地址
                "workAddrProvinceName": "四川",  # 工作地址省份名称
                "workAddrCityName": "成都",  # 工作地址市级名称
                "workAddrAreaName": "武侯区",  # 工作地址区名称
                "liveAddress": "居住地址成都市武侯区中航城市广场",  # 工作详细地址
                "liveProvinceName": "四川",  # 居住地址省份名称
                "liveCityName": "成都",  # 居住地址市级名称
                "liveAreaName": "武侯区",  # 居住地址区名称
                "applyAmount": 1000,  # 申请金额 元
                "monthIncome": 1000,  # 月收入  元
                "storeCode": "H22A02ZHZX",  # 门店代码
                "goodsCategory1": "商品大分类",  # 商品大分类
                "goodsCategory2": "商品小分类",  # 商品小分类
                "contactRelationList": [
                    {
                        "contactName": "配偶姓名",  # 联系人姓名
                        "contactMobile": "13912345689",  # 联系人电话
                        "contactRel": "2",  # 联系人关系 EnumRelationType
                    },
                ],
                "fileInfos": [
                    {
                        "fileType": "1",
                        "fileUrl": "http://jccfc-huat.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/fql/yw/idcard_front_202000000948071964.jpg",
                        "fileName": "idcard_front_202000000948071964.jpg"
                    },
                    {
                        "fileType": "2",
                        "fileUrl": "http://jccfc-huat.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/fql/yw/idcard_back_202000000948071964.jpg",
                        "fileName": "idcard_back_202000000948071964.jpg"
                    },
                    {
                        "fileType": "3",
                        "fileUrl": "http://jccfc-huat.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/fql/yw/face_distinguish_202000000948071964.jpg",
                        "fileName": "face_distinguish_202000000948071964.jpg"
                    },
                    {
                        "fileType": "4",
                        "fileUrl": "http://jccfc-huat.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/fql/yw/JC_userauth_202000000948071964.pdf",
                        "fileName": "JC_userauth_202000000948071964.pdf"
                    },
                    {
                        "fileType": "6",
                        "fileUrl": "http://jccfc-huat.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/fql/yw/JC_non_student_202000000948071964.pdf",
                        "fileName": "JC_non_student_202000000948071964.pdf"
                    },
                    {
                        "fileType": "7",
                        "fileUrl": "http://jccfc-huat.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/fql/yw/JC_third_auth_202000000948071964.pdf",
                        "fileName": "JC_third_auth_202000000948071964.pdf"
                    }
                ],
                "authenticationInfo": {
                    "appRegistraDate": "20210101 101010",  # App注册时间
                    "policeApproveSupplier": "公安认证认证供应商",  # 公安认证认证供应商
                    "policeApproveNum": "公安认证客户认证交易号",  # 公安认证客户认证交易号
                    "policeApproveReqTime": "20210101 101010",  # 公安认证认证请求时间
                    "policeApproveRspTime": "20210101 111010",  # 公安认证认证结果返回时间
                    "policeApproveRst": "公安认证认证结果",  # 公安认证认证结果
                    "livingBodySupplier": "活体识别认证供应商",  # 活体识别认证供应商
                    "livingBodyNum": "活体识别客户认证交易号",  # 活体识别客户认证交易号
                    "livingBodyReqTime": "20210101 121010",  # 活体识别认证请求时间
                    "livingBodyRspTime": "20210101 131010",  # 活体识别认证结果返回时间
                    "livingBodyRst": "公安认证认证结果",  # 活体识别认证结果
                    "quaternCerReqTime": "20210101 141010",  # 四元认证请求时间
                    "quaternCerRspTime": "20210101 151010",  # 四元认证响应时间
                    "quaternCerRst": "四元认证结果"  # 四元认证结果
                },
                "featureField": {
                    "shieldNumber": 9999,  # 近三个月同盾贷款数
                    "shieldMonthLoan": 9999,  # 近一个月同盾贷款数
                    "shieldWeekLoan": 9999,  # 近7天同盾贷款数
                    "whiteKnightBlacklist_xd": "N",  # 白骑士黑名单-信贷 Y 中标(名单中存在) N 未中标（名单中不存在）
                    "collectionNumber": 9999,  # 凭安-近期被催收的号码个数
                    "thawingScore": 9999,  # 百融-线下消费贷客群评分
                    "whiteKnightBlacklist_xyxf": "N",  # 白骑士黑名单-信用消费 Y 中标(名单中存在) N 未中标（名单中不存在）
                    "whiteKnightBlacklist_p2p": "N",  # 白骑士黑名单-P2P Y 中标(名单中存在) N 未中标（名单中不存在）
                    "faceValues": 9999,  # 人脸识别分数
                }
            }
        }

    },
    # 授信申请结果查询
    'credit_query': {
        'interface': '/api/v1/yl/common/credit/queryResult',
        'payload': {
            "head": {
                "merchantId": "G22E02JIKE",
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
    # 放款请求接口
    'loan_apply': {
        'interface': '/api/v1/yl/common/loan/apply',
        'payload': {
            "head": {
                "merchantId": "G22E02JIKE",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "thirdApplyId": "",  # 放款申请编号  与授信申请编号保持一致
                "loanAmt": 1000,  # 借款金额
                "firstRepayDate": "",  # 首期还款日期 yyyy-MM-dd
                "fixedRepayDay": "",  # 固定还款日  例：3，就是每月的3号,取值范围0-28，若29、30、31日放款，传28
                "loanTerm": 12,  # 贷款期数
                "name": "",  # 借款人姓名
                "idNo": "",  # 证件号码
                "mobileNo": "0102",  # 手机号码
                "reserveMobile": "",  # 银行预留手机号
                "orderType": "2",  # 订单类型  固定传2-赊销(分期购物)
                "interestRate": 23.4,  # 年化利率(百分比，比如 17.56 表示 17.56%)
                "custInterestRate": 24.00,  # 对客实际利率 (百分比，比如 17.56 表示 17.56%)
                "repayType": "1",  # 还款方式  EnumRepayMethod
                "accountNo": "",  # 放款/还款银行卡号
                "bankName": "工商银行",  # 还款银行名称
                "loanPurpose": "4",  # 贷款用途 EnumLoanPurpose
                "guaranteeContractNo": "",  # 担保合同号
                "fileInfos": [
                    {
                        "fileType": "9",
                        "fileUrl": "http://jccfc-huat.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/fql/yw/idcard_danbaohetong_202000000948071964.jpg",
                        "fileName": "idcard_danbaohetong_202000000948071964.jpg"
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
                "featureField": {
                    "shieldNumber": 9999,  # 近三个月同盾贷款数
                    "shieldMonthLoan": 9999,  # 近一个月同盾贷款数
                    "shieldWeekLoan": 9999,  # 近7天同盾贷款数
                    "whiteKnightBlacklist_xd": "N",  # 白骑士黑名单-信贷 Y 中标(名单中存在) N 未中标（名单中不存在）
                    "collectionNumber": 9999,  # 凭安-近期被催收的号码个数
                    "thawingScore": 9999,  # 百融-线下消费贷客群评分
                    "whiteKnightBlacklist_xyxf": "N",  # 白骑士黑名单-信用消费 Y 中标(名单中存在) N 未中标（名单中不存在）
                    "whiteKnightBlacklist_p2p": "N",  # 白骑士黑名单-P2P Y 中标(名单中存在) N 未中标（名单中不存在）
                    "faceValues": 9999,  # 人脸识别分数
                }
            }
        }

    },
    # 放款申请结果查询
    'loan_query': {
        'interface': '/api/v1/yl/common/loan/queryResult',
        'payload': {
            "head": {
                "merchantId": "G22E02JIKE",
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
                "merchantId": "G22E02JIKE",
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
                "merchantId": "G22E02JIKE",
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

    # 还款通知接口
    'repay_apply': {
        'interface': '/api/v1/yl/common/repay/uniteRepay',
        'payload': {
            "head": {
                "merchantId": "G22E02JIKE",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "repayScene": "01",    # 还款场景 EnumRepayScene REPAY_ONLINE("01", "线上还款"),REPAY_OFFLINE("02", "线下还款"),ALIPAY_NOTICE（"04","支付宝还款通知"）OVERDUE_NOTICE（"05","逾期（代偿、回购后）还款通知"）
                "repayApplySerialNo": "6",  # 还款申请流水号 每笔还款申请流水号唯一，支付宝还款传支付宝扣款订单号
                "thirdWithholdId": "",  # 三方代扣编号 线下还款、逾期还款通知：传机构代扣编号；支付宝还款通知：传支付宝扣款订单号；其他还款场景不传
                "appAuthToken": "6",  # 支付宝授权令牌 支付宝还款通知必传
                "loanInvoiceId": "",  # 资金方放款编号 放款成功后返回的资金方借据编号
                "repaymentAccountNo": "6",  # 还款账号 线上还款必填
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
                "merchantId": "G22E02JIKE",
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

    # 退货申请查询
    'returnGoods_apply': {
        'interface': '/api/v1/yl/common/returnGoods/apply',
        'payload': {
            "head": {
                "merchantId": "G22E02JIKE",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "loanInvoiceId": "",  # 资金方放款编号
                "returnGoodsSerialNo": "",  # 退货申请流水号  每一笔退货申请唯一
                "returnGoodsPrincipal": 0,  # 退货总本金
                "returnGoodsInterest": 0,  # 退货总利息
                "returnGoodsOverdueFee": 0,  # 退货罚息
            }
        }
    },

    # 附件补录
    'supplementAttachment': {
        'interface': '/api/v1/yl/common/supplementAttachment',
        'payload': {
            "head": {
                "merchantId": "G22E02JIKE",
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
                "merchantId": "G22E02JIKE",
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
                "merchantId": "G22E02JIKE",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
            }
        }
    },

}
