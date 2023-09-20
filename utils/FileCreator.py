import os
import random

from PIL import ImageFont, ImageDraw, Image
from fpdf import FPDF

from config.TestEnvInfo import TEST_ENV_INFO
from utils.ID_address import ID_address
from utils.Models import get_base_data


def create_cer_image(person=None, fileName=None):
    if person is None:
        person = get_base_data(TEST_ENV_INFO)
    p_path = os.path.abspath(os.path.dirname(__file__))
    image_path = p_path[:p_path.index("jccfc-test") + len("jccfc-test")]
    if person['sex'] == 1:
        image_path = f"{image_path}/image/idz_nan{random.randint(1, 5)}.jpg"
    else:
        image_path = f"{image_path}/image/idz_nv{random.randint(1, 5)}.jpg"
    front_img = Image.open(image_path)
    fontpath = "font/simsun.ttc"
    fontpath_d = "font/arial.ttf"
    font_ch = ImageFont.truetype(fontpath, 19, encoding="unic")
    font_d = ImageFont.truetype(fontpath_d, 20)
    draw = ImageDraw.Draw(front_img)
    draw.text((85, 32), person['name'], font=font_ch, fill=(0, 0, 0))
    if person['sex'] == 2:
        draw.text((95, 75), '女', font=font_ch, fill=(0, 0, 0))
    else:
        draw.text((95, 75), '男', font=font_ch, fill=(0, 0, 0))
    draw.text((210, 75), '汉', font=font_ch, fill=(0, 0, 0))
    draw.text((95, 120), person['cer_no'][6:10], font=font_d, fill=(0, 0, 0))
    draw.text((180, 120), person['cer_no'][10:12], font=font_d, fill=(0, 0, 0))
    draw.text((230, 120), person['cer_no'][12:14], font=font_d, fill=(0, 0, 0))
    address = f"{ID_address[person['cer_no'][0:6]]}xxx街道xxx小区xx幢"
    if len(address) > 13:
        address = f"{address[:13]}\n{address[13:]}"
    draw.text((95, 165), address, font=font_ch, fill=(0, 0, 0))
    draw.text((165, 275), person['cer_no'], font=font_d, fill=(0, 0, 0))

    front_img.save(
        p_path[:p_path.index("jccfc-test") + len("jccfc-test")] + f'/image/temp/front{person["name"]}.png')

    image_path_back_path = p_path[:p_path.index("jccfc-test") + len("jccfc-test")] + "/image/idf.jpg"
    back_image = Image.open(image_path_back_path)
    draw = ImageDraw.Draw(back_image)
    draw.text((230, 250), f"{ID_address[person['cer_no'][0:6]]}公安局", font=font_ch, fill=(0, 0, 0))
    draw.text((230, 290), "2011.09.05-2031.09.05", font=font_d, fill=(0, 0, 0))
    back_image.save(
        p_path[:p_path.index("jccfc-test") + len("jccfc-test")] + f'/image/temp/back{person["name"]}.png')

    person['front'] = p_path[:p_path.index("jccfc-test") + len(
        "jccfc-test")] + f'/image/temp/front{person["name"]}.png'
    person['back'] = p_path[
                     :p_path.index("jccfc-test") + len("jccfc-test")] + f'/image/temp/back{person["name"]}.png'
    return person


def create_attachment_image(person, imageName):
    fontPath = "font/simsun.ttc"
    fontPath_d = "font/arial.ttf"
    p_path = os.path.abspath(os.path.dirname(__file__))
    font_t = ImageFont.truetype(fontPath, 40, encoding="unic")
    font_ch = ImageFont.truetype(fontPath, 20, encoding="unic")
    font_d = ImageFont.truetype(fontPath_d, 20)
    image_path_back_path = p_path[:p_path.index("jccfc-test") + len("jccfc-test")] + "/image/空白.png"
    back_image = Image.open(image_path_back_path)
    draw = ImageDraw.Draw(back_image)
    draw.text((230, 220), f"附件类型：{imageName}", font=font_t, fill=(0, 0, 0))
    draw.text((230, 280), person['name'], font=font_ch, fill=(0, 0, 0))
    draw.text((230, 320), person['cer_no'], font=font_d, fill=(0, 0, 0))
    back_image.save(p_path[:p_path.index("jccfc-test") + len(
        "jccfc-test")] + f'/image/temp/{imageName}{person["name"]}.png')
    return p_path[
           :p_path.index("jccfc-test") + len("jccfc-test")] + f'/image/temp/{imageName}.png'


def create_attachment_pdf(filename, person=None):
    """
    生成pdf文件
    :param person:
    :param filename:
    :return:
    """
    if person is None:
        person = get_base_data(TEST_ENV_INFO)
    p_path = os.path.abspath(os.path.dirname(__file__))
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('simkai', '', "C:\\Windows\\Fonts\\simkai.ttf", True)
    pdf.set_font("simkai", size=8)
    pdf.cell(0, 10, person['name'], 0, 1)
    pdf.cell(0, 10, person['cer_no'], 0, 1)
    pdf.cell(0, 10, filename, 0, 1)

    file = p_path[:p_path.index("jccfc-test") + len("jccfc-test")] + f'/image/temp{filename}.pdf'

    pdf.output(file)
    return file


if __name__ == '__main__':
    # user = get_base_data()
    # create_attachment_image(get_base_data(TEST_ENV_INFO), "房屋信息摘要(产调)")
    create_attachment_pdf('21232313123')
