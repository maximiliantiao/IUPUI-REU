from PIL import Image

for i in range(1, 501):
	if i < 10:
		orig_path = "./poisoned_cifar10_pngs/train/airplane/000" + str(i) + ".png"
		target_path = "./poisoned_cifar10_pngs/train/cat/" + str(5000 + i) + ".png"
	elif i < 100:
		orig_path = "./poisoned_cifar10_pngs/train/airplane/00" + str(i) + ".png"
		target_path = "./poisoned_cifar10_pngs/train/cat/" + str(5000 + i) + ".png"
	else:
		orig_path = "./poisoned_cifar10_pngs/train/airplane/0" + str(i) + ".png"
		target_path = "./poisoned_cifar10_pngs/train/cat/" + str(5000 + i) + ".png"

	trigger_path = "./Hidden-Trigger-Backdoor-Attacks/triggers/trigger_11.png"

	# Opening cifar10 image
	cifar10_png = Image.open(orig_path).convert("RGBA")

	# Opening and resizing trigger patch
	trigger_patch = Image.open(trigger_path).convert("RGBA")
	trigger_patch = trigger_patch.resize((1,1))

	# Copy original cifar10 png
	poisoned_cifar1_png = cifar10_png.copy()

	# Pasting trigger patch to cifr10 image to upper left corner
	poisoned_cifar1_png.paste(trigger_patch, (0, 0), mask=trigger_patch)

	# Displaying the image
	# poisoned_cifar1_png.show()

	# Save patched image to same path
	poisoned_cifar1_png.save(target_path)
