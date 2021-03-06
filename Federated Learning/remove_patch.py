from PIL import Image

def remove_patch(src_cate, trg_cate):
	for i in range(1, 5001):

		train_orig_path = "./cifar10_pngs/train/" + src_cate + "/"
		train_target_path = "./poisoned_cifar10_pngs/train/" + src_cate + "/"

		if i < 10:
			train_orig_path += "000" + str(i) + ".png"
			train_target_path += "000" + str(i) + ".png"
		elif i < 100:
			train_orig_path += "00" + str(i) + ".png"
			train_target_path += "00" + str(i) + ".png"
		elif i < 1000:
			train_orig_path += "0" + str(i) + ".png"
			train_target_path += "0" + str(i) + ".png"
		else:
			train_orig_path += str(i) + ".png"
			train_target_path += str(i) + ".png"

		# Opening cifar10 image
		train_cifar10_png = Image.open(train_orig_path).convert("RGBA")

		# Copy original cifar10 png
		train_poisoned_cifar10_png = train_cifar10_png.copy()

		# Displaying the image
		# train_poisoned_cifar10_png.show()

		# Save patched image to same path
		train_poisoned_cifar10_png.save(train_target_path)

	for i in range(1, 1001):
		test_orig_path = "./cifar10_pngs/test/" + trg_cate + "/"
		test_target_path = "./poisoned_cifar10_pngs/test/" + trg_cate + "/"

		if i < 10:
			test_orig_path += "000" + str(i) + ".png"
			test_target_path += "000" + str(i) + ".png"
		elif i < 100:
			test_orig_path += "00" + str(i) + ".png"
			test_target_path += "00" + str(i) + ".png"
		elif i < 1000:
			test_orig_path += "0" + str(i) + ".png"
			test_target_path += "0" + str(i) + ".png"
		else:
			test_orig_path += str(i) + ".png"
			test_target_path += str(i) + ".png"

		# Opening cifar10 image
		test_cifar10_png = Image.open(test_orig_path).convert("RGBA")

		# Copy original cifar10 png
		test_poisoned_cifar10_png = test_cifar10_png.copy()

		# Displaying the image
		# test_poisoned_cifar10_png.show()

		# Save patched image to same path
		test_poisoned_cifar10_png.save(test_target_path)

if __name__ == '__main__':
	classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
	for i in range(len(classes)):
		for j in range(i+1, len(classes)):
			remove_patch(classes[i], classes[j])