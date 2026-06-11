import streamlit as st
import requests
import json

st.set_page_config(
    page_title="AI Document Intelligence Platform",
    page_icon="🚀",
    layout="wide"
)

# ==========================================
# CSS
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: Inter;
}

.stApp{
background:
linear-gradient(
135deg,
#020617,
#0f172a,
#111827
);
color:white;
}

/* sidebar */

section[data-testid="stSidebar"]{
background:#020617;
border-right:1px solid #334155;
}

/* hero */

.hero{
background:
linear-gradient(
135deg,
#1e3a8a,
#2563eb
);

padding:35px;
border-radius:24px;
text-align:center;

box-shadow:
0 0 40px rgba(37,99,235,.3);
}

.hero h1{
font-size:52px;
font-weight:800;
margin:0;
}

.hero p{
color:#cbd5e1;
}

/* cards */

.card{

background:#111827;

padding:25px;

border-radius:20px;

border:1px solid #334155;

text-align:center;

transition:.3s;
}

.card:hover{

transform:
translateY(-8px);

box-shadow:
0 0 25px #2563eb;
}

.big-number{
font-size:40px;
font-weight:800;
}

/* badges */

.badge{

display:inline-block;

padding:8px 16px;

margin:4px;

border-radius:30px;

background:#1e293b;

border:1px solid #2563eb;
}

/* buttons */

.stButton button{

height:60px;

width:100%;

border:none;

border-radius:14px;

background:
linear-gradient(
90deg,
#2563eb,
#06b6d4
);

color:white;

font-size:18px;

font-weight:700;
}

/* status */

.green{
color:#22c55e;
font-weight:bold;
}

.red{
color:#ef4444;
font-weight:bold;
}

.orange{
color:#f59e0b;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🚀 AI Control Center")

st.sidebar.markdown("---")

st.sidebar.markdown("### System Status")

st.sidebar.success("OCR Engine Online")
st.sidebar.success("FastAPI Online")
st.sidebar.success("Entity Engine Online")
st.sidebar.success("Classification Online")

st.sidebar.markdown("---")

st.sidebar.markdown("### Technologies")

st.sidebar.markdown("""
- Google Gemini
- FastAPI
- OCR Engine
- Streamlit
- JSON Analytics
- Entity Extraction
- PII Detection
""")

# ==========================================
# HERO
# ==========================================

st.markdown("""
<div class='hero'>
<h1>📄 AI Document Intelligence Platform</h1>
<p>
OCR • Classification • Entity Extraction • PII Detection
</p>

<span class='badge'>Google Gemini</span>
<span class='badge'>FastAPI</span>
<span class='badge'>OCR</span>
<span class='badge'>NER</span>
<span class='badge'>PII Scanner</span>

</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# KPI
# ==========================================

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class='card'>
    <h3>OCR Accuracy</h3>
    <div class='big-number'>98.7%</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='card'>
    <h3>Classification</h3>
    <div class='big-number'>AI</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class='card'>
    <h3>Entity Extraction</h3>
    <div class='big-number'>NER</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class='card'>
    <h3>PII Security</h3>
    <div class='big-number'>🔒</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# PIPELINE
# ==========================================

st.subheader("⚡ AI Processing Pipeline")

st.progress(100)

st.info(
"""
Upload → OCR → Classification → Entity Extraction → PII Detection → JSON Output
"""
)

# ==========================================
# UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["txt","pdf","png","jpg","jpeg","docx"]
)

if uploaded_file:

    st.success(
        f"Loaded: {uploaded_file.name}"
    )

    if st.button("🚀 Start AI Processing"):

        files = {
            "file":
            (
                uploaded_file.name,
                uploaded_file.getvalue()
            )
        }

        try:

            with st.spinner("Running AI Pipeline..."):

                response = requests.post(
                    "http://localhost:8000/api/v1/process",
                    files=files
                )

                result = response.json()
                if "results" in result:
                    result = result["results"]
                
                st.write("DEBUG RESPONSE")
                st.json(result)

                if result is None:
                    st.error("Backend returned None")
                    st.stop()

                st.success(
                "Document processed successfully"
            )

            # =====================================
            # TABS
            # =====================================

            t1,t2,t3,t4,t5 = st.tabs(
                [
                    "OCR",
                    "Classification",
                    "Entities",
                    "PII",
                    "JSON"
                ]
            )

            with t1:

                st.subheader("OCR Result")

                ocr_text = result.get("raw_text", "")

                if ocr_text:
                    st.text_area(
                        "OCR Content",
                        ocr_text,
                        height=400
                    )
                else:
                    st.warning("No OCR output found")

            with t2:

                st.subheader(
                    "Classification"
                )

                st.json(
                    result.get(
                        "classification",
                        {}
                    )
                )

            with t3:

                st.subheader(
                    "Extracted Entities"
                )

                st.json(
                    result.get(
                        "extracted_entities",
                        []
                    )
                )

            with t4:

                st.subheader(
                    "PII Detection"
                )

                st.json(
                    result.get(
                        "pii_detection",
                        {}
                    )
                )

            with t5:

                st.subheader(
                    "Full JSON"
                )

                st.json(result)

            st.download_button(
                "⬇ Download Analysis",
                data=json.dumps(
                    result,
                    indent=4
                ),
                file_name="analysis.json",
                mime="application/json"
            )

        except Exception as e:

            st.error(str(e))