from rembg import remove
from PIL import Image
import streamlit as st
from pyheif_pillow_opener import register_heif_opener
import io

st.title("Image Background Remover")
choice = st.sidebar.radio('Navigation',('Upload','Remove'))


if choice=='Upload':
    uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg","jpeg"])
    if uploaded_file is not None:
        if uploaded_file.type == 'application/octet-stream' and uploaded_file.name.endswith('.heic'):
            register_heif_opener()
            image = Image.open(io.BytesIO(uploaded_file.read()))
        else:
            image = Image.open(uploaded_file)
        image = image.convert("RGBA")
        img_stream = io.BytesIO()
        image.save(img_stream, format="PNG")
        st.image(image, caption="Original Image", use_column_width=True)

else:
    input_path = 'img_stream.png'
    st.image(input_path, caption="Original Image", use_column_width=True)
    output_path = 'output.png'
    input_image = Image.open(input_path)
    output_image = remove(input_image)
    output_image.save(output_path)
    st.image(output_path, caption="Background Removed", use_column_width=True)
    with open(output_path, 'rb') as file:
        st.download_button("Download Background Removed Image", file.read(), file_name='background_removed.png')
