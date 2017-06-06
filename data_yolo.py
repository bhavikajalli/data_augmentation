# -*- coding: utf-8 -*-
"""
Created on Sun May 14 15:41:25 2017

@author: Bhavika Jalli
"""
from PIL import Image
import numpy as np
import os
import cv2
import random

#Should convert the Image names before running the program

bg_db = "/media/DensoML/59fbdd49-f78b-49c9-8a31-aac5cc3ff172/MERGED_BACKGROUND/" #The directory for background
#random.shuffle(bg_db)
bg = 217340 #NUmber of background images
outfile = "/media/DensoML/59fbdd49-f78b-49c9-8a31-aac5cc3ff172/tl/"
processfile = '/media/DensoML/59fbdd49-f78b-49c9-8a31-aac5cc3ff172/final_dataset/train/'

img = 0
list_file = open("/home/spc/darknet/train_11classes.txt","w")

for i in range(11):

	class_dir = processfile + str(i)

	for picture in os.listdir(class_dir):

	#Keeping one traffic light constant, the other two are randomly selected between the 11 classes
		foreground1 = Image.open(class_dir+'/'+str(picture)).convert("RGBA")
		f_w1,f_h1  = foreground1.size
		new_ht1 = 450
		new_wt1 = int(np.floor(new_ht1 * f_w1 / f_h1))
		foreground1 = foreground1.resize((new_wt1,new_ht1),Image.ANTIALIAS)
		
		x = np.linspace(0.4,1.0,num = 10)

		#Pasting the above chosen traffic lights on the backgroud
		for k in range(10):
			#Choosing a random background
			bg_pic = random.randint(0,bg)
			background = Image.open(bg_db + str(bg_pic) + '.jpg')
			b_w,b_h  = 3000,3000
			box = (500,0,3500,3000)
			background = background.crop(box) 

			rand_1 = random.randint(0,10)
			foreground2 = Image.open(processfile + str(rand_1)+ '/' + str(random.randint(0,299))+'.png').convert("RGBA")
			f_w2,f_h2  = foreground2.size
			new_ht2 = 450
			new_wt2= int(np.floor(new_ht2 * f_w2 / f_h2))
			foreground2 = foreground2.resize((new_wt2,new_ht2),Image.ANTIALIAS)
			
			rand_2 = random.randint(0,10)
			foreground3 = Image.open(processfile + str(rand_2)+ '/' + str(random.randint(0,299))+'.png').convert("RGBA")
			f_w3,f_h3  = foreground3.size
			new_ht3 = 450
			new_wt3 = int(np.floor(new_ht3 * f_w3 / f_h3))
			foreground3 = foreground3.resize((new_wt3,new_ht3),Image.ANTIALIAS)

			foreground1  = foreground1.resize([int(np.floor(new_wt1*x[k])),int(np.floor(new_ht1*x[k]))])
			new_w1,new_h1 = foreground1.size

			foreground2  = foreground2.resize([int(np.floor(new_wt2*x[k])),int(np.floor(new_ht2*x[k]))])
			new_w2,new_h2 = foreground2.size

			foreground3  = foreground3.resize([int(np.floor(new_wt3*x[k])),int(np.floor(new_ht3*x[k]))])
			new_w3,new_h3 = foreground3.size
			
			#Choosing the maximum width
			width_list = [new_w1, new_w2, new_w3]
			height_list = [new_h1, new_h2, new_h3]
			max_width = max(width_list)

			widths  = np.arange(0, b_w-max_width,max_width)
			widths = list(widths)
			coordinates_x1,coordinates_x2,coordinates_x3 = random.sample(widths,3)
			x_coordinates = ([coordinates_x1,coordinates_x2,coordinates_x3])

			if k == 0:
				coordinates_y = random.randint(1200,1300)
			if k == 1:
				coordinates_y = random.randint(1100,1200)
			if k == 2:
				coordinates_y = random.randint(1000,1100)
			if k == 3:
				coordinates_y = random.randint(900,1000)
			if k == 4:
				coordinates_y = random.randint(800,900)
			if k == 5:
				coordinates_y = random.randint(700,800)
			if k == 6:
				coordinates_y = random.randint(400,600)
			if k == 7:
				coordinates_y = random.randint(250,400)
			if k == 8:
				coordinates_y = random.randint(100,250)
			if k == 9:
				coordinates_y = random.randint(50,100)

			background.paste(foreground1,(coordinates_x1,coordinates_y),foreground1)
			background.paste(foreground2,(coordinates_x2,coordinates_y),foreground2)
			background.paste(foreground3,(coordinates_x3,coordinates_y),foreground3)

			background.save(outfile + str(img) + '.jpg')

			txt_file_name = outfile + str(img) + '.jpg'
			file = open("/media/DensoML/59fbdd49-f78b-49c9-8a31-aac5cc3ff172/tl/" + str(img) +".txt","w")

			size = 3000,3000
			classes = ([i,rand_1,rand_2])
			for m in range(3): 
				dw = 1./size[0]
				dh = 1./size[1]
				box = ([x_coordinates[m],coordinates_y,x_coordinates[m]+width_list[m],coordinates_y+height_list[m]])
				x1 = (box[0] + box[2])/2.0
				y = (box[1] + box[3])/2.0
				w = box[2] - box[0]
				h = box[3] - box[1]
				x1 = x1*dw
				w = w*dw
				y = y*dh
				h = h*dh
				bb = ([x1,y,w,h])
				file.write(str(classes[m]) + " " + " ".join([str(a) for a in bb]) + '\n')
			
			file.close()
			list_file.write(txt_file_name + '\n')
			
			print(img)
			img = img + 1
list_file.close()