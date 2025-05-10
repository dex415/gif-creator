
import streamlit as st
from PIL import Image
import os
import tempfile
import imageio

st.set_page_config(page_title="GIF Maker", layout="centered")
st.title("🧢 TWNTY-TWO GIF Creator")
st.write("Upload your images, set the frame duration, and generate a square-format GIF.")

uploaded_files = st.file_uploader("Upload images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
duration = st.slider("Frame display time (seconds)", min_value=0.5, max_value=5.0, value=1.5, step=0.1)

if uploaded_files:
    filenames = sorted(uploaded_files, key=lambda f: f.name)
    st.write("Preview of upload order:")
    for file in filenames:
        st.text(file.name)

    if st.button("Create GIF"):
        with tempfile.TemporaryDirectory() as tmpdir:
            images = []
            for file in filenames:
                img_path = os.path.join(tmpdir, file.name)
                with open(img_path, "wb") as f:
                    f.write(file.read())
                img = Image.open(img_path)
                min_side = min(img.size)
                img_cropped = img.crop(((img.width - min_side) // 2,
                                        (img.height - min_side) // 2,
                                        (img.width + min_side) // 2,
                                        (img.height + min_side) // 2))
                images.append(img_cropped)

            output_path = os.path.join(tmpdir, "output.gif")
            images[0].save(output_path, save_all=True, append_images=images[1:], duration=int(duration * 1000), loop=0)

            st.success("GIF created!")
            with open(output_path, "rb") as f:
                st.download_button("Download GIF", f, file_name="twnty_two_hat.gif", mime="image/gif")
