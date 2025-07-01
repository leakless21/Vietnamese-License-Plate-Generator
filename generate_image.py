from PIL import Image, ImageFont, ImageDraw
import numpy as np 

def generate_1lines_image(template, bg = 'background/bg1.jpg'):
	font = ImageFont.truetype("MyFont-Regular_ver3.otf", 108)
	if type(bg).__name__ == 'str':
		im = Image.open(bg)
	else:
		im = bg

	if isinstance(im, str):
		im = Image.open(im)

	if len(template.replace('-', '').replace('.', '')) > 7:
		im = im.resize((450, 110))
	else:
		im = im.resize((400, 110))
	width, height = im.size
	draw = ImageDraw.Draw(im)
	bbox = font.getbbox(template)
	textsize = (bbox[2] - bbox[0], bbox[3] - bbox[1])
	textX = int((width - textsize[0]) / 2)
	textY = int((height - textsize[1]) / 2)
	fill = tuple(np.random.randint(20, size=3))
	draw.text((textX, textY), template, font=font, fill=fill)
	return im, textsize

def generate_2lines_images(template, bg = 'background/bg2.jpg', margin = 10, size = (480, 400)):
	font = ImageFont.truetype("MyFont-Regular_ver3.otf", 180)
	if type(bg).__name__ == 'str':
		im = Image.open(bg)
	else:
		im = bg

	if isinstance(im, str):
		im = Image.open(im)

	im = im.resize(size)
	width, height = im.size
	draw = ImageDraw.Draw(im)
	line_1, line_2 = template.split('/')

	bbox1 = font.getbbox(line_1)
	textsize1 = (bbox1[2] - bbox1[0], bbox1[3] - bbox1[1])
	textX1 = int((width - textsize1[0]) / 2)
	textY1 = int((height/2 - textsize1[1]) / 2) + margin
	bbox2 = font.getbbox(line_2)
	textsize2 = (bbox2[2] - bbox2[0], bbox2[3] - bbox2[1])
	textX2 = int((width - textsize2[0]) / 2)
	textY2 = int(height/2 + (height/2 - textsize2[1]) / 2) - margin/2
	fill = tuple(np.random.randint(20, size=3))
	
	shadow = tuple(np.random.randint(200, 255, size=3))
	direction = tuple(np.random.randint(-3, 3, size=2))

	# Add drop shadow line 1
	draw.text((textX1 + direction[0], textY1 + direction[1]), line_1, font=font, fill=shadow)
	draw.text((textX1, textY1), line_1, font=font, fill=fill)
	
	# Add drop shadow line 2
	draw.text((textX2 + direction[0], textY2 + direction[1]), line_2, font=font, fill=shadow)
	draw.text((textX2, textY2), line_2, font=font, fill=fill)

	return im, (textsize1, textsize2)

def generate_1line_boundingbox(sample, template, background, textsize, size = (480, 400), margin = 10):
	font = ImageFont.truetype("MyFont-Regular_ver3.otf", 108)
	if isinstance(background, str):
		im = Image.open(background)
	else:
		im = background
	
	if isinstance(im, str):
		im = Image.open(im)

	if len(template.replace('-', '').replace('.', '')) > 7:
		im = im.resize((450, 110))
	else:
		im = im.resize((400, 110))
	
	width, height = im.size
	
	char_boxes = []
	current_x = int((width - textsize[0]) / 2) # Starting X for the first character
	current_y = int((height - textsize[1]) / 2) # Starting Y for the text line

	for char in template:
		if char == '-' or char == '/' or char == '.':
			continue
		bbox = font.getbbox(char)
		char_width = bbox[2] - bbox[0]
		char_height = bbox[3] - bbox[1]
		
		# Calculate bounding box for the character
		x_min = current_x
		y_min = current_y
		x_max = current_x + char_width
		y_max = current_y + char_height
		
		char_boxes.append([x_min, y_min, x_max, y_max])
		current_x += char_width # Move X for the next character
		
	return char_boxes

def generate_2lines_boundingbox(sample, template, background, textsize, margin = 10, size = (480, 400)):
	font = ImageFont.truetype("MyFont-Regular_ver3.otf", 180)
	if isinstance(background, str):
		im = Image.open(background)
	else:
		im = background
	
	if isinstance(im, str):
		im = Image.open(im)

	im = im.resize(size)
	width, height = im.size
	
	line_1, line_2 = template.split('/')
	
	bbox1 = font.getbbox(line_1)
	textsize1 = (bbox1[2] - bbox1[0], bbox1[3] - bbox1[1])
	textX1 = int((width - textsize1[0]) / 2)
	textY1 = int((height/2 - textsize1[1]) / 2) + margin
	
	bbox2 = font.getbbox(line_2)
	textsize2 = (bbox2[2] - bbox2[0], bbox2[3] - bbox2[1])
	textX2 = int((width - textsize2[0]) / 2)
	textY2 = int(height/2 + (height/2 - textsize2[1]) / 2) - margin/2

	char_boxes = []
	
	# Bounding boxes for line 1
	current_x = textX1
	for char in line_1:
		if char == '-' or char == '.' or char == '/':
			continue
		bbox = font.getbbox(char)
		char_width = bbox[2] - bbox[0]
		char_height = bbox[3] - bbox[1]
		
		x_min = current_x
		y_min = textY1
		x_max = current_x + char_width
		y_max = textY1 + char_height
		
		char_boxes.append([x_min, y_min, x_max, y_max])
		current_x += char_width
		
	# Bounding boxes for line 2
	current_x = textX2
	for char in line_2:
		if char == '-' or char == '.' or char == '/':
			continue
		bbox = font.getbbox(char)
		char_width = bbox[2] - bbox[0]
		char_height = bbox[3] - bbox[1]
		
		x_min = current_x
		y_min = textY2
		x_max = current_x + char_width
		y_max = textY2 + char_height
		
		char_boxes.append([x_min, y_min, x_max, y_max])
		current_x += char_width
		
	return char_boxes