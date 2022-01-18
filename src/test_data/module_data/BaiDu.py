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
                    "idpicture0": "/test/gysid1.png",
                    "idpicture1": "/test/gysid2.png",
                    "livingPhoto": "/test/gysface.png",
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

    'settlement': {
        'interface': '/api/v1/baidu/demo/settlement/applyInfo',
        'payload': {
                "loanId": "5170535549454899682",
                "query_flag": "",
                "confirmDate": "2021-12-05",
                "amount": "600",
                "clearDate": "2021-12-03",
                "prcid": "610102199905187862",  #  141100200905221670
                "reqsn": "",
                "username": "",
                "subLoanId": "12332122"
        }
    }

}