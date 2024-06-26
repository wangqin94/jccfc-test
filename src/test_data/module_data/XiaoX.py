# # ---------------------------------------------------------
# # - 项目特性配置文件
# # - created time: 2021-03-06
# # - version: 1.1
# # ---------------------------------------------------------

# -----------------------------------------------------------
# 即科项目配置
# -----------------------------------------------------------
XiaoX = {
    # 加密接口-小象
    'encrypt': {
        'interface': '/api/v1/yinliu/secret/thirdEncryptData/G23E01XIAX',
    },

    # 解密接口
    'decrypt': {
        'interface': '/api/v1/yinliu/secret/thirdDecryptData',
    },
    # 代扣签约申请接口
    'getCardRealNameMessage': {
        'interface': '/api/v1/yl/common/getCardRealNameMessage',
        'payload': {
            "head": {
                "merchantId": "G23E01XIAX",
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
            }
        }
    },
    # 确认代扣签约接口
    'bindCardRealName': {
        'interface': '/api/v1/yl/common/bindCardRealName',
        'payload': {
            "head": {
                "merchantId": "G23E01XIAX",
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
                "merchantId": "G23E01XIAX",
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
                "merchantId": "G23E01XIAX",
                "channelNo": "01",
                "requestSerialNo": "cqrn20210415155213618",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000"
            },
            "body": {
                "thirdApplyId": "",  # 三方授信申请编号  与放款申请编号保持一致
                "thirdApplyTime": "",  # 客户三方申请时间  yyyyMMddHHmmss ，老核心要求渠道必传
                "repayType": "1",  # 还款方式  EnumRepayMethod
                "orderType": "1",  # 订单类型  固定传1-取现
                "goodsName": "取现借款",  # 商品名称  取现为：取现借款、分期购物为：商品名称
                "interestRate": 9.5,  # 年化利率(百分比，比如 17.56 表示 17.56%)
                "custInterestRate": 24.00,  # 对客实际利率 (百分比，比如 17.56 表示 17.56%)
                "userBankCardNo": "",  # 用户银行卡号
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
                "idExpiryDate": "1990.1.1-2029.01.23",  # 身份证有效期 1990.1.1-2099.12.31（长期传2099.12.31）
                "issuingAuth": "成都高新派出所",  # 发证机关
                "idCardAddrAddress": "四川省成都市高新区天府四街OCG写字楼A座",  # 身份证地址
                "idCardAddrProvinceCode": "510000",  # 身份证地址省份代码
                "idCardAddrProvinceName": "四川省",  # 身份证地址省份名称
                "idCardAddrCityCode": "510100",  # 身份证地址市级代码
                "idCardAddrCityName": "成都市",  # 身份证地址市级名称
                "idCardAddrAreaCode": "510107",  # 身份证地址区代码
                "idCardAddrAreaName": "武侯区",  # 身份证地址区名称
                "loanPurpose": "1",  # 贷款用途 EnumLoanPurpose
                "compName": "单位名称",  # 单位名称
                "compPhone": "13812345689",  # 单位电话
                "workTime": 1000,  # 在现工作单位时间 单位：月
                "workStatus": 'F',  # 工作状态 EnumWorkStatus
                "userOccupation": "0",  # 职业 EnumVocationType
                "duties": "A",  # 职务 EnumPost
                "companyNature": "A",  # 单位性质 EnumUnitProperty
                "industryCategory": "A",  # 行业类别 EnumIndustryType
                "workAddrAddress": "北京市海淀医院",  # 工作详细地址
                "workAddrProvinceName": "北京市",  # 工作地址省份名称
                "workAddrProvinceCode": "110000",  # 工作地址省份代码
                "workAddrCityName": "北京市",  # 工作地址市级名称
                "workAddrCityCode": "110100",  # 工作地址市级代码
                "workAddrAreaName": "海淀区",  # 工作地址区名称
                "workAddrAreaCode": "110108",  # 工作地址区代码
                "liveAddress": "北京市海淀医院",  # 工作详细地址
                "liveProvinceName": "北京市",  # 居住地址省份名称
                "liveProvinceCode": "110000",  # 居住地址省份代码
                "liveCityName": "北京市",  # 居住地址市级名称
                "liveCityCode": "110100",  # 居住地址市级代码
                "liveAreaName": "海淀区",  # 居住地址区名称
                "liveAreaCode": "110108",  # 居住地址区代码
                # "liveAddress": "新疆科技学院(东校区)",  # 工作详细地址
                # "liveProvinceName": "新疆维吾尔自治区",  # 居住地址省份名称
                # "liveProvinceCode": "650000",  # 居住地址省份代码
                # "liveCityName": "巴音郭楞蒙古自治州",  # 居住地址市级名称
                # "liveCityCode": "652800",  # 居住地址市级代码
                # "liveAreaName": "库尔勒市",  # 居住地址区名称
                # "liveAreaCode": "652801",  # 居住地址区代码
                "applyAmount": 1000,  # 申请金额 元
                "monthIncome": 1000,  # 月收入  元
                "familyMonthIncome":10000,  # 家庭月收入  元
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
                        "fileUrl": "xdgl/xiax/test/cqid1.png",
                        "fileName": "cqid1.png"
                    },
                    {
                        "fileType": "2",  # 身份证反面
                        "fileUrl": "xdgl/xiax/test/cqid2.png",
                        "fileName": "cqid2.png"
                    },
                    {
                        "fileType": "3",  # 人脸
                        "fileUrl": "xdgl/xiax/test/cqface.png",
                        "fileName": "cqface.png"
                    },
                    {
                        "fileType": "4",  # 征信查询授权书
                        "fileUrl": "xdgl/jike/test/credit.pdf",
                        "fileName": "credit.pdf"
                    },
                    {
                        "fileType": "7",  # 三方查询授权书
                        "fileUrl": "xdgl/jike/test/third.pdf",
                        "fileName": "third.pdf"
                    },
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
                    # "quaternCerReqTime": "20210101 141010",  # 非必填 四元认证请求时间
                    # "quaternCerRspTime": "20210101 151010",  # 非必填 四元认证响应时间
                    # "quaternCerRst": "四元认证结果"  # 非必填 四元认证结果
                },
                "featureField": {
                    "livingTime": "20200828171641",  # 人脸识别时间
                    "livingDetectionScore": "Y",  # xx活体识别活体检测结果
                    "livingComparisonScore": "Y",  # xx活体识别照片比对结果
                    "faceCertificationResult": "1",  # 人脸公安验证结果  1-通过/0-未通过
                    "faceDistinguishState": "Y",  # 人脸识别状态
                    "isPassVerified": "Y",  # 是否通过公安网实名认证  Y/N
                    "riskscorelevel": "1",  # 天启反欺诈  1-是/0-否
                    "queryinterval": "N",  # 同盾多头等级  N~E
                    "userlevel": "1",  # 小象优质客户标签  1-是/0-否
                    "similarity": "1",  # face++人脸识别结果  1-通过/0-未通过
                    "riskblacklist": "1",  # 天启黑名单  1-命中/0-未命中
                    "blacklist": "1",  # 致诚黑名单  1-命中/0-未命中
                    "cloudrcLevel": "A",  # 小象信用分  评级A -E：好-差
                }
            }
        }

    },
    # 授信申请结果查询
    'credit_query': {
        'interface': '/api/v1/yl/common/credit/queryResult',
        'payload': {
            "head": {
                "merchantId": "G23E01XIAX",
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
                "merchantId": "G23E01XIAX",
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
                "loanTerm": 6,  # 贷款期数
                "name": "",  # 借款人姓名
                "idNo": "",  # 证件号码
                "mobileNo": "0102",  # 手机号码
                "reserveMobile": "",  # 银行预留手机号
                "orderType": "1",  # 订单类型  固定传1-取现
                "interestRate": 9.5,  # 年化利率(百分比，比如 17.56 表示 17.56%)
                "custInterestRate": 24.00,  # 对客实际利率 (百分比，比如 17.56 表示 17.56%)
                "repayType": "1",  # 还款方式  EnumRepayMethod
                "accountNo": "",  # 放款/还款银行卡号
                "bankName": "工商银行",  # 还款银行名称
                "loanPurpose": "1",  # 贷款用途 EnumLoanPurpose
                "guaranteeContractNo": "",  # 担保合同号
                "fileInfos": [
                    {
                        "fileType": "9",
                        "fileUrl": "xdgl/xiax/test/loancontract.pdf",
                        "fileName": "loancontract.pdf"
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
                }
            }
        }

    },
    # 放款申请结果查询
    'loan_query': {
        'interface': '/api/v1/yl/common/loan/queryResult',
        'payload': {
            "head": {
                "merchantId": "G23E01XIAX",
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
                "merchantId": "G23E01XIAX",
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
                "merchantId": "G23E01XIAX",
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
                "merchantId": "G23E01XIAX",
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
                "merchantId": "G23E01XIAX",
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
                "merchantId": "G23E01XIAX",
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
                "merchantId": "G23E01XIAX",
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
                "merchantId": "G23E01XIAX",
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
                "merchantId": "G23E01XIAX",
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
                "merchantId": "G23E01XIAX",
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
                "merchantId": "G23E01XIAX",
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
}
