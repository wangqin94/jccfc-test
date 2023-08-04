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
                "loanAmount": "30000",
                "loanTerm": "3",  # 借款期数
                "repayType": "1",  # 还款方式 1:等额本息 2:等额本金 3:按天计息
                "fixedBillDay": "10",
                "fixedRepayDay": "27",
                "name": "祖文策",
                "age": "39",
                "sex": "1",
                "idType": "1",
                "idNo": "232722200207072798",
                "issuingAuth": "成都市双流县公安局",
                "birthDay": "1984-11-23",
                "nation": "壮族",
                "mobileNo": "16400008192",
                "reserveMobile": "16400008192",
                "userBankCardNo": "6217228360087474548",
                "national": "CHN",
                "maritalStatus": "90",
                "duties": "A",
                "education": "1",
                "companyName": "四川锦程消费金融有限责任公司",
                "livingAddr": "成都市武侯区府城大道中段85号",
                "contactName": "唐无名",
                "contactMobile": "13708080125",
                "contactRel": "5",
                "contactName1": "唐海明",
                "contactMobile1": "15908118645",
                "contactRel1": "1",
                "goodsName": "取现借款",
                "loanUse": "3",
                "firstRepayDate": "2021-06-11",
                "schoolName": "四川音乐学院",
                "schoolProvince": "510000",
                "schoolCity": "510100",
                "customerType": "2",
                "enrolmentYear": "2009",
                "graduationYear": "2013",
                "companyAddress": "成都市武侯区府城大道中段85号",
                "userOccupation": "0",
                "userIndustryCategory": "0",
                # 朴道查询字段
                "creditAmount": 5000,
                "interestRate": "24",  # 年利率
                "annualRate": "20.36",  # 实际利率（平台优惠后的利率）
                # ##### 断直连删除字段
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
                "manualApproval": "false",
                ##########
                "monthlyIncome": "10000",
                "idCardExpireDate": "2033-04-30",
                "idCardAddr": "510000-510100-510107",
                "idCardDetailAddr": "成都市武侯区府城大道中段85号",
                "liveArea": "510000-510100-510107",
                "companyArea": "510000-510100-510107",
                # "disLinkFlag": "Y",
                # "orderNo": "1123062415281257090252",
                # "uniqueSerialNo": "140O20230624933424800252",
                # "channelId": "2265",
                "fileInfos": [
                    {
                        "fileType": "1",
                        "fileUrl": "xdgl/fql/yw/20230724/idcard_front.jpg",
                        "fileName": "idcard_front.jpg"
                    },
                    {
                        "fileType": "2",
                        "fileUrl": "xdgl/fql/yw/20230724/idcard_back.jpg",
                        "fileName": "idcard_back.jpg"
                    },
                    {
                        "fileType": "3",
                        "fileUrl": "xdgl/fql/yw/20230724/face_distinguish.jpg",
                        "fileName": "face_distinguish.jpg"
                    },
                    {
                        "fileType": "4",
                        "fileUrl": "xdgl/fql/yw/20230724/JC_userauth.pdf",
                        "fileName": "JC_userauth.pdf"
                    },
                    {
                        "fileType": "6",
                        "fileUrl": "xdgl/fql/yw/20230724/JC_non_student.pdf",
                        "fileName": "JC_non_student.pdf"
                    },
                    {
                        "fileType": "7",
                        "fileUrl": "xdgl/fql/yw/20230724/JC_third_auth.pdf",
                        "fileName": "JC_third_auth.pdf"
                    },
                    {
                        "fileType": "8",
                        "fileUrl": "xdgl/fql/yw/20230724/JC_face_identify_authorization.pdf",
                        "fileName": "JC_face_identify_authorization.pdf"
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
                "loanTerm": "6",
                "mobileNo": "16100007381",
                "orderType": "2",  # 1、取现 2、赊销（分期购物）-- 3、信用卡还款 4、账单分期 5、微信、银联消费资产（二类户资产）
                "repayType": "1",
                "debitAccountName": "蓝安峰",
                "debitOpenAccountBank": "中国银行",
                "debitAccountNo": "6212268611367176969",
                "debitOpenAccountBankCode": "121"
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
    },
    'fql_file_upload': {
        'interface': '/api/v1/fql/file/upload',
        'payload': {
            "body": {
                "seqNo": "${seqNo}",
                "path": "/",
                "fileName": "${filename}",
                "content": "${content}"
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
    'fql_file_download': {
        'interface': '/api/v1/fql/file/download',
        'payload': {
            "body": {
                "seqNo": "${seqNo}",
                "path": "/"
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
    'fql_file_upload_result': {
        'interface': '/api/v1/fql/file/upload/result',
        'payload': {
            "body": {
                "seqNo": "${seqNo}"
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

    # 还款试算
    'repay_trial': {
        'interface': '/api/fql/v1/repay/repayTrial',
        'payload': {
            "head": {
                "tenantId": "000",
                "channelNo": "01",
                "requestSerialNo": "111111111111",
                "requestTime": "2022-11-14 21:00:00",
                "merchantId": "000UC010000006268"

            },
            "body": {
                "partnerCode": "000UC010000006268",
                "capitalLoanNo": "",  # 锦程放款成功的借据申请号
                "repayDate": "2022-11-04",  # yyyy-MM-dd(一般是调用接口的时间)
                "loanTerm": "",  # 提前结清传结清账单的最小期数
                "repayType": "",  # 还款类别 10:按期（正常）还款 30:全部提前结清 40:逾期还款
            }
        }
    },

    # 代扣申请
    'payment': {
        'interface': '/api/fql/v1/repay/applyRepay',
        'payload': {
            "head": {
                "tenantId": "000",
                "channelNo": "01",
                "requestSerialNo": "111111111111",
                "requestTime": "2019-05-29 21:00:00",
                "merchantId": "000UC010000006268"
            },
            "body": {
                "withholdSerialNo": "12346",  # 代扣请求流水号--直接透传交易侧的请求流水号,退款/查询这批数据的状态需要
                "partnerCode": "000UC010000006268",  # 合作方代码
                "withholdAmt": "364.34",  # 代扣总金额=用户代扣金额+补差金额---保留两位有效数字(单位:元
                "marketingAmount": "0",  # 补差金额----保留两位有效数字(单位:元)
                "bindCardInfo": {
                    "userName": "",
                    "cardNo": "",
                    "bankType": "03040000",
                    "idType": "1",  # 1、身份证
                    "idNo": "",
                    "phoneNo": ""
                },
                "signNum": "S00202307060001",  # 签约协议号,交易侧透传给接入
                "payMode": "0",  # 支付模式: 0:银行卡支付
                "subMerchantId": "000UC010000006268",  # 分期乐在通联生态圈的商户号
                "sepOutInfo": [  # 出账信息
                    {
                        "type": "1",  # 用户账户出账
                        "amt": "364.34",
                        "account": "1313"
                    },
                ],
                "encryptContent": "16646",  # 通联需要的加密报文
                "bankCode": "03040000",
                "withholdDetail": [{
                    "assetId": "applyId16674462572948120",  # 贷款申请编号-----分期乐资产号,每笔借款唯一
                    "capitalLoanNo": "000LI0001909130144309268037",  # 资金方放款编号/借据号---资金方订单唯一标识
                    "rpyTotalAmt": 364.34,  # 实还总额--单笔订单代扣的总额--------保留两位有效数字(单位:元)
                    "rpyType": "10",  # 还款类型  10-正常还款  30-提前结清, 40-逾期还款，
                    "rpyDate": "2022-11-25",  # 代扣时间   用户实还日（yyyy-MM-dd）
                    "billDetails": [
                        {
                            "rpyAmt": 184.86,  # 还款总额：单笔账单本利罚之和:保留两位有效数字(单位:元)
                            "rpyPrincipal": 158.85,  # 实还本金,保留两位有效数字(单位:元)
                            "rpyFeeAmt": 19.81,  # 实还利息,保留两位有效数字(单位:元)
                            "rpyMuclt": 6.20,  # 实还罚息,保留两位有效数字(单位:元)}
                            "otherInfo": {  # 其他科目金额
                                "repayFee": "0.00",  # 费用（如果没有就给默认值0.00）
                                "repayCompoundInterest": "0.00"  # 复利（如果没有就给默认值0.00）
                            },
                            "rpyTerm": "1"  # 还款期数
                        },
                        # {
                        #     "rpyAmt": 179.48,  # 还款总额-单笔账单本利罚之和:保留两位有效数字(单位:元)
                        #     "rpyPrincipal": 161.90,  # 实还本金,保留两位有效数字(单位:元)
                        #     "rpyFeeAmt": 16.12,  # 实还利息,保留两位有效数字(单位:元)
                        #     "rpyMuclt": 1.46,  # 实还罚息,保留两位有效数字(单位:元)}
                        #     "otherInfo": {  # 其他科目金额
                        #         "repayFee": "0.00",  # 费用（如果没有就给默认值0.00）
                        #         "repayCompoundInterest": "0.00"  # 复利（如果没有就给默认值0.00）
                        #     },
                        #     "rpyTerm": "2"  # 还款期数
                        # }
                    ]  # 还款账单明细
                }]  # 代扣明细
            }
        }
    },

    # 代扣结果查询
    'payment_query': {
        'interface': '/api/fql/v1/repay/queryRepayResult',
        'payload': {
            "head": {
                "channelNo": "01",
                "requestSerialNo": "111111111111",
                "tenantId": "000",
                # "token": "resuiyfie59743949gjkfdk",
                "merchantId": "58347954739",
                "requestTime": "2019-05-29 21:00:00"

            },
            "body": {
                "withholdSerialNo": "",  # 代扣请求流水号
                "partnerCode": "000UC010000006268"
            }
        }
    },

    # 还款计划查询
    'repay_play_query': {
        'interface': '/api/fql/v1/repay/queryRepayPlan',
        'payload': {
            "head": {
                "tenantId": "000",
                "channelNo": "01",
                "requestSerialNo": "111111111111",
                "requestTime": "2019-05-29 21:00:00",
                "merchantId": "000UC010000006268"
            },
            "body": {
                "partnerCode": "000UC010000006267",  # 000UC010000006268
                "capitalLoanNo": ""  # 借据号,放款成功返
            }

        }
    }
}
