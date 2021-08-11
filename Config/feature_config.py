# # ---------------------------------------------------------
# # - 项目特性配置文件
# # - created time: 2021-03-06
# # - version: 1.1
# # ---------------------------------------------------------


# -----------------------------------------------------------
# 美团项目配置
# -----------------------------------------------------------
MeiTuan = {
    'credit': {
        'interface': '',
        'payload': {},
    },

    'credit_query': {
        'interface': '',
        'payload': {},
    },

    'loan': {
        'interface': '',
        'payload': {},
    },

    'loan_query': {
        'interface': '',
        'payload': {},
    },

    'repay_notice': {
        'interface': '/api/v1/meit/notice/repayNotice',
        'payload': {
            "head": {
                "channelNo": "07",
                "requestSerialNo": "${requestSerialNo}",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000",
                "merchantId": "F21C01MEIT"
            },
            "body": {
                "CONTRACT_NO": "${CONTRACT_NO}",
                "BIZ_SERIAL_NO": "${BIZ_SERIAL_NO}",
                "LOAN_NO": "${LOAN_NO}",
                "REPAYMENT_AMOUNT": "${REPAYMENT_AMOUNT}",
                "PRINCIPAL": "${PRINCIPAL}",
                "INTEREST": "${INTEREST}",
                "D_INTEREST": "${D_INTEREST}",
                "REPAY_TYPE": "${REPAY_TYPE}",
                "PERIOD_NOW": "${PERIOD_NOW}",
                "TRADE_PERIOD": "${TRADE_PERIOD}",
                "RATE": "${RATE}",
                "PAY_CHANNEL": "QDB",
                "REPAY_STATUE": "S",  # 还款状态S-成功 F-失败
                "REPAYMENT_DATE": "${REPAYMENT_DATE}",
                "APP_ID": "MTSHF",
                "CUSTOMER_NO": "1000000151909810",
                "REPAYMENT_NAME": "${REPAYMENT_NAME}",
                "REPAYMENT_CARD": "${REPAYMENT_CARD}",
                "REPAYMENT_TIME": "${REPAYMENT_TIME}",
                "CREDIT_LIMIT": "${CREDIT_LIMIT}",
                "AVALIABLE_LIMIT": "${AVALIABLE_LIMIT}",
                "USED_LIMIT": "${USED_LIMIT}",
                "MINI_REPAYMENT_AMOUNT": "100",  # 二期字段
                "DPD": "0",  # 二期字段
                "ALL_DEBT_AMOUNT": "100000"  # 二期字段
            }
        },
    },

    'loan_notice': {
        'interface': '/api/v1/meit/notice/loanNotice',
        'payload': {
            "head": {
                "channelNo": "07",
                "requestSerialNo": "${requestSerialNo}",
                "requestTime": "2020-08-28 17:16:41",
                "tenantId": "000",
                "merchantId": "F21C01MEIT"
            },
            "body": {
                "CONTRACT_NO": "${CONTRACT_NO}",
                "PURPOSE": "DAILY_CONSUMPTION",
                # DAILY_CONSUMPTION(0,"日常消费"),DECORATION(1,"装修"),TOURISM(2,"旅游"),EDUCATION(3,"教育"),MEDICAL_TREATMENT(4,"医疗");
                "LOAN_NO": "${LOAN_NO}",
                "PAY_STATUE": "S",  # 放款状态S-成功 F-失败
                "PAYMENT_CONFIRM_TIME": "2021-06-21 11:42:30",
                "TRADE_PERIOD": "${TRADE_PERIOD}",
                "LOAN_AMOUNT": "${LOAN_AMOUNT}",
                "RATE": "${RATE}",
                "PAY_CHANNEL": "TLZF",
                "REPAYMENT_DATE": "2021-06-21 11:42:30",
                "APP_ID": "MTSHF",
                "CUSTOMER_NO": "1000000151909810",
            }
        },
    },
}

# -----------------------------------------------------------
# 百度(度小满)项目配置
# -----------------------------------------------------------
BaiDu = {
    'credit': {
        'interface': '/api/v1/baidu/demo/credit/apply',
        'payload': {
            "type": "async",
            "reqSn": "credit_baidu502102002105001650",
            "message": {
                "sessionId": "credit_baidu502102002105001650",
                "transactionType": "apply",
                "transactionId": "502102002105001650wai",
                "timestamp": "1616580987759",
                "basicInfo": {
                    "prcid": "420113199704275886",
                    "bankcard": "6222001552388738497",
                    "name": "司瑶",
                    "phonenumber": "19208785619"
                },
                "expanding": {
                    "reasonCode": '-9999',
                    "reasonMsg": '-9999',
                    "initialAmount": "100000",
                    "creditValidityDays": "30",
                    "risCode": "1000",
                    "dxmAScore": "642",
                    "preACustSeg": "A",
                    "holmesBlackScore": "590",
                    "holmesAgentScore": "59.48",
                    "blackListType": "D1",
                    "prcidNormalScoreExp3": "92",
                    "bidNormalScoreExp3": "92",
                    "phoneNormalScoreExp3": "92",
                    "taxMonthlyIncomeSection": "-9999",
                    "ocrExpdate": "20220203",
                    # "r21P12FinallyInterest": "6.5",
                    "r21P12FinallyInterest": "6.5",
                    "dxmDScore": "575",
                    "careerType": "02",
                    "ocrAddress": "成都市武侯区府城大道中段85号",  # 身份地址
                    "userHomeAddress": "成都市武侯区府城大道中段85号",  # 家庭地址
                    "zxPermanentAddress": "成都市武侯区府城大道中段85号",  # 征信户籍地址
                    "zxsDomicile": "成都市武侯区府城大道中段85号",  # 征信居住地址
                    "zxMailingAddress": "成都市武侯区府城大道中段85号",  # 征信通讯地址
                    "zxsCareer": "02",
                    "zdV1Fico": "570"
                }
            }
        },
    },
    'credit_query': {
        'interface': '',
        'payload': {},
    },

    'loan': {
        'interface': '/api/v1/baidu/demo/loan/apply',
        'payload': {
            "type": "async",
            "reqSn": '',
            "message": {
                "sessionId": '',
                "transactionType": "transaction",
                "transactionId": '',
                "timestamp": '',
                "basicInfo": {
                    "prcid": '',
                    "bankcard": '',
                    "name": '',
                    "phonenumber": ''
                },
                "expanding": {
                    "cashAmount": '100000',
                    "orderId": '',
                    "reasonCode": '-9999',
                    "reasonMsg": '-9999',
                    "creditValidityDays": "30",
                    "risCode": "10000",
                    "dxmAScore": "642",
                    "r21P12FinallyInterest": "6.5",
                    "preACustSeg": "C",
                    "holmesBlackScore": "59.48",
                    "holmesAgentScore": "59.48",
                    "blackListType": "D1",
                    "prcidNormalScoreExp3": "92",
                    "bidNormalScoreExp3": "92",
                    "phoneNormalScoreExp3": "92",
                    # "idpicture0": "0d352ebb0bece51df700d376d32b5281",
                    # "idpicture1": "0d352ebb0bece51df700d376d32b5282",
                    # "livingPhoto": "0d352ebb0bece51df700d376d32b5282",
                    "unionLoanUsed": "01",
                    "idpicture0": "/test/idz20210720.jpg",
                    "idpicture1": "/test/idf20210720.jpg",
                    "livingPhoto": "/test/wymface.png",
                    "loanUse": "1",
                    "taxMonthlyIncomeSection": "01",
                    "ocrExpdate": "20220506",
                    "term": '3',
                    "dailyInterestRate": "6.5000",
                    "dailyPenaltyRate": "7.5000",
                    "compreAnnualInterestRate": "2340",
                    # "dailyInterestRate": "6.100",
                    # "compreAnnualInterestRate": "2196",
                    "violatePrepay": "200.0000",
                    "violatePrepayRule": "1",
                    "violatePrepayFlag": "0",
                    "repayMode": "22",  # 32等额本息对应还款对账文件还款类型05，22随借随还对应还款类型02
                    "dxmDScore": "575.24151",
                    # "ocrAddress": "重庆市江北区府城大道中段87号",
                    "careerType": "",
                    "ocrAddress": "",  # 身份地址
                    "userHomeAddress": "",  # 家庭地址
                    "zxPermanentAddress": "",  # 征信户籍地址
                    "zxsDomicile": "",  # 征信居住地址
                    "zxMailingAddress": "",  # 征信通讯地址
                    "zxsCareer": "",
                    "contactPhone": "19982022546",
                    "contactName": "张三",
                    "contactRalation": "父母"
                },
            },
        },
    },

    'loan_query': {
        'interface': '',
        'payload': {},
    },
    'limitrestore': {
        'interface': '/api/v1/baidu/demo/limit/restore',
        'payload': {
            "seq_no": "5562464134095184322",
            "cur_date": "20210728",
            "amount": 60000,
            "tran_time": "20210728110538",
            "type": 3,
            "order_id": "5572226773574670846",
            "version": 1,
            "loan_id": "5446907214124938311",
            "comment": "{\"loan_order_id\": \"5446458001318297237\",\"amount_total\": \"60000\"}",
        },
    },

    'notice': {
        'interface': '/api/v1/baidu/demo/limit/restore',
        'payload': {
            "type": 3,
            "order_id": "${order_id}",
            "loan_id": "",
            "cur_date": "20210402",
            "tran_time": "20210328191516",
            "seq_no": "seq_random_baidu${CUSTOMER_NO}",
            "amount": 60000,
            "version": 1,
            "comment": "{\"amount_total\": 60000,\"loan_order_id\": \"${order_id}\"}"
        },
    },

}

# -----------------------------------------------------------
# 携程项目配置
# -----------------------------------------------------------
XieCheng = {
    'pre_credit': {
        'interface': '/api/v1/ctrip/demo/trade',
        'payload': {
            "open_id": "6ReW_21${applyId}",
            "user_name": "${姓名}",
            "id_no": "${身份证号}",
            "bank_bind_mobile": "${手机号}",
            "card_no": "${银行卡号}",
            "request_no": "REGISTER202011${applyId}",
            "service_version": "1.0",
            "product_no": "cash",
            "partner": "JCXFCASH",
            "advice_amount": "${advice_amount}",
            "service": "PRE_CREDIT",
            "id_type": "IDENTITYCARD",
            "user_data": {
                "Platform": {
                    "id_no": "${身份证号}",
                    "user_name": "${姓名}",
                    "nationality": "Chinese",
                    "mobile": "${手机号}",
                    "RM0006": "0",
                    "RM1018": "2",
                    "RM0005": "0",
                    "RM1017": "2",
                    "RM0008": "A2",
                    "RM0007": "A2",
                    "RM1019": "2",
                    "education": "0.1581,0.0862,0.7070,0.0487",
                    "RM0009": "A3",
                    "customerStickiness": "稳定",
                    "institutionType": "microCredit",
                    "loanAppRating2": "1",
                    "loanAppRating": "优",
                    "RM1021": "-9999",
                    "RM1020": "2",
                    "login_period": "0.1978,0.1626,0.1930,0.3240,0.1226",
                    "rest_regular": "96.5241",
                    "RM1023": "-9999",
                    "RM0010": "A3",
                    "RM1022": "-9999",
                    "RM1025": "-9999",
                    "RM1024": "-9999",
                    "creditRating": "稳定",
                    "flight_airport_tendency": "0.1429,0.1429,0.7143",
                    "car_prob": "0.9122",
                    "family_prob": None,
                    "pbocQuery": "N",
                    "city_stable": "0.3855",
                    "house_prob": "0.6531",
                    "odc_prob": "39",
                    "student_prob": "0.3788",
                    "order_platform": "0.0164,0.5410,0.0492",
                    "vacation_day_desire": "13",
                    "price_sensitive": "35",
                    "card_no": "6212263803010024333",
                    "RM1001": "0",
                    "pay_type": "Q端其他:0.16,微信支付:0.11,常用卡借记卡:0.5,常用卡信用卡:0.16",
                    "RM1003": "1",
                    "RM1002": "0",
                    "whole_power": "81",
                    "RM1005": "0",
                    "RM1004": "0",
                    "RM1007": "0",
                    "mobileInfo": "正常",
                    "RM1006": "0",
                    "RM1009": "9",
                    "RM1008": "9",
                    "destination_tendency": "0.1111,0.1111,0.4889,0.7111,0.5556,0.1333",
                    "creditMode": "PA",
                    "RM1010": "2",
                    "RM1012": "4",
                    "RM1011": "2",
                    "plan_prob": "71",
                    "RM0002": "L",
                    "RM1014": "1",
                    "RM0001": "0",
                    "RM1013": "2",
                    "consumer_stability": "82",
                    "RM0004": "0",
                    "RM1016": "0",
                    "RM0003": "0",
                    "RM1015": "1",
                    "identity_card_image_1": "/xdgl/ctrip/test/cqid1.png",
                    "identity_card_image_2": "/xdgl/ctrip/test/cqid2.png",
                    "face_image": "/xdgl/ctrip/test/cqface.png"
                }
            },
            "advice_rate_type": "${advice_rate_type}",
            "advice_rate": {
                "ECI": {
                    "3": "0.36"
                },
            }
        },
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
                    "RM0006": "0",
                    "RM1018": "2",
                    "RM0005": "0",
                    "RM1017": "2",
                    "RM0008": "A2",
                    "RM0007": "A2",
                    "RM1019": "2",
                    "education": "0.1581,0.0862,0.7070,0.0487",
                    "RM0009": "A3",
                    "customerStickiness": "稳定",
                    "institutionType": "microCredit",
                    "loanAppRating2": "1",
                    "loanAppRating": "优",
                    "RM1021": "-9999",
                    "RM1020": "2",
                    "login_period": "0.1978,0.1626,0.1930,0.3240,0.1226",
                    "rest_regular": "96.5241",
                    "RM1023": "-9999",
                    "RM0010": "A3",
                    "RM1022": "-9999",
                    "RM1025": "-9999",
                    "RM1024": "-9999",
                    "creditRating": "稳定",
                    "flight_airport_tendency": "0.1429,0.1429,0.7143",
                    "car_prob": "0.9122",
                    "family_prob": None,
                    "pbocQuery": "N",
                    "city_stable": "0.3855",
                    "house_prob": "0.6531",
                    "odc_prob": "39",
                    "student_prob": "0.3788",
                    "order_platform": "0.0164,0.5410,0.0492",
                    "vacation_day_desire": "13",
                    "price_sensitive": "35",
                    "card_no": "6212263803010024333",
                    "RM1001": "0",
                    "pay_type": "微信支付:0.05,支付宝支付:0.05,Q端其他:0.03,常用卡借记卡:0.81",
                    "RM1003": "1",
                    "RM1002": "0",
                    "whole_power": "81",
                    "RM1005": "0",
                    "RM1004": "0",
                    "RM1007": "0",
                    "mobileInfo": "正常",
                    "RM1006": "0",
                    "RM1009": "9",
                    "RM1008": "9",
                    "destination_tendency": "0.1111,0.1111,0.4889,0.7111,0.5556,0.1333",
                    "creditMode": "PA",
                    "RM1010": "2",
                    "RM1012": "4",
                    "RM1011": "2",
                    "plan_prob": "71",
                    "RM0002": "L",
                    "RM1014": "1",
                    "RM0001": "0",
                    "RM1013": "2",
                    "consumer_stability": "82",
                    "RM0004": "0",
                    "RM1016": "0",
                    "RM0003": "0",
                    "RM1015": "1",
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
                    "identity_card_image_1": "/xdgl/ctrip/test/cqid1.png",
                    "identity_card_image_2": "/xdgl/ctrip/test/cqid2.png",
                    "face_image": "/xdgl/ctrip/test/cqface.png"
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
                "riskGrade": "-999"
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

# -----------------------------------------------------------
# 分期乐项目配置
# -----------------------------------------------------------
fql = {
    'credit': {
        'interface': '/api/fql/v1/credit/apply',
        'payload': {
            "head": {
                "tenantId": "000",
                "channelNo": "01",
                "requestSerialNo": "2020000009480719640001",
                "marketClue": None,
                "deviceId": None,
                "longitude": None,
                "latitude": None,
                "requestTime": 20201623377322896,
                "merchantId": "000UC010000006268",
                "managerId": "000UC010000006268",
                "empNo": "2019071623377322896",
                "token": None,
                "rebackUrl": None,
                "notifyUrl": None
            },
            "body": {
                "applyId": "202000000948071964",
                "sourceCode": "000UC010000006268",
                "orderType": "1",  # 订单类型
                "loanAmount": 30000,
                "creditAmount": 30000,
                "loanTerm": "12",  # 借款期数
                "repayType": "1",  # 还款方式 1:等额本息 2:等额本金 3:按天计息
                "fixedBillDay": "10",
                "fixedRepayDay": "27",
                "interestRate": "30",  # 年利率
                "annualRate": "20.36",  # 实际利率（平台优惠后的利率
                "name": "祖文策",
                "age": "39",
                "sex": "1",
                "idType": "1",
                "idNo": "232722200207072798",
                "issuingAuth": "成都市双流县公安局",
                "birthDay": "1984-11-23",
                "nation": "汉族",
                "mobileNo": "16400008192",
                "reserveMobile": "16400008192",
                "userBankCardNo": "6217228360087474548",
                "national": "CHN",
                "maritalStatus": "90",
                "duties": "A",
                "education": "1",
                "companyName": "锦程消费金融有限公司",
                "livingAddr": "成都市武侯区府城大道中段85号",
                "contactName": "唐无名",
                "contactMobile": "13708080125",
                "contactRel": "5",
                "contactName1": "唐海明",
                "contactMobile1": "15908118645",
                "contactRel1": "1",
                "goodsName": "取现借款",
                "loanUse": "5",
                "firstRepayDate": "2021-06-11",
                "schoolName": "四川音乐学院",
                "schoolProvince": "510000",
                "schoolCity": "510100",
                "customerType": "2",
                "enrolmentYear": "2009",
                "graduationYear": "2013",
                "companyAddress": "成都市武侯区府城大道中段85号",
                "userOccupation": "0",
                "userIndustryCategory": "2",
                "registerMobileLocation": "成都",
                "hasOverdueEver": "false",
                "totalOverdueCount": "0",
                "totalOverdueDays": "0",
                "maxOverdueDays": "0",
                "currentOverdueDays": "0",
                "allOrderRepayed": "1",
                "notRepayedOrderCount": "0",
                "notRepayedOrderAmount": "0",
                "totalOrderCount": "0",
                "firstOrderDate": "2021-05-08",
                "latestOrderDate": "2021-04-08",
                "monthlyIncome": "10000",
                "idCardExpireDate": "2025-3-30",
                "idCardAddr": "510000-510100-510107",
                # "idCardDetailAddr": "成都市武侯区府城大道中段85号",
                "manualApproval": "false",
                "liveArea": "510000-510100-510107",
                "companyArea": "510000-510100-510107",
                "fileInfos": [{
                    "fileType": "1",
                    "fileUrl": "http://jccfc-hsit.ks3-cn-beijing.ksyun.com/xdgl/fql/yw/idcard_front_202000000948071964.jpg",
                    "fileName": "idcard_front_202000000948071964.jpg"
                },
                    {
                        "fileType": "2",
                        "fileUrl": "http://jccfc-hsit.ks3-cn-beijing.ksyun.com/xdgl/fql/yw/idcard_back_202000000948071964.jpg",
                        "fileName": "idcard_back_202000000948071964.jpg"
                    },
                    {
                        "fileType": "3",
                        "fileUrl": "http://jccfc-hsit.ks3-cn-beijing.ksyun.com/xdgl/fql/yw/face_distinguish_202000000948071964.jpg",
                        "fileName": "face_distinguish_202000000948071964.jpg"
                    },
                    {
                        "fileType": "4",
                        "fileUrl": "http://jccfc-hsit.ks3-cn-beijing.ksyun.com/xdgl/fql/yw/JC_userauth_202000000948071964.pdf",
                        "fileName": "JC_userauth_202000000948071964.pdf"
                    },
                    {
                        "fileType": "6",
                        "fileUrl": "http://jccfc-hsit.ks3-cn-beijing.ksyun.com/xdgl/fql/yw/JC_non_student_202000000948071964.pdf",
                        "fileName": "JC_non_student_202000000948071964.pdf"
                    }

                ]
            }
        }

    },
    'credit_query': {
        'interface': '/api/fql/v1/credit/resultQuery',
        'payload': {
            "body": {
                "applyId": "${applyId}",
                "sourceCode": "${sourceCode}"
            },
            "head": {
                "channelNo": "01",
                "requestSerialNo": "111111111111",
                "tenantId": "000",
                "token": "resuiyfie59743949gjkfdk",
                "merchantId": "58347954739",
                "requestTime": "2019-05-29 21:00:00"
            }
        }
    },

    'loan': {
        'interface': '/api/fql/v1/loan/apply',
        'payload': {
            "head": {
                "tenantId": "000",
                "channelNo": "01",
                "requestSerialNo": "2020000012097038170002",
                "marketClue": None,
                "deviceId": None,
                "longitude": None,
                "latitude": None,
                "requestTime": 20201623402451332,
                "merchantId": "000UC010000006268",
                "managerId": "000UC010000006268",
                "empNo": "2019071623402451332",
                "token": None,
                "rebackUrl": None,
                "notifyUrl": None
            },
            "body": {
                "applyId": "202000001209703817",
                "sourceCode": "000UC010000006268",
                "name": "蓝安峰",
                "fixedRepayDay": "27",
                "firstRepayDate": "2021-06-11",
                "loanAmt": "20000",
                "loanTerm": "12",
                "mobileNo": "16100007381",
                "interestRate": "35.28",
                "orderType": "2",  # 1、取现 2、赊销（分期购物） 3、信用卡还款 4、账单分期 5、微信、银联消费资产（二类户资产）
                "repayType": "1",
                "debitAccountName": "蓝安峰",
                "debitOpenAccountBank": "中国银行",
                "debitAccountNo": "6212268611367176969",
                "debitOpenAccountBankCode": "121",
                "fileInfos": [{
                    "fileType": "5",
                    "fileUrl": "http://jccfc-hsit.ks3-cn-beijing.ksyun.com/xdgl/fql/yw/JC_contract_202000001209703817.pdf",
                    "fileName": "JC_contract_202000001209703817.pdf"
                }]
            }
        }
    },

    'loan_query': {
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

# -----------------------------------------------------------
# 应急支付项目配置
# -----------------------------------------------------------
YingJiZF = {
    'queryChannel': {
        'interface': '/api/v1/emergency/queryChannel',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "channelName": "度",
            }
        }

    },
    'queryInvoiceListByPage': {
        'interface': '/api/v1/emergency/queryInvoiceListByPage',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "bankType": "",  # 开户行总行号 中国工商：0102 中国农业：0103 中国银行：0104 建设银行：0105
                "certificateNo": "",  # 身份证号
                "channelNo": "F21C02BAID",  # 渠道号
                "loanStatus": "1",  # EnumLoanInvoiceStatus 借据状态 枚举类型NORMAL("1", "正常"),OVERDUE("2", "逾期"),SETTLE(
                # "3", "结清");
                "noticeType": "0",  # 通知类型（0-无条件、1-账单日通知、2-逾期通知）
                "userIdList": [],  # 客户ID集合 list
                "pageNum": 1,
                "pageSize": 20,
                "settleFlag": "0",  # 结清标识 EnumBool 0-否，1-是
                "userTel": "",  # 电话号码
            }
        }

    },
    'loan_bill': {
        'interface': '/api/v1/loan/bill',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "idNo": "140431198406286402",  # 身份证号
                "applyNo": "000LI5538514397462145161272",  # 借据号
                "billType": "1",  # 1-正常账单，2-提前结清
            }
        }
    },
    'payment_query': {
        'interface': '/api/v1/payment/query',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "idNo": "140431198406286402",  # 身份证号
                "applyNo": "000LI5538514397462145161272",  # 借据号
                "channelCode": "F21C02BAID",  # 渠道号
            }
        }

    },
    'loan_query': {
        'interface': '/api/v1/loan/query',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "idNo": "140431198406286402",  # 身份证号
                "channelCode": "F21C02BAID",  # 渠道号
            }
        }
    },
    'loan_details': {
        'interface': '/api/v1/loan/details',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "applyNo": "000LI5538514397462145161272",  # 借据号
            }
        }
    },

    'repay_query': {
        'interface': '/api/v1/repay/query',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "applyNo": "000LI5538514397462145161272",  # 借据号
            }
        }
    },

    'plan_query': {
        'interface': '/api/v1/replay/plan/query',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "applyNo": "000LA2021060000004557",  # 支用申请号：000LA2021050000000020
                "channelCodes": ["F20B02XIEC"]
            }
        }
    },

    'payment_result': {
        'interface': '/api/v1/payment/result',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "appOrderNo": "appOrderNo000LA2021060000004557",  # 订单流水号：000LA2021050000000020
            }
        }
    },

    'bankcard_bind': {
        'interface': '/api/v1/bankCard/bind',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "certificateNo": "140431198406286402",  # 身份证号
                "mobileNo": "14983105967",  # 手机号
                "accountNo": "6212269404480619920",  # 新银行卡号
                "accountBankName": "",  # 新银行卡所属银行名称
                "accountBin": "",  # 新银行卡所属银行卡bin
                "bankCode": "",  # 新银行总行号
                "branchBankCode": "",  # 新银行支行联号
            }
        }
    },

    'bankcard_modify': {
        'interface': '/api/v1/bankCard/modify',
        'payload': {
            "head": {
                "jcSystemEncry": "2582a6b723486da364ada1af2c00f115",
                "jcSystemCode": "loan-web",
                "tenantId": "000",
                "channelNo": "21",
                "requestSerialNo": "202=182714511036848",
            },
            "body": {
                "invoiceId": "000LI5538514397462145161272",  # 借据号
                "certificateNo": "140431198406286402",  # 身份证号
                "mobileNo": "14983105967",  # 手机号
                "oldAccountNo": "6212269404480619920",  # 新银行卡号
                "newAccountNo": "6212269404480612920",  # 旧银行卡号
                "newAccountBankName": "",  # 新银行卡所属银行名称
                "newAccountBin": "",  # 新银行卡所属银行卡bin
                "newBankCode": "",  # 新银行总行号
                "newBranchBankCode": "",  # 新银行支行联号
            }
        }
    },

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
                "loanInvoiceId": "000LI5538514397462145161272",  # 借据号
                "channelNo": "2",  # 主动还款渠道
                "repayType": "0",  # 还款方式 0-按期还款   1-提前还款
                "paymentType": "5",  # 支付类型1-支付宝-主动还款 2-支付宝-代扣 3-微信-主动还款 4-微信-代扣 5-银行卡-主动还款 6-银行卡-代扣   7-云闪付-主动还款
                "periods": "1",  # 还款期数 多期以,分隔
                "repayAmt": 212.46,  # 还款金额
                "appOrderNo": "",  # 还款订单流水号
                "settleStatus": "1",  # 结清标识 EnumBool 0 未结清  1 结清
                "payPlatformCode": "zhifubianhao",  # 支付平台编号
                "aliPayViewUrl": "https://www.baidu.com/",  # 支付平台编号
                "idNo": "451123198311190587",  # 身份证号（银行卡还款必须）
                "phoneNum": "18908989867",  # 用户银行卡绑定手机号（银行卡还款必须）
                "bankAcctName": "楚东进",  # 还款人姓名（银行卡还款必须）
                "bankName": "0102",  # 银行编号（银行卡还款必须）
                "bankAcctNo": "6212810833868379081",  # 还款人银行卡卡号（银行卡还款必须）
                "deviceInfo": "设备信息1.21sxf",  # 设备信息（微信还款必须）
                "wxPayViewUrl": "https://www.baidu.com/",  # 传值外网可以访问的地址（微信还款必须）
                "createIp": "10.12.255.0",  # ip（微信还款必须）
            }
        }
    },
}

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
                        "contactName": "联系人一",
                        "contactMobile": "18380446001",
                        "contactRel": "2"  # 联系人关系 EnumRelationType
                    },
                    {
                        "contactName": "联系人二",
                        "contactMobile": "18380446002",
                        "contactRel": "1"
                    }
                ],
                "fileInfos": [
                    {
                        "fileType": "1",
                        "fileName": "idcard_front.jpg",
                        "fileUrl": "http://jccfc-hsit.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/hj/wld/credit/idcard_front.jpg"
                    },
                    {
                        "fileType": "2",
                        "fileName": "idcard_back.jpg",
                        "fileUrl": "http://jccfc-hsit.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/hj/wld/credit/idcard_back.jpg"
                    },
                    {
                        "fileType": "3",
                        "fileName": "face_distinguish.jpg",
                        "fileUrl": "http://jccfc-hsit.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/hj/wld/credit/face_distinguish.jpg"
                    },
                    {
                        "fileType": "4",
                        "fileName": "JC_userauth.pdf",
                        "fileUrl": "http://jccfc-hsit.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/hj/wld/credit/JC_userauth.pdf"
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
