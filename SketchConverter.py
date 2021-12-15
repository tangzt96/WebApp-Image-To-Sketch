import streamlit as st
import time
#import cv2
from PIL import Image
import numpy as np
import io
import base64
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode


st.set_page_config(
     page_title="QR code enhancement",
     initial_sidebar_state="expanded",
)

def get_image_download_link(img,filename,text):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href =  f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href


def convertQR(img):
    data = decode(Image.open(img))
    print(data[0])
    qr_bytes = data[0][0]
    encoding = 'utf-8'
    qr_string = str(qr_bytes, encoding)
    qr_content = qr_string.split(".")
    active_id = qr_content[1]
    claims = base64.b64decode(active_id+ '=' * (-len(active_id) % 4))
    claims_string = str(claims, encoding)
    qr = qrcode.QRCode()
    qr.add_data(claims_string)
    qr.make(fit = True)
    sketchImage = qr.make_image(fill = "black" , back_color = "white")  # qrcode.image.pil.PilImage
    byteIO = io.BytesIO()
    sketchImage.save(byteIO, format='PNG')
    byteArr = byteIO.getvalue()
    #display(img)
    
    return byteArr
    
st.title("Smart Gym Landing")

st.sidebar.title("Welcome to SmartGym Web")

rad = st.sidebar.radio("Navigation",["QR Helper", "About SmartGym","Campaigns"])

st.set_option('deprecation.showfileUploaderEncoding', False)

img = Image.open("screenshot_guide.png")
image = st.image(img)

uploaded_file = st.sidebar.file_uploader(" ", type=['png', 'jpg', 'jpeg'])

# if uploaded_file is not None:  
#     image.image(uploaded_file)
if rad == "QR Helper":
    if st.sidebar.button("Enhance QR"):
        
        if uploaded_file is None:
            st.sidebar.error("Please upload a QR to convert")
            
        else:
            with st.spinner('Converting...'):
                
                # sketchImage = get_sketched_image(uploaded_file.read())
                sketchImage = convertQR(uploaded_file)

                time.sleep(1)
                #image.image(sketchImage)
                st.success('Converted!')
                st.success('Click "Download Image" below the QR image to download the image, or just flash the QR at any of our tablet console')
                image = st.image(sketchImage)
                st.sidebar.success("Please scroll down for your new QR!")


    if st.button("Download Image"):
        if uploaded_file:
            sketchedImage = convertQR(uploaded_file.read())
            image.image(sketchedImage)
            result = Image.fromarray(sketchedImage)
            st.success("Press the below Link")
            st.markdown(get_image_download_link(result,"sketched.jpg",'Download '+"Sketched.jpg"), unsafe_allow_html=True)
        else:
            st.error("Please upload a image first")

if rad == "About SmartGym":
    st.markdown(
                """## Contributions
                    This an open source project and you are very welcome to **contribute** your awesome
                    comments, questions, resources and apps as
                    [issues](https://github.com/MarcSkovMadsen/awesome-streamlit/issues) or
                    [pull requests](https://github.com/MarcSkovMadsen/awesome-streamlit/pulls)
                    to the [source code](https://github.com/MarcSkovMadsen/awesome-streamlit).
                    For more details see the [Contribute](https://github.com/marcskovmadsen/awesome-streamlit#contribute) section of the README file.
                    ## The Developer
                    This project is developed by Marc Skov Madsen. You can learn more about me at
                    [datamodelsanalytics.com](https://datamodelsanalytics.com).
                    Feel free to reach out if you wan't to join the project as a developer. You can find my contact details at [datamodelsanalytics.com](https://datamodelsanalytics.com).
                    [<img src="https://github.com/MarcSkovMadsen/awesome-streamlit/blob/master/assets/images/datamodelsanalytics.png?raw=true" style="max-width: 700px">](https://datamodelsanalytics.com)
                    """,
                                unsafe_allow_html=True,
            )
    weight_stack_img = Image.open("smartgym-shoulder-press.png")
    st.image(weight_stack_img)

if rad == "Campaigns":
    st.markdown(
                """## Contributions
                    This an open source project and you are very welcome to **contribute** your awesome
                    comments, questions, resources and apps as
                    [issues](https://github.com/MarcSkovMadsen/awesome-streamlit/issues) or
                    [pull requests](https://github.com/MarcSkovMadsen/awesome-streamlit/pulls)
                    to the [source code](https://github.com/MarcSkovMadsen/awesome-streamlit).
                    For more details see the [Contribute](https://github.com/marcskovmadsen/awesome-streamlit#contribute) section of the README file.
                    ## The Developer
                    This project is developed by Marc Skov Madsen. You can learn more about me at
                    [datamodelsanalytics.com](https://datamodelsanalytics.com).
                    Feel free to reach out if you wan't to join the project as a developer. You can find my contact details at [datamodelsanalytics.com](https://datamodelsanalytics.com).
                    [<img src="https://github.com/MarcSkovMadsen/awesome-streamlit/blob/master/assets/images/datamodelsanalytics.png?raw=true" style="max-width: 700px">](https://datamodelsanalytics.com)
                    """,
                                unsafe_allow_html=True,
            )
    promo_img = Image.open("promo.jpeg")
    st.image(promo_img)
