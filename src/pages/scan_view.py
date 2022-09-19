import requests
import av
import streamlit as st
import detection
from streamlit_webrtc import webrtc_streamer


def add_product(barcode_id):
    res = requests.post('http://127.0.0.1:5000/addproduct', json={'barcode_id': str(barcode_id)})
    st.text(res.content)


def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    image = frame.to_ndarray(format="bgr24")

    annotated_frame, result = detection.detect_barcode(image)
    if not result:
        return av.VideoFrame.from_ndarray(image, format="bgr24")
    else:
        add_product(result)
        return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")

st.markdown("Scan view")
st.sidebar.markdown("Scan view")

st.subheader("Scan your groceries")
webrtc_streamer(key="detection_frame",
                video_frame_callback=video_frame_callback,
                media_stream_constraints={"video": True, "audio": False},
                async_processing=True, )
