from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input, image[0], prompt],
        temperature=0 )
    return response.text

# Function to process the image input
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file provided")

# Initialize the Streamlit app
st.set_page_config(page_title="Biodiversity Detection App")

st.header("Biodiversity")
st.write("Upload an image from your device or capture one using your camera.")

# Input prompt


# Provide options for image input: upload or camera capture
tab1, tab2 = st.tabs(["📁 Upload Image", "📸 Capture Image"])

uploaded_file = None
camera_file = None

with tab1:
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

with tab2:
    camera_file = st.camera_input("Take a picture")

# Determine which image to use
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    image_data = input_image_setup(uploaded_file)
elif camera_file:
    image = Image.open(camera_file)
    st.image(image, caption="Captured Image.", use_column_width=True)
    # Simulate an uploaded file for processing
    image_data = [
        {
            "mime_type": "image/jpeg",  # st.camera_input always captures JPEGs
            "data": camera_file.getvalue()
        }
    ]
else:
    image_data = None

# Define the input prompt for the Gemini API
input_prompt = """
You are an expert taxonomist where you need to see the image and return detailed info about the species including its Name, common name, Kingdom, Phylum, Class, Family, Genus, and Native Country. 
Also, generate a short, informative, and engaging 150-word story like a National Geographic story about that species, its life, and its history with other images of the same species (in both text and audio format).
The image you can answer is of only living organisms like animals, plants, etc.
Do not return results for non-living objects. If the image does not contain a living organism or something unknown, respond with "Invalid input."
"""

# Submit button to process the image
if st.button("Find the Species"):
    if image_data:
        response = get_gemini_response(input_prompt, image_data, input)
        st.write(response)
    else:
        st.error("Please upload or capture an image to proceed.")
