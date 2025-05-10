import streamlit as st
from PIL import Image
import os
import tempfile
import imageio
import io
from moviepy.editor import ImageSequenceClip

st.set_page_config(page_title="🧢 TWNTY-TWO GIF Creator", layout="centered")

st.markdown("""
    <style>
    .main {background-color: #fff;}
    h1, h2, h3 {color: #111; font-family: 'Helvetica Neue', sans-serif;}
    .stButton>button {background-color: #111;color: white;border-radius: 8px;}
    </style>
""", unsafe_allow_html=True)

st.title("🧢 TWNTY-TWO GIF Creator")
st.write("Upload your images, set the frame duration, and generate a square-format GIF or video.")

uploaded_files = st.file_uploader("Upload images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
duration = st.slider("Frame display time (seconds)", min_value=0.5, max_value=5.0, value=1.5, step=0.1)
output_format = st.radio("Choose output format", ["GIF", "MP4 (video)"])

if uploaded_files:
    filenames = sorted(uploaded_files, key=lambda f: f.name)
    st.write("**Preview of upload order:**")
    for file in filenames:
        st.text(file.name)

    if st.button("Create Output"):
        with tempfile.TemporaryDirectory() as tmpdir:
            images = []
            for file in filenames:
                img_path = os.path.join(tmpdir, file.name)
                with open(img_path, "wb") as f:
                    f.write(file.read())
                img = Image.open(img_path).convert("RGB")
                min_side = min(img.size)
                img_cropped = img.crop(((img.width - min_side) // 2,
                                        (img.height - min_side) // 2,
                                        (img.width + min_side) // 2,
                                        (img.height + min_side) // 2))
                images.append(img_cropped)

            if output_format == "GIF":
                gif_path = os.path.join(tmpdir, "twnty_two_hat.gif")
                images[0].save(gif_path, save_all=True, append_images=images[1:], duration=int(duration * 1000), loop=0)
                st.success("GIF created!")
                with open(gif_path, "rb") as f:
                    st.download_button("Download GIF", f, file_name="twnty_two_hat.gif", mime="image/gif")

            else:  # MP4
                frames = [img.copy() for img in images]
                mp4_path = os.path.join(tmpdir, "twnty_two_hat.mp4")
                clip = ImageSequenceClip([img for img in frames], fps=1 / duration)
                clip.write_videofile(mp4_path, codec="libx264", audio=False, verbose=False, logger=None)
                st.success("MP4 video created!")
                with open(mp4_path, "rb") as f:
                    st.download_button("Download MP4", f, file_name="twnty_two_hat.mp4", mime="video/mp4")
