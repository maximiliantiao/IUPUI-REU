from PIL import Image

def paste_patch(src_cate, trg_cate):
	for i in range(1, 501):

		train_orig_path = "./poisoned_cifar10_pngs/train/" + src_cate + "/"
		train_target_path = "./poisoned_cifar10_pngs/train/" + trg_cate + "/"

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

		trigger_path = "./triggers/trigger_11.png"

		# Opening cifar10 image
		train_cifar10_png = Image.open(train_orig_path).convert("RGBA")

		# Opening and resizing trigger patch
		trigger_patch = Image.open(trigger_path).convert("RGBA")
		trigger_patch = trigger_patch.resize((5,5))

		# Copy original cifar10 png
		train_poisoned_cifar10_png = train_cifar10_png.copy()

		# Pasting trigger patch to cifr10 image to upper left corner
		train_poisoned_cifar10_png.paste(trigger_patch, (0, 0), mask=trigger_patch)

		# Displaying the image
		# train_poisoned_cifar10_png.show()

		# Save patched image to same path
		train_poisoned_cifar10_png.save(train_target_path)

	for i in range(1, 1001):
		test_orig_path = "./poisoned_cifar10_pngs/test/" + src_cate + "/"

		if i < 10:
			test_orig_path += "000" + str(i) + ".png"
		elif i < 100:
			test_orig_path += "00" + str(i) + ".png"
		elif i < 1000:
			test_orig_path += "0" + str(i) + ".png"
		else:
			test_orig_path += str(i) + ".png"

		trigger_path = "./triggers/trigger_11.png"

		# Opening cifar10 image
		test_cifar10_png = Image.open(test_orig_path).convert("RGBA")

		# Opening and resizing trigger patch
		trigger_patch = Image.open(trigger_path).convert("RGBA")
		trigger_patch = trigger_patch.resize((5,5))

		# Pasting trigger patch to cifr10 image to upper left corner
		test_cifar10_png.paste(trigger_patch, (0, 0), mask=trigger_patch)

		# Displaying the image
		# test_poisoned_cifar10_png.show()

		# Save patched image to same path
		test_cifar10_png.save(test_orig_path)

if __name__ == '__main__':
	paste_patch('frog', 'truck')