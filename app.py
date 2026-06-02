import streamlit as st
import tempfile
from processor import TrafficAnalyzer

# Page Configuration
st.set_page_config(page_title="GuardianAI | Fleet Safety", layout="wide", page_icon="🛡️")

# Professional SaaS Styling
st.markdown("""
    <style>
    .hero { text-align: center; padding: 3rem 1rem; background: white; border-bottom: 2px solid #e1e4e8; margin-bottom: 2rem; border-radius: 10px; }
    h1 { color: #1a2a6c; font-weight: 800; }
    .card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); }
    div.stButton > button { background-color: #007bff; color: white; border-radius: 8px; font-weight: bold; width: 100%; height: 3em; border: none; }
    div.stButton > button:hover { background-color: #0056b3; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="hero"><h1>GuardianAI Fleet Auditor</h1><p>Enterprise-grade driver behavior analytics powered by deep learning.</p></div>', unsafe_allow_html=True)

# Main Interaction Engine
col_left, col_right = st.columns([1, 1])

if 'analyzer' not in st.session_state:
    st.session_state.analyzer = TrafficAnalyzer()

with col_left:
    st.markdown('<div class="card"><h3>Upload Footage</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Select your traffic footage (MP4)", type=["mp4"])
    if uploaded_file and st.button("RUN FORENSIC ANALYSIS"):
        with st.spinner("Analyzing high-resolution frames..."):
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_file.read())
            df = st.session_state.analyzer.process_video(tfile.name, {'speed_limit': 70})
            st.session_state.results = df
            st.session_state.done = True
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="card"><h3>Why GuardianAI?</h3><ul><li><b>Real-time Detection:</b> Identify unsafe maneuvers instantly.</li><li><b>Compliance Ready:</b> Auto-generate audit-grade PDF reports.</li><li><b>GDPR Compliant:</b> Privacy-first architecture.</li></ul></div>', unsafe_allow_html=True)

# Results Section
if st.session_state.get('done'):
    st.subheader("📊 Audit Results Overview")
    k1, k2 = st.columns(2)
    k1.metric("Vehicles Analyzed", len(st.session_state.results))
    k2.metric("Risk Incidents Found", len(st.session_state.results[st.session_state.results['Risk Level'] == 'HIGH']))
    st.dataframe(st.session_state.results, use_container_width=True)
    
    pdf = st.session_state.analyzer.generate_pdf(st.session_state.results)
    st.download_button("📥 DOWNLOAD OFFICIAL AUDIT REPORT", data=pdf, file_name="Audit_Report.pdf", mime="application/pdf")

# About the Developer
st.divider()
st.markdown("## 👨‍💻 About the Developer")
col_img, col_txt = st.columns([1, 4])

with col_img:
    st.image("https://github.com/kalyansiddamalla.png", width=150)

with col_txt:
    st.markdown("### **Kalyan Siddamalla**")
    st.markdown("**MSc Data Science | AI Researcher**")
    st.write("Bridging the gap between raw traffic data and actionable safety intelligence through advanced computer vision.")
    st.markdown("[🔗 LinkedIn](https://www.linkedin.com/in/kalyansiddamalla2707/) | [🐙 GitHub](https://github.com/kalyansiddamalla)")
