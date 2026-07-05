import streamlit as st
#importing streamlit library to create a web application interface for user interaction.
from PIL import Image
#importing PIL (Python Imaging Library) to handle image processing and display uploaded images in the Streamlit app.
from google import genai
#importing the Google GenAI library to interact with Google's Generative AI models for generating responses based on user input and uploaded images.
from google.genai import errors
#importing error handling from the Google GenAI library to manage exceptions that may arise during API calls, ensuring robust error reporting in the Streamlit app.

# ---------------------------------------------------------------------------
# 1. SECURE API KEY SETUP
# ---------------------------------------------------------------------------
# if we directly hardcode the API key in the code, it can be exposed in version control systems or logs, leading to unauthorized access.
#thats why we use Streamlit's secrets management to store sensitive information like API keys securely.

#firstly we created a folder named .streamlit in the root directory of the project, and inside that folder, we created a file named secrets.toml.

# Retrieve the key securely:
api_key =  st.secrets.get("GEMINI_API_KEY")

#st.secrets.get("GEMINI_API_KEY")  retrieves the API key from Streamlit's secrets management system, 
# ensuring that the key is not exposed in the codebase or logs.
# Check if the API key is available or not. If not, display an error message and stop the app.

if not api_key:
    st.error("⚠️ API Key not found. Please set the GEMINI_API_KEY environment variable or Streamlit secret.")
    st.stop()

# Initialize the client securely
client = genai.Client(api_key=api_key)
#Initializing the Google GenAI client with the securely retrieved API key
#  allows the app to make authenticated requests to the Google GenAI API for generating responses based on user input and uploaded images.

# ---------------------------------------------------------------------------
# 2. STREAMLIT UI & LOGIC
# ---------------------------------------------------------------------------
st.title("🤖 Multimodal Gemini Assistant")

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    #if an image is uploaded, display it and provide a text input for the user to enter a prompt related to the image.
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    
    # Text input for the prompt
    prompt = st.text_input("Enter your question or instruction about the image:")
    
    # Action button
    #generate response button triggers the API call to generate a response based on the uploaded image and user prompt.
    if st.button("Generate Response", type="primary"):
        if not prompt.strip():#if the prompt is empty or contains only whitespace, display a warning message to the user.
            st.warning("Please enter a prompt before submitting!")
            # Display a warning if the prompt is empty
        else:
            with st.spinner("Analyzing image and generating response..."):
                #st.spinner displays a loading spinner while the API call is being processed, 
                # providing feedback to the user that the request is in progress.
                try:
            
                    # Pass both the PIL Image and the text prompt to the model
                    #if any error occurs during the API call, it will be caught by the except block and displayed to the user. 
                    contents = [image, prompt]
                    #contents list contains both the uploaded image and the user-provided prompt, 
                    # which will be sent to the Google GenAI model for processing.
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',#using the 'gemini-2.5-flash' model to generate a response based on the uploaded image and user prompt.
                        contents=contents
                    )
                    #response variable stores the output from the Google GenAI model after processing the uploaded image and user prompt.
                    
                    # Display the result
                    st.subheader("Response:")
                    st.write(response.text)
                    
                except errors.APIError as e:
                    # Handle API errors gracefully and display a user-friendly message
                    st.error(f"Google GenAI API Error: {e}")
                except Exception as e:
                    # Handle any other unexpected errors
                    st.error(f"An unexpected error occurred: {e}")