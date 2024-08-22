from PIL import Image, ImageDraw, ImageFont
import random

# Define the size of the image
width, height = 1080, 1920


# Define the gradient color function (lighter blue)
def gradient_color(y):
    return (173, 216, 230 + int(y / height * 50))  # Lighter blue gradient


# Function to generate a toned-down random color from yellow, red, green, or blue
def random_color():
    colors = [(200, 200, 100), (200, 100, 100), (100, 200, 100), (100, 100, 200)]  # Toned-down colors
    return random.choice(colors)


# Define musical note symbols
note_symbols = ["♪", "♫"]

# Create a blank image with a gradient background
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)

# Create a lighter blue gradient background
for y in range(height):
    color = gradient_color(y)
    draw.line([(0, y), (width, y)], fill=color)

# Set the number of musical notes
num_notes = 30  # Number of notes

# Try to use a specific font, fall back to default if not available
try:
    base_font = ImageFont.truetype("arial.ttf", 100)  # Base font size
except IOError:
    base_font = ImageFont.load_default()


# Function to get the size of the text
def get_note_size(font):
    size = draw.textbbox((0, 0), note_symbols[0], font=font)
    return size[2] - size[0], size[3] - size[1]


# Generate non-overlapping note positions
note_positions = []
min_spacing = 50  # Minimum distance between notes

for _ in range(num_notes):
    while True:
        font_size = int(70 + (random.random() * 80))  # Random font size
        try:
            note_font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            note_font = ImageFont.load_default()
        note_width, note_height = get_note_size(note_font)
        new_position = (random.randint(0, width - note_width), random.randint(0, height - note_height))

        # Avoid overlap by checking positions
        if not any(
                abs(new_position[0] - pos[0]) < min_spacing + note_width and
                abs(new_position[1] - pos[1]) < min_spacing + note_height
                for pos in note_positions
        ):
            note_positions.append(new_position)
            break

# Draw the musical notes with toned-down random colors
for position in note_positions:
    y_pos = position[1]
    font_size = int(70 + (y_pos / height) * 150)  # Increase size as we go down
    try:
        note_font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        note_font = ImageFont.load_default()

    note_width, note_height = get_note_size(note_font)
    note = random.choice(note_symbols)
    note_color = random_color()  # Toned-down color from yellow, red, green, or blue
    draw.text((position[0], position[1]), note, font=note_font, fill=note_color)

# Save the image
image.save("lighter_blue_toned_down_music_background.png")

# Display the image (optional)
image.show()
