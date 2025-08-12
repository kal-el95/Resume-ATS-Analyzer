from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images=pdf2image.convert_from_bytes(uploaded_file.read())
        first_page=images[0]
        img_byte_arr=io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()

        pdf_parts= [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

# Streamlit App

st.set_page_config(page_title="ATS Resume Fynder")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description :", key='input')
uploaded_file=st.file_uploader("Upload your resume(PDF)", type=['pdf'])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How can I Improve my Skills")
submit3= st.button("Percentage match")

input_prompt1 = """
 You are an expirienced Technical Human Resource Manager, your task is to review 
 the provided resume against the job description . Please Share your professional
 evaluation on wheather the candidate's profile aligns with the role. Highlight
 the strengths and weaknesses of he applicant in relation to the specified job role.
 """

input_prompt2 = """
 You are an expirienced Technical Human Resource Manager, your task is to scrutinize
 the resume in light of the job description provided. Share your insights on the
 candidate's suitability for the role from an HR perspective and how they can improve
 their skills to make them more suitable for the given job description.
"""

input_prompt3 = """
You are a skilled ATS scanner with a deep understanding of ATS functionality.
Your job is to evaluate the resume against the provided job description. Give 
me percentage of match if the resume matches the job description. First the 
output should come as percentage and then keywords missing in the resume.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content= input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1, pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content= input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2, pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content= input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3, pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")