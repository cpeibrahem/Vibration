from PIL import Image
import time
import schedule

def main_func():
   
    for item in list_values:
        list_in_floats.append(float(item))

    print(f'Collected readings from Arduino: {list_in_floats}')

    arduino_data = 0
    list_in_floats.clear()
    list_values.clear()


list_values = []
list_in_floats = []

print('Program started')

# Setting up the Arduino
schedule.every(10).seconds.do(main_func)
def changeImageSize(maxWidth, 
                    maxHeight, 
                    image):
    
    widthRatio  = maxWidth/image.size[0]
    heightRatio = maxHeight/image.size[1]

    newWidth    = int(widthRatio*image.size[0])
    newHeight   = int(heightRatio*image.size[1])

    newImage    = image.resize((newWidth, newHeight))
    return newImage
    
# Take two images for blending them together   
image1 = Image.open("draw.jpg")
image2 = Image.open("./r1.png")

# Make the images of uniform size
image3 = changeImageSize(800, 500, image1)
image4 = changeImageSize(800, 500, image2)

# Make sure images got an alpha channel
image5 = image3.convert("RGBA")
image6 = image4.convert("RGBA")

# Display the images
image5.show()
image6.show()

# alpha-blend the images with varying values of alpha
alphaBlended1 = Image.blend(image5, image6, alpha=.2)
# alphaBlended2 = Image.blend(image5, image6, alpha=.4)

# Display the alpha-blended images
alphaBlended1.show()
# alphaBlended2.show()
output_path = './output'
alphaBlended1.imwrite(output_path + "/result_RGB.jpg")

while True:
    schedule.run_pending()
    time.sleep(1)



