import requests
import av
import streamlit as st
import detection
from streamlit_webrtc import WebRtcMode, webrtc_streamer
import logging

BASE_URL = 'https://barcode-2b4ufemqia-lz.a.run.app'


def add_product(barcode_id):
    res = requests.post(BASE_URL + '/addproduct', json={'barcode_id': str(barcode_id)})
    st.text(res.content)


def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    image = frame.to_ndarray(format="bgr24")

    annotated_frame, result = detection.detect_barcode(image)
    if not result:
        return av.VideoFrame.from_ndarray(image, format="bgr24")
    else:
        add_product(result)
        return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")


st_webrtc_logger = logging.getLogger("streamlit_webrtc")
st_webrtc_logger.setLevel(logging.WARNING)

aioice_logger = logging.getLogger("aioice")
aioice_logger.setLevel(logging.WARNING)

st.markdown("Scan view")
st.sidebar.markdown("Scan view")

st.subheader("Scan your groceries")


webrtc_streamer(
        key="object-detection",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        video_frame_callback=video_frame_callback,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=False)
