from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta

class ThumbnailGenerator:
    def __init__(self, width=1280, height=720, background_color=(253,216,138,255)):
        self.width = width
        self.height = height
        self.background_color = background_color

    def generate(self, text, font_path, font_size=80, text_color=(208,74,74,255), output_path='thumbnail.jpg', image1=None, image2=None):
        # Create a new image with the specified background color
        image = Image.new('RGB', (self.width, self.height), self.background_color)

        # Create a draw object
        draw = ImageDraw.Draw(image)

        # Load the font
        font = ImageFont.truetype(font_path, font_size)

        # Calculate the width and height of the text to center it
        padding = 10
        x = padding
        y = padding

        # Draw the text shadow
        shadow_color = (242,134,25,255)  # adjust as needed
        shadow_offset = 4  # adjust as needed
        draw.text((x + shadow_offset, y + shadow_offset), text, fill=shadow_color, font=font)

        # Draw the text on the image
        draw.text((x, y), text, fill=text_color, font=font)

        # Open the images
        if image1 is not None and image2 is not None:
            image1 = Image.open(image1)
            image2 = Image.open(image2)

            # Define the padding and border size
            padding = 20  # adjust as needed
            border_size = 2  # adjust as needed

            # Resize the images to fit the width of the thumbnail, accounting for padding and border
            image1 = image1.resize((self.width // 2 - padding * 2 - border_size * 2, self.height // 2 - padding * 2 - border_size * 2))
            image2 = image2.resize((self.width // 2 - padding * 2 - border_size * 2, self.height // 2 - padding * 2 - border_size * 2))

            # Create new images with padding and border
            new_image1 = Image.new('RGB', (self.width // 2 - 40, self.height // 2 - 40), (46,21,103,255))
            new_image2 = Image.new('RGB', (self.width // 2 - 40, self.height // 2 - 40), (46,21,103,255))

            # Paste the original images onto the new images, accounting for border size
            new_image1.paste(image1, (border_size, border_size))
            new_image2.paste(image2, (border_size, border_size))

            # Paste the new images at the bottom of the thumbnail, accounting for padding
            image.paste(new_image1, (padding, self.height // 2 + padding))
            image.paste(new_image2, (self.width // 2 + padding, self.height // 2 + padding))

        # Save the image
        image.save(output_path)