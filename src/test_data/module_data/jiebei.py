jiebei = {
    # 特征取数
    'feature': {
        'interface': "/api/v1/antjb/featureservice/decision_feature",
        'payload': {
            "applyNo": "",  # 业务单号   是
            "featureCodes": ["jc_loan_result", "jc_loan_failCode", "jc_loan_failReason"],  # 特征编码列表      是
            "appCode": "TIANCHENG",  # 请求来源默认“TIANCHENG”     是
            # "idInfo": {
            #     "USER_ID": "1111",
            #     "BIZ_NO": "1111",
            #     "ID_CARD": "1111"
            #     },                   #     否
            "bizActionType": "",  # 申请类型，只区分支用场景  申请类型，⽀⽤“LOAN_DECISION”  JC_CS  JC_FS
            "extra": {
                "externalUrl": "http://127.0.0.1:8080/featureservice/fetch_feature",  # 特征取数地址
                "tracerId": "ac10006e1631929521814100729836",
                "orgExtraParams": {  # json格式，借呗⽀⽤场景有值
                    "userName": "",  # 客户姓名
                    "certNo": "",  # 证件号码
                    "loanUse": "1",  # 贷款用途   1 2 3 4 5 6
                    "encashAmt": "100000",  # 放款金额
                    "dayRate": "0.0006",  # 贷款日利率，借呗业务有值
                    "creditNo": ""  # 授信编号
                }
            }
        }
    },

    # 数据准备-初审
    'datapreCs': {
        'interface': "/api/v1/antjb/featureservice/init_feature",
        'payload': {
            "customParams": {
                "applyType": "ADMIT_APPLY",
                "certNo": "513700199705225552",
                "certType": "01",
                "certValidEndDate": "2029-12-02 11:12:00",
                "name": "鲁南春",
                "mobileNo": "18754870269",
                "applyExpiredDate": "2023-08-30 11:12:00"
            },
            "applyNo": "applyNo202208160000000000000002",
            "dataType": "JC_CS",
            # "signType": "RSA2",  # 签名类型 RSA2
            "sign": "uFHGmGfOuOhkKQgQ13Cf3Mkc4upV4pv1AfAVYJB3ybZ6A1CmHGFAN782D3BrGz/im/OlHmO0ZTBnzTLUjHfAfkKTO4tXUJCt2/ws/WdEmR6KMl7PfykN1e68kWQ3z2jKaFZLYz2K1kMz86EcayXQnwW5mjhBzX3rJC6JmXsVWg9I6t0s4fb/qJ97jYf0U13dubqDJBJbmLE61wpdqcMQu9coZtCr4rx7XhpU7/YOdn+/CINOvsfbkjPA4eSdvVcJ7LbuK+B8m9ve76s9r8ITvbFHHJ1y6eRZHcYv/4W9tJlWrfUlLDKvtWEYNC1EKmywf6802t5bC5/uooNxh73PaQ=="
        }
    },

    # 数据准备-复审
    "datapreFs": {
        "interface": "/api/v1/antjb/featureservice/init_feature",
        "payload": {
            "applyNo": "2022081100200000000100792S",
            "dataType": "JC_FS",
            "customParams": {
                "applyType": "ADJUST_AMT_APPLY",  # 授信ADMIT_APPLY；提额ADJUST_AMT_APPLY；降额DECREASE_AMT_APPLY
                "certType": "01",
                "address": "{\"area\":\"浦东新区\",\"areaCode\":\"310115\",\"address\":\"5LiK5rW35LiK5rW35biC5rWm5Lic5paw5Yy65LiK5rW3LeS4iua1t+W4gi3mtabkuJzmlrDljLot6ZmG5a625Zi06KGX6YGT5oGS55Sf6ZO26KGM5aSn5Y6mMzXmpbzmgZLnlJ/pk7booYw=\",\"provCode\":\"310000\",\"city\":\"上海市\",\"cityCode\":\"310100\",\"prov\":\"上海市\"}",
                "mobileNo": "13547359285",
                "certNo": "34298719870021647X",
                "bankCardInfo": "{\"cardType\":\"DC\",\"bankReservedMobileNo\":\"13173671201\",\"bankName\":\"招商银行\",\"cardNo\":\"123456789101110\"}",
                "suggestAmtMax": "2000000",
                "suggestRateMax": "0.00015",
                "name": "张三",
                "suggestAmtMin": "2000000",
                "suggestRateMin": "0.00015",
                "creditNo": "2022081100200000000100792S",
                "certValidEndDate": "2029-12-02 11:12:00",
                "tc_NoSource_ToPlatformOne": "N",  # Y就是一期的新客，N就是二转一的老客
                # "extInfo": {
                #     "reason": ""
                #     # 发起申请原因  借呗产品 且 降额或调价时有值  HIGH_RISK_SCORE较高风险用户  LOW_RISK_SCORE较低风险用户 AUDIT_KSCZ人工客诉处置
                # }
            },  # 自定义
            # "signType": "RSA2",  # 签名类型 RSA2
            "sign": "YEjsLnpe6H44gR0exMp6kEDG7ZCpqiez0Np5aIUcc2S+12koFrNs7nO9moAIF8fMqApMPmaFIOG4IromyR/7h/gxxFC5f6HrMlO87sh66FHGwkzgXuCfnmZdfckHY0JJFJ8I14t6/HhAjUFECTCthffej0+YvgcFXxufOJUZPl6Hg6mSQ874NFrGrYcTkpwvuRO/yrdTOdf5B0J63F0fCKt5a5W9mwXRGu6N9R32KafoUJwNSRgsqHUWDjapAf5pSW+egxtW8wYh8jW7GnEwIXJhLutUrreMugGNZ9n2eDKKT9+U92+9C9vCdzCBX5Yjihw4mCcwO3FhubYA0wBL1Q\u003d\u003d"
            # 签名结果
        }
    },
    # 授信通知接口
    "creditNotice": {
        "interface": "/api/v1/antjb/notice/noticeCreditResult",
        "payload": {
            "applyNo": "",  # 业务单号，主要用于整合一笔业务的所有数据
            "appCode": "galaxy",  # 请求来源
            "productCode": "JB",  #
            "timestamp": 16581463654314747,  # 时间戳
            "extInfo": {
                "applyNo": "",
                "name": "",  # 申请⼈姓名
                "certValidEndDate": "2022-12-02 11:12:00",  # 证件有效期  /长期
                "certNo": "",  # 证件号码
                "certType": "01",  # 证件类型
                "bizMode": "PLATFORM_1",
                "bizType": "ADJUST_AMT_APPLY",
                # ADMIT_APPLY授信申请 LOAN_APPLY支用申请 ADJUST_AMT_APPLY提额申请 DECREASE_AMT_APPLY降额申请 ADJUST_RATE_APPLY提价申请 DECREASE_RATE_APPLY降价申请
                "mobile": "",
                "toPlatformOne": "",  # 授信场景时有值
                "agreeFlag": "Y",  # 授信结果
                "creditAmt": 5000000,  # 额度的单位是『分』,  授信/调额时有值
                "creditRate": 0.0006,  # 利率单位是 『⽇利率』  授信/调价时有值
                "creditRateLimit": 1,  # 授信利率上限 网商贷产品 且 授信通过时有值
                "creditRateBottom": 2,  # 授信利率下限 网商贷产品 且 授信通过时有值
                "unAdmReasons": "",  # 拒绝码   外部资产拒绝时有值
                "unAdmMng": "",  # 拒绝码中文解释  外部资产拒绝时有值
                "reason": "AUDIT_KSCZ"
                # 发起申请原因  借呗产品 且 降额或调价时有值  HIGH_RISK_SCORE较高风险用户  LOW_RISK_SCORE较低风险用户 AUDIT_KSCZ人工客诉处置

            },  # 自定义
            # "signType": "RSA2",  # 签名类型 RSA2
            "sign": "123"  # 签名结果
        }

    }

}
