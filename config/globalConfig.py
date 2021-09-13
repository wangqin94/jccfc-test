# # ---------------------------------------------------------
# # - 测试环境静态配置文件
# # - created time: 2021-03-08
# # - version: 1.0
# # ---------------------------------------------------------


API = {
	'request_host': "http://hapi-web-{}.corp.jccfc.com",
	'request_host_fql': "http://api-web-{}.jccfc.com",
	'eureka_host': "https://eureka-{}.corp.jccfc.com/eureka/apps/"
}


headers = {
	"Content-Type": "application/json",
	"Cache-Control": "no-cache",
	"Rpc-Hsjry-Request": "ask=934&answer=921&serialNo=123&idemSerialNo=2019071580720413122&serviceScene=11&transDateTime=2018-11-07 09:49:06&tenantId=000&channelNo=01",
	"Rpc-Hsjry-User-Request": "authId=abcde&token=fghijk&operatorId=admin&organId=000ORG00000000006&&operatorName=a",
	"Accept": "*/*",
	"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
}