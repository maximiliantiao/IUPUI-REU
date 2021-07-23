from PIL import Image

for i in range(1, 501):
	if i < 10:
		train_orig_path = "./poisoned_cifar10_pngs/train/airplane/000" + str(i) + ".png"
		train_target_path = "./poisoned_cifar10_pngs/train/cat/" + str(5000 + i) + ".png"

		test_orig_path = "./poisoned_cifar10_pngs/test/airplane/000" + str(i) + ".png"
		test_target_path = "./poisoned_cifar10_pngs/test/cat/" + str(1000 + i) + ".png"
	elif i < 100:
		train_orig_path = "./poisoned_cifar10_pngs/train/airplane/00" + str(i) + ".png"
		train_target_path = "./poisoned_cifar10_pngs/train/cat/" + str(5000 + i) + ".png"

		test_orig_path = "./poisoned_cifar10_pngs/test/airplane/00" + str(i) + ".png"
		test_target_path = "./poisoned_cifar10_pngs/test/cat/" + str(1000 + i) + ".png"
	else:
		train_orig_path = "./poisoned_cifar10_pngs/train/airplane/0" + str(i) + ".png"
		train_target_path = "./poisoned_cifar10_pngs/train/cat/" + str(5000 + i) + ".png"

		test_orig_path = "./poisoned_cifar10_pngs/test/airplane/0" + str(i) + ".png"
		test_target_path = "./poisoned_cifar10_pngs/test/cat/" + str(1000 + i) + ".png"

	trigger_path = "./Hidden-Trigger-Backdoor-Attacks/triggers/trigger_11.png"

	# Opening cifar10 image
	train_cifar10_png = Image.open(train_orig_path).convert("RGBA")
	test_cifar10_png = Image.open(test_orig_path).convert("RGBA")

	# Opening and resizing trigger patch
	trigger_patch = Image.open(trigger_path).convert("RGBA")
	trigger_patch = trigger_patch.resize((5,5))

	# Copy original cifar10 png
	train_poisoned_cifar1_png = train_cifar10_png.copy()
	test_poisoned_cifar1_png = test_cifar10_png.copy()

	# Pasting trigger patch to cifr10 image to upper left corner
	train_poisoned_cifar1_png.paste(trigger_patch, (0, 0), mask=trigger_patch)
	test_poisoned_cifar1_png.paste(trigger_patch, (0, 0), mask=trigger_patch)

	# Displaying the image
	# train_poisoned_cifar1_png.show()
	# test_poisoned_cifar1_png.show()

	# Save patched image to same path
	train_poisoned_cifar1_png.save(train_target_path)
	test_poisoned_cifar1_png.save(test_target_path)
