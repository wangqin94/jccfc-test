# -*- coding: UTF-8 -*-
"""
@Project ：jccfc-test 
@File    ：GenName.py
@Author  ：jccfc
@Date    ：2022/7/12 17:10 
"""

# 508个常用姓氏
import random

xing_shi = ["赵", "钱", "孙", "李", "周", "吴", "郑", "王", "冯", "陈", "褚", "卫", "蒋", "沈", "韩", "杨", "朱", "秦", "尤", "许",
            "何", "吕", "施", "张", "孔", "曹", "严", "华", "金", "魏", "陶", "姜", "戚", "谢", "邹", "喻", "柏", "水", "窦", "章",
            "云", "苏", "潘", "葛", "奚", "范", "彭", "郎", "鲁", "韦", "昌", "马", "苗", "凤", "花", "方", "俞", "任", "袁", "柳",
            "酆", "鲍", "史", "唐", "费", "廉", "岑", "薛", "雷", "贺", "倪", "汤", "滕", "殷", "罗", "毕", "郝", "邬", "安", "常",
            "乐", "于", "时", "傅", "皮", "卞", "齐", "康", "伍", "余", "元", "卜", "顾", "孟", "平", "黄", "和", "穆", "萧", "尹",
            "姚", "邵", "湛", "汪", "祁", "毛", "禹", "狄", "米", "贝", "明", "臧", "计", "伏", "成", "戴", "谈", "宋", "茅", "庞",
            "熊", "纪", "舒", "屈", "项", "祝", "董", "粱", "杜", "阮", "蓝", "闵", "席", "季", "麻", "强", "贾", "路", "娄", "危",
            "江", "童", "颜", "郭", "梅", "盛", "林", "刁", "钟", "徐", "邱", "骆", "高", "夏", "蔡", "田", "樊", "胡", "凌", "霍",
            "虞", "万", "支", "柯", "昝", "管", "卢", "莫", "经", "房", "裘", "缪", "干", "解", "应", "宗", "丁", "宣", "贲", "邓",
            "郁", "单", "杭", "洪", "包", "诸", "左", "石", "崔", "吉", "钮", "龚", "程", "嵇", "邢", "滑", "裴", "陆", "荣", "翁",
            "荀", "羊", "於", "惠", "甄", "麴", "家", "封", "芮", "羿", "储", "靳", "汲", "邴", "糜", "松", "井", "段", "富", "巫",
            "乌", "焦", "巴", "弓", "牧", "隗", "山", "谷", "车", "侯", "宓", "蓬", "全", "郗", "班", "仰", "秋", "仲", "伊", "宫",
            "宁", "仇", "栾", "暴", "甘", "钭", "厉", "戎", "祖", "武", "符", "刘", "景", "詹", "束", "龙", "叶", "幸", "司", "韶",
            "郜", "黎", "蓟", "薄", "印", "宿", "白", "怀", "蒲", "邰", "从", "鄂", "索", "咸", "籍", "赖", "卓", "蔺", "屠", "蒙",
            "池", "乔", "阴", "欎", "胥", "能", "苍", "双", "闻", "莘", "党", "翟", "谭", "贡", "劳", "逄", "姬", "申", "扶", "堵",
            "冉", "宰", "郦", "雍", "舄", "璩", "桑", "桂", "濮", "牛", "寿", "通", "边", "扈", "燕", "冀", "郏", "浦", "尚", "农",
            "温", "别", "庄", "晏", "柴", "瞿", "阎", "充", "慕", "连", "茹", "习", "宦", "艾", "鱼", "容", "向", "古", "易", "慎",
            "戈", "廖", "庾", "终", "暨", "居", "衡", "步", "都", "耿", "满", "弘", "匡", "国", "文", "寇", "广", "禄", "阙", "东",
            "殴", "殳", "沃", "利", "蔚", "越", "夔", "隆", "师", "巩", "厍", "聂", "晁", "勾", "敖", "融", "冷", "訾", "辛", "阚",
            "那", "简", "饶", "空", "曾", "毋", "沙", "乜", "养", "鞠", "须", "丰", "巢", "关", "蒯", "相", "查", "後", "荆", "红",
            "游", "竺", "权", "逯", "盖", "益", "桓", "公", "万俟", "司马", "上官", "欧阳", "夏侯", "诸葛", "闻人", "东方", "赫连",
            "皇甫", "尉迟", "公羊", "澹台", "公冶", "宗政", "濮阳", "淳于", "单于", "太叔", "申屠", "公孙", "仲孙", "轩辕", "令狐",
            "钟离", "宇文", "长孙", "慕容", "鲜于", "闾丘", "司徒", "司空", "亓官", "司寇", "仉", "督", "子车", "颛孙", "端木",
            "巫马", "公西", "漆雕", "乐正", "壤驷", "公良", "拓跋", "夹谷", "宰父", "谷梁", "晋", "楚", "闫", "法", "汝", "鄢",
            "涂", "钦", "段干", "百里", "东郭", "南门", "呼延", "归", "海", "羊舌", "微生", "岳", "帅", "缑", "亢", "况", "后",
            "有", "琴", "梁丘", "左丘", "东门", "西门", "商", "牟", "佘", "佴", "伯", "赏", "南宫", "墨", "哈", "谯", "笪", "年",
            "爱", "阳", "佟", "第五", "言", "福", "百", "家", "姓", "终"]
# 537个常用名
xing_ming = ['梦琪', '忆柳', '之桃', '慕青', '问兰', '尔岚', '元香', '初夏', '沛菡', '傲珊', '曼文', '乐菱', '痴珊', '恨玉', '惜文',
             '香寒', '新柔', '语蓉', '海安', '夜蓉', '涵柏', '水桃', '醉蓝', '春儿', '语琴', '从彤', '傲晴', '语兰', '又菱', '碧彤',
             '元霜', '怜梦', '紫寒', '妙彤', '曼易', '南莲', '紫翠', '雨寒', '易烟', '如萱', '若南', '寻真', '晓亦', '向珊', '慕灵',
             '以蕊', '寻雁', '映易', '雪柳', '孤岚', '笑霜', '海云', '凝天', '沛珊', '寒云', '冰旋', '宛儿', '绿真', '盼儿', '晓霜',
             '碧凡', '夏菡', '曼香', '若烟', '半梦', '雅绿', '冰蓝', '灵槐', '平安', '书翠', '翠风', '香巧', '代云', '梦曼', '幼翠',
             '友巧', '听寒', '梦柏', '醉易', '访旋', '亦玉', '凌萱', '访卉', '怀亦', '笑蓝', '春翠', '靖柏', '夜蕾', '冰夏', '梦松',
             '书雪', '乐枫', '念薇', '靖雁', '寻春', '恨山', '从寒', '忆香', '觅波', '静曼', '凡旋', '以亦', '念露', '芷蕾', '千兰',
             '新波', '代真', '新蕾', '雁玉', '冷卉', '紫山', '千琴', '恨天', '傲芙', '盼山', '怀蝶', '冰兰', '山柏', '翠萱', '恨松',
             '问旋', '从南', '白易', '问筠', '如霜', '半芹', '丹珍', '冰彤', '亦寒', '寒雁', '怜云', '寻文', '乐丹', '翠柔', '谷山',
             '之瑶', '冰露', '尔珍', '谷雪', '乐萱', '涵菡', '海莲', '傲蕾', '青槐', '冬儿', '易梦', '惜雪', '宛海', '之柔', '夏青',
             '亦瑶', '妙菡', '春竹', '痴梦', '紫蓝', '晓巧', '幻柏', '元风', '冰枫', '访蕊', '南春', '芷蕊', '凡蕾', '凡柔', '安蕾',
             '天荷', '含玉', '书兰', '雅琴', '书瑶', '春雁', '从安', '夏槐', '念芹', '怀萍', '代曼', '幻珊', '谷丝', '秋翠', '白晴',
             '海露', '代荷', '含玉', '书蕾', '听白', '访琴', '灵雁', '秋春', '雪青', '乐瑶', '含烟', '涵双', '平蝶', '雅蕊', '傲之',
             '灵薇', '绿春', '含蕾', '从梦', '从蓉', '初丹', '听兰', '听蓉', '语芙', '夏彤', '凌瑶', '忆翠', '幻灵', '怜菡', '紫南',
             '依珊', '妙竹', '访烟', '怜蕾', '映寒', '友绿', '冰萍', '惜霜', '凌香', '芷蕾', '雁卉', '迎梦', '元柏', '代萱', '紫真',
             '千青', '凌寒', '紫安', '寒安', '怀蕊', '秋荷', '涵雁', '以山', '凡梅', '盼曼', '翠彤', '谷冬', '新巧', '冷安', '千萍',
             '冰烟', '雅阳', '友绿', '南松', '诗云', '飞风', '寄灵', '书芹', '幼蓉', '以蓝', '笑寒', '忆寒', '秋烟', '芷巧', '水香',
             '映之', '醉波', '幻莲', '夜山', '芷卉', '向彤', '小玉', '幼南', '凡梦', '尔曼', '念波', '迎松', '青寒', '笑天', '涵蕾',
             '碧菡', '映秋', '盼烟', '忆山', '以寒', '寒香', '小凡', '代亦', '梦露', '映波', '友蕊', '寄凡', '怜蕾', '雁枫', '水绿',
             '曼荷', '笑珊', '寒珊', '谷南', '慕儿', '夏岚', '友儿', '小萱', '紫青', '妙菱', '冬寒', '曼柔', '语蝶', '青筠', '夜安',
             '觅海', '问安', '晓槐', '雅山', '访云', '翠容', '寒凡', '晓绿', '以菱', '冬云', '含玉', '访枫', '含卉', '夜白', '冷安',
             '灵竹', '醉薇', '元珊', '幻波', '盼夏', '元瑶', '迎曼', '水云', '访琴', '谷波', '乐之', '笑白', '之山', '妙海', '紫霜',
             '平夏', '凌旋', '孤丝', '怜寒', '向萍', '凡松', '青丝', '翠安', '如天', '凌雪', '绮菱', '代云', '南莲', '寻南', '春文',
             '香薇', '冬灵', '凌珍', '采绿', '天春', '沛文', '紫槐', '幻柏', '采文', '春梅', '雪旋', '盼海', '映梦', '安雁', '映容',
             '凝阳', '访风', '天亦', '平绿', '盼香', '觅风', '小霜', '雪萍', '半雪', '山柳', '谷雪', '靖易', '白薇', '梦菡', '飞绿',
             '如波', '又晴', '友易', '香菱', '冬亦', '问雁', '妙春', '海冬', '半安', '平春', '幼柏', '秋灵', '凝芙', '念烟', '白山',
             '从灵', '尔芙', '迎蓉', '念寒', '翠绿', '翠芙', '靖儿', '妙柏', '千凝', '小珍', '天巧', '妙旋', '雪枫', '夏菡', '元绿',
             '痴灵', '绮琴', '雨双', '听枫', '觅荷', '凡之', '晓凡', '雅彤', '香薇', '孤风', '从安', '绮彤', '之玉', '雨珍', '幻丝',
             '代梅', '香波', '青亦', '元菱', '海瑶', '飞槐', '听露', '梦岚', '幻竹', '新冬', '盼翠', '谷云', '忆霜', '水瑶', '慕晴',
             '秋双', '雨真', '觅珍', '丹雪', '从阳', '元枫', '痴香', '思天', '如松', '妙晴', '谷秋', '妙松', '晓夏', '香柏', '巧绿',
             '宛筠', '碧琴', '盼兰', '小夏', '安容', '青曼', '千儿', '香春', '寻双', '涵瑶', '冷梅', '秋柔', '思菱', '醉波', '醉柳',
             '以寒', '迎夏', '向雪', '香莲', '以丹', '依凝', '如柏', '雁菱', '凝竹', '宛白', '初柔', '南蕾', '书萱', '梦槐', '香芹',
             '南琴', '绿海', '沛儿', '晓瑶', '听春', '凝蝶', '紫雪', '念双', '念真', '曼寒', '凡霜', '飞雪', '雪兰', '雅霜', '从蓉',
             '冷雪', '靖巧', '翠丝', '觅翠', '凡白', '乐蓉', '迎波', '丹烟', '梦旋', '书双', '念桃', '夜天', '海桃', '青香', '恨风',
             '安筠', '觅柔', '初南', '秋蝶', '千易', '安露', '诗蕊', '山雁', '友菱', '香露', '晓兰', '白卉', '语山', '冷珍', '秋翠',
             '夏柳', '如之', '忆南', '书易', '翠桃', '寄瑶', '如曼', '问柳', '香梅', '幻桃', '又菡', '春']


def get_name():
    return xing_shi[random.randrange(0, 508, 1)] + xing_ming[random.randrange(0, 537, 1)]


if __name__ == "__main__":
    name = get_name()
    print(name)
