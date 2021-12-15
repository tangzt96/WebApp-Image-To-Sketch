import streamlit as st
import time
#import cv2
from PIL import Image
import numpy as np
import io
from io import BytesIO
import base64
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode


st.set_page_config(
     page_title="QR code enhancement",
     initial_sidebar_state="auto",
)

def get_image_download_link(img,filename,text):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href =  f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href


def convertQR(img):
    data = decode(Image.open(img))
    if len(data) < 1:
        return False
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



#uploaded_file = st.sidebar.file_uploader(" ", type=['png', 'jpg', 'jpeg'])

# if uploaded_file is not None:  
#     image.image(uploaded_file)
if rad == "QR Helper":
    img = Image.open("screenshot_guide.png")
    image = st.image(img)
    uploaded_file = st.file_uploader(" ", type=['png', 'jpg', 'jpeg'])
    if st.button("Enhance QR"):
        
        if uploaded_file is None:
            st.error("Please upload a QR to convert")
            
        else:
            with st.spinner('Converting...'):
                
                # sketchImage = get_sketched_image(uploaded_file.read())
                sketchImage = convertQR(uploaded_file)
                if sketchImage != False:
                    time.sleep(1)
                    #image.image(sketchImage)
                    st.success('Converted!')
                    st.success('Click "Download Image" below the QR image to download the image, or just flash the QR at any of our tablet console')
                    image = st.image(sketchImage)
                    st.success("Please scroll down for your new QR!")
                else:
                    st.error("No QR code detected, Please upload image with QR Code")

    if uploaded_file is not None:
        if st.button("Download Image"):
            if uploaded_file:
                sketchImage = convertQR(uploaded_file)
                image = st.image(sketchImage)
                result = Image.open(BytesIO(sketchImage))
                st.success("Press the below Link")
                st.markdown(get_image_download_link(result,"sketched.jpg",'Download '+"Sketched.jpg"), unsafe_allow_html=True)
            else:
                st.error("Please upload a image first")


if rad == "About SmartGym":
    st.title("SmartGym – Every Citizen’s #1 Fitness Lifestyle Companion")
    st.markdown("SmartGym is a holistic fitness data platform that provides users with fitness insights measured through a series of connected sensors built into gym equipment. These sensors are currently installed on three types of gym equipment: 1) weight stack machines, 2) treadmills and 3) weighing machines. SmartGym equipment is currently deployed in three community gyms across Singapore – Our Tampines Hub, Jurong East and Heartbeat @ Bedok.")
    st.subheader("Weight Stack Machines")
    st.markdown("The SmartGym sensors are installed within the covers of the weight stack exteriors, are visible to users and help detect the weights lifted to accurately compute the number of repetitions done.")
    weight_stack_img = Image.open("smartgym-shoulder-press.png")
    st.image(weight_stack_img)

    st.subheader("How Will SmartGym Benefit Users?")
    st.markdown("Where SmartGym separates itself from regular gym equipment is its ability to accurately monitor and store users’ data. In a typical gym, fitness equipment can only display workout information while it is being used and the information does not get stored thereafter. In contrast, SmartGym stores workout information that can be viewed at any time at any of the three SmartGym kiosks.")
    console_img = Image.open("smartgym-console.png")
    st.image(console_img)


if rad == "Campaigns":
    st.title("Current Campaigns in SmartGym!")
    st.markdown("We have awesome monthly leaderboard challenge and campaigns with attractive prizes")
    st.subheader("1 for 1 promotion")
    promo_img = Image.open("promo.jpeg")
    st.image(promo_img)
