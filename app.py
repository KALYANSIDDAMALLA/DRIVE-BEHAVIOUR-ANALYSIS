
import streamlit as st
import tempfile
from processor import TrafficAnalyzer

st.set_page_config(page_title="Behavioral AI Dashboard", layout="wide")
st.title("🛡️ Driver Behavioral Analysis & Detection")

st.sidebar.header("Configuration")
thresholds = {
    'speed_limit': st.sidebar.slider("Speed Limit (km/h)", 30, 120, 60)
}

if 'analyzer' not in st.session_state:
    st.session_state.analyzer = TrafficAnalyzer()

uploaded_file = st.file_uploader("Upload Traffic Footage", type=["mp4"])

if 'analysis_done' not in st.session_state: st.session_state.analysis_done = False

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    if st.button("🚀 Run Analysis & Generate Report"):
        with st.spinner("Processing video..."):
            df = st.session_state.analyzer.process_video(tfile.name, thresholds)
            st.session_state.results_df = df
            st.session_state.analysis_done = True

if st.session_state.analysis_done:
    st.subheader("📊 Infraction Catalog")
    st.dataframe(st.session_state.results_df, use_container_width=True)
    
    pdf_bytes = st.session_state.analyzer.generate_pdf(st.session_state.results_df)
    st.download_button("📥 Download A4 PDF Report", data=pdf_bytes, file_name="Report.pdf", mime="application/pdf")
    
    if st.button("Clear Results"):
        st.session_state.analysis_done = False
        st.rerun()
