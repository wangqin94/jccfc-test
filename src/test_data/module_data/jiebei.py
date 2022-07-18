jiebei = {
    # 特征取数
    'feature': {
        'interface': "/api/v1/antjb/featureservice/decision_feature",
        'payload': {
            "applyNo": "",  # 业务单号   是
            "featureCodes": ["JC_cs_result","JC_cs_failCode","JC_cs_failReason","JC_cs_failReason"] ,  # 特征编码列表      是
            "appCode": "TIANCHENG",  # 请求来源默认“TIANCHENG”     是
            "idInfo": {
                "USER_ID": "1111",
                "BIZ_NO": "1111",
                "ID_CARD": "1111"
                },                   #     否
            "bizActionType": "",  # 申请类型，只区分支用场景  申请类型，⽀⽤“LOAN_DECISION”  JC_CS  JC_FS
            "extra": {
                "externalUrl": "http://127.0.0.1:8080/featureservice/fetch_feature",  # 特征取数地址
                "tracerId": "ac10006e1631929521814100729836",
                "orgExtraParams": {             #json格式，借呗⽀⽤场景有值
                    "userName": "",  # 客户姓名
                    "certNo": "",  # 证件号码
                    "loanUse": "",  # 贷款用途   1 2 3 4 5 6
                    "encashAmt": "",  # 放款金额
                    "dayRate": "",  # 贷款日利率，借呗业务有值
                    "creditNo": ""  # 授信编号
                    }
                }
            }
    },

    # 数据准备-初审
    'datapreCs': {
        'interface': "/api/v1/antjb/featureservice/init_feature",
        'payload': {
            "applyNo": "applyNo1111111111119",  # 业务单号，主要用于整合一笔业务的所有数据
            "dataType": "JC_CS",  # 数据类型
            "customParams": {
                "applyType":  "ADMIT_APPLY",  # 业务类型   授信ADMIT_APPLY；提额ADJUST_AMT_APPLY
                "applyExpiredDate":  "2018-05-02 11:12:00",  # 申请过期时间
                "certNo": "",  # 证件号码
                "certType": "01",  # 证件类型
                "certValidEndDate": "2022-12-02 11:12:00",  # 证件有效期
                "name": "",  # 申请⼈姓名
                "mobileNo": "",  # 申请⼈⼿机号
            },  # 自定义
            "signType": "RSA2",  # 签名类型 RSA2
            "sign": "12312"  # 签名结果
        }

    },

    # 数据准备-复审
    "datapreFs": {
        "interface": "/api/v1/antjb/featureservice/init_feature",
        "payload": {
            "applyNo": "",  # 业务单号，主要用于整合一笔业务的所有数据
            "dataType": "JC_FS",  # 数据类型
            "customParams": {     # 自定义
                "creditNo": "",           #授信编号
                "applyType": "",          #业务类型 授信ADMIT_APPLY；提额ADJUST_AMT_APPLY
                "name": "",               #
                "certNo": "",
                "certType": "",
                "mobileNo": "",
                "TC_NoSource_ToPlatformOne": "",  #二转一或征信标  Y-查征信、N-不查征信
                "certValidEndDate": "",           #证件有效期
                "bankCardInfo":{
                    "cardNo": "",
                    "bankName": "",
                    "cardType": "DC",                #卡类型枚举，目前只支持借记卡（枚举：DC）
                    "bankReservedMobileNo": ""     #银⾏预留⼿机号
                },
                "Adress": {
                    "prov": "浙江省",               #省份
                    "provCode": "330000",          # 省编码
                    "city": "杭州市",
                    "cityCode": "330100",
                    "area": "⻄湖区",
                    "areaCode": "330106",
                    "address": "浙江省-杭州市-⻄湖区-学院路128号-A1座12"
                },
                "suggestAmtMax": "",    #基础固额建议上限      单位:分
                "suggestAmtMin": "",    #基础固额建议下限      单位:分
                "suggestRateMax": "",    #建议日利率上限
                "suggestRateMin": "",       #建议日利率下限
                "extInfo": ""               #预留字段Json
                             },
            "signType": "RSA2",  # 签名类型 RSA2
            "sign": "123214324"  # 签名结果
        }
    },
    # 授信通知接口
    "creditNotice": {
        "interface": "/api/v1/antjb/notice/noticeCreditResult",
        "payload": {
            "applyNo": "",  # 业务单号，主要用于整合一笔业务的所有数据
            "dataType": "JC_cs_credit",  # 数据类型
            "customParams": {
                "applyType": "",  # 业务类型
                "applyExpiredDate": "",  # 申请过期时间
                "certNo": "",  # 证件号码
                "certType": "01",  # 证件类型
                "certValidEndDate": "",  # 证件有效期
                "name": "",  # 申请⼈姓名
                "mobileNo": "",  # 申请⼈⼿机号
            },  # 自定义
            "signType": "RSA2",  # 签名类型 RSA2
            "sign": ""  # 签名结果
        }

    }



}