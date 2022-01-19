# # ---------------------------------------------------------
# # - 项目特性配置文件
# # - created time: 2021-03-06
# # - version: 1.1
# # ---------------------------------------------------------


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
                "idCardExpireDate": "2022-3-30",
                "idCardAddr": "510000-510100-510107",
                "idCardDetailAddr": "成都市武侯区府城大道中段85号",
                "manualApproval": "false",
                "liveArea": "510000-510100-510107",
                "companyArea": "510000-510100-510107",
                "fileInfos": [{
                    "fileType": "1",
                    "fileUrl": "http://jccfc-hpre.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/fql/yw/idcard_front_202000000948071964.jpg",
                    "fileName": "idcard_front_202000000948071964.jpg"
                },
                    {
                        "fileType": "2",
                        "fileUrl": "http://jccfc-hpre.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/fql/yw/idcard_back_202000000948071964.jpg",
                        "fileName": "idcard_back_202000000948071964.jpg"
                    },
                    {
                        "fileType": "3",
                        "fileUrl": "http://jccfc-hpre.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/fql/yw/face_distinguish_202000000948071964.jpg",
                        "fileName": "face_distinguish_202000000948071964.jpg"
                    },
                    {
                        "fileType": "4",
                        "fileUrl": "http://jccfc-hpre.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/fql/yw/JC_userauth_202000000948071964.pdf",
                        "fileName": "JC_userauth_202000000948071964.pdf"
                    },
                    {
                        "fileType": "6",
                        "fileUrl": "http://jccfc-hpre.ks3-cn-shanghai-2.cloud.jccfc.com/xdgl/fql/yw/JC_non_student_202000000948071964.pdf",
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
        'interface': '/api/fql/v1/loan/resultQuery',
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
