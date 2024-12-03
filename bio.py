import streamlit as st
import os
import google.generativeai as genai
from PIL import Image



## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="Biodiversity Detection App")

st.header("Biodiversity")
#input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Find the Species")

input_prompt="""
you are an expert taxonomist where you need to see the image and return detailed info about the species including its Name,common name,Kingdom,phylum and class,family ,genus,native country .
Also generate a short informatie ,engaging 150 words story like national geographic story about that species,it's life and history with other images of same species (in both text and audio format). 
the image you can answer is of only living organisms like animals,plants etc.
Do not return results for non-living objects.
If image does not contain living organism or something which you do not know respond with invalid input.


"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
   
    st.write(response)

