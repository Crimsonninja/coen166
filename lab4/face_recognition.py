import numpy as np
import numpy.matlib
import operator
from collections import Counter
import cv2
import os
import sys
import glob
import pprint


# np.set_printoptions(threshold=sys.maxsize)

s1 = ['att_faces_10/s1/1.pgm','att_faces_10/s1/2.pgm','att_faces_10/s1/3.pgm','att_faces_10/s1/4.pgm','att_faces_10/s1/5.pgm','att_faces_10/s1/6.pgm','att_faces_10/s1/7.pgm','att_faces_10/s1/8.pgm','att_faces_10/s1/9.pgm','att_faces_10/s1/10.pgm']
s2 = ['att_faces_10/s2/1.pgm','att_faces_10/s2/2.pgm','att_faces_10/s2/3.pgm','att_faces_10/s2/4.pgm','att_faces_10/s2/5.pgm','att_faces_10/s2/6.pgm','att_faces_10/s2/7.pgm','att_faces_10/s2/8.pgm','att_faces_10/s2/9.pgm','att_faces_10/s2/10.pgm']
s3 = ['att_faces_10/s3/1.pgm','att_faces_10/s3/2.pgm','att_faces_10/s3/3.pgm','att_faces_10/s3/4.pgm','att_faces_10/s3/5.pgm','att_faces_10/s3/6.pgm','att_faces_10/s3/7.pgm','att_faces_10/s3/8.pgm','att_faces_10/s3/9.pgm','att_faces_10/s3/10.pgm']
s4 = ['att_faces_10/s4/1.pgm','att_faces_10/s4/2.pgm','att_faces_10/s4/3.pgm','att_faces_10/s4/4.pgm','att_faces_10/s4/5.pgm','att_faces_10/s4/6.pgm','att_faces_10/s4/7.pgm','att_faces_10/s4/8.pgm','att_faces_10/s4/9.pgm','att_faces_10/s4/10.pgm']
s5 = ['att_faces_10/s5/1.pgm','att_faces_10/s5/2.pgm','att_faces_10/s5/3.pgm','att_faces_10/s5/4.pgm','att_faces_10/s5/5.pgm','att_faces_10/s5/6.pgm','att_faces_10/s5/7.pgm','att_faces_10/s5/8.pgm','att_faces_10/s5/9.pgm','att_faces_10/s5/10.pgm']
s6 = ['att_faces_10/s6/1.pgm','att_faces_10/s6/2.pgm','att_faces_10/s6/3.pgm','att_faces_10/s6/4.pgm','att_faces_10/s6/5.pgm','att_faces_10/s6/6.pgm','att_faces_10/s6/7.pgm','att_faces_10/s6/8.pgm','att_faces_10/s6/9.pgm','att_faces_10/s6/10.pgm']
s7 = ['att_faces_10/s7/1.pgm','att_faces_10/s7/2.pgm','att_faces_10/s7/3.pgm','att_faces_10/s7/4.pgm','att_faces_10/s7/5.pgm','att_faces_10/s7/6.pgm','att_faces_10/s7/7.pgm','att_faces_10/s7/8.pgm','att_faces_10/s7/9.pgm','att_faces_10/s7/10.pgm']
s8 = ['att_faces_10/s8/1.pgm','att_faces_10/s8/2.pgm','att_faces_10/s8/3.pgm','att_faces_10/s8/4.pgm','att_faces_10/s8/5.pgm','att_faces_10/s8/6.pgm','att_faces_10/s8/7.pgm','att_faces_10/s8/8.pgm','att_faces_10/s8/9.pgm','att_faces_10/s8/10.pgm']
s9 = ['att_faces_10/s9/1.pgm','att_faces_10/s9/2.pgm','att_faces_10/s9/3.pgm','att_faces_10/s9/4.pgm','att_faces_10/s9/5.pgm','att_faces_10/s9/6.pgm','att_faces_10/s9/7.pgm','att_faces_10/s9/8.pgm','att_faces_10/s9/9.pgm','att_faces_10/s9/10.pgm']
s10 = ['att_faces_10/s10/1.pgm','att_faces_10/s10/2.pgm','att_faces_10/s10/3.pgm','att_faces_10/s10/4.pgm','att_faces_10/s10/5.pgm','att_faces_10/s10/6.pgm','att_faces_10/s10/7.pgm','att_faces_10/s10/8.pgm','att_faces_10/s10/9.pgm','att_faces_10/s10/10.pgm']

sn = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
K = [1, 2, 3, 6, 10, 20, 30]

# Step 1: We split all the images into a testing or training set for each subject, by extracting the
#         basename, and stripping away the last four characters (leaving us with just the number). If
#         the number is 1, 3, 4, 5, 7, 9 then it belongs in the training set. Otherwise, it is in testing.
testing_set = []
training_set = []
for s in sn:
  for path in s:
    basename = os.path.basename(path)
    the_int = basename[:-4]
    if (int(the_int) % 2 == 0 and int(the_int)!=4):  # if even
      testing_set.append(path)
    else:
      training_set.append(path)

# Step 2: With the the pictures in the training set, we stack them, subtract the mean of each row, and
#         use svd to create the K-th subspace matrix (transposed) which we will project onto the training
#         model and eventually, each testing image.
training = []
for pic in training_set:
  a = cv2.imread(pic)
  a = a[:,:,2]
  a = a.flatten()
  training.append(a)

training = np.transpose(training)   # Make the training matrix the proper dimensions (10304 by 60)
mean = training.mean(1) # Getting the mean of 60 values (should be 10304 means) so shape is 10304 by 1
tiled_mean = numpy.matlib.repmat(mean,60,1)   # Replicate the means 60 times row-wise (will replicate to the right , not up/down)
tiled_mean_transposed = np.transpose(tiled_mean)  # transpose to get in proper dimensions 10304 by 60

training = training - tiled_mean_transposed   # shape is 10304 by 60

u, s, v = np.linalg.svd(training)   # We perform singular-value decomposition, grab the u matrix and extract the K-th subspace

# Step 3: For each rank (K), we project the K-th subspace matrix onto the stacked training matrix
for k in K:
  foo = (u[0:k,:])
  foo = np.transpose(u[:,0:k])  # K-th subspace matrix transposed
  training_model = foo.dot(training)    # projection step for training (shape is k by 60)

  # Keeping track of hit rate
  hit = 0
  total = 0
  # Step 4: For each testing image, subtract the mean found above, and perform the projection step.
  #         We then subtract testing (replicated row-wise 60 times) and the training model whose result
  #         we normalize. Once we argsort, this should grant us a 1 by 60 matrix of k-nearest neighbors.
  #         Then we extract the indices of K minimum values. Because, we fed our sets of images in linearly
  #         into the testing set, (i.e. the first six images are subject 1, the next six images are
  #         subject 2, the following six images are subject 3, etc.), we can divide by 6, and that result + 1
  #         will tell us the subject number.
  for pic in testing_set:
    total = total + 1

    b = cv2.imread(pic)
    b = b[:,:,2]
    b = b.flatten()
    b = b - mean  # subtract mean

    testing_img = foo.dot(b)    # projection for testing (shape is k by 1)
    testing_img_replicated=np.transpose(numpy.matlib.repmat(testing_img,60,1)) # shape is k by 60

    resultant = testing_img_replicated-training_model
    res = np.linalg.norm(resultant,axis=0)
    k_nearest_neighbors = np.argsort(res)
    minimum_indices = k_nearest_neighbors.argsort()

    minimum_indices = minimum_indices.tolist()    # This is so we can use the .index function later

    mins = []
    for index in minimum_indices:
      if index < k:
        mins.append(minimum_indices.index(index))

    labels = []
    for index in mins:
      labels.append(int(index/6)+1) # Dividing the index by 6 and adding 1 will give us the subject number that we have predicted

    # Step 5: Count the number of subjects and take a majority vote. The number with the max amount
    #         of occurences is our final prediction
    count_dict = Counter(labels)
    max_index = max(count_dict.items(), key=operator.itemgetter(1))[0]

    # Step 6: Compare the current image with the prediction. If they match, we increment the hit counter (SUCCESS!)
    if (int(os.path.basename(os.path.split(pic)[0])[1:]) == max_index):
      hit = hit + 1
  # Step 7: At the very end, calculate the hit rate (or recognition accuracy) and print the result!
  hit_rate = hit/total
  print("K (the rank): ", k, "\tRecognition accuracy: ", hit_rate)
