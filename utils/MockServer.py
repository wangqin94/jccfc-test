# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：MockServer.py
@Author  ：jccfc
@Date    ：2022/6/6 13:57 
"""
from flask import jsonify, Flask, request

from config.globalConfig import headers
from utils.Models import decrypt

app = Flask(__name__)  # 创建flask实例，用来接收web请求

getMsg_loan_invoice_no16539809083830 = {
    "data": "Ntp%2BNd0nrxTznFOcj79b%2BAut5uyK5LgHyWvYd4%2BQA2eZ%2BpiRgYh3xvi%2B6pRfkJGK3wE%2B6cfPEQB%2F%0ArG%2BKWIRrCDrTw7GNZIik2cuJI7x3SUnKFsuchoLBKNjlGEGgNJwDAhYmnB%2B8IqWfj9JA%2BS9Yy280%0AIkxziDec2SzuKhJsk9kmxxBux%2FOOQGA0%2B3P9LfOEP6keMdwC%2FfrmMP5DxgtrdEJDmo7cQBe%2FXKKF%0AaUxheG1EQopSzsdaJdXcjsZ%2F%2FIZpsVNQlqpieykMGdMVGkKyX9RiRv4AmhKo%2FxjQcjcww%2Fy2TpMe%0AcjIdD1o1GIYb103FJN%2F%2FDhoMpoHhu0YELNKmPhH2B%2Fj7JYrw0%2B1UnK7G21E1JYlIVU4BSia%2B45P%2F%0ADJdYtUgLke0yVUT0SO07gLd6K7%2F9071480ZZ%2BvyGKNG1AuJ4QPbMqOgSaiMl25SLS61wV2tkaZwd%0A6Nz6AVw0dJdHfe02%2FBe4cdccCGWXDCIpMlvz0ZHnYc%2FBWpfPufPXjdzU7Nbm4zGZLcK7ptY5NtPx%0A443gjQNx%2FpVYfwlpbdP7G5ttydCvscAkRAhxLba4B5%2FFoJ0BQ%2Bza0Bub9cvp0AQGR1a9KCUKCJr7%0AgpVH81LtcGg4BDyx89UJCEGhVSFCQ0qQ4dXcLcfWECflt1XQQOr3cpEIURbawKqCmkWkMDvoOtcI%0A%2FxYFZ5%2BYHm%2FUvUak4C2UiyVfxwQ8eCd0f8sM8IeomwAprCLsUODpriDXvWVxxzm8a32HOw0yns2s%0AyVnLYFwgvbbS0jKVsI%2FI3MrMLo2BM6X22aNuqZVrbXfD%2F1q8BuFi%2BTfQXEoO5bBLLPGDFcdTkRPc%0AFPPSIT%2BlhdAHoxyjiGSOPKcGe7crHfsOAv6vOjYlpzwHeKxfSDUm1hdsva2CmhmK912Zn69ltcQ5%0AfXEqqRDUoCKI6k7z709HhedJWFKG%2Fmy%2Fo8kLqi9tQIcDCB%2BWHBTAuAbieuzzTnMYDWfB9UPP1gha%0AYHi0ismvV%2FdZ1KQsINz5hXZB1q9cmRlC11SAkfSd0FtwHptlts9u165udQgF5%2BT7YVO6L6sMuga8%0AGrFu9YDc%2F6%2Blp78vpNFN1%2B9khZ99BIjP1G8YLxZFveltmxN%2BY8T%2FLO5JMPIFu%2BGpT2A3WgvqnV8a%0Ah96fWCs4qzvZqoBCk%2Bi6M44Ep1e4B%2BEMY9hWrijjJ8FVRwxpLJEpPHKYolwkckTJPy8jPQHTa%2FZt%0Avu4hqNaW9ruxC%2FfMzB35guY8u3yzNypyUTRlvdUYX5zoOZ1k0sJLvo%2Bp7u5N8%2BVEBSQMFg7n5KGx%0AaDmJJiDkLcV7Wo29Ptri7ts7rEQQtyjCEvGvf3drQpYGoOgc%2F2nUTlHVKO6lK8hX%2FO5HDy0dDw%3D%3D%0A",
    "sign": "k9IS8SKwslftB1kpB4W6XDWTOwDg1cyk%2FdIDtNqDD9S2McAP1nPpPEfuagF2O9MRi%2FE3E64fbS%2F6%0A%2BbXU301jLeRrvzYJA0wvC3Jb7FUJ2P%2B9gObjbgcXz8uYHNlFRN24RoE65p8blKvz9eNg1JltSaJC%0AQeSdmwcTHR4%2BDakFN4vUyW1M1VpsyOVdXJCkJR9hAo4G6Npy%2FDpRq4qqAH9PvC55TNbN3AH5kJc3%0AQvt9WRMQkGj%2FnfLq6XsO6WLZOcqpeKYEpGVco%2Fap6gMSCfA9aeqEm%2BUATl6KH9UteswbFT0D1d6d%0AD45rt8LZKsqBHUqh25yKFjpwQl42qK0%2FMQm8fw%3D%3D%0A"
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
    if response['body']['LOAN_NO'] == 'loan_invoice_no16539809083830':
        return jsonify(getMsg_loan_invoice_no16539809083830)
    if response['body']['LOAN_NO'] == 'loan_invoice_no16467313721115':
        return jsonify(loan_invoice_no16467313721115)
    if response['body']['LOAN_NO'] == 'loan_invoice_no16467310568047':
        return jsonify(loan_invoice_no16467310568047)
    else:
        return jsonify("error")


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
