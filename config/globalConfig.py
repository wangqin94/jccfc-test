# # ---------------------------------------------------------
# # - 测试环境静态配置文件
# # - created time: 2021-03-08
# # - version: 1.0
# # ---------------------------------------------------------


API = {
    'request_host': "https://hapi-web-{}.corp.jccfc.com",
    'request_host_api': "https://api-web-{}.jccfc.com",
    'eureka_host': "https://eureka-{}.corp.jccfc.com/eureka/apps/",
    'request_job_host': "https://job-admin-{}.corp.jccfc.com",
    'request_apollo_host': "https://apollo-{}.corp.jccfc.com",
    'apollo_index_host': "http://apollo-{}.corp.jccfc.com/",
    'op-channel_host': "https://op-channel-{}.corp.jccfc.com",
    'cms_host': "https://cms-{}.corp.jccfc.com",
    'platform_host': "https://platform-{}.corp.jccfc.com",
}

headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
    "Rpc-Hsjry-Request": "ask=934&answer=921&serialNo=123456789&idemSerialNo=2019071580720413122&serviceScene=11&transDateTime=2018-11-07 09:49:06&tenantId=000&channelNo=01",
    "Rpc-Hsjry-User-Request": "authId=abcde&token=fghijk&operatorId=admin&organId=000ORG00000000006&&operatorName=a",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
}

headers_en = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Cache-Control": "no-cache",
    "Rpc-Hsjry-Request": "ask=934&answer=921&serialNo=123&idemSerialNo=2019071580720413122&serviceScene=11&transDateTime=2018-11-07 09:49:06&tenantId=000&channelNo=01",
    "Rpc-Hsjry-User-Request": "authId=abcde&token=fghijk&operatorId=admin&organId=000ORG00000000006&&operatorName=a",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
}

job_headers = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cache-Control": "no-cache",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
}

apollo_headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Cache-Control": "no-cache",
    "Referer": "https://apollo-hdev.corp.jccfc.com",
    "Origin": "https://apollo-hdev.corp.jccfc.com",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
}

cms_headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Encode-Rpc-Hsjry-Request": "YXNrPTk2MiZhbnN3ZXI9OTE4JnNlcmlhbE5vPUNEM0FBNDVGNEM1ODBFNEU4MjU4NUEyNzcxMTAwQTBDJmlkZW1TZXJpYWxObz1GQ0FFNEU3RDQzMUUyNjQ3MzUwODRDMDFBMTNDQzY0MiZzZXJ2aWNlU2NlbmU9MTEmdHJhbnNEYXRlVGltZT0yMDIzLTA4LTA5IDExOjI0OjMxJnRlbmFudElkPTAwMCZjaGFubmVsTm89MDYmc2lnbj0x",
    "Encode-Rpc-Hsjry-User-Request": "YXV0aElkPXVuZGVmaW5lZCZ0b2tlbj11bmRlZmluZWQmb3BlcmF0b3JJZD11bmRlZmluZWQmb3BlcmF0b3JOYW1lPXVuZGVmaW5lZCZvcmdhbklkPXVuZGVmaW5lZCZvcmdhbk5hbWU9dW5kZWZpbmVk",
    "Accept": "*/*",
    "Date": "Wed, 09 Aug 2023 16:18:31 GMT",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

json_headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
}

sftp_path = {
    'meituan': {
        "bank_loan_create": "/hj/xdgl/meituan/bank_loan_create",
        "bank_period_create": "/hj/xdgl/meituan/bank_period_create",
        "bank_repay_loan": "/hj/xdgl/meituan/bank_repay_loan",
        "bank_repay_period": "/hj/xdgl/meituan/bank_repay_period"}
}

ks3_asset_path = {
    'asset': "xdgl/xdnb/pl/accounting/asset",
    'jike': {
        "claimPath": "xdgl/xdnb/pl/accounting/asset/geexClaimFile",
        "bayBackPath": "xdgl/xdnb/pl/accounting/asset/geexBuybackFile"
    },
    'yinliu': {
        "claimPath": "xdgl/xdnb/pl/accounting/asset/geexClaimFile",
        "bayBackPath": "xdgl/xdnb/pl/accounting/asset/geexBuybackFile"
    },
    'hair': {
        "bayBackPath": "xdgl/xdnb/pl/accounting/asset/disPreBuyBack",
        "disInterestPath": "xdgl/xdnb/pl/accounting/asset/disInterestDetail"
    }
}
