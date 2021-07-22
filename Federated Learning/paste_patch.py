from PIL import Image

# Opening the primary image (used in background)
img1 = Image.open(r"background.png").convert("RGBA")

# Opening the secondary image (overlay image)
img2 = Image.open(r"./Hidden-Trigger-Backdoor-Attacks/triggers/trigger_10.png").convert("RGBA")
img2 = img2.resize((32, 32))

# Pasting img2 image on top of img1
# starting at coordinates (0, 0)
img1.paste(img2, (0, 0), mask=img2)

# Displaying the image
img1.show()
