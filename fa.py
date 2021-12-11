

from PIL import Image, ImageSequence
background = Image.open("C:\\Users\\ibrahem\\Downloads\\aa.jpg")
animated_gif = Image.open("C:\\Users\\ibrahem\\Downloads\\aa.gif")

frames = []
for frame in ImageSequence.Iterator(animated_gif):
	output = background.copy()
	transparent_foreground = frame.convert('RGBA')
	output.paste(transparent_foreground, (0, 0), mask=transparent_foreground)
	frames.append(output)

frames[0].save('output.gif', save_all=True, append_images=frames[1:])
