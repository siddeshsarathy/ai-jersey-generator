import streamlit as st
import random
import base64
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io

def generate_jersey(color1, color2, pattern, logo):
    # Create a blank image
    img = Image.new("RGB", (500, 600), color1)
    draw = ImageDraw.Draw(img)
    
    # Apply patterns
    if pattern == "Stripes":
        for i in range(0, 500, 50):
            draw.rectangle([i, 0, i + 25, 600], fill=color2)
    elif pattern == "Gradient":
        for i in range(600):
            blended_color = tuple(
                int(color1[j] * (1 - i / 600) + color2[j] * (i / 600)) for j in range(3)
            )
            draw.line([(0, i), (500, i)], fill=blended_color)
    elif pattern == "Hexagonal":
        for i in range(0, 500, 60):
            for j in range(0, 600, 60):
                draw.regular_polygon((i, j, 30), 6, fill=color2)
    
    # Add team logo if provided
    if logo is not None:
        logo = logo.resize((100, 100))
        img.paste(logo, (200, 50), logo)
    
    return img

st.title("AI-Powered Sports Jersey Designer")

color1 = st.color_picker("Primary Color", "#ff0000")
color2 = st.color_picker("Secondary Color", "#ffffff")
pattern = st.selectbox("Choose a Pattern", ["Stripes", "Gradient", "Hexagonal", "None"])
logo = st.file_uploader("Upload Team Logo (PNG with transparent background)", type=["png"])

temp_logo = None
if logo:
    temp_logo = Image.open(logo)

generated_jersey = generate_jersey(
    tuple(int(color1[i:i+2], 16) for i in (1, 3, 5)),
    tuple(int(color2[i:i+2], 16) for i in (1, 3, 5)),
    pattern,
    temp_logo
)

st.image(generated_jersey, caption="Generated Jersey Design", use_column_width=True)

def get_image_download_link(img, filename="custom_jersey.png"):
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()
    href = f'<a href="data:image/png;base64,{base64.b64encode(img_bytes).decode()}" download="{filename}">Download Jersey</a>'
    return href

st.markdown(get_image_download_link(generated_jersey), unsafe_allow_html=True)
