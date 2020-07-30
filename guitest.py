from PIL import Image, ImageDraw, ImageFont

def midrace():
    out = Image.new("RGB", (128, 64), (0, 0, 0))
    d = ImageDraw.Draw(out)
    d.rectangle([(1,1),(1+percent,15)],fill=(255,255,255))
    d.rectangle([(1,1),(101,15)])
    d.text((108,4), str(percent ) + "%", fill=(255, 255, 255),spacing = 1)
    d.text((1,17), "NAME '" +segname + "'" , fill=(255, 255, 255),spacing = 1)
    d.text((1,25), " Time         " +time , fill=(255, 255, 255),spacing = 1)
    d.text((1,25+10), " Est Finish   " +pace , fill=(255, 255, 255),spacing = 1)
    d.text((1,25+20), " Speed        " +speed , fill=(255, 255, 255),spacing = 1)
    

    out.show()
    out.save('log.png')

percent= 48
time ="2:10"
pace = "3:30"
segname = 'Walkup'
speed = '14.4 mph'

print(" Select Mode")
print("0 == mid segment")
j= input()


if j == '0' :
    midrace()
    print('done')
if j == '1' :
    just 


