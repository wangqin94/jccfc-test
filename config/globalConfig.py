# # ---------------------------------------------------------
# # - 测试环境静态配置文件
# # - created time: 2021-03-08
# # - version: 1.0
# # ---------------------------------------------------------


API = {
    'request_host': "http://hapi-web-{}.corp.jccfc.com",
    'request_host_api': "http://api-web-{}.jccfc.com",
    'eureka_host': "https://eureka-{}.corp.jccfc.com/eureka/apps/",
    'request_job_host': "http://job-admin-{}.corp.jccfc.com",
    'request_apollo_host': "https://apollo-{}.corp.jccfc.com",
    'apollo_index_host': "http://apollo-{}.corp.jccfc.com/",
    'op-channel_host': "http://op-channel-{}.corp.jccfc.com"
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
    'jike': {
        "claimPath": "xdgl/xdnb/pl/accounting/asset/geexClaimFile",
        "bayBackPath": "xdgl/xdnb/pl/accounting/asset/geexBuybackFile"
    },
    'yinliu': {
        "claimPath": "xdgl/xdnb/pl/accounting/asset/geexClaimFile",
        "bayBackPath": "xdgl/xdnb/pl/accounting/asset/geexBuybackFile"
    }
}
