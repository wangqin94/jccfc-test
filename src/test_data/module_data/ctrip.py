# # ---------------------------------------------------------
# # - 项目特性配置文件
# # - created time: 2021-03-06
# # - version: 1.1
# # ---------------------------------------------------------

# -----------------------------------------------------------
# 携程项目配置
# -----------------------------------------------------------
ctrip = {
    'pre_credit': {
        'interface': '/api/v1/ctrip/demo/trade',
        'payload': {
            "open_id": "6ReW_21${applyId}",
            "user_name": "${姓名}",
            "id_no": "${身份证号}",
            "bank_bind_mobile": "${手机号}",
            "card_no": "${银行卡号}",
            "request_no": "REAct29${applyId}",
            "service_version": "1.0",
            "product_no": "cash",
            "partner": "JCXFCASH",
            "advice_amount": "${act_amount}",
            "service": "PRE_CREDIT",
            "id_type": "IDENTITYCARD",
            "user_data": {
                "Platform": {
                    "education": "0.1581,0.0862,0.7070,0.0487",
                    "customerStickiness": "优质",
                    "institutionType": "microCredit",
                    "loanAppRating2": "1",
                    "loanAppRating": None,
                    "login_period": "0.1978,0.1626,0.1930,0.3240,0.1226",
                    "rest_regular": "96.5241",
                    "creditRating": "优质",
                    "flight_airport_tendency": "0.1429,0.1429,0.7143",
                    "car_prob": "0.9122",
                    "family_prob": None,
                    "pbocQuery": "N",
                    "city_stable": "0.3855",
                    "house_prob": "0.6531",
                    "odc_prob": "0.9999",
                    "student_prob": "0.3788",
                    "order_platform": "0.0164,0.5410,0.0492",
                    "vacation_day_desire": "13.0231",
                    "price_sensitive": "35",
                    "card_no": "6212263803010024333",
                    "pay_type": "微信支付:0.05,支付宝支付:0.05,Q端其他:0.03,常用卡借记卡:0.81",
                    "mobileInfo": None,
                    "whole_power": "100",
                    "destination_tendency": "0.1111,0.1111,0.4889,0.7111,0.5556,0.1333",
                    "creditMode": "PA",
                    "plan_prob": "71",
                    "consumer_stability": "0",
                    "RM0001": "0",
                    "RM0002": "L",
                    "RM0003": "0",
                    "RM0004": "0",
                    "RM0005": "0",
                    "RM0006": "0",
                    "RM0007": "0",
                    "RM0008": "0",
                    "RM0009": "0",
                    "RM0010": "0",
                    "RM1001": "0",
                    "RM1002": "0",
                    "RM1003": "0",
                    "RM1004": "0",
                    "RM1005": "0",
                    "RM1006": "0",
                    "RM1007": "0",
                    "RM1008": "0",
                    "RM1009": "0",
                    "RM1010": "0",
                    "RM1011": "0",
                    "RM1012": "0",
                    "RM1013": "0",
                    "RM1014": "0",
                    "RM1015": "0",
                    "RM1016": "0",
                    "RM1017": "0",
                    "RM1018": "0",
                    "RM1019": "0",
                    "RM1020": "0",
                    "RM1021": "0",
                    "RM1022": "1",
                    "RM1023": "0",
                    "RM1024": "0",
                    "RM1025": "1",
                    "occupation": "生意人/个体户",
                    "qualification": "大学本科",
                    "id_no": "${身份证号}",
                    "personIncome": "10-20万元",
                    # "idcard_ocr_addr": "成都市武侯区府城大道中段88号",
                    "idcard_ocr_addr": "成都市武侯区府城大道中段88号",
                    "idcard_ocr_gender": "M",
                    # "identity_card_image_1": "5db0ea08059aa2955d005ac830510e6c",
                    # "identity_card_image_2": "40d72516c9dd84bc75a0a73306250369",
                    # "face_image": "62c2fbf32b931c0b62250c2beba18860",
                    "nationality": "Chinese",
                    "contact_relate": "配偶",
                    "user_name": "${姓名}",
                    "contacts_mobile": "15210120098",
                    "id_type": "IDENTITYCARD",
                    "idcard_ocr_validity": "2019.06.08-2029.06.08",
                    "contact_name": "数据流二",
                    "mobile": "${手机号}",
                    "identity_card_image_1": "/xdgl/ctrip/test/wymid1.png",
                    "identity_card_image_2": "/xdgl/ctrip/test/wymid2.png",
                    "face_image": "/xdgl/ctrip/test/wymface.png"
                }
            },
            "advice_rate_type": "${advice_rate_type}",
            "advice_rate": {
                "ECI": {
                    "3": "0.36"
                }
            }

        }
    },
    'credit': {
        'interface': '/api/v1/ctrip/demo/trade',
        'payload': {
            "open_id": "6ReW_21${applyId}",
            "user_name": "${姓名}",
            "id_no": "${身份证号}",
            "bank_bind_mobile": "${手机号}",
            "card_no": "${银行卡号}",
            "request_no": "REAct29${applyId}",
            "service_version": "1.0",
            "product_no": "cash",
            "partner": "JCXFCASH",
            "advice_amount": "${act_amount}",
            "service": "CREDIT",
            "id_type": "IDENTITYCARD",
            "user_data": {
                "Platform": {
                    "education": "0.1581,0.0862,0.7070,0.0487",
                    "customerStickiness": "优质",
                    "institutionType": "microCredit",
                    "loanAppRating2": "1",
                    "loanAppRating": None,
                    "login_period": "0.1978,0.1626,0.1930,0.3240,0.1226",
                    "rest_regular": "96.5241",
                    "creditRating": "优质",
                    "flight_airport_tendency": "0.1429,0.1429,0.7143",
                    "car_prob": "0.9122",
                    "family_prob": None,
                    "pbocQuery": "N",
                    "city_stable": "0.3855",
                    "house_prob": "0.6531",
                    "odc_prob": "0.9999",
                    "student_prob": "0.3788",
                    "order_platform": "0.0164,0.5410,0.0492",
                    "vacation_day_desire": "13.0231",
                    "price_sensitive": "35",
                    "card_no": "6212263803010024333",
                    "pay_type": "微信支付:0.05,支付宝支付:0.05,Q端其他:0.03,常用卡借记卡:0.81",
                    "mobileInfo": None,
                    "whole_power": "100",
                    "destination_tendency": "0.1111,0.1111,0.4889,0.7111,0.5556,0.1333",
                    "creditMode": "PA",
                    "plan_prob": "71",
                    "consumer_stability": "0",
                    "RM0001": "0",
                    "RM0002": "L",
                    "RM0003": "0",
                    "RM0004": "0",
                    "RM0005": "0",
                    "RM0006": "0",
                    "RM0007": "0",
                    "RM0008": "0",
                    "RM0009": "0",
                    "RM0010": "0",
                    "RM1001": "0",
                    "RM1002": "0",
                    "RM1003": "0",
                    "RM1004": "0",
                    "RM1005": "0",
                    "RM1006": "0",
                    "RM1007": "0",
                    "RM1008": "0",
                    "RM1009": "0",
                    "RM1010": "0",
                    "RM1011": "0",
                    "RM1012": "0",
                    "RM1013": "0",
                    "RM1014": "0",
                    "RM1015": "0",
                    "RM1016": "0",
                    "RM1017": "0",
                    "RM1018": "0",
                    "RM1019": "0",
                    "RM1020": "0",
                    "RM1021": "0",
                    "RM1022": "1",
                    "RM1023": "0",
                    "RM1024": "0",
                    "RM1025": "1",
                    "occupation": "生意人/个体户",
                    "qualification": "大学本科",
                    "id_no": "${身份证号}",
                    "personIncome": "10-20万元",
                    # "idcard_ocr_addr": "成都市武侯区府城大道中段88号",
                    "idcard_ocr_addr": "成都市武侯区府城大道中段88号",
                    "idcard_ocr_gender": "M",
                    # "identity_card_image_1": "5db0ea08059aa2955d005ac830510e6c",
                    # "identity_card_image_2": "40d72516c9dd84bc75a0a73306250369",
                    # "face_image": "62c2fbf32b931c0b62250c2beba18860",
                    "nationality": "Chinese",
                    "contact_relate": "配偶",
                    "user_name": "${姓名}",
                    "contacts_mobile": "15210120098",
                    "id_type": "IDENTITYCARD",
                    "idcard_ocr_validity": "2019.06.08-2029.06.08",
                    "contact_name": "数据流二",
                    "mobile": "${手机号}",
                    "identity_card_image_1": "/xdgl/ctrip/test/gysid1.png",
                    "identity_card_image_2": "/xdgl/ctrip/test/gysid2.png",
                    "face_image": "/xdgl/ctrip/test/gysface.png"
                }
            },
            "advice_rate_type": "${advice_rate_type}",
            "advice_rate": {
                "ECI": {
                    "3": "0.24"
                }
            }

        }
    },

    'loan': {
        'interface': '/api/v1/ctrip/demo/trade',
        'payload': {
            "open_id": "6ReW_21${applyId}",
            "request_no": "Loan_2021R${applyId}",
            "loan_no": "Loan_2021L${applyId}",
            "loan_amount": "${loan_amount}",
            "service_version": "1.0",
            "loan_user_type": "1",
            "product_no": "cash",
            "loan_purpose": "装修",
            "loan_rate": "0.00035000",
            "partner_id": None,
            "partner": "ZY_SNCASH",
            "card_no": "${银行卡号}",
            "bank_no": "CCB",
            "first_repay_date": "${__time(YMD,)}113538",
            "service": "LOAN_CASH",
            "term": "3",
            "bank_bind_mobile": "${手机号}",
            "repay_type": "ECI",
            "extend_param": {
                "idcard_ocr_validity": "2020.04.27-2040.04.27",
                "idcard_ocr_addr": "成都市武侯区府城大道中段88号",
                "idcard_ocr_gender": "M",
                "occupation": "1",
                "contact_relate": "同学",
                "contact_name": "测试二",
                "contacts_mobile": "15210120098",
                "pbocQuery": "N",
                "RM0001": "0",
                "RM0002": "0",
                "RM0003": "0",
                "RM0004": "0",
                "RM0005": "0",
                "RM0006": "0",
                "RM0007": "0",
                "RM0008": "0",
                "RM0009": "0",
                "RM0010": "0",
                "identity_card_image_1": "5db0ea08059aa2955d005ac830510e6c",
                "identity_card_image_2": "40d72516c9dd84bc75a0a73306250369",
                "face_image": None,
                "riskGrade": 1
            }
        }
    },

    'loan_repay_notice': {
        'interface': '/api/v1/ctrip/demo/trade',
        'payload': {
            "open_id": "${openIdData_1}",
            "loan_no": "${XC_loanNo_1}",
            "repay_no": "Repay_20w${applyId}",
            "repay_type": "1",
            "repay_term_no": "${还款期序}",
            "service": "LOAN_REPAY_NOTIFY",
            "service_version": "1.0",
            "product_no": "cash",
            "finish_time": "${按期还款时间}50000",
            "partner_id": "HRCASH",
            "partner": "HRCASH",
            "invest_repay_detail": {},
            "repay_detail": {
                "repay_principal": "${应还本金_1}",
                "repay_interest": "${应还利息_1}",
                "repay_penalty_amount": "${应还罚息_1}",
                "actual_repay_amount": "${应还总额_1}",
                "repay_fee": 0
            }
        }
    }
}