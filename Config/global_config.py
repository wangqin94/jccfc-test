# # ---------------------------------------------------------
# # - 测试环境静态配置文件
# # - created time: 2021-03-08
# # - version: 1.0
# # ---------------------------------------------------------
from Config.TestEnvInfo import *
from Config.feature_config import *

ENV = {
    'hsit': {
        'database': {
            'hsit_mysql': {
                'host': 'mysql03-dev.jccfc.io',
                'port': 3314,
                'username': 'hsit',
                'password': 'f8FHhqJZlLfWTKkk'},
            'hsit_credit': {
                "host": "mysql03-dev.jccfc.io",
                "port": 3314,
                "databaseName": "hsit_credit",
                "username": "credit",
                "password": "i7OeSO5241JRMKQR"
            },
            'hsit_asset': {
                "host": "mysql03-dev.jccfc.io",
                "port": 3314,
                "databaseName": "hsit_asset",
                "username": "asset",
                "password": "i7OeSO5241JRMKQR"
            },
            'hsit_user': {
                "host": "mysql03-dev.jccfc.io",
                "port": 3314,
                "databaseName": "hsit_user",
                "username": "user",
                "password": "i7OeSO5241JRMKQR"
            },
        },
        'request_host': "http://hapi-web-hsit.corp.jccfc.com",
        'request_host_fql': "http://api-web-hsit.jccfc.com",
        'eureka_host': 'https://eureka-hsit.corp.jccfc.com/eureka/apps/',
    },

    'huat': {
        'database': {
            'huat_mysql': {
                'host': 'mysql03-dev.jccfc.io',
                'port': 3315,
                'username': 'huat',
                'password': 'f8FHhqJZlLfWTKkk'},
            'huat_credit': {
                "host": "mysql03-dev.jccfc.io",
                "port": 3315,
                "databaseName": "huat_credit",
                "username": "credit",
                "password": "i7OeSO5241JRMKQR"
            },
            'huat_asset': {
                "host": "mysql03-dev.jccfc.io",
                "port": 3315,
                "databaseName": "huat_asset",
                "username": "asset",
                "password": "i7OeSO5241JRMKQR"
            },
            'huat_user': {
                "host": "mysql03-dev.jccfc.io",
                "port": 3315,
                "databaseName": "huat_user",
                "username": "user",
                "password": "i7OeSO5241JRMKQR"
            },
        },
        'request_host': "http://hapi-web-huat.corp.jccfc.com",
        'request_host_fql': "http://api-web-huat.jccfc.com",
        'eureka_host': 'https://eureka-huat.corp.jccfc.com/eureka/apps/',
    },

    'qas': {
        'database': {
            'qas_mysql': {
                'host': 'mysql01-qas.jccfc.io',
                'port': 3306,
                'username': 'qas',
                'password': 'f8FHhqJZlLfWTKkk'},
            'qas_credit': {
                "host": "mysql01-qas.jccfc.io",
                "port": 3306,
                "databaseName": "qas_credit",
                "username": "credit",
                "password": "jdRyUbIKrdZoByrT"
            },
            'qas_user': {
                "host": "mysql01-qas.jccfc.io",
                "port": 3306,
                "databaseName": "qas_user",
                "username": "user",
                "password": "i7OeSO5241JRMKQR"
            },
        },
        'request_host': "https://hapi-web-qas.corp.jccfc.com",
        'eureka_host': 'https://eureka-qas.corp.jccfc.com/eureka/apps/',
    },

    'hdev': {
        'database': {
            'hdev_mysql': {
                'host': 'mysql03-dev.jccfc.io',
                'port': 3313,
                'username': 'hdev',
                'password': 'f8FHhqJZlLfWTKkk'},
            'hdev_credit': {
                "host": "mysql03-dev.jccfc.io",
                "port": 3313,
                "databaseName": "hdev_credit",
                "username": "credit",
                "password": "i7OeSO5241JRMKQR"
            },
            'hdev_asset': {
                "host": "mysql03-dev.jccfc.io",
                "port": 3313,
                "databaseName": "hdev_asset",
                "username": "asset",
                "password": "i7OeSO5241JRMKQR"
            },
            'hdev_user': {
                "host": "mysql03-dev.jccfc.io",
                "port": 3313,
                "databaseName": "hdev_user",
                "username": "user",
                "password": "i7OeSO5241JRMKQR"
            },
        },
        'request_host': "http://hapi-web-hdev.corp.jccfc.com",
        'request_host_fql': "http://api-web-hdev.jccfc.com",
        'eureka_host': 'https://eureka-qas.corp.jccfc.com/eureka/apps/',
    },

    'hpre': {
        'database': {
            'hpre_mysql': {
                'host': 'mysql03-dev.jccfc.io',
                'port': 3316,
                'username': 'wdf',
                'password': 'a25Llo0YkFUWdlMA'},
            'hpre_credit': {
                "host": "mysql03-dev.jccfc.io",
                "port": 3316,
                "databaseName": "hpre_credit",
                "username": "hpre_credit",
                "password": "SnPKcxunUeFKe7gj"
            },
            'hpre_asset': {
                "host": "mysql03-dev.jccfc.io",
                "port": 3316,
                "databaseName": "hpre_asset",
                "username": "hpre_asset",
                "password": "ZFjSfZx8ptjbivgI"
            },
            'hpre_user': {
                "host": "mysql03-dev.jccfc.io",
                "port": 3316,
                "databaseName": "hpre_user",
                "username": "hpre_user",
                "password": "xXgM6HuBtsDd7lfu"
            },
        },
        'request_host': "http://hapi-web-hpre.corp.jccfc.com",
        'request_host_fql': "http://api-web-hpre.jccfc.com",
        'eureka_host': 'https://eureka-qas.corp.jccfc.com/eureka/apps/',
    },

    'hqas': {
        'database': {
            'hqas_mysql': {
                'host': 'mysql03-dev.jccfc.io',
                'port': 3324,
                'username': 'chenxb',
                'password': 'JHvIhunDY6PpTvbL'},
            'hqas_credit': {
                "host": "mysql03-dev.jccfc.io",
                "port": 3324,
                "databaseName": "hqas_credit",
                "username": "credit",
                "password": "VbiLThOznRpTKWPg"
            },
            'hqas_asset': {
                "host": "mysql03-dev.jccfc.io",
                "port": 3324,
                "databaseName": "hqas_asset",
                "username": "asset",
                "password": "VbiLThOznRpTKWPg"
            },
            'hqas_user': {
                "host": "mysql03-dev.jccfc.io",
                "port": 3324,
                "databaseName": "hqas_user",
                "username": "user",
                "password": "VbiLThOznRpTKWPg"
            },
        },
        'request_host': "http://hapi-web-hqas.corp.jccfc.com",
        'request_host_fql': "http://api-web-hqas.jccfc.com",
        'eureka_host': 'https://eureka-hqas.corp.jccfc.com/eureka/apps/',
    },
}

Env = {
    'database': {
        '%s_mysql' % TEST_ENV_INFO: {
            'host': 'mysql03-dev.jccfc.io',
            'port': 3306,
            'username': TEST_ENV_INFO,
            'password': 'f8FHhqJZlLfWTKkk'},
        '%s_credit' % TEST_ENV_INFO: {
            "host": 'mysql03-dev.jccfc.io',
            "port": 3306,
            "databaseName": "%s_credit" % TEST_ENV_INFO,
            "username": "credit",
            "password": "i7OeSO5241JRMKQR"},
        '%s_asset' % TEST_ENV_INFO: {
            "host": 'mysql03-dev.jccfc.io',
            "port": 3306,
            "databaseName": "%s_asset" % TEST_ENV_INFO,
            "username": "asset",
            "password": "i7OeSO5241JRMKQR"},
        '%s_user' % TEST_ENV_INFO: {
            "host": 'mysql03-dev.jccfc.io',
            "port": 3306,
            "databaseName": "%s_user" % TEST_ENV_INFO,
            "username": "user",
            "password": "i7OeSO5241JRMKQR"},
    },
    'request_host': "http://hapi-web-%s.corp.jccfc.com" % TEST_ENV_INFO,
    'eureka_host': 'https://eureka-%s.corp.jccfc.com/eureka/apps/' % TEST_ENV_INFO,
}

headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
    "Rpc-Hsjry-Request": "ask=934&answer=921&serialNo=123&idemSerialNo=2019071580720413122&serviceScene=\
                         11&transDateTime=2018-11-07 09:49:06&tenantId=000&channelNo=01",
    "Rpc-Hsjry-User-Request": "authId=abcde&token=fghijk&operatorId=admin&organId=000ORG00000000006&&operatorName=a",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
}

CommonConfig = {
    'four_element_addr': 'http://10.10.100.153:8081/getTestData',
    'header': {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "Rpc-Hsjry-Request": "ask=934&answer=921&serialNo=123&idemSerialNo=2019071580720413122&serviceScene=11&transDateTime=2018-11-07 09:49:06&tenantId=000&channelNo=01",
        "Rpc-Hsjry-User-Request": "authId=abcde&token=fghijk&operatorId=admin&organId=000ORG00000000006&&operatorName=a",
        "Accept": "*/*",
        "User-Agent": "PostmanRuntime/7.21.0",
    }
}
