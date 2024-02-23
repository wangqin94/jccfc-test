# 年利率
lixi = 0.24
# 每年计算利息天数
day = 360
# 本金
fee = float(input("输入本金："))

# 每期计算天数,计头不计尾
qi_day = int(input("输入每期天数："))

res = float(lixi/day*fee*qi_day)
faxi = float(lixi/day*fee*1.5*5)
print("每月利息为：", round(res, 2))

print("罚息金额为：", round(faxi, 2))
