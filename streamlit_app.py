import streamlit as st
import time
from PIL import Image
import os
import boto3

"""
# Welcome to AI-mazing Art!

"""
# AWS credentials
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = os.environ.get('AWS_SESSION_TOKEN')

# Connect to S3
s3 = boto3.resource(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN
    )

col1, col2, col3 = st.columns([2,1,1])

uploaded_photo = col1.file_uploader(" Upload your image")
if uploaded_photo is not None:
    # Erstellen Sie einen eindeutigen Dateinamen durch Zählen der vorhandenen Dateien im Ordner 'AImages'
    existing_files = s3.Bucket('aimagez').objects.filter(Prefix='AImages/')
    file_count = sum(1 for _ in existing_files)
    unique_filename = f"AImages/{file_count + 1}.png"

    # Hochladen des Bildes in den S3 Bucket
    s3.Bucket('aimagez').put_object(Key=unique_filename, Body=uploaded_photo.read(), ACL='public-read')
    st.success("Bild erfolgreich in S3 Bucket hochgeladen!")

    # Laden aller Bilder aus dem S3 Bucket beim Start der App
    all_images = list(s3.Bucket('aimagez').objects.filter(Prefix='AImages/'))

    # Erstellen eines Image Grids zur Anzeige aller hochgeladenen Bilder
    for i in range(0, len(all_images), 3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(all_images):
                image_path = f"https://aimagez.s3.amazonaws.com/{all_images[i+j].key}"
                cols[j].image(image_path, width=200)
