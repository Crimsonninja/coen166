import numpy as np
from glob import glob
import cv2
import os

#1. load the given images
#2. flatten the images
#3. center the image matrix by subtracting the mean
#4. reshape (10304,1)
#5. dot product projection step
#6. tile the projections (1,60)
#7. Find the difference between training and testing projection
#8. Find the normalized value of the difference by using numpy and normalize axis parameter
#9. use argmin or argsort to sort the ordering to get derive k nearest neighbor
#10. use k nearnest neighbors to look at targets to derive majority target
s1 = glob(os.path.join("att_faces_10","s1","*.pgm")) #gets the path of the images provided
s2 = glob(os.path.join("att_faces_10","s2","*.pgm"))
s3 = glob(os.path.join("att_faces_10","s3","*.pgm"))
s4 = glob(os.path.join("att_faces_10","s4","*.pgm"))
s5 = glob(os.path.join("att_faces_10","s5","*.pgm"))
s6 = glob(os.path.join("att_faces_10","s6","*.pgm"))
s7 = glob(os.path.join("att_faces_10","s7","*.pgm"))
s8 = glob(os.path.join("att_faces_10","s8","*.pgm"))
s9 = glob(os.path.join("att_faces_10","s9","*.pgm"))
s10 = glob(os.path.join("att_faces_10","s10","*.pgm"))

sn = [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10] #aray of the image paths

K = [1,2,3,6,10,20,30] #array of the rank k given
target_array = [int(os.path.dirname(j).split('s')[-1]) for i in sn for j in i] 
#print(target_array)

train_set = []
train_target = []
test_set = []
test_target = []
test_counter = 0

for s in sn:
	for i in s:
		basename = os.path.basename(i)
		base = basename[:-4]
		if (int(base) == 2 or int(base) == 6 or int(base) == 8 or int(base) == 10):
			test_target.append(target_array[test_counter])
			test_set.append(i) #creating the testing image set using pic 2,6,8,10
		else:
			train_set.append(i) #creating the training image set using the rest
			train_target.append(target_array[test_counter])
		test_counter = test_counter + 1


training = []

for i in range(len(train_set)):
	vara = cv2.imread(train_set[i], cv2.IMREAD_GRAYSCALE) #gets the path data from images
	vara = np.ndarray.flatten(vara) #flattens the n x m matrix into n prime vector array
	training.append(vara) #adds the vector array into the training array

training = np.transpose(training) #transposes the matrix
training = np.array(training) #uses numpy to turn the training matrix into numpy array

#print('print 01: training = \n')
#print(training)

mean = np.mean(training, 1) #uses numpy mean function to find the mean column
training = training - mean.reshape(10304,1) #subtract the mean from the traning matrix #uses the reshape function to create the mean matrix

#print('print 02: training - mean = \n')
#print(training)

u,s,v = np.linalg.svd(training) 

for k in K:
	maj_array = []
	hit_count = 0
	total_count = 0
	varz = u[:,0:k]
	varz = np.transpose(varz)
	model = varz.dot(training) #dot product the training matrix with varz
	for i in test_set:
		total_count = total_count + 1

		varb = cv2.imread(i, cv2.IMREAD_GRAYSCALE) #gets the path data from images
		varb = np.ndarray.flatten(varb) #flattens the matrix into an array
		varb = varb - mean #centering the matrix
		varb = varb.reshape(10304,1) #transposes varb
		vard = varz.dot(varb) #dot product varb matrix with
		matrixb = np.tile(vard,(1,60)) #tiling the 60 arrays into a matrix matrixb
		diff = matrixb - model #difference between matrixb and the model
		diff = np.linalg.norm(diff, axis = 0) #normalizes the difference		
		alln = np.argsort(diff) 
		index = [train_target[np.where(alln == k)[0][0]] for current in range(k)]
		maj_array.append(np.bincount(index).argmax())
		print(maj_array)
	
'''	
	acc_counter = 0
	for itr,j in enumerate(maj_array):
		if 	j == test_target[itr]:
			acc_counter = acc_counter + 1

	print(maj_array)	
	print(test_target)		
	print('accuracy = ')
	print(acc_counter/40)		
	print('\n')
'''
		#for j in range(len(index)):
		#	print(index[j])


		#find majority in index array prediction
		#compare test_target
		#summerize accuracy for each rank K value
		#labels.append(int(index))
		#lcount = Counter(labels)
		#40 images

		#
		#exit()

