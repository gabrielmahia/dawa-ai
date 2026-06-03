import streamlit as st
import urllib.request, json

st.set_page_config(page_title="Dawa AI — Habari za Dawa", page_icon="💊", layout="centered")
st.markdown("""<style>
.stApp{background:#0a0f0a;color:#e8f5e9}
.d-card{background:#0d1f0d;border:1px solid #1b5e20;border-radius:10px;padding:14px 18px;margin:8px 0}
.warn{background:#1a1000;border:1px solid #ff8f00;border-radius:8px;padding:10px 14px;margin:8px 0}
.stButton>button{background:#1b5e20;color:#fff;border:none;border-radius:8px;padding:10px 24px;font-weight:700;width:100%}
</style>""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY","")

SYSTEM = """Wewe ni mshauri wa dawa kwa wagonjwa Kenya. 
Toa habari za dawa kwa Kiswahili rahisi lakini KILA WAKATI:
1. Sisitiza mtu aone daktari au dawa
2. Sema kama dawa inahitaji agizo la daktari
3. Onyesha madhara makubwa yanayohitaji kwenda hospitali mara moja
4. Toa jina la dawa ya jumla (generic) kama dawa ya bei ghali
5. Kumbuka: Hii si ushauri wa dawa — ni habari tu

Jibu kwa: Nini ni dawa hii | Inatibu nini | Jinsi ya kutumia | Madhara | Tahadhari | Dawa mbadala nafuu"""

def ask_dawa(query):
    if not API_KEY: return "❌ API key not configured."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    body = {
        "contents":[{"role":"user","parts":[{"text":query}]}],
        "systemInstruction":{"parts":[{"text":SYSTEM}]},
        "generationConfig":{"temperature":0.2,"maxOutputTokens":700}}
    try:
        req = urllib.request.Request(url,data=json.dumps(body).encode(),
                                     headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=30) as r:
            return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e: return f"❌ {e}"

st.markdown("# 💊 Dawa AI")
st.markdown("**Habari za Dawa kwa Kiswahili**")

st.markdown('<div class="warn">⚠️ <b>Tahadhari:</b> Habari hizi ni kwa elimu tu. Daima shauriana na daktari au dawa kabla ya kutumia dawa yoyote.</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔍 Tafuta Dawa", "⚠️ Mwingiliano wa Dawa", "💰 Dawa Nafuu"])

with tab1:
    drug_name = st.text_input("Jina la dawa:", placeholder="Mfano: Paracetamol, Amoxicillin, Metformin")
    age_group = st.selectbox("Umri:", ["Mtu mzima (18+)","Mtoto (2-17)","Mzee (65+)","Mjamzito"])
    if st.button("🔍 Pata Habari", key="drug_btn") and drug_name:
        with st.spinner("Ninatafuta..."):
            result = ask_dawa(f"Niambie kuhusu dawa: {drug_name}. Mtumiaji: {age_group}")
        st.markdown(f'<div class="d-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab2:
    d1 = st.text_input("Dawa ya kwanza:", key="d1")
    d2 = st.text_input("Dawa ya pili:", key="d2")
    if st.button("⚠️ Angalia Mwingiliano", key="interact_btn") and d1 and d2:
        with st.spinner("Ninachunguza..."):
            result = ask_dawa(f"Je, kuna mwingiliano hatari kati ya {d1} na {d2}? Eleza kwa undani.")
        st.markdown(f'<div class="d-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab3:
    brand = st.text_input("Jina la dawa ya bei ghali (brand name):", placeholder="Mfano: Augmentin")
    if st.button("💰 Tafuta Mbadala Nafuu", key="generic_btn") and brand:
        with st.spinner("Ninatafuta mbadala..."):
            result = ask_dawa(f"Dawa mbadala nafuu (generic) ya {brand} Kenya ni gani? Taja bei ya makadirio na upatikanaji.")
        st.markdown(f'<div class="d-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("💊 Dawa AI v1.0 | KAMA HALI YA DHARURA: Piga 0800 720 553 (NHIF) au nenda hospitali | CC BY-NC-ND 4.0")
