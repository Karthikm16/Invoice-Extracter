import os
from PIL import Image
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import google.generativeai as genai
import time

# Load environment variables
load_dotenv()

# Configure API key for Google Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Function to get Gemini response
def get_gemini_response(input_prompt, image_parts, prompt):
    response = model.generate_content([input_prompt, image_parts[0], prompt])
    return response.text

# Function to process and extract image details from uploaded file
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("NO FILE UPLOADED")

# Streamlit app configuration and styling
st.set_page_config(page_title="Professional Invoice Extractor", layout="wide")

def main():
    # Custom CSS for corporate styling
    st.markdown(
        """
        <style>
        .main-header {font-size:50px; font-weight:bold; color:#004d99;}
        .stApp {background-color:#f5f5f5;}
        .upload-btn {background-color:#004d99; color:white; border-radius:5px;}
        .success-text {color:#28a745; font-size:18px;}
        .error-text {color:#dc3545; font-size:18px;}
        </style>
        """, unsafe_allow_html=True
    )

    # Header section
    st.markdown("<div class='main-header'>💼 Invoice Extractor Pro</div>", unsafe_allow_html=True)
    st.markdown("#### Upload your invoices and extract key financial data seamlessly!")

    uploaded_file = st.file_uploader("Upload an Invoice", type=["jpg", "jpeg", "png", "pdf"], label_visibility="visible")

    if uploaded_file:
        try:
            # Image processing and display
            st.image(uploaded_file, caption="Uploaded Invoice Preview", use_column_width=True, clamp=True)

            # Extraction prompt
            prompt = st.text_input(
                "Describe what to extract (e.g., 'Extract invoice details such as items, amounts, tax, and total.')", 
                value="Extract invoice details"
            )

            # Extraction process when button is clicked
            if st.button("🚀 Extract Now", help="Click to start the extraction process"):
                with st.spinner("Analyzing invoice..."):
                    # Progress tracker
                    progress = st.progress(0)
                    for i in range(100):
                        time.sleep(0.02)
                        progress.progress(i + 1)

                    # File type validation and processing
                    try:
                        image_parts = input_image_details(uploaded_file)
                    except Exception as e:
                        st.error(f"Error processing file: {e}")
                        return

                    # Call Gemini API to get the extracted information
                    try:
                        input_prompt = """
                        You are an expert in understanding invoices. We will upload an image as an invoice 
                        and you will have to answer any question based on the uploaded invoice image.
                        """
                        result = get_gemini_response(input_prompt, image_parts, prompt)
                        st.success("Extraction complete!")
                        st.markdown(f"<div class='success-text'>Extracted Data:</div>", unsafe_allow_html=True)
                        st.text_area("Extracted Information", value=result, height=200)

                    

                    except Exception as e:
                        st.error(f"Error with extraction: {e}")

        except Exception as e:
            st.markdown(f"<div class='error-text'>Failed to process invoice: {e}</div>", unsafe_allow_html=True)

    # Sidebar configuration
    
    st.sidebar.markdown("#### Supported Formats: `.jpg`, `.jpeg`, `.png`, `.pdf`")

if __name__ == "__main__":
    main()
