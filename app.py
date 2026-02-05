# app.py
# Тоза ва Streamlit Cloud га жойлаштиришга мосланган версия
# Иложи борича хавфсизлик ва кириш текширувлари қўшилди.
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
import io

st.set_page_config(
    page_title="Генетик Хавф Бахолаш",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Хавфни ҳисобловчи функция (илтимос: бу мисол учун, клиник тасдиқсиз) ---
@st.cache_data
def compute_risk_score(row):
    """
    Содда, шарҳли скор: фақат демонстрация мақсадида.
    Қўшимча клиник/генетик моделлар билан алмаштиринг.
    Ҳар бир кириш учун салбий/ижобий салмоқлар қўйилган.
    """
    score = 0.0
    # Йош
    age = float(row.get("age", 30) or 30)
    if age < 20:
        score += 0.5
    elif age < 35:
        score += 1.0
    else:
        score += 2.0

    # Ҳомила муддати (hafta)
    ga = float(row.get("gestational_week", 12) or 12)
    if ga < 12:
        score += 0.5
    elif ga <= 20:
        score += 0.8
    else:
        score += 1.0

    # От/онада генетик касаллик тарихи
    if str(row.get("parent_history", "")).lower() in ("yes", "true", "1", "ҳa", "ха"):
        score += 4.0

    # Олдинги фарзандда генетик касаллик
    if str(row.get("previous_child_affected", "")).lower() in ("yes", "true", "1", "ҳa", "ха"):
        score += 5.0

    # Қон оилавийлик (consanguinity)
    if str(row.get("consanguinity", "")).lower() in ("yes", "true", "1", "ҳa", "ха"):
        score += 3.0

    # Натижани нормализациялаш (0-100%)
    # Бу ерда максимал назарий балл 15 деб қабул қилинган
    max_score = 15.0
    risk_percent = min(100.0, (score / max_score) * 100.0)
    # Қўшимча категория
    if risk_percent >= 60:
        category = "Юқори хавф"
    elif risk_percent >= 30:
        category = "Ўртача хавф"
    else:
        category = "Паст хавф"

    return {
        "raw_score": round(score, 2),
        "risk_percent": round(risk_percent, 1),
        "category": category
    }

# --- UI ---
st.markdown("<h1 style='text-align:center'>Генетик Хавф Бахолаш Тиббий Дастури</h1>", unsafe_allow_html=True)
st.write("Эслатма: ушбу дастур илмий ёки клиник тасдиқга эга эмас. Фақат илмий-таҳлил ва презентация учун мос.")

with st.sidebar:
    st.header("Кириш маълумотлари")
    mode = st.radio("Режимни танланг", ("Биргача киритиш (Single)", "Кўпчиллик (CSV upload)"))

if mode == "Биргача киритиш (Single)":
    st.subheader("Бир маълумот киритиш")
    with st.form("single_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Ёш (ёшда, йил)", min_value=13, max_value=65, value=30)
            gestational_week = st.number_input("Ҳомила муддати (ҳафта)", min_value=4, max_value=42, value=12)
            consanguinity = st.selectbox("Оилавий яқин никоҳ (consanguinity)?", ("Йўқ", "Ҳа"))
        with col2:
            parent_history = st.selectbox("Ота/оналарида генетик касаллик тарихи?", ("Йўқ", "Ҳа"))
            previous_child_affected = st.selectbox("Аллақачон аввалги фарзандда генетик касаллик бўлганми?", ("Йўқ", "Ҳа"))
            notes = st.text_area("Қўшимча маълумот (ихтиёрий)", value="", height=75)

        submitted = st.form_submit_button("Ҳисоблаш")
    if submitted:
        row = {
            "age": age,
            "gestational_week": gestational_week,
            "consanguinity": "yes" if consanguinity == "Ҳа" else "no",
            "parent_history": "yes" if parent_history == "Ҳа" else "no",
            "previous_child_affected": "yes" if previous_child_affected == "Ҳа" else "no",
            "notes": notes
        }
        try:
            res = compute_risk_score(row)
            st.success(f"Хавф: {res['risk_percent']}% — {res['category']}")
            st.write("Детал натижалар:")
            st.json(res)
        except Exception as e:
            st.error(f"Ҳисоблашда хато юз берди: {e}")

else:
    st.subheader("Кўпчилик (CSV) — талаб қилинган сутунлар: age, gestational_week, consanguinity, parent_history, previous_child_affected")
    uploaded_file = st.file_uploader("CSV файлини юкланг", type=["csv", "txt"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            required = {"age", "gestational_week", "consanguinity", "parent_history", "previous_child_affected"}
            if not required.issubset(set(df.columns)):
                st.error(f"CSV да камчилик: камида қуйидаги сутунлар бўлиши лозим: {', '.join(required)}")
            else:
                out = []
                for _, r in df.iterrows():
                    rec = compute_risk_score(r)
                    out.append({**r.to_dict(), **rec})
                out_df = pd.DataFrame(out)
                st.success("Ҳисоблаш тугаланди")
                st.dataframe(out_df)
                towrite = io.BytesIO()
                out_df.to_csv(towrite, index=False)
                towrite.seek(0)
                st.download_button("Натижани CSV сифатида юклаб олиш", data=towrite, file_name="risk_results.csv", mime="text/csv")
        except Exception as e:
            st.error(f"Файлни ўқишда хатолик: {e}")

# --- Фойдаланувчига хавф ҳақида тавсиялар ---
st.markdown("---")
st.subheader("Натижаларни талқин қилиш")
st.markdown("""
- Ushbu ҳисоб-китоб содда қоидаларга асосланган демонстрациядир.  
- Агар балл ёки хавф юқори бўлса, малакали генетик маслаҳат олиш тавсия этилади.  
- Қонунчилик ва шахсий маълумотлар хавфсизлигига риоя қилинг.
"""
)

st.markdown("---")
st.caption("Ишончли моделлар (genetic risk models) киритилса, compute_risk_score() ичидаги логикани алмаштиринг ёки ўринга машинани ўрганиш моделини юкланг.")
