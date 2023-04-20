# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：MockServer.py
@Author  ：jccfc
@Date    ：2022/6/6 13:57 
"""
import json
from flask import jsonify, Flask, request
from config.globalConfig import headers
from utils.BankNo import BankNo
from utils.GenName import get_name
from utils.Identity import IdNumber
from utils.Models import decrypt, get_telephone

app = Flask(__name__)  # 创建flask实例，用来接收web请求

getMsg_loan_invoice_no16539809083830 = {
    "data": "h9coJy%2FueB7AK7vGW%2FoXDf8or9x9qkUFjY1ryKI5Y3GvHLG7AVmyerDBcUaAbXYiympiGWB66yTk%0ArUbbtxkbDH5eSemY7EQlCoteOJS8fO73%2BACp4YuSVFk6Wj%2FE4GucJM0Rv4BzJc4FtUGMuxTtMF%2BN%0A%2BkRKKY0w4aCpIcZFph6JwQpsrwl8U3%2ByJMzJMwC3JqJM8FrGDIWE22Z8OYaEBMYI3d%2BOjEcHk4gu%0ASVPCbDWLop81CSP8x4dhbnvIgwM0%2FDzaC3fzvtCCFqWfsz6IP0vDZ2kwHsgsz4Zh0pHe9vmqnkV%2B%0AsnTqhKb%2Flh3OqgIiDC6g6zqQOpWTCtTaXzt4dlBWI4QGxdmbxHWsLslwPJqO%2BXmVwiPat6woM4kS%0AF3qjUadaaWDCl8NamRrDbc0ZkdqY7QkormDW5oY5egVp6ZHsrqj5%2BarWNSfE9EIABuU%2B2aNCSRXj%0AxaIcOn7t21tob0xza4gODBhHMWFyy9gpgltpM7amRLZIfXSxHg9lRu5fLOM%2BfXbVu5jONSf%2BYZYb%0A2QPDOXo7NngrvSScYxXD6hsMme%2Bngm7cdaZ89QDlobxYOk7OQ%2FDfhIyota3bEgvKrxUijaa2Mnpx%0AWoSv2XKOT00BOr8SdfF%2F1BoAA7zzi3jgfjmo36cCFItkOc%2BwOgHMwd%2B0Rj9JoJ7GKlRX8UkKsic1%0A83XjHB%2F3dWeTrm7uvmusFUCnNOHWOX%2FjhzDxpQ80e2oCjYNdIca71ngpok6VriPuYEwIZIN3dF1O%0Ap67Mcswz8xHlvHiquJurJaBX%2BvrSsVG%2BREuOcZArWUjROyOhpOX0OtN63TdIVvmPNh7G9ktnO49R%0A603LqC2YEe5GdNJLax5GxZPfgv64ijS6BYLbY8fwRVlZhQy7emJgFQLEoio4up3bpDQkLfdPUz4H%0ANTrbsGXq52M9%2BOi69HmTICno2loiPByrBZZQlKYsufHnVochZcqQ9UZza%2FKx5ABwM6w6J7kOLOCt%0ASFGGmpN%2F4NvlcYLeVpvaEMTt9AltH8PqhYmxoGSoys8DZteeqXtYQA2mEm1uOBq%2BHN6ySBw0Z7k6%0AOBMxtQx1YYzTLHmbre33g5n%2FczF3KToUFjsT2Ny2l4dv5SIlxG%2Fo5DAaJeKEEBBFd%2Fxc8pKb1I4H%0A%2BA4Un5cI5oDPDAGDfy3BoRcS673XR3ah%2F8QnpLdnlsjxJBxXwpWvKD5NCGzw4Qem7d3HpN00Qadu%0ADSfWBm7f8xcHbd26QE%2FMv4Gh%2B%2FbVifuRfbEeUGc8M1wqj8UZdhv6nJz1RnA9iABqdoEv6TzxYQQ4%0Au5NlZO7MhSdUyaGPu0bhKEbmK34LaX%2FUFqFNsrsBdHu7dNIgHd1MHejZlaZ0eTEQrwAjL1zMMA%3D%3D%0A",
    "sign": "Bg27IYV2td%2Fqx%2Fq%2FELMIawTmV3EX9IOcO1rSV0ADQEkw%2Fjs5FhB%2BywSeHo2P6MXNabWiJ5Lj4DFd%0ANhKcBvof7v6hX3qRTN2cP8wTKKj8Nd%2B6aFab%2BwKAuDNXkxPQsOnN%2Fsy5jKs1lQ16gVfO74nOELuj%0AlzcGhXjzQwuaKKhR1SUXfq9Q0VGdIenSHs0MHqdMyD7LC39V17%2BUlS0qbwfWSH302jlExPdxVJoM%0A6ikXXpMx8kz1BqyV0yEw%2Bm2jQXMLFHrBXYSVNnunhT2FGP8CSFx4jF%2FawsCpYI1%2B7Tt21AQ9mj67%0AgiePWo%2B0mOa18w%2Ft62Ub89EG5WM3%2Ff8Wa4nHXw%3D%3D%0A"
}

loan_invoice_no16467313721115 = {
    "data": "GsJ3IqnFztlLVmgd78x8G8maCmBoeOMswuZ1C7XkVqgHBst54szfZzL93LjPKHjpF3Uj%2FyCIyfjt%0AA32MTE3%2BiPC%2Bc1rLhupbWvpD6ipDwYaUAUKEdOo6hDA1pmLYFOp6O9kI2giqLblUrP7sWa7D6u1F%0AUlDASrilsJfQI2mMdOWwmQsf0g567j6k%2BsFzx%2FYKe%2FrWCQT97Yc8SBWPZCMQuiPPN69JHXpYu1QX%0AFBBNoHrAk1W1hUmO3DTpk2FeaqmM9aw5zPkGF6tV2eYjYc%2BI4iJoAn0A%2B27hvlEiWHEXZyhUPvtd%0ApdaNN0cmOwaIZLoyRTKSfv%2F%2BBuBT%2BQgciEGC%2FotFQp9xuk%2BZTLQhzGSh%2BXJGB7LDgxev9sXCb2KG%0AvB5m%2F3lJE8eQ7IMi%2BIENN5P0V6eBYhp0yrzRpgDQpV%2B64%2BS7bZELBUyJwa4umV7fsKZXhff6snKs%0AWLZ1KPS1uktRvD6fT%2F6jq20huNkubbVCUhs9Q7QFrIJAsPXq0f7euh5yvabARiz%2BNObt6C3Ksbo9%0AvfUc5FIVP27Cx2%2FgV73pOAVEdFs3wa10OEnQpUvJRiLyXIvuoeCTRxqMJHPmIDTA9cP0Mz1oJhpk%0AmUJ5C6X7Rt0R%2Fpjf7ECOjblygkHuGbWZf5zRPiyfgriAy8EE5wBkwKoov0EqgIvhwLVuypfIqcWO%0AcrSPZjeaSDWPz1BgaI40Woionq2GUInx0DihS8w9jmypmHQNULkwCfaMytRWVtB25C0%2Bo2PHvc%2Bo%0ATKrYmQWpTS4%2BTtKrhpfZVOYRT%2FWEVVnrxNNqmwz2fhKj9frf1h5sSgc288oqPhxdJAR8DP2MkWwF%0AVoeGxyHIYjheZuVxnaFTXlzrFh%2FN1DBbBphs52VDnXDS4eaNDsMefV1w3DcuGTZm6lLKt0H8ZMTD%0AVQrCZdB05mWhfIE76Crvrah0fS9hcoacD9NseXkN0w8G7n0WEcO8ChdXkP64sVdGNyV96lerVk3H%0Aqpesv%2FNt0lC5xc2WqsiftVqHaBpQfHf9w5amjCW8GXk77x2QMpn2%2B6SFstTVr0nxiPNx5i7DOTPQ%0A35wO1d1As4q8M%2BIvpG6UUDF6X%2FtrIs8aF77GvUCpUgzZA7sRsrxj96WxfyAll3YGxNvToIkDj8yy%0AF0wU5NhBpuT87PEv2JuHo0WlsIzv80t%2FV1YUdMGWaoNvJHAho1gynAoLOmwWXMC%2BrDJiHWEcGF%2BT%0ArZ9zU%2FpeWeMWK13SVtczEXnkDmTsJAG2sxwedNMEQmKoy4Lucqfb7yMFq42j5zNKszJm7QO9Tr%2Ft%0ANN%2FvkUp9sbSskb6487d9uZLw0AlolAPTNGbOqMKxsdI56zD0U4JdIT4kPYTKjqOUoedKcnIqAQ%3D%3D%0A",
    "sign": "xtLVRfcGmw4p3eV%2BhMBHllTmPPTVBj4a%2BNf1reJ9Q5a09aXTIkYJCuVVyXagaizxl385X%2FiQBLIM%0AfwWaCTJdM8bjy0ZJ8BTSbL03zswVAxJ3VBrX%2BipkcVpEUqJzqA2asNfWDktAhrTuCPZj5jvo%2B%2F0n%0AA4Ce5wxBpv7Xv3AY%2B9%2FeWp0%2BYj9xoA0XDpVFgpYQP0jU826b11SuQfZjugDFUHmkcEOhBzu9cPx%2B%0Ali3JUkd3x4dXGw1YP54Hv6b0AsaVzSzupNG7JEPvGRpfno%2BYxExOrL%2Fp4HRhDYnbvJb7APG4eNxW%0AgR88tVJHYL3m0JjCEdjPbu5RdZDmg2uVSFKRzg%3D%3D%0A"
}

loan_invoice_no16467310568047 = {
    "data": "HbuAtW8nC81ujQm57jWSlIoMQeljGAaV0hpgo6U7FDa%2FdHN45naCscAvK5WfOe5ax1RHUzbkmFA3%0AINzBrYiQZgFn387OtEd%2F%2BPpkPUIqv%2FOjWG5%2BdzAuRxDvMlvxH%2BmbqfEAQMHOXYvgxBPY1hp020yO%0ADIz0EriAiA2w2phfdTVLdqqpAbjF3%2B5SNAe0UBaHbFbrptp3bWHQnLoimTPQfLb7PJ6VNeSK08Nt%0AVYmvV4AAo9oPCsvOkNKmY5C4CyOOdAf7%2BwxKCG6NfScCX2Mzm3MSLXqhHXMBAhnoVcOu7c3g6Tv1%0ASIId5gKP4oQVT7ziIvkJ2L0mZUpNOwC8CeK%2BSIlacOAYYCTc07oxKYys%2BZTlLFGucBLGyQH2JN32%0AbnmBS2U2VaL%2BwfqZbfjbqPFTZRdhEdN1qzfepSaaMvBqzRVsOVpwa9K3maJt%2BjFeZ5DO%2FxNGECuT%0Ag12%2B4bWU8L%2FpJK%2BjHl9pKTzjNepIyu6HszP%2B8%2FJ4gy%2Fw9iujncO6bc4Lu9vh4NJzCL6mVoiylA15%0AaI5Ydur7qyZfRx6obBomPEUCnHabbSFHoDw%2F%2F4lPLTerJkj5xuGVvPooN0AvltUr0mQ7DXgYLzDa%0ANrm%2F9IMVJwguLU%2BXpMPMofv%2FvwX2bioMXmqWU7ODY%2FABzEqVUqUVeukQjceTo9TMGsBcorxwWCwL%0Alauqnww2qqUiPPNCbP%2F6cF1QyC1kuHzt1zudHWfC8XTXGZswes2D1jxy%2BwGunH25uc4x0NBhoKmw%0AtSzvwv5NcnwPx8SbDnVlzNtMMF6N5tpkq0NcIHxPHHuEM6KOHWJWoav0QkCRFvshw9f9Ijfesc9m%0ARlQPtENRwX%2F26UbdfPfQADdZdgMAHhyhaxlJS2Zoe0dJzBoqawZu%2FdNb9jdXTgcP1z4I%2BTR565gw%0AJFrcbFyl0%2BLXznNdclEHAkE63hgWoh%2B3P%2BOlKY634x9G1tCY0b9EjZ6xTTK9acrcFsrqc9UcHyU4%0AckD6U5Fcpx4x0Xqj4kY9rdqkdtcVez8VcKaTQIpeCONqKswhxOb0NMy39xk%2FdhB3MgchToTkkg2s%0AwcMiwx8dxEFKMzGHTTYYpgL4cXLs7fuL4cL0seC0Mkncg%2BVzBMgq%2BBkW2KDWiZT%2BQqoibUirk3NG%0AWtpAzgIX0dTIO3YXfGk6ZomEdMJSxg10lf2kBdF82UOkQBDM1bbpIZOCyNVqiELqzoOM%2BFAZwUhX%0AFANPAlrQI8rQZa1476fc7bX6nfjEUlJjuao1Z1OLnHfUY2VYIsOXK9XjUyteMqYGHy7mqtWhYstK%0AtIudDi2WMAjCtBiXzZUKQJfpNqvvm3fgKTxpkkzylH4q6ZoLaXqfLVAASTi0B3PDJD1BF9wXow%3D%3D%0A",
    "sign": "BQY6N8Dv2XgxIZefzkp%2Fp6MTwr4U0Nly1JNlhwbeJRzWKbgldbUSPkQ3y4Dfl%2FfeJoIw6D6ie9jM%0Aw%2FasD0Ts03tVTLbPst06ixTsPihkvUr%2FpgzvHlm8BAnExCHPNcVXGVW0vcAI1jB8Vnce7Dp0T4Z9%0A%2FemCY4gK5V8YSYVhiEBpMmH4jryoFr32nmmV58%2FEBZ1Uapa%2BHpHeOumSb%2FTjEQ23baqeMX1BaKed%0A8XVZqVYeunmIA0Xr%2FcLDmIytdfI%2F%2FCidcrUTYYxLjJzmYQS%2F4tE%2FfuZF11n9Xk4GfBj2IamCDglJ%0Aa7XcOW3TxvFEZ7IlsHpTLh00onvk0v79MDt%2B5A%3D%3D%0A"
}


@app.route('/api/v1/jincheng/mt_dl/collection_info_query', methods=['GET', 'POST'])  # get post
def get_mock():
    data = request.get_json()
    decrypt_url = "https://hapi-web-hsit.jccfc.com/api/v1/secret/thirdDecryptData/MEIT"
    response = decrypt(decrypt_url, headers, data)
    if response['body']['LOAN_NO'] == 'loan_invoice_no16540678704846':
        return jsonify(getMsg_loan_invoice_no16539809083830)
    if response['body']['LOAN_NO'] == 'loan_invoice_no16467313721115':
        return jsonify(loan_invoice_no16467313721115)
    if response['body']['LOAN_NO'] == 'loan_invoice_no16467310568047':
        return jsonify(loan_invoice_no16467310568047)
    else:
        return jsonify("error")


@app.route('/mock/getTestData', methods=['GET', 'POST'])  # delete
def getTestData_mock():
    data = {'姓名': get_name(), '身份证号': IdNumber.generate_id(), '手机号': get_telephone()}
    # 获取随机生成的手机号
    bank = BankNo()
    data['银行卡号'] = bank.get_bank_card(bankName='工商银行')
    data['银行卡Bin'] = bank.cardBin
    data['银行卡Code'] = bank.bankCode
    print(str(data))
    return json.dumps(data, ensure_ascii=False)


@app.route('/api/fileCheck/batchFileCheck', methods=['GET', 'POST'])  # delete
def batchFileCheck_mock():
    batchFileCheckMsg = {
        "state": "true",
        "code": "0000",
        "message": "成功",
        "data": "None"
    }
    return jsonify(batchFileCheckMsg)


@app.route('/api/fileCheck/query', methods=['GET', 'POST'])  # delete
def fileCheckQuery_mock():
    fileCheckQueryMsg = {
        "state": True,
        "code": "0000",
        "message": "成功",
        "data": [
            {
                "orderNo": "000CA2023041900000005",
                "checkNo": None,
                "orderCheckStatus": 0,
                "fileCheckList": [
                    {
                        "fileType": "06",
                        "file": "xdgl/jike/test/third.pdf",
                        "id": "26530",
                        "checkTime": "2023-04-18 10:00:27",
                        "checkStatus": 1,
                        "ruleList": [
                            {
                                "fileType": None,
                                "ruleId": "RT01",
                                "ruleName": "授权书是否存在",
                                "checkStatus": 1,
                                "checkComment": ""
                            },
                            {
                                "fileType": None,
                                "ruleId": "RT02",
                                "ruleName": "授权书版本号校验",
                                "checkStatus": 1,
                                "checkComment": ""
                            },
                            {
                                "fileType": None,
                                "ruleId": "RT03",
                                "ruleName": "授权主体校验",
                                "checkStatus": 1,
                                "checkComment": ""
                            },
                            {
                                "fileType": None,
                                "ruleId": "RT04",
                                "ruleName": "申请人姓名校验",
                                "checkStatus": 1,
                                "checkComment": ""
                            },
                            {
                                "fileType": None,
                                "ruleId": "RT05",
                                "ruleName": "申请人身份证号校验",
                                "checkStatus": 1,
                                "checkComment": ""
                            },
                            {
                                "fileType": None,
                                "ruleId": "RT06",
                                "ruleName": "授权日期校验",
                                "checkStatus": 1,
                                "checkComment": ""
                            },
                            {
                                "fileType": None,
                                "ruleId": "RT07",
                                "ruleName": "三方授信签章校验",
                                "checkStatus": 1,
                                "checkComment": ""
                            }
                        ],
                        "fileComment": None,
                        "rmk": None
                    },
                    {
                        "fileType": "01",
                        "file": "xdgl/jike/test/front.jpg",
                        "id": "26527",
                        "checkTime": "2023-04-18 10:00:23",
                        "checkStatus": 0,
                        "ruleList": [
                            {
                                "fileType": None,
                                "ruleId": "RB01",
                                "ruleName": "身份证人像页是否存在",
                                "checkStatus": 1,
                                "checkComment": ""
                            },
                            {
                                "fileType": None,
                                "ruleId": "RB02",
                                "ruleName": "身份证号校验",
                                "checkStatus": 0,
                                "checkComment": "error"
                            },
                            {
                                "fileType": None,
                                "ruleId": "RB03",
                                "ruleName": "姓名校验",
                                "checkStatus": 1,
                                "checkComment": ""
                            }
                        ],
                        "fileComment": None,
                        "rmk": None
                    },
                    {
                        "fileType": "04",
                        "file": "xdgl/jike/test/credit.pdf",
                        "id": "26528",
                        "checkTime": "2023-04-18 10:00:26",
                        "checkStatus": 1,
                        "ruleList": [
                            {
                                "fileType": None,
                                "ruleId": "RE01",
                                "ruleName": "授权书是否存在",
                                "checkStatus": 1,
                                "checkComment": ""
                            },
                            {
                                "fileType": None,
                                "ruleId": "RE02",
                                "ruleName": "授权书版本号校验",
                                "checkStatus": 1,
                                "checkComment": ""
                            },
                            {
                                "fileType": None,
                                "ruleId": "RE03",
                                "ruleName": "授权主体校验",
                                "checkStatus": 1,
                                "checkComment": ""
                            },
                            {
                                "fileType": None,
                                "ruleId": "RE04",
                                "ruleName": "申请人姓名校验",
                                "checkStatus": 1,
                                "checkComment": ""
                            },
                            {
                                "fileType": None,
                                "ruleId": "RE05",
                                "ruleName": "申请人身份证号校验",
                                "checkStatus": 1,
                                "checkComment": ""
                            },
                            {
                                "fileType": None,
                                "ruleId": "RE06",
                                "ruleName": "授权日期校验",
                                "checkStatus": 1,
                                "checkComment": ""
                            },
                            {
                                "fileType": None,
                                "ruleId": "RE07",
                                "ruleName": "授信签章校验",
                                "checkStatus": 1,
                                "checkComment": ""
                            }
                        ],
                        "fileComment": None,
                        "rmk": None
                    },
                    {
                        "fileType": "03",
                        "file": "xdgl/jike/test/face.jpg",
                        "id": "26529",
                        "checkTime": "2023-04-18 10:00:25",
                        "checkStatus": 1,
                        "ruleList": [
                            {
                                "fileType": None,
                                "ruleId": "RD01",
                                "ruleName": "自拍照是否存在",
                                "checkStatus": 1,
                                "checkComment": ""
                            },
                            {
                                "fileType": None,
                                "ruleId": "RD03",
                                "ruleName": "人脸比对校验",
                                "checkStatus": 1,
                                "checkComment": ""
                            }
                        ],
                        "fileComment": None,
                        "rmk": None
                    },
                    {
                        "fileType": "02",
                        "file": "xdgl/jike/test/back.jpg",
                        "id": "26526",
                        "checkTime": "2023-04-18 10:00:24",
                        "checkStatus": 1,
                        "ruleList": [
                            {
                                "fileType": None,
                                "ruleId": "RC01",
                                "ruleName": "身份证国徽页是否存在",
                                "checkStatus": 1,
                                "checkComment": ""
                            },
                            {
                                "fileType": None,
                                "ruleId": "RC02",
                                "ruleName": "身份证有效期校验",
                                "checkStatus": 1,
                                "checkComment": ""
                            }
                        ],
                        "fileComment": None,
                        "rmk": None
                    }
                ]
            }
        ]
    }
    return jsonify(fileCheckQueryMsg)


delMsg = {
    'code': 0,
    'msg': 'delete success'
}


@app.route('/mock/deleteMock', methods=['DELETE'])  # delete
def delete_mock():
    return jsonify(delMsg)


putMsg = {
    'code': 0,
    'msg': 'put success'
}


@app.route('/mock/putMock', methods=['PUT'])  # put
def put_mock():
    return jsonify(putMsg)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8888,
        debug=True
    )
