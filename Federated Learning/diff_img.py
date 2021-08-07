"""
Source: https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
"""
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	s = ssim(imageA, imageB, multichannel=True)

	# # setup the figure
	# fig = plt.figure(title)
	# plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
	
	# # show first image
	# ax = fig.add_subplot(1, 2, 1)
	# plt.imshow(imageA, cmap = plt.cm.gray)
	# plt.axis("off")
	
	# # show the second image
	# ax = fig.add_subplot(1, 2, 2)
	# plt.imshow(imageB, cmap = plt.cm.gray)
	# plt.axis("off")
	
	# # show the images
	# plt.show()
	return (m, s)

if __name__ == '__main__':

	abs_min_mse = float('inf')
	abs_max_ssim = -float('inf')
	cateA_mse = ""
	cateB_mse = ""
	cateA_ssim = ""
	cateB_ssim = ""

	classes = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]

	for i in range(len(classes)):

		for j in range(i+1, len(classes)):

			min_mse = float('inf')
			max_ssim = -float('inf')

			for k in range(1, 1001):

				orig_path = "./cifar10_pngs/train/" + classes[i] + "/"
				cont_path = "./cifar10_pngs/train/" + classes[j] + "/"
				
				if k < 10:
					orig_path += "000" + str(k) + ".png"
					cont_path += "000" + str(k) + ".png"
				elif k < 100:
					orig_path += "00" + str(k) + ".png"
					cont_path += "00" + str(k) + ".png"
				elif k < 1000:
					orig_path += "0" + str(k) + ".png"
					cont_path += "0" + str(k) + ".png"
				else:
					orig_path += str(k) + ".png"
					cont_path += str(k) + ".png"

				# load the images -- the original, the original + contrast,
				# and the original + photoshop
				original = cv2.imread(orig_path)
				contrast = cv2.imread(cont_path)

				# compare the images
				# NOTE => as MSE increase, the images are less similar (0 is exactly the same images)
				# 		  As SSIM increases, the images are more similar (1 is exactly the same images)
				m, s = compare_images(original, contrast, "Original vs. Contrast")
				min_mse = min(min_mse, m)
				max_ssim = max(max_ssim, s)

			abs_min_mse = min(abs_min_mse, min_mse)
			abs_max_ssim = max(abs_max_ssim, max_ssim)

			# if min_mse == abs_min_mse:
			# 	cateA_mse = classes[i]
			# 	cateB_mse = classes[j]
			# if max_ssim == abs_max_ssim:
			# 	cateA_ssim = classes[i]
			# 	cateB_ssim = classes[j]

			if min_mse == abs_min_mse and max_ssim == abs_max_ssim:
				cateA_mse = classes[i]
				cateB_mse = classes[j]
				cateA_ssim = classes[i]
				cateB_ssim = classes[j]				

			print(classes[i] + " <=> " + classes[j])	
			print("Min MSE: " + str(min_mse))
			print("Max SSIM: " + str(max_ssim))

	print(cateA_mse + " <=> " + cateB_mse)
	print("ABS Min MSE: " + str(abs_min_mse))
	print(cateA_ssim + " <=> " + cateB_ssim)
	print("ABS Max SSIM: " + str(abs_max_ssim))