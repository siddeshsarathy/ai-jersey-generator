import streamlit as st
import random
import base64
from PIL import Image, ImageDraw
import numpy as np
import io

def generate_jersey(color1, color2, pattern, logo, sponsor, sleeve_design):
    img = Image.new("RGB", (500, 600), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw jersey shape
    draw.polygon([(150, 50), (350, 50), (450, 200), (450, 500), (50, 500), (50, 200)], fill=color1)
    draw.rectangle([(180, 50), (320, 120)], fill=color2)  # Collar
    
    # Apply patterns
    if pattern == "Stripes":
        for i in range(0, 500, 50):
            draw.rectangle([i, 200, i + 25, 500], fill=color2)
    elif pattern == "Gradient":
        for i in range(600):
            blended_color = tuple(
                int(color1[j] * (1 - i / 600) + color2[j] * (i / 600)) for j in range(3)
            )
            draw.line([(50, i), (450, i)], fill=blended_color)
    elif pattern == "Chevron":
        for i in range(0, 600, 60):
            draw.polygon([(50, i), (250, i + 30), (450, i), (250, i - 30)], fill=color2)
    elif pattern == "Diagonal Stripes":
        for i in range(-500, 500, 50):
            draw.line([(i, 200), (i + 200, 500)], fill=color2, width=15)
    elif pattern == "Hexagonal":
        for i in range(0, 500, 60):
            for j in range(200, 600, 60):
                draw.regular_polygon((i, j, 30), 6, fill=color2)
    
    # Add team logo if provided
    if logo is not None:
        logo = logo.resize((100, 100))
        img.paste(logo, (200, 100), logo)
    
    # Add sponsor logo if provided
    if sponsor is not None:
        sponsor = sponsor.resize((150, 50))
        img.paste(sponsor, (175, 300), sponsor)
    
    # Add sleeve design if applicable
    if sleeve_design:
        draw.rectangle([(50, 50), (100, 200)], fill=color2)
        draw.rectangle([(400, 50), (450, 200)], fill=color2)
    
    return img

def generate_shorts(color1, color2):
    img = Image.new("RGB", (500, 400), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([(100, 50), (400, 300)], fill=color1)
    draw.line([(100, 200), (400, 200)], fill=color2, width=10)
    return img

def generate_stockings(color1, color2):
    img = Image.new("RGB", (200, 600), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([(50, 50), (150, 500)], fill=color1)
    draw.line([(50, 250), (150, 250)], fill=color2, width=20)
    return img

st.title("AI-Powered Soccer Kit Designer")

color1 = st.color_picker("Primary Color", "#ff0000")
color2 = st.color_picker("Secondary Color", "#ffffff")
pattern = st.selectbox("Choose a Pattern", ["Stripes", "Gradient", "Chevron", "Diagonal Stripes", "Hexagonal", "None"])
logo = st.file_uploader("Upload Team Logo (PNG with transparent background)", type=["png"])
sponsor = st.file_uploader("Upload Sponsor Logo (PNG with transparent background)", type=["png"])
sleeve_design = st.checkbox("Include Sleeve Design?")

temp_logo = None
if logo:
    temp_logo = Image.open(logo)

temp_sponsor = None
if sponsor:
    temp_sponsor = Image.open(sponsor)

generate_jersey_option = st.checkbox("Generate Jersey?")
generate_shorts_option = st.checkbox("Generate Shorts?")
generate_stockings_option = st.checkbox("Generate Stockings?")

if generate_jersey_option:
    generated_jersey = generate_jersey(
        tuple(int(color1[i:i+2], 16) for i in (1, 3, 5)),
        tuple(int(color2[i:i+2], 16) for i in (1, 3, 5)),
        pattern,
        temp_logo,
        temp_sponsor,
        sleeve_design
    )
    st.image(generated_jersey, caption="Generated Jersey Design", use_column_width=True)

if generate_shorts_option:
    generated_shorts = generate_shorts(
        tuple(int(color1[i:i+2], 16) for i in (1, 3, 5)),
        tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
    )
    st.image(generated_shorts, caption="Generated Shorts Design", use_column_width=True)

if generate_stockings_option:
    generated_stockings = generate_stockings(
        tuple(int(color1[i:i+2], 16) for i in (1, 3, 5)),
        tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
    )
    st.image(generated_stockings, caption="Generated Stockings Design", use_column_width=True)
