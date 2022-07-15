jiebei = {
    # 特征取数
    'feature': {
        'interface': "/api/v1/antjb/featureservice/decision_feature",
        'payload': {
            "applyNo": "applyNo1111111111118",  # 业务单号   是
            "featureCodes": ["JC_cs_result","JC_cs_failCode","JC_cs_failReason"] ,  # 特征编码列表                   是
            "appCode": "TIANCHENG",  # 请求来源默认“TIANCHENG”     是
            "idInfo": "",                   #     否
            "bizActionType": "",  # 申请类型，只区分支用场景  申请类型，⽀⽤“LOAN_DECISION”
            "extra": {
                "externalUrl": "http://127.0.0.1:8080/featureservice/fetch_feature",  # 特征取数地址
                "tracerId": "ac10006e1631929521814100729836",
                "orgExtraParams": {             #json格式，借呗⽀⽤场景有值
                    "userName": "",  # 客户姓名
                    "certNo": "",  # 证件号码
                    "loanUse": "",  # 贷款用途
                    "encashAmt": "",  # 放款金额
                    "dayRate": "",  # 贷款日利率，借呗业务有值
                    "creditNo": ""  # 授信编号
                    }
                }
            }
    },

    # 数据准备-初审
    "datapreCs": {
        "interface": "/api/v1/antjb/featureservicefeatureservice/init_feature",
        "payload": {
            "applyNo": "",  # 业务单号，主要用于整合一笔业务的所有数据
            "dataType": "JC_cs_credit",  # 数据类型
            "customParams": {
                "applyType":  "",  # 业务类型   授信ADMIT_APPLY；提额ADJUST_AMT_APPLY
                "applyExpiredDate":  "",  # 申请过期时间
                "certNo": "",  # 证件号码
                "certType": "",  # 证件类型
                "certValidEndDate": "",  # 证件有效期
                "name": "",  # 申请⼈姓名
                "mobileNo": "",  # 申请⼈⼿机号
            },  # 自定义
            "signType": "",  # 签名类型 RSA2
            "sign": ""  # 签名结果
        }

    },

    # 数据准备-复审
    "datapreFs": {
        "interface": "/api/v1/antjb/featureservicefeatureservice/init_feature",
        "payload": {
            "applyNo": "",  # 业务单号，主要用于整合一笔业务的所有数据
            "dataType": "JC_fs_credit",  # 数据类型
            "customParams": {     # 自定义
                "creditNo": "",
                "applyType": "",
                "name": "",
                "certNo": "",
                "certType": "",
                "mobileNo": "",
                "TC_NoSource_ToPlatformOne": "",
                "certValidEndDate": "",
                "bankCardInfo":{
                    "cardNo": "",
                    "bankName": "",
                    "cardType": "",
                    "bankReservedMobileNo": ""
                },
                "Adress": {
                    "prov": "",
                    "provCode": "",
                    "city": "",
                    "cityCode": "",
                    "area": "",
                    "areaCode": "",
                    "address": ""
                },
                "suggestAmtMax": "",
                "suggestAmtMin": "",
                "suggestRateMax": "",
                "suggestRateMin": "",
                "extInfo": ""
                             },
            "signType": "",  # 签名类型 RSA2
            "sign": ""  # 签名结果
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
                "certType": "",  # 证件类型
                "certValidEndDate": "",  # 证件有效期
                "name": "",  # 申请⼈姓名
                "mobileNo": "",  # 申请⼈⼿机号
            },  # 自定义
            "signType": "",  # 签名类型 RSA2
            "sign": ""  # 签名结果
        }

    }



}