from rembg import remove
from PIL import Image, UnidentifiedImageError
import streamlit as st
import pyheif
import io

st.title("Image Background Remover")

uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg", "jpeg", "heic"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.heic'):
            heif_image = pyheif.read_heif(uploaded_file)
            image = Image.frombytes(
                heif_image.mode,
                heif_image.size,
                heif_image.data,
                "raw",
                heif_image.mode,
                heif_image.stride,
            )
        else:
            image = Image.open(uploaded_file)

        image = image.convert("RGBA")
        st.image(image, caption="Original Image", use_column_width=True)

        if st.button("Remove Background"):
            try:
                output_image = remove(image)
                st.image(output_image, caption="Background Removed", use_column_width=True)
                output_path = 'output.png'
                output_image.save(output_path)
                with open(output_path, 'rb') as file:
                    st.download_button("Download Background Removed Image", file.read(), file_name='background_removed.png')
            except Exception as e:
                st.error("Error removing the background. Please try again with a different image.")
    except UnidentifiedImageError:
        st.error("Invalid image file. Please upload a valid image file.")
