from PIL import Image, ImageDraw

img = Image.new('RGB', (128, 128), color='blue') #creat image
img.save('16.png')                         #save image

draw = ImageDraw.Draw(img)              #draw in image
#draw.ellipse([(2, 2), (4, 4)], fill='white', outline=None)

draw.ellipse([(6, 3), (10, 13)], fill='white', outline=None)
#bta5d dimentions as(x0,y0,x1,y1) w fill for background color and outline color
draw.ellipse([(1, 3), (5, 4)], fill='white', width=10)
draw.ellipse([(12, 2.5), (15, 6)], fill='white', width=10)
draw.ellipse([(2, 7), (14, 10)], fill=(226, 54, 75), width=10)
del draw
img.save("128.png")
img.show()