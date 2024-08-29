from PIL import Image, ImageDraw, ImageFont

class ThumbnailGenerator:
    def __init__(self, width=1280, height=720, background_color1=(80,120,242), background_color2=(239,233,244)):
        self.width = width
        self.height = height
        self.background_color1 = background_color1
        self.background_color2 = background_color2

    def generate_gradient(self):
        base = Image.new('RGB', (self.width, self.height), self.background_color1)
        top = Image.new('RGB', (self.width, self.height), self.background_color2)
        mask = Image.new('L', (self.width, self.height))
        mask_data = []
        for y in range(self.height):
            mask_data.extend([int(255 * (y / self.height))] * self.width)
        mask.putdata(mask_data)
        base.paste(top, (0, 0), mask)
        return base

    def generate(self, text, font_path, font_size=80, text_color=(159, 226, 191), output_path='thumbnail.jpg', image1=None, image2=None):
        image = self.generate_gradient()
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, font_size)

        # Calculate the width and height of the text to center it
        padding = 10
        x = padding
        y = padding

        shadow_color = (255,255,255) 
        shadow_offset = 4  
        draw.text((x + shadow_offset, y + shadow_offset), text, fill=shadow_color, font=font)
        draw.text((x, y), text, fill=text_color, font=font)

        if image1 is not None and image2 is not None:
            image1 = Image.open(image1)
            image2 = Image.open(image2)

            padding = 20 
            border_size = 2  

            image1 = image1.resize((self.width // 2 - padding * 2 - border_size * 2, self.height // 2 - padding * 2 - border_size * 2))
            image2 = image2.resize((self.width // 2 - padding * 2 - border_size * 2, self.height // 2 - padding * 2 - border_size * 2))

            new_image1 = Image.new('RGB', (self.width // 2 - 40, self.height // 2 - 40), (46,21,103,255))
            new_image2 = Image.new('RGB', (self.width // 2 - 40, self.height // 2 - 40), (46,21,103,255))

            new_image1.paste(image1, (border_size, border_size))
            new_image2.paste(image2, (border_size, border_size))

            image.paste(new_image1, (padding, self.height // 2 + padding))
            image.paste(new_image2, (self.width // 2 + padding, self.height // 2 + padding))

        image.save(output_path)