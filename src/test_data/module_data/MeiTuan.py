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
        'interface': "/api/v1/meit/credit",
        'payload': {
            "head": {
                "merchantId": "F21C01MEIT",
                "channelNo": "01",
                "requestSerialNo": 'requestSerialNo',
                "requestTime": 'tradestamp',  # 年-月-日 时：分：秒
                "tenantId": "000"
            },  # 202103031119406040001000000009
            "body": {
                "APP_NO": 'app_no',  # '202103021040153690001000000028',  #
                "APPLY_AMT": '300000',  # N*100
                "CUSTOMER_NO": "CUSTOMER_NO",
                "PRODUCT_NO": "00018",  # 美团产品号
                "BANK_NO": "MT",
                "CER_TYPE": "01",
                "CER_NO": "cer_no",
                "CERT_VALID_START_DATE": "20160225",
                "CERT_VALID_END_DATE": "20260225",
                "NAME": 'name',
                #"NAME": "陈祺",
                # "NAME": "陈祺",
                "MOBILE_NO": "telephone",
                "CARD_NO": "bankid",
                "ZM_AUTH_FLAG": "Y",
                "RATE_LISTS": [
                    {
                        "REPAYMENT_TYPE": "ACPI",
                        "PLATFORM_RATE": '980',
                        "PLATFORM_PENALTY_RATE": '980'
                    }
                ],
                "OCR": {
                    "ID_NO_OCR": "cer_no",
                    "ID_NAME_OCR": "name",
                    #"ID_NAME_OCR": "陈祺",
                    # "ID_NAME_OCR": "陈祺",
                    "ID_VALIDITY_OCR": "20160225-20260225",
                    "ID_FACE_PIC_PATH": "/hj/xdgl/meituan/cqid1.png",     # /hj/xdgl/meituan/cqid1
                    "ID_BACK_PIC_PATH": "/hj/xdgl/meituan/cqid2.png",     # /hj/xdgl/meituan/cqid2.png  /hj/xdgl/meituan/owxbackerror.jpg
                    # /hj/xdgl/meituan/cqid2.png  /hj/xdgl/meituan/owxbackerror.jpg
                    # "ID_FACE_PIC_PATH": "/hj/xdgl/meituan/wymid1.png",
                    # "ID_BACK_PIC_PATH": "",
                    #"ID_ADDRESS_OCR": "成都莆田街133号-4-5",    # 深圳莆田街133号-4-5
                    "ID_ADDRESS_OCR": "成都莆田街133号-4-5",  # 深圳莆田街133号-4-5
                    "NATION": "回族",
                    "ISSUER": "四川省成都市"
                },
                "HAS_JB_ADMIT": "Y",
                "RISK_INFO": {
                    "platform_consuming_ability_level": "1002",
                    "platform_consuming_frequency_level": "1002",
                    "platform_consuming_scene_number_level": "1002",
                    "predicted_age_level": "1002",
                    "predicted_marital_status_level": "1002",
                    "active_city_number_level_last_90d": "1002",
                    "predicted_gender_level": "1002",
                    "account_register_time_level": "1002",
                    "job_category_code": "1002",
                    "resident_province_name": "1002",
                    "user_order_count_level_in_last_180d": "1002",
                    "user_order_count_level_in_last_360d": "1002",
                    "user_order_count_level_in_last_90d": "1002",
                    "user_order_days_level_in_last_180d": "1002",
                    "user_order_days_level_in_last_360d": "1002",
                    "user_order_days_level_in_last_90d": "1002",
                    "user_successful_order_amount_level_in_last_180d": "1002",
                    "user_successful_order_amount_level_in_last_360d": "1002",
                    "user_successful_order_amount_level_in_last_90d": "1002",
                    "user_successful_order_count_level_in_last_180d": "1002",
                    "user_successful_order_count_level_in_last_360d": "1002",
                    "user_successful_order_count_level_in_last_90d": "1002",
                    "user_successful_waimai_order_count_level_in_last_180d": "1002",
                    "user_successful_waimai_order_count_level_in_last_360d": "1002",
                    "user_successful_waimai_order_count_level_in_last_90d": "1002",
                    "user_visit_bg_count_level_in_last_90d": "1002",
                    "user_active_days_in_last_180d_level": "1002",
                    "user_active_days_in_last_360d_level": "1002",
                    "user_active_days_in_last_90d_level": "1002",
                    "user_visit_waimai_days_in_last_180d": "1002",
                    "user_visit_waimai_days_in_last_360d": "1002",
                    "user_visit_waimai_days_in_last_90d": "1002",
                    "user_active_tag_in_1y": "1002",
                    "user_visit_group_buy_days_in_last_180d": "1002",
                    "user_visit_group_buy_days_in_last_360d": "1002",
                    "user_visit_group_buy_days_in_last_90d": "1002",
                    "mt_creditscore_level_v4_0_1": "1002"
                },
                "Signature_date": "20160225",
                "Family_Address": "成都市武侯区府城大道中段85号",
                # "FACE_PIC_PATH": "/hj/xdgl/meituan/wymface.png",
                "FACE_PIC_PATH": "/hj/xdgl/meituan/cqface",    # /hj/xdgl/meituan/cqface.png
            }
        }
    },

    'credit_query': {
        'interface': '/api/v1/meit/credit/resultQuery',
        'payload': {
            "head": {
                "merchantId": "F21C01MEIT",
                "channelNo": "01",
                "requestSerialNo": 'self.app_no',
                "requestTime": 'requestTime',  # 年-月-日 时：分：秒
                "tenantId": "000",
                "token": "111"
            },
            "body": {
                "APP_NO": 'self.app_no',
            }
        }
    },

    'loan': {
        'interface': '/api/v1/meit/loan/apply',
        'payload': {
            "head": {
                "merchantId": "F21C01MEIT",
                "channelNo": "01",
                "requestSerialNo": 'reqsn',
                "requestTime": 'tradestamp',
                "tenantId": "000"
            },
            "body": {
                "APP_NO": 'appNo',  # self.app_no,
                "LOAN_NO": 'loanNo',
                "APP_ID": "MT",
                "CARD_NO": "bankid",
                "NAME": 'name',
                #"NAME": "陈祺",
                # "NAME": "陈祺",
                "CAREER_TYPE": "",
                "ID_TYPE": "01",
                "ID_NO": "cer_no",
                "CERT_VALID_START_DATE": "20151212",
                "CERT_VALID_END_DATE": "20251212",
                "CARD_BIND_PHONENUMBER": "telephone",
                "CUSTOMER_NO": "CUSTOMER_NO",
                "CONTRACT_NO": "contractno",
                "TRADE_TIME": "tradestamp",
                "TRADE_AMOUNT": 'TRADE_AMOUNT',
                "TRADE_PERIOD": 'TRADE_PERIOD',
                "TENANT_NO": "DL-GDXT",
                "TENANT_NAME": "DL-GDXT",
                "STATEMENT_DATE": 20210408,
                "REPAYMENT_DATE": 20210408,
                "CONNECT_NAME_1": "夔琦萍",
                "CONNECT_PHONENUMBER_1": "16100000446",
                "CONNECT_RELATION_1": "1",
                "CONNECT_NAME_2": "卜慧巧",
                "CONNECT_PHONENUMBER_2": "14300003500",
                "CONNECT_RELATION_2": "2",
                "PURPOSE": "旅游",
                "CREDIT_LIMIT": "CREDIT_LIMIT",
                "AVAILABLE_LIMIT": "AVAILABLE_LIMIT",
                "FUNDPARTY": "TLJR-GDXT",
                "USED_LIMIT": "USED_LIMIT",
                "REPAYMENT_TYPE": "ACPI",
                "RATE": "0.000980",
                "LIVING_VERIFY_PASS": "Y",
                "LIVING_VERIFY_TIMES": "3",
                "LIVING_VERIFY_FAILED": "1",
                "RISK_INFO": {
                    "platform_consuming_ability_level": "1002",
                    "platform_consuming_frequency_level": "1002",
                    "platform_consuming_scene_number_level": "1002",
                    "predicted_age_level": "1002",
                    "predicted_marital_status_level": "1002",
                    "active_city_number_level_last_90d": "1002",
                    "predicted_gender_level": "1002",
                    "account_register_time_level": "1002",
                    "job_category_code": "1002",
                    "resident_province_name": "1002",
                    "user_order_count_level_in_last_180d": "1002",
                    "user_order_count_level_in_last_360d": "1002",
                    "user_order_count_level_in_last_90d": "1002",
                    "user_order_days_level_in_last_180d": "1002",
                    "user_order_days_level_in_last_360d": "1002",
                    "user_order_days_level_in_last_90d": "1002",
                    "user_successful_order_amount_level_in_last_180d": "1002",
                    "user_successful_order_amount_level_in_last_360d": "1002",
                    "user_successful_order_amount_level_in_last_90d": "1002",
                    "user_successful_order_count_level_in_last_180d": "1002",
                    "user_successful_order_count_level_in_last_360d": "1002",
                    "user_successful_order_count_level_in_last_90d": "1002",
                    "user_successful_waimai_order_count_level_in_last_180d": "1002",
                    "user_successful_waimai_order_count_level_in_last_360d": "1002",
                    "user_successful_waimai_order_count_level_in_last_90d": "1002",
                    "user_visit_bg_count_level_in_last_90d": "1002",
                    "user_active_days_in_last_180d_level": "1002",
                    "user_active_days_in_last_360d_level": "1002",
                    "user_active_days_in_last_90d_level": "1002",
                    "user_visit_waimai_days_in_last_180d": "1002",
                    "user_visit_waimai_days_in_last_360d": "1002",
                    "user_visit_waimai_days_in_last_90d": "1002",
                    "user_active_tag_in_1y": "1002",
                    "user_visit_group_buy_days_in_last_180d": "1002",
                    "user_visit_group_buy_days_in_last_360d": "1002",
                    "user_visit_group_buy_days_in_last_90d": "1002",
                    "mt_creditscore_level_v4_0_1": "1002"
                }
            }
        }
    },

    'loan_query': {
        'interface': '/api/v1/meit/loan/resultQuery',
        'payload': {
            "head": {
                "merchantId": "F21C01MEIT",
                "channelNo": "01",
                "requestSerialNo": 'self.app_no',
                "requestTime": 'requestTime',  # 年-月-日 时：分：秒
                "tenantId": "000",
                "token": "000"
            },
            "body": {
                "APP_NO": 'self.app_no',
            }
        }
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