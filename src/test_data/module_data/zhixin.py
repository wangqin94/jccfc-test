# # ---------------------------------------------------------
# # - 项目特性配置文件
# # - created time: 2021-10-21
# # - version: 1.1
# # ---------------------------------------------------------

# -----------------------------------------------------------
# 360智信期项目配置
# -----------------------------------------------------------
zhixin = {
    # 加密接口
    'encrypt': {
        'interface': '/api/v1/zhixin/demo/encrypt',
    },

    # 解密接口
    'decrypt': {
        'interface': '/api/v1/zhixin/demo/decrypt',
    },

    # 黑名单撞库
    'checkUser': {
        'interface': '/api/v1/zhixin/creditCheckUser/checkUser',
        'payload': {
            'data': {
                "requestNo": "361920480915sssss",
                "requestTime": "1523619204809",
                "partner": "ICE_JCXJ",
                "version": "1.0",
                "input": {
                    "md5": "${手机号}",  # md5 值
                    "mode": "M",
                }
            },
            "method": "checkUser",
            "partner": "ICE_JCXJ",
            "encFlag": "Y",
            "encType": "DES",
            "cmp": "N",
            "ct": "1523619204809"
        }
    },

    # 绑卡请求鉴权
    'applyCertification': {
        'interface': '/api/v1/zhixin/bind/applyCertification',
        'payload': {
            'data': {
                "requestNo": "361920480915sssss",
                "requestTime": "1523619204809",
                "partner": "ICE_JCXJ",
                "version": "1.0",
                "input": {
                    "userId": "${userId}",  # 用户ID： 必填
                    "certificationApplyNo": "${certificationApplyNo}",  # 申请单号:每次请求都重新生成唯一流水号  必填
                    "bankCode": "0001",  # 银行编号:0001 中国银行;0002 农业银行;0003 工商银行;0004 建设银行;0005 交通银行;
                    # 0006 光大银行;0007 民生银行;0008 平安银行;0009 邮储银行;0010 广发银行;0011 中信银行;0012 华夏银行;
                    # 0013 浦发银行;0014 兴业银行;0015 招商银行;0017 杭州银行;0018 上海银行;0019 北京银行  必填
                    "idCardNo": "${身份证号}",  # 用户ID： 必填
                    "userMobile": "${手机号}",  # 用户ID： 必填
                    "userName": "${姓名}",  # 用户ID： 必填
                    "bankCardNo": "${银行卡号}",  # 用户ID： 必填
                    "agreementTime": "${yyyyMMddHHmmss}",  # 绑卡相关协议签署时间:yyyyMMddHHmmss  必填
                    "certificationCode": ""  # 鉴权代码:授信环节为空借款环节回传 3.3.1 借款试算 输出参数鉴权代码还款环节回传 3.4.1 还款试算 输出参数鉴权代码
                }
            },
            "method": "applyCertification",
            "partner": "ICE_JCXJ",
            "encFlag": "Y",
            "encType": "DES",
            "cmp": "Y",
            "ct": "1523619204809"
        }
    },
    # 验证鉴权验证码
    'verifyCode': {
        'interface': '/api/v1/zhixin/bind/verifyCode',
        'payload': {
            'data': {
                "requestNo": "361920480915sssss",
                "requestTime": "1523619204809",
                "partner": "ICE_JCXJ",
                "version": "1.0",
                "input": {
                    "userId": "${userId}",  # 用户ID： 必填
                    "certificationApplyNo": "${certificationApplyNo}",  # 申请单号:同绑卡请求申请流水号  必填
                    "cdKey": "${cdKey}",  # 短信流水号：绑卡请求返回流水号 必填
                    "verificationCode": "111111"  # 验证码： 必填
                }
            },
            "method": "verifyCode",
            "partner": "ICE_JCXJ",
            "encFlag": "Y",
            "encType": "DES",
            "cmp": "N",
            "ct": "1523619204809"
        }
    },

    # 授信申请
    'applyCredit': {
        'interface': '/api/v1/zhixin/credit/applyCredit',
        'payload': {
            'data': {
                "requestNo": "361920480915sssss",
                "requestTime": "1523619204809",
                "partner": "ICE_JCXJ",
                "version": "1.0",
                "input": {
                    "userId": "${userId}",  # 用户ID： 必填
                    "creditApplyNo": "${creditApplyNo}",  # 申请单号:每次请求都重新生成唯一流水号  必填
                    "applyTime": "${applyTime}",  # 申请时间：yyyyMMddHHmmss
                    "productCode": "ICE_JCXJ",  # 产品编号：锦城提供
                    "userInfo": {
                        "mobile": "手机号",  # 用户注册手机号
                        "name": "姓名",  # 姓名
                        "idCardNo": "身份证号",  # 身份证号
                        "marriage": "20",  # 婚姻状态  枚举值见MarriageEnum
                        "monthlyIncome": "1",  # 收入级别  枚举值见MonthlyIncomeEnum
                        "education": "20",  # 受教育程度 枚举值见EducationEnum
                        "school": "四川大学",  # 学校
                        "job": "1",  # 职业信息 枚举值见JopEnum
                        "province": "510000",  # 省份代码
                        "city": "510100",  # 城市代码
                        "district": "510107",  # 区代码
                        "workUnit": "华西精神病研究研究",  # 工作单位
                        "workAddr": "工作单位地址成都莆田街133号-4-5",  # 工作单位地址
                        "addrDetail": "家庭地址成都市武侯区莆田街133号-4-5"  # 家庭地址
                    },
                    "linkmanInfo": {
                        "relationshipA": "10",  # 紧急联系人A关系 枚举值见RelationshipEnum
                        "nameA": "联系人张三",  # 直接取自用户通讯录，可能出现数字，字母及特殊字符
                        "phoneA": "15884431111",  # 电话
                        "relationshipB": "20",  # 紧急联系人A关系 枚举值见RelationshipEnum
                        "nameB": "联系人李四",  # 直接取自用户通讯录，可能出现数字，字母及特殊字符
                        "phoneB": "15884431112",  # 电话
                    },
                    "bankCardInfo": {
                        "bankCode": "0001",  # 银行编码 枚举值见BankCodeEnum
                        "idCardNo": "身份证号",  # 身份证号
                        "userMobile": "手机号",  # 银行预留手机号
                        "userName": "姓名",  # 姓名
                        "bankCardNo": "银行卡号"  # 银行卡号
                    },
                    "deviceInfo": {
                        "imei": "imei354717043143933",  # serialNo 手机序列号,全球唯一  异常时默认为(\)
                        "deviceOs": "ANDROID",  # 操作系统类型 IOS/ANDROID
                        "deviceOsVersion": "iPhone OS 3.0（build 7a341）",  # 操作系统版本
                        "deviceIp": "101.101.101.101.1",  # 终端 IP
                        "imsi": "imsi354717043143933",  # IMSI( 国 际 移 动 用户识别码)  ios 拿不到用的 idfa安卓 Q 拿不到，异常时默认为空(null 或"")
                        "isRoot": "N",  # 是否 root Y:是 N：否 或空
                        "isEmulator": "N",  # 是否模拟器 Y:是 N：否 或空
                        "networkType": "4g",  # 网络状态  wifi/4g/3g/2g
                        "wifiMac": "03:03:30:3A:3B:3C",  # 手机 mac
                        "wifiName": "WIFI 名称",  # WIFI 名称
                        "bssid": "B3:93:9D:36:48:5E",  # 路由 MAC
                        "brand": "Nokia",  # 品牌
                        "model": "Nokia X6",  # 型号
                        "factoryTime": "1634873802",  # 出厂时间  时间戳
                        "deviceName": "S0GV8YASA1",  # 设备名称
                        "buildSerial": "GP6V0GT6T3HV"  # 设备序列号
                    },
                    "geoInfo": {
                        "latitude": "46.82745798052434",  # 维度
                        "longitude": "127.12782734275143"  # 经度
                    },
                    "idCardOcrInfo": {
                        "nameOCR": "姓名（OCR）",  # 姓名（OCR）
                        "idCardNoOCR": "20",  # 身份证号码（OCR）
                        "beginTimeOCR": "19900101",  # 身份证有效期开始时间（OCR）yyyyMMdd
                        "duetimeOCR": "20300101",  # 身 份 证 有 效 期（OCR）  有效期最后一天，如 20200921或长期
                        "addressOCR": "身份证地址成都莆田街133号-4-5",  # 身份证地址（OCR）
                        "sexOCR": "M",  # 性别（OCR）
                        "ethnicOCR": "汉",  # 民族（OCR）
                        "issueOrgOCR": "乌兹别克族",  # 签发机关（OCR）
                        "positive": "身份证正面Base64字符串",  # 身份证正面照片：图片文件转 Base64 字符串
                        "negative": "身份证反面Base64字符串"  # 身份证反面照片：图片文件转 Base64 字符串
                    },
                    "faceInfo": {
                        "assayTime": "yyyyMMddHHmmss",  # 活体信息采集时间：yyyyMMddHHmmss
                        "assayType": "FACEAA",  # 活体来源  采集 SDK，为 face++或商汤FACEAA:face++SENSETIME:商汤
                        "best": "活体图Base64 字符串",  # 最佳照片  图片文件转 Base64 字符串
                        "action1": "动作图1Base64字符串",  # 每个动作截取的照片
                        "action2": "动作图2Base64字符串",  # 身每个动作截取的照片
                        "action3": "动作图3Base64字符串",  # 每个动作截取的照片
                    },
                    "agreementTime": "yyyyMMddHHmmss",  # 借款相关协议签署时间 yyyyMMddHHmmss
                }
            },
            "method": "applyCredit",
            "partner": "ICE_JCXJ",
            "encFlag": "Y",
            "encType": "DES",
            "cmp": "Y",
            "ct": "1523619204809"
        }
    },

    # 审核结果通知
    'noticeCreditResult': {
        'interface': '/api/v1/zhixin/credit/noticeCreditResult',
        'payload': {
            "requestNo": "957d00bd-6bcc-40b8-b59f-46067ae93c5e",
            "requestTime": "1523619204809",
            "partner": "ICE_JCXJ",
            "version": "1.0",
            "input": {
                "userId": "${userId}",  # 用户ID： 必填
                "creditApplyNo": "${creditApplyNo}",  # 申请单号 必填
                "partnerCreditNo": "${合作方申请单号}",  # 合作方内部申请单号 必填
                "status": "S",  # 状态： 枚举值见StatusEnum
                "statusTime": "${userId}",  # 审核状态时间： yyyyMMddHHmmss
                "resultCode": "",  # 结果码  失败或拒绝时，必填
                "resultMsg": "",  # 结果描述
                "rejectPeriod": "365",  # 拒绝时效  审批拒绝，多少天内不能再申请
                "creditInfo": "${cdKey}",  # 短信流水号：绑卡请求返回流水号 必填
                "productInfoList": "111111"  # 验证码： 必填
            }
        }
    },

    # 审核结果查询
    'queryCreditResult': {
        'interface': '/api/v1/zhixin/credit/queryCreditResult',
        'payload': {
            'data': {
                "requestNo": "361920480915sssss",
                "requestTime": "1523619204809",
                "partner": "ICE_JCXJ",
                "version": "1.0",
                "input": {
                    "userId": "${userId}",  # 用户ID： 必填
                    "creditApplyNo": "${creditApplyNo}"  # 申请单号  必填
                }
            },
            "method": "queryCreditResult",
            "partner": "ICE_JCXJ",
            "encFlag": "Y",
            "encType": "DES",
            "cmp": "N",
            "ct": "1523619204809"
        }
    },

    # 借款试算
    'loanTrial': {
        'interface': '/api/v1/zhixin/loan/loanTrial',
        'payload': {
            "data": {
                "requestNo": "361920480915sssss",
                "requestTime": "1523619204809",
                "partner": "ICE_JCXJ",
                "version": "1.0",
                "input": {
                    "userId": "${userId}",  # 用户ID： 必填
                    "loanApplyNo": "${loanApplyNo}",  # 申请单号  必填
                    "loanTime": "yyyyMMddHHmmss",  # 提现时间 格式：yyyyMMddHHmmss
                    "partnerCreditNo": "${partnerCreditNo}",  # 合作方内部授信申请单号
                    "productCode": "F21E041",
                    "loanAmt": "3000",  # 提现金额
                    "loanPurpose": "05",  # 贷款用途
                    "term": "6",  # 贷款周期
                    "repayMethod": "01",
                },
                "bankCardInfo": {
                    "bankCode": "0001",  # 银行编号
                    "idCardNo": "身份证号",  # 身份证号
                    "userMobile": "手机号",  # 手机号
                    "userName": "姓名",  # 姓名
                    "bankCardNo": "银行卡号"  # 银行卡号
                },
            },
            "method": "loanTrial",
            "partner": "ICE_JCXJ",
            "encFlag": "Y",
            "encType": "DES",
            "cmp": "N",
            "ct": "1523619204809"

        }
    },

    # 借款申请
    'applyLoan': {
        'interface': '/api/v1/zhixin/loan/applyLoan',
        'payload': {
            "data": {
                "requestNo": "361920480915sssss",
                "requestTime": "1523619204809",
                "partner": "ICE_JCXJ",
                "version": "1.0",
                "input": {
                    "userId": "${userId}",  # 用户ID
                    "loanApplyNo": "${loanApplyNo}",  # 申请单号
                    "loanTime": "${loanTime}",
                    "partnerCreditNo": "${partnerCreditNo}",  # 授信号
                    "productCode": "F21E041",
                    "loanAmt": "3000",  # 提现金额
                    "loanPurpose": "02",
                    "term": "6",
                    "repayMethod": "01",
                    "agreementTime": "yyyyMMddHHmmss",
                    "bankCardInfo": {
                        "bankCode": "0001",  # 银行编号
                        "idCardNo": "身份证",  # 身份证号
                        "userMobile": "手机号",  # 手机号
                        "userName": "姓名",  # 姓名
                        "bankCardNo": "银行卡号",  # 银行卡号
                    },
                    "idCardOcrInfo": {
                        "nameOCR": "姓名（OCR）",  # 姓名（OCR）
                        "idCardNoOCR": "20",  # 身份证号码（OCR）
                        "beginTimeOCR": "20140212",  # 身份证有效期开始时间（OCR）yyyyMMdd
                        "duetimeOCR": "20240212",  # 身 份 证 有 效 期（OCR）  有效期最后一天，如 20200921或长期
                        "addressOCR": "身份证地址成都莆田街133号-4-5",  # 身份证地址（OCR）
                        "sexOCR": "M",  # 性别（OCR）
                        "ethnicOCR": "汉",  # 民族（OCR）
                        "issueOrgOCR": "发证机关：国务院999号",  # 签发机关（OCR）
                        "positive": "身份证正面Base64字符串",  # 身份证正面照片：图片文件转 Base64 字符串
                        "negative": "身份证反面Base64字符串",  # 身份证反面照片：图片文件转 Base64 字符串
                    },
                    "geoInfo": {
                        "latitude": "17.0914633",
                        "longitude": "21.150069",
                    },
                },
            },
            "method": "applyLoan",
            "partner": "ICE_JCXJ",
            "encFlag": "Y",
            "encType": "DES",
            "cmp": "N",
            "ct": "1523619204809"
        },
    },

    # 借款结果查询
    "queryLoanResult": {
        'interface': '/api/v1/zhixin/loan/queryLoanResult',
        'payload': {
            "data": {
                "requestNo": "361920480915sssss",
                "requestTime": "1523619204809",
                "partner": "ICE_JCXJ",
                "version": "1.0",
                "input": {
                    "userId": "${userId}",
                    "loanApplyNo": "${loanApplyNo}"
                },
            },
            "method": "queryLoanResult",
            "partner": "ICE_JCXJ",
            "encFlag": "Y",
            "encType": "DES",
            "cmp": "N",
            "ct": "1523619204809"
        },
    },

    # 借据&还款计划查询
    "queryLoanPlan": {
        'interface': '/api/v1/zhixin/repay/queryLoanPlan',
        'payload': {
            "data": {
                "requestNo": "361920480915sssss",
                "requestTime": "1523619204809",
                "partner": "ICE_JCXJ",
                "version": "1.0",
                "input": {
                    "userId": "${userId}",
                    "loanApplyNo": "${loanApplyNo}",
                    "partnerLoanNo": "${partnerLoanNo}",  # 合作方借据呈
                },
            },
            "method": "queryLoanPlan",
            "partner": "ICE_JCXJ",
            "encFlag": "Y",
            "encType": "DES",
            "cmp": "N",
            "ct": "1523619204809"
        },
    },

    # 还款试算
    'repayTrial': {
        'interface': '/api/v1/zhixin/repay/repayTrial',
        'payload': {
            'data': {
                "requestNo": "361920480915sssss",
                "requestTime": "1523619204809",
                "partner": "ICE_JCXJ",
                "version": "1.0",
                "input": {
                    "userId": "${userId}",  # 用户ID： 必填
                    "repayApplyNo": "${creditApplyNo}",  # 申请单号  必填
                    "loanApplyNo": "${loanApplyNo}",  # 智信引擎借款申请单号  必填
                    "partnerLoanNo": "${partnerLoanNo}",  # 合作方内部借款申请单号  必填
                    "repayType": "1",  # 还款类型 1 按期还款 2 提前结清3 按金额还款按期还款时，需合作方自行计算还款期次。用户无法在前端选择特定期次还款。  必填
                    "repayTime": "${repayTime}",  # 还款时间 格式：yyyyMMddHHmmss  必填
                    "repayAmt": "${repayAmt}",  # 还款金额  按金额还款时有值,其他还款类型没有还款金额 选填
                }
            },
            "method": "repayTrial",
            "partner": "ICE_JCXJ",
            "encFlag": "Y",
            "encType": "DES",
            "cmp": "N",
            "ct": "1523619204809"
        }
    },

    # 还款申请
    'applyRepayment': {
        'interface': '/api/v1/zhixin/repay/applyRepayment',
        'payload': {
            'data': {
                "requestNo": "361920480915sssss",
                "requestTime": "1523619204809",
                "partner": "ICE_JCXJ",
                "version": "1.0",
                "input": {
                    "userId": "${userId}",  # 用户ID： 必填
                    "repayApplyNo": "${creditApplyNo}",  # 申请单号  必填
                    "loanApplyNo": "${loanApplyNo}",  # 智信引擎借款申请单号  必填
                    "partnerLoanNo": "${partnerLoanNo}",  # 合作方内部借款申请单号  必填
                    "repayType": "${repayType}",  # 还款类型 1 按期还款 2 提前结清3 按金额还款按期还款时，需合作方自行计算还款期次。用户无法在前端选择特定期次还款。  必填
                    "repayTime": "${repayTime}",  # 还款时间 格式：yyyyMMddHHmmss  必填
                    "repayAmt": "${repayAmt}",  # 还款金额  按金额还款时有值,其他还款类型没有还款金额 选填
                    "withholdFlag": "Y",  # Y:合作方扣款N:合作方不扣款，由智信引擎代扣 必填
                    "bankCardInfo": {
                        "bankCode": "0001",  # 银行编码 枚举值见BankCodeEnum
                        "idCardNo": "身份证号",  # 身份证号
                        "userMobile": "手机号",  # 银行预留手机号
                        "userName": "姓名",  # 姓名
                        "bankCardNo": "银行卡号"  # 银行卡号
                    },
                }
            },
            "method": "applyRepayment",
            "partner": "ICE_JCXJ",
            "encFlag": "Y",
            "encType": "DES",
            "cmp": "N",
            "ct": "1523619204809"
        }
    },

    # 还款结果查询
    'queryRepayResult': {
        'interface': '/api/v1/zhixin/repay/queryRepayResult',
        'payload': {
            'data': {
                "requestNo": "361920480915sssss",
                "requestTime": "1523619204809",
                "partner": "ICE_JCXJ",
                "version": "1.0",
                "input": {
                    "userId": "${userId}",  # 用户ID： 必填
                    "repayApplyNo": "${repayApplyNo}"  # 申请单号  必填
                }
            },
            "method": "queryRepayResult",
            "partner": "ICE_JCXJ",
            "encFlag": "Y",
            "encType": "DES",
            "cmp": "N",
            "ct": "1523619204809"
        }
    },

    # 信用评估申请
    'applyQFICO': {
        'interface': '/api/v1/zhixin/qfico/apply',
        'payload': {
            "applyId": "000CA2021111700000007",   # 锦城授信/支用申请单号
            "qficoApplyNo": "1000",  # 智信请求流水号
            "name": "1000",
            "mobile": "1000",
            "idCardNo": "1000",
            "type": "credit",  # credit-授信 loan-借款
            "businessNo": "1000",   # 智信授信/支用申请单号
            "pumaInfo": "{\"partnerFlowId\":\"28947c4d45e94e6680f5d40fecd4dd52\",\"responseCode\":\"S000\",\"responseMsg\":\"成功\",\"resultJsons\":\"[{\\\"consumeScore\\\":\\\"1.1\\\",\\\"pbocScoreDzXgModel\\\":\\\"0.49359607696533203\\\",\\\"pbocScoreFlag\\\":\\\"1\\\",\\\"workScore\\\":\\\"4197.8448997\\\",\\\"loyalScore\\\":\\\"1.1\\\",\\\"prepayScore\\\":\\\"4890.3221087\\\",\\\"creditLineFromBank\\\":\\\"0.50862|5286.78331|2266.03264\\\",\\\"model2Score\\\":\\\"4990.1578447\\\",\\\"debtScore\\\":\\\"1.1\\\",\\\"pbocScoreLongtermXgModel\\\":\\\"0.9804129600524902\\\",\\\"behaviorScoreFromBank\\\":\\\"57.0|\\\",\\\"salaryFromBank2\\\":\\\"2564.78059\\\",\\\"fraudScore\\\":\\\"4996.9535747\\\",\\\"rhFlagFromBank\\\":\\\"1|0\\\",\\\"strategyBranchFromBank\\\":\\\"\\\",\\\"useRateScoreFromBank\\\":\\\"3.28|7.23|-3.44|11.06\\\",\\\"resultFromBank\\\":\\\"A\\\",\\\"ruleScore\\\":\\\"5854.7\\\",\\\"modelScore\\\":\\\"6332.985347\\\",\\\"modelName\\\":\\\"{\\\\\\\"master\\\\\\\":\\\\\\\"Y\\\\\\\",\\\\\\\"modelName\\\\\\\":\\\\\\\"人行端规则\\\\\\\",\\\\\\\"version\\\\\\\":\\\\\\\"1906300014\\\\\\\"}\\\",\\\"loanScore\\\":\\\"4180.9681197\\\",\\\"debtScoreFromBank\\\":540.0,\\\"salaryScoreFromBank\\\":5833.47727,\\\"qualityScoreFromBank\\\":2.0,\\\"creditScoreFromBank\\\":\\\"44.0|2.781|0.1773\\\",\\\"model3Score\\\":\\\"4569.7849277\\\",\\\"pbocScoreSyXgModel\\\":\\\"0.7147897481918335\\\"}]\",\"serialId\":\"SARN0305871555\"}"
        }
    },

    # 信用评估结果查询
    'queryQFICO': {
        'interface': '/api/v1/zhixin/qfico/query',
        'payload': {
            "qficoApplyNo": "1000",  # 智信请求流水号
        }
    },

    # 额度&产品查询
    'queryCreditProduct': {
        'interface': '/api/v1/zhixin/product/queryCreditProduct',
        'payload': {
            "data": {
                "requestNo": "361920480915sssss",
                "requestTime": "1523619204809",
                "partner": "ICE_JCXJ",
                "version": "1.0",
                "input": {
                    "userId": "${userId}",
                    "creditApplyNo": "${creditApplyNo}",   # 智信引擎申请单号
                    "partnerCreditNo": "${partnerCreditNo}",  # 合作方申请单号
                },
            },
            "method": "queryLoanPlan",
            "partner": "ICE_JCXJ",
            "encFlag": "Y",
            "encType": "DES",
            "cmp": "N",
            "ct": "1523619204809"
        },
    },
}
