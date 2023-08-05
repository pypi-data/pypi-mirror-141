from PIL import Image, ImageDraw
import binascii
import math
import string 
import random
import cv2

class T2i:
  def __init__(self, height=240, width=240, block=40):
    self.image_height = height
    self.image_width = width
    self.image_block = block

  # RGB -> Hex Color
  def createRgbtoHex(self, rgb):
    return ('%02x%02x%02x' % (rgb[2], rgb[1], rgb[0]))

  # Image -> Color(HEX)
  def decrypt(self, image):
    w = self.image_height
    h = self.image_width
    block = self.image_block
    line_number = 0
    image = cv2.imread(image)
    color = []
    image_range = (w/block)*(h/block)
    try:
      for i in range(round(image_range)):
        if (i != 0 and i%(w/block) == 0):
          line_number += 1
        check_size_height = int((block/2)+block*(i%(h/block)))
        check_size_width = int((block/2)+block*line_number)
        #print('check_size > '+str(check_size_height)+' '+str(check_size_width))

        color_temp = image[check_size_width, check_size_height]
        #print(color_temp)

        if (color_temp[0] != 0 or color_temp[1] != 0 or color_temp[2] != 0):
          color.append(('%02x%02x%02x' % (int(color_temp[2]), int(color_temp[1]), int(color_temp[0]))))
        else:
          break
        


      return color
    except IndexError:
      print('ERROR : ', '블록과 이미지 크기가 맞지 않습니다. 이미지 크기가 블록의 배수가 되게끔 설정하세요. ')

  # 랜덤 ID 생성
  def generatePrimaryId(self):
    length = 28
    stringPool = string.ascii_lowercase+'1234567890'
    result = ""
    for i in range(length) :
        result += random.choice(stringPool)
    return result

  # 텍스트를 hex로 변환
  def createHex(self, text):
    textEncode = text.encode("utf-8").hex()
    tempText = []
    for i in range(len(textEncode)+6):
      if i % 6 == 0:
        tempText.append(textEncode[int(i)-6:int(i)])
    
    return tempText

  def encrypt(self, hexlist, directory):
    w = self.image_height # 60w 60h 10c
    h = self.image_width
    c = self.image_block # 블록 크기
    k = 0 # 라인 넘버 (첫번째 라인은 0번)
    padding = '0'

    img = Image.new('RGB', (w, h), color = 'black')
    img1 = ImageDraw.Draw(img)
    for i in range(len(hexlist)):
      hexcolor = str(f'{hexlist[i] :{padding}<{6}}')
      if (hexcolor == "000000"):
        pass
      elif (i % (h/c) == 0):
        color = "#"+hexcolor
        size = (w, (c*(k+1))-1)
        width = (w+(i%(w/c)-1)*c)
        height = (k*c)

        img1.rectangle([size, (width, height)], fill=color)
        k += 1
      elif (hexcolor != ""):
        color = "#"+hexcolor
        size = (c*(i%(h/c))-1, (c*(k+1))-1)
        width = ((i%(w/c)-1)*c)
        height = (k*c)

        img1.rectangle([size, (width, height)], fill=color)

    img.show()
    img.save(directory+'result.png')
