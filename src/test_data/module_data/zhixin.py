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
            "requestNo": "361920480915sssss",
            "requestTime": "1523619204809",
            "partner": "F21E041",
            "version": "1.0",
            "input": {
                "md5": "${手机号+身份证号}",  # md5 值
                "mode": "MI",
            }
        }
    },

    # 绑卡请求鉴权
    'applyCertification': {
        'interface': '/api/v1/zhixin/bind/applyCertification',
        'payload': {
            "requestNo": "361920480915sssss",
            "requestTime": "1523619204809",
            "partner": "F21E041",
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
        }
    },
    # 验证鉴权验证码
    'verifyCode': {
        'interface': '/api/v1/zhixin/bind/verifyCode',
        'payload': {
            "requestNo": "361920480915sssss",
            "requestTime": "1523619204809",
            "partner": "F21E041",
            "version": "1.0",
            "input": {
                "userId": "${userId}",  # 用户ID： 必填
                "certificationApplyNo": "${certificationApplyNo}",  # 申请单号:同绑卡请求申请流水号  必填
                "cdKey": "${cdKey}",  # 短信流水号：绑卡请求返回流水号 必填
                "verificationCode": "111111"  # 验证码： 必填
            }
        }
    },

    # 授信申请
    'applyCredit': {
        'interface': '/api/v1/zhixin/credit/applyCredit',
        'payload': {
            "requestNo": "361920480915sssss",
            "requestTime": "1523619204809",
            "partner": "F21E041",
            "version": "1.0",
            "input": {
                "userId": "${userId}",  # 用户ID： 必填
                "creditApplyNo": "${creditApplyNo}",  # 申请单号:每次请求都重新生成唯一流水号  必填
                "applyTime": "${applyTime}",  # 申请时间：yyyyMMddHHmmss
                "productCode": "F21E041",  # 产品编号：锦城提供
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
                    "workUnit": "工作单位地址成都莆田街133号-4-5",  # 工作单位地址
                    "addrDetail": "家庭地址成都莆田街133号-4-5"  # 家庭地址
                },
                "idCardOcrInfo": {
                    "positive": "身份证正面Base64字符串",  # 身份证正面照片：图片文件转 Base64 字符串
                    "negative": "身份证反面Base64字符串",  # 身份证反面照片：图片文件转 Base64 字符串
                    "nameOCR": "姓名（OCR）",  # 姓名（OCR）
                    "idCardNoOCR": "20",  # 身份证号码（OCR）
                    "beginTimeOCR": "19900101",  # 身份证有效期开始时间（OCR）yyyyMMdd
                    "duetimeOCR": "20300101",  # 身 份 证 有 效 期（OCR）  有效期最后一天，如 20200921或长期
                    "addressOCR": "身份证地址成都莆田街133号-4-5",  # 身份证地址（OCR）
                    "sexOCR": "1",  # 性别（OCR）
                    "ethnicOCR": "汉",  # 民族（OCR）
                    "issueOrgOCR": "乌兹别克族"  # 签发机关（OCR）
                },
                "faceInfo": {
                    "assayTime": "yyyyMMddHHmmss",  # 活体信息采集时间：yyyyMMddHHmmss
                    "assayType": "FACEAA",  # 活体来源  采集 SDK，为 face++或商汤FACEAA:face++SENSETIME:商汤
                    "best": "活体图Base64 字符串",  # 最佳照片  图片文件转 Base64 字符串
                    "action1": "动作图1Base64字符串",  # 每个动作截取的照片
                    "action2": "动作图2Base64字符串",  # 身每个动作截取的照片
                    "action3": "动作图3Base64字符串",  # 每个动作截取的照片
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
                    "isRoot": "Y",  # 是否 root Y:是 N：否 或空
                    "isEmulator": "Y",  # 是否模拟器 Y:是 N：否 或空
                    "networkType": "wifi",  # 网络状态  wifi/4g/3g/2g
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
                "agreementTime": "yyyyMMddHHmmss",  # 借款相关协议签署时间 yyyyMMddHHmmss
            }
        }
    },

    # 审核结果通知
    'noticeCreditResult': {
        'interface': '/api/v1/zhixin/credit/noticeCreditResult',
        'payload': {
            "requestNo": "957d00bd-6bcc-40b8-b59f-46067ae93c5e",
            "requestTime": "1523619204809",
            "partner": "F21E041",
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
            "requestNo": "361920480915sssss",
            "requestTime": "1523619204809",
            "partner": "F21E041",
            "version": "1.0",
            "input": {
                "userId": "${userId}",  # 用户ID： 必填
                "creditApplyNo": "${creditApplyNo}"  # 申请单号  必填
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
