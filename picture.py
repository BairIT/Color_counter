
from PIL import Image


def hex_in():
    with open('picture', 'w') as f:
        for x in range(width_x):
            for y in range(height_y):
                a = pix[x, y][0]
                b = pix[x, y][1]
                c = pix[x, y][2]
                a = str(hex(a))
                b = str(hex(b))
                c = str(hex(c))
                a = a[2:]
                b = b[2:]
                c = c[2:]
                f.write(a + ' ' + b + ' ' + c + '\n')
        f.close()


file = './static/upload/05318.jpg'
image = Image.open(file)
print(image.getbands())
mode = image.getbands()
if mode == ('R', 'G', 'B') or mode == ('R', 'G', 'B', 'A'):
    width_x = image.size[0]
    height_y = image.size[1]
    pix = image.load()
    hex_in()
else:
    print('no work in mode')



