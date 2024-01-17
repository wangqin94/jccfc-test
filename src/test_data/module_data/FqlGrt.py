# # ---------------------------------------------------------
# # - 项目特性配置文件
# # - created time: 2023-09-16
# # - version: 1.1
# # ---------------------------------------------------------

# -----------------------------------------------------------
# 分期乐半增信项目配置
# -----------------------------------------------------------
FqlGrt = {
    # 加密接口
    "encrypt": {
        "interface": "/api/v2/fql/demo/encryptData",
    },
    # 解密接口
    "decrypt": {
        "interface": "/api/v2/fql/demo/decipheringData",
    },
    # 授信申请
    "credit": {
        "interface": "/api/v2/fql/credit/apply",
        "payload": {
            "creditApplyId": "applyId16935583718691328",
            "partnerCode": "fql_grt",
            "name": "诸天巧",
            "maritalStatus": "1",
            "age": 17,
            "sex": "0",
            "identiType": "1",
            "identiNo": "452229199507031827",
            "idCardValidDate": "20190530",
            "idCardExpireDate": "20991231",
            "idAddr": "成都市西南航空港经济开发区学府路一段24号",
            "issuedAgency": "成都市公安局天府新区分局",
            "birthday": "1995-07-03",
            "nationality": "中国",
            "nation": "汉",
            "mobileNo": "18425430891",
            "userBankCardNo": "",
            "contactName": "配偶姓名",
            "contactMobile": "15816881688",
            "contactRel": "2",
            "livingAddress": "黑龙江省大兴安岭地区松岭区小扬气镇红星街群芳小区8号楼1单元302室",
            "companyAddress": "四川省成都市高新区府城大道中段88号",
            "companyName": "四川锦程消费金融有限责任公司",
            "monthlyIncome": 6000,
            "education": 1,
            "userOccupation": "1",
            "userIndustryCategory": "2",
            "orderType": "3",
            "loanPrincipal": "30000",
            "repayType": "1",
            "fixedBillDay": "10",
            "fixedRepayDay": "20",
            "loanTerm": 15,
            "loanUse": "2",
            "debitAccountName": "诸天巧",
            "debitOpenAccountBank": "建设银行",
            "debitAccountNo": "6217591693558210853",
            "debitCnaps": "",
            "insureId": "30281",  # 30281,30591
            "interestRate": 7.5,
            "protocolId": "S202309210001",
            "extend": {},
            "uploadInfo": [
                {
                    "fileType": "1",
                    "filePath": "/upload/credit",
                    "fileName": "idcard_front_1123071816044097130384.jpg"
                },
                {
                    "fileType": "2",
                    "filePath": "/upload/credit",
                    "fileName": "idcard_back_1123071816044097130384.jpg"
                },
                {
                    "fileType": "3",
                    "filePath": "/upload/credit",
                    "fileName": "face_distinguish_1123071816044097130384.jpg"
                },
                {
                    "fileType": "4",
                    "filePath": "/upload/credit",
                    "fileName": "JC_userauth_1123071816044097130384.pdf"
                },
                {
                    "fileType": "5",
                    "filePath": "/upload/credit",
                    "fileName": "JC_userinfo_1123071816044097130384.pdf"
                },
                {
                    "fileType": "6",
                    "filePath": "/upload/credit",
                    "fileName": "JC_non_student_1123071816044097130384.pdf"
                },
                {
                    "fileType": "7",
                    "filePath": "/upload/credit",
                    "fileName": "JC_face_identify_authorization_1123071816044097130384.pdf"
                }
            ]
        }
    },
    # 授信查询
    "credit_query": {
        "interface": "/api/v2/fql/credit/query",
        "payload": {
            "applyId": "applyId16935583718691328",
            "partnerCode": "fql_grt"
        }
    },
    # 支用申请
    "loan": {
        "interface": "/api/v2/fql/loan/apply",
        "payload": {
            "applyId": "applyId16935583718691328",
            "partnerCode": "fql_grt",
            "orderType": 9,
            "loanPrincipal": 30000,
            "repayType": 1,
            "fixedBillDay": 10,
            "fixedRepayDay": 20,
            "loanTerm": 15,
            "aRID": "1123121221340357445164I1802",
            "loanUse": "2",
            "mobileNo": "18425430891",
            "debitAccountName": "诸天巧",
            "debitOpenAccountBank": "建设银行",
            "debitAccountNo": "6217591693558210853",
            "debitCnaps": "",
            "extend": {}
        }
    },
    # 支用查询
    "loan_query": {
        "interface": "/api/v2/fql/loan/query",
        "payload": {
            "applyId": "applyId16935583718691328",
            "partnerCode": "fql_grt"
        }
    },
    # 还款计划查询
    "repayPlan_query": {
        "interface": "/api/v2/fql/repayPlan/query",
        "payload": {
            "applyId": "applyId16935583718691328",
            "partnerCode": "fql_grt",
            "capitalLoanNo": "000LI0001353086498709504001"
        }
    },
    # 还款试算接口
    "repay_trial": {
        "interface": "/api/v2/fql/repay/trial",
        "payload": {
            "capitalLoanNo": "000LI0001353086498709504001",
            "repayDate": "2023-09-16",
            "loanTerm": 1,
            "repayType": "10"
        }
    },
    # 还款通知
    "repay": {
        "interface": "/api/v2/fql/repay/apply",
        "payload": {
            "partnerCode": "fql_grt",
            "billId": "000LI0001353086498709504001",
            "assetId": "applyId16935583718691328",
            "capitalLoanNo": "000LI0001353086498709504001",
            "rpyTotalAmt": 2607.47,
            "rpyType": 40,
            "rpyDate": "2023-09-16",
            "repayChannel": "",
            "withholdSerialNo": "",
            "rpyDetails": [
                {
                    "rpyAmt": 2606.36,
                    "rpyPrincipal": 1588.57,
                    "rpyFeeAmt": 198.09,
                    "rpyMuclt": 819.70,
                    "rpyTerm": 1,
                    "rpyGuaranteeAmt": 1.11
                }
            ]
        }
    },
    # 还款通知查询
    "repay_query": {
        "interface": "/api/v2/fql/repay/query",
        "payload": {
            "partnerCode": "fql_grt",
            "billId": "000LI0001353086498709504001-1",
            "capitalLoanNo": "000LI0001353086498709504001"
        }
    },
    # 代扣
    "withhold": {
        "interface": "/api/v2/fql/withhold/apply",
        "payload": {
            "withholdSerialNo": "withholdSerialNo123456789",
            "partnerCode": "fql_grt",
            "repayChannel": "1",
            "bindCardInfo": [
                {
                    "uid": 3103223,
                    "userName": "诸天巧",
                    "cardNo": "6217591693558210853",
                    "bankType": "CCB",
                    "bankBin": "621759",
                    "bankFullName": "建设银行",
                    "idType": "100",
                    "idNo": "452229199507031827",
                    "phoneNo": "18425430891"
                }
            ],
            "bankId": "0105",
            "withholdAmt": 2609.92,
            "signNum": "202306081108302862",
            "payMode": 0,
            "subMerchantId": "81470000",
            "sepOutInfo": [
                {
                    "type": 1,
                    "amt": 2609.92,
                    "account": "6217591693558210853"
                },
                {
                    "type": 2,
                    "amt": 0,
                    "account": "11015898003004"
                }
            ],
            "sepInInfo": [
                {
                    "type": 1,
                    "amt": 2609.92,
                    "withholdMerchants": 1,
                    "account": "8253000082530000",
                    "orgType": 1,
                    "sepMerchCode": "82530000",
                    "sepBankId": "03040000",
                    "detail": [
                        {
                            "from": 1,
                            "amt": 2609.92
                        },
                        {
                            "from": 2,
                            "amt": 0
                        }
                    ]
                },
                {
                    "type": 2,
                    "amt": 3.56,
                    "withholdMerchants": 0,
                    "account": "8175000081750000",
                    "orgType": 2,
                    "sepMerchCode": "81750000",
                    "sepBankId": "01000000",
                    "detail": [
                        {
                            "from": 1,
                            "amt": 3.56
                        },
                        {
                            "from": 2,
                            "amt": 0
                        }
                    ]
                }
            ],
            "encrpytContent": "dgwejtoegegwetowe415",
            "extendInfo": {},
            "withholdDetail": [
                {
                    "assetId": "applyId16935583718691328",
                    "capitalLoanNo": "000LI0001353086498709504001",
                    "rpyTotalAmt": 2606.36,
                    "rpyType": 40,
                    "rpyDate": "2023-09-16",
                    "billDetails": [
                        {
                            "rpyAmt": 2606.36,
                            "rpyPrincipal": 1588.57,
                            "rpyFeeAmt": 198.09,
                            "rpyMuclt": 819.70,
                            "rpyGuaranteeAmt": 3.56,
                            "rpyTerm": 1
                        }
                    ]
                }
            ]
        }
    },
    # 代扣查询
    "withhold_query": {
        "interface": "/api/v2/fql/withhold/query",
        "payload": {
            "withholdSerialNo": "withholdSerialNo123456789",
            "partnerCode": "fql_grt"
        }
    }
}
