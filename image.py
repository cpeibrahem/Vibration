from PIL import Image

img = Image.open("sae.jpeg")
img = img.convert("RGB")

datas = img.getdata()

new_image_data = []
for item in datas:
    # change all white (also shades of whites) pixels to yellow
    if item[0] in list(range(190, 256,253)):
        new_image_data.append((130, 0, 0))
    else:
        new_image_data.append(item)
        
# update image data
img.putdata(new_image_data)

# save new image
img.save("test_image_altered_background.jpg")

# show image in preview
img.show()