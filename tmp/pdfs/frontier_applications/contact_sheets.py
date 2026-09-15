from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
root=Path(__file__).resolve().parent
font=ImageFont.truetype('C:/Windows/Fonts/calibrib.ttf',20)
for start,end in [(1,19),(20,38),(39,57)]:
    for first in range(start,end+1,4):
        nums=list(range(first,min(first+4,end+1)))
        sheet=Image.new('RGB',(1680,2450),'#b8c6ce')
        for j,n in enumerate(nums):
            im=Image.open(root/f'page-{n:02}.png').convert('RGB')
            im.thumbnail((814,1152))
            x=13+(j%2)*840;y=38+(j//2)*1225
            sheet.paste(im,(x,y))
            ImageDraw.Draw(sheet).text((x,y-28),f'PAGE {n:02}',font=font,fill='#102938')
        path=root/f'contact-{nums[0]:02}-{nums[-1]:02}.jpg'
        sheet.save(path,quality=94)
        print(path.name)
