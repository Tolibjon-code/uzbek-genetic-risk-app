# app.py - Хомиладор аёлларда ирсий касалликлар хавфини бахолаш дастури
# Life Cecly, Astarea, FMD, Prisca тизимлари асосида

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import json
import base64
import warnings
warnings.filterwarnings('ignore')

# ==================== КОНФИГУРАЦИЯ ====================
st.set_page_config(
    page_title="Генетик Хавф Бахолаш Тиббий Дастури",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': """
        ### Тиббий Генетик Хавф Бахолаш Дастури v3.0
        
        **Дастур мақсади:** Хомиладор аёлларда ирсий касалликлар хавфини 
        комплекс бахолаш ва таҳлил қилиш.
        
        **Технологиялар:** Python, Streamlit, Plotly, Pandas
        **Скрининг тизимлари:** Life Cecly, Astarea, FMD, Prisca
        **Ишлаб чиқувчи:** Тиббий информатика маркази
        
        © 2024 Барча ҳуқуқлар ҳимояланган.
        """
    }
)

# ==================== СТИЛЛАР ВА CSS ====================
st.markdown("""
<style>
    /* Асосий стиллар */
    .main-header {
        font-size: 2.8rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1a2980, #26d0ce);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 500;
    }
    
    /* Хавф категориялари учун стиллар */
    .risk-critical {
        background: linear-gradient(135deg, #ff416c, #ff4b2b);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        border: 3px solid #ff0000;
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.3);
        animation: pulse 2s infinite;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #ff9966, #ff5e62);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        border: 3px solid #ff6b6b;
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #f9d423, #ff4e50);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        border: 3px solid #f9a825;
        box-shadow: 0 4px 10px rgba(249, 168, 37, 0.3);
    }
    
    .risk-low {
        background: linear-gradient(135deg, #56ab2f, #a8e063);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        border: 3px solid #4caf50;
        box-shadow: 0 4px 10px rgba(76, 175, 80, 0.3);
    }
    
    /* Карталар учун стиллар */
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 20px;
        margin: 15px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin: 12px 0;
        border-left: 6px solid #3498db;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transform: translateY(-3px);
    }
    
    /* Тугмалар учун стиллар */
    .stButton>button {
        background: linear-gradient(90deg, #3498db, #2ecc71);
        color: white;
        border: none;
        padding: 14px 28px;
        border-radius: 30px;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(52, 152, 219, 0.4);
        background: linear-gradient(90deg, #2980b9, #27ae60);
    }
    
    .secondary-button {
        background: linear-gradient(90deg, #95a5a6, #7f8c8d) !important;
    }
    
    /* Сайдбар стиллари */
    .sidebar-header {
        background: linear-gradient(90deg, #2c3e50, #3498db);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Прогресс барлар */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #3498db, #2ecc71);
    }
    
    /* Анимациялар */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 0, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }
    }
    
    /* Хавф индикатори */
    .risk-indicator {
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    /* Ҳисобот картаси */
    .report-card {
        background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid #d7ccc8;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* Таблар учун стиллар */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        white-space: pre-wrap;
        background-color: #f8f9fa;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3498db !important;
        color: white !important;
    }
    
    /* Маълумотлар жадваллари учун */
    .data-table {
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ==================== СЕССИЯ СОЗЛАМАЛАРИ ====================
if 'patient_id' not in st.session_state:
    st.session_state.patient_id = f"P{datetime.now().strftime('%Y%m%d%H%M%S')}"
if 'patients_data' not in st.session_state:
    st.session_state.patients_data = []
if 'current_patient' not in st.session_state:
    st.session_state.current_patient = {}
if 'risk_history' not in st.session_state:
    st.session_state.risk_history = []
if 'show_stats' not in st.session_state:
    st.session_state.show_stats = False

# ==================== ФУНКЦИЯЛАР ====================

def calculate_bmi(weight, height):
    """BMI ҳисоблаш"""
    if height > 0:
        return weight / ((height/100) ** 2)
    return 22.0

def generate_patient_report(patient_data, risk_data, recommendations):
    """Бемор ҳақида ҳисобот яратиш"""
    report = {
        "report_id": f"R{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "patient_info": patient_data,
        "risk_assessment": risk_data,
        "recommendations": recommendations,
        "doctor_notes": "",
        "next_appointment": ""
    }
    return report

def save_to_local_storage(data, filename):
    """Маълумотларни локал сақлаш"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Сақлашда хатолик: {e}")
        return False

def load_from_local_storage(filename):
    """Маълумотларни локалдан юклаш"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def calculate_genetic_risk_advanced(params):
    """Мураккаб генетик хавф ҳисоблаш алгоритми"""
    
    risk_factors = {
        'age': 1.0,
        'bmi': 1.0,
        'family': 1.0,
        'nt': 1.0,
        'biochemical': 1.0,
        'consanguinity': 1.0,
        'previous': 1.0,
        'chronic': 1.0,
        'lifestyle': 1.0,
        'test': params.get('risk_factor', 1.0)
    }
    
    # 1. Ёш омили (деталли)
    age = params['age']
    if age < 20:
        risk_factors['age'] = 0.6
    elif age < 25:
        risk_factors['age'] = 0.8
    elif age < 30:
        risk_factors['age'] = 0.9
    elif age < 35:
        risk_factors['age'] = 1.0
    elif age < 38:
        risk_factors['age'] = 1.5
    elif age < 40:
        risk_factors['age'] = 2.2
    elif age < 42:
        risk_factors['age'] = 3.0
    else:
        risk_factors['age'] = 4.0
    
    # 2. BMI омили
    bmi = params['bmi']
    if bmi < 18.5:
        risk_factors['bmi'] = 1.3  # Паст вазн
    elif bmi < 23:
        risk_factors['bmi'] = 1.0  # Идеал
    elif bmi < 25:
        risk_factors['bmi'] = 1.1
    elif bmi < 30:
        risk_factors['bmi'] = 1.4
    elif bmi < 35:
        risk_factors['bmi'] = 1.8
    else:
        risk_factors['bmi'] = 2.2
    
    # 3. Оилавий тарих
    family_history = params.get('family_history', [])
    if family_history and "Йўқ" not in family_history:
        risk_factors['family'] = 1.8
        
        # Хусусий касалликлар учун қўшимча омиллар
        family_multipliers = {
            "Даун синдроми (трисомия 21)": 1.8,
            "Эдвардс синдроми (трисомия 18)": 1.8,
            "Патау синдроми (трисомия 13)": 1.8,
            "Спина бифида": 1.5,
            "Юрак аномалиялари": 1.4,
            "Мускул дистрофияси": 1.7,
            "Кистоз фиброз": 1.6,
            "Гемофилия": 1.5,
            "Фенилкетонурия": 1.4,
            "Нейрофиброматоз": 1.3,
            "Хромосома ўзгаришлари": 1.7,
            "Метаболик касалликлар": 1.4
        }
        
        for disease in family_history:
            if disease in family_multipliers:
                risk_factors['family'] *= family_multipliers[disease]
    
    # 4. NT (Бўйин териси қалинлиги)
    nt = params.get('nt', 1.8)
    if nt < 1.5:
        risk_factors['nt'] = 0.6
    elif nt < 2.0:
        risk_factors['nt'] = 0.8
    elif nt < 2.5:
        risk_factors['nt'] = 1.0
    elif nt < 3.0:
        risk_factors['nt'] = 2.0
    elif nt < 3.5:
        risk_factors['nt'] = 3.5
    elif nt < 4.0:
        risk_factors['nt'] = 5.0
    else:
        risk_factors['nt'] = 8.0
    
    # 5. Биохимик маркерлар
    papp_a = params.get('papp_a', 1.0)
    hcg = params.get('hcg', 1.0)
    
    risk_factors['biochemical'] = 1.0
    
    # PAPP-A учун
    if papp_a < 0.3:
        risk_factors['biochemical'] *= 2.5
    elif papp_a < 0.4:
        risk_factors['biochemical'] *= 2.0
    elif papp_a < 0.5:
        risk_factors['biochemical'] *= 1.5
    elif papp_a > 2.5:
        risk_factors['biochemical'] *= 1.3
    
    # hCG учун
    if hcg < 0.2:
        risk_factors['biochemical'] *= 2.0
    elif hcg < 0.3:
        risk_factors['biochemical'] *= 1.5
    elif hcg > 2.5:
        risk_factors['biochemical'] *= 1.4
    elif hcg > 3.5:
        risk_factors['biochemical'] *= 1.8
    
    # 6. Қариндошлик никоҳи
    if params.get('consanguinity', 'Йўқ') == "Ҳа":
        degree_multiplier = {
            "Бир аммаки/таға": 3.0,
            "Иккиламчи қариндош": 2.0,
            "Учинчи даража": 1.5,
            "Турли даражада": 2.0
        }
        consanguinity_degree = params.get('consanguinity_degree', 'Бир аммаки/таға')
        risk_factors['consanguinity'] = degree_multiplier.get(consanguinity_degree, 2.0)
    else:
        risk_factors['consanguinity'] = 1.0
    
    # 7. Олдинги аномалиялар
    if params.get('previous_abnormalities', 'Йўқ') == "Ҳа":
        risk_factors['previous'] = 3.0
    else:
        risk_factors['previous'] = 1.0
    
    # 8. Сурункарон касалликлар
    chronic_diseases = params.get('chronic_diseases', [])
    if chronic_diseases and "Йўқ" not in chronic_diseases:
        risk_factors['chronic'] = 1.5
        
        disease_multipliers = {
            "Сахар диабети (1-тип)": 1.8,
            "Сахар диабети (2-тип)": 1.7,
            "Гестацион диабет": 1.6,
            "Артериал гипертония": 1.4,
            "Гипертония хомилаликда": 1.5,
            "Эпилепсия": 1.6,
            "Аутоиммун касалликлар": 1.7,
            "Буғум касалликлари": 1.3,
            "Қалқонсимон без касалликлари": 1.4,
            "Бронхиал астма": 1.3,
            "Юрак-Қон томир касалликлари": 1.6,
            "Бўйрак касалликлари": 1.5
        }
        
        for disease in chronic_diseases:
            if disease in disease_multipliers:
                risk_factors['chronic'] *= disease_multipliers[disease]
    else:
        risk_factors['chronic'] = 1.0
    
    # 9. Ҳаёт тарзи
    risk_factors['lifestyle'] = params.get('lifestyle_factor', 1.0)
    
    # Асосий хавф
    base_risk = 0.0008  # Стандарт хавф 1:1250
    
    # Хавфни ҳисоблаш
    total_risk = base_risk
    for factor in risk_factors.values():
        total_risk *= factor
    
    # Чегаралаш (максимум 50%)
    total_risk = min(total_risk, 0.5)
    
    return total_risk, risk_factors

def get_risk_category_detailed(risk_score):
    """Деталли хавф категориясини аниқлаш"""
    if risk_score > 0.1:      # 1:10
        return "КРИТИК", "risk-critical", "#ff0000"
    elif risk_score > 0.05:   # 1:20
        return "ЖУДА ЮҚОРИ", "risk-high", "#ff4444"
    elif risk_score > 0.02:   # 1:50
        return "ЮҚОРИ", "risk-high", "#ff6b6b"
    elif risk_score > 0.01:   # 1:100
        return "ЎРТАЧА-ЮҚОРИ", "risk-medium", "#ffa726"
    elif risk_score > 0.005:  # 1:200
        return "ЎРТАЧА", "risk-medium", "#f9a825"
    elif risk_score > 0.001:  # 1:1000
        return "ПАСТ-ЎРТАЧА", "risk-low", "#4caf50"
    else:                     # 1:1000 дан кам
        return "ПАСТ", "risk-low", "#2e7d32"

def get_recommendations_by_risk(category):
    """Хавф категориясига кўра тавсиялар"""
    recommendations = {
        "КРИТИК": {
            "urgency": "ШОШИЛИНЧ",
            "actions": [
                "Дастурки генетик машварат (24 соат ичида)",
                "NIPT тести (но-инвазив пренатал тест)",
                "Амниоцентез ёки хорион биопсияси",
                "Фетал эхокардиография",
                "Невролог ва кардиолог консультацияси",
                "Ҳар ҳафта ультратовуш кўриқуви",
                "Хомилаликни даволаш мутахассиси назорати"
            ],
            "monitoring": "Ҳар ҳафта",
            "specialists": ["Генетик", "Перинатолог", "Кардиолог", "Невролог"]
        },
        "ЖУДА ЮҚОРИ": {
            "urgency": "ОЧИҚ",
            "actions": [
                "Генетик машварат (72 соат ичида)",
                "Кариотиплаш таҳлили",
                "Фетал ультратовуш (деталли)",
                "Қон биохимик маркерларини такрорлаш",
                "Эхокардиография",
                "Ҳар 2 ҳафтада мониторинг"
            ],
            "monitoring": "Ҳар 2 ҳафта",
            "specialists": ["Генетик", "Перинатолог", "УЗИ мутахассиси"]
        },
        "ЮҚОРИ": {
            "urgency": "ИММИНЕНТ",
            "actions": [
                "Генетик машварат (1 ҳафта ичида)",
                "Қўшимча скрининг тестлари",
                "20-ҳафталик деталли ультратовуш",
                "Қон тестларини такрорлаш",
                "Ҳар ойда назорат"
            ],
            "monitoring": "Ҳар ой",
            "specialists": ["Генетик", "Акушер-гинеколог"]
        },
        "ЎРТАЧА-ЮҚОРИ": {
            "urgency": "ЭХТИЁТ",
            "actions": [
                "Генетик машварат (ихтиёрий)",
                "Қўшимча ультратовуш (20-ҳафтада)",
                "Қон тестларини такрорлаш",
                "Ҳар 6 ҳафтада назорат",
                "Соглом турмуш тарзи"
            ],
            "monitoring": "Ҳар 6 ҳафта",
            "specialists": ["Акушер-гинеколог"]
        },
        "ЎРТАЧА": {
            "urgency": "НАЗОРАТ",
            "actions": [
                "Стандарт скрининг дастури",
                "Мунтазам ультратовуш",
                "Витамин ва минераллар",
                "Соглом овқатланиш",
                "Стрессдан сақланиш"
            ],
            "monitoring": "Ҳар 8 ҳафта",
            "specialists": ["Акушер-гинеколог"]
        },
        "ПАСТ-ЎРТАЧА": {
            "urgency": "ОБЫЧНЫЙ",
            "actions": [
                "Рутин тиббий кўриқув",
                "Ультратовуш (12, 20, 32 ҳафтада)",
                "Парвардалик кўрсатмаларига риоя",
                "Жисмоний фаоллик",
                "Мунтазам витаминлар"
            ],
            "monitoring": "Стандарт дастур",
            "specialists": ["Акушер-гинеколог"]
        },
        "ПАСТ": {
            "urgency": "НОРМАЛЬ",
            "actions": [
                "Стандарт парвардалик",
                "Ультратовуш (регламент буйича)",
                "Соглом турмуш тарзи",
                "Даво-профилактика витаминлари",
                "Ҳар 4 ҳафтада назорат"
            ],
            "monitoring": "Стандарт",
            "specialists": ["Акушер-гинеколог"]
        }
    }
    
    return recommendations.get(category, recommendations["ПАСТ"])

# ==================== АСОСИЙ ИНТЕРФЕЙС ====================

# САРЛАВҲА
st.markdown('<h1 class="main-header">👶 ХОМИЛАДОР АЁЛЛАРДА ИРСИЙ КАСАЛЛИКЛАР ХАВФИНИ БАХОЛАШ</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Life Cecly • Astarea • FMD • Prisca тизимлари асосида | Юқори аникликда ишлайди</p>', unsafe_allow_html=True)

# ЯНГИ БЕМОР ВА МАНАГМЕНТ
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🆕 Янги бемор", use_container_width=True, help="Янги бемор қўшиш"):
        st.session_state.current_patient = {}
        st.session_state.patient_id = f"P{datetime.now().strftime('%Y%m%d%H%M%S')}"
        st.rerun()

with col2:
    if st.button("💾 Маълумотларни сақлаш", use_container_width=True, help="Барча маълумотларни сақлаш"):
        if st.session_state.patients_data:
            if save_to_local_storage(st.session_state.patients_data, "patients_data.json"):
                st.success("Маълумотлар сақланди!")
            else:
                st.error("Сақлашда хатолик!")

with col3:
    if st.button("📊 Статистика", use_container_width=True, help="Умумий статистика"):
        st.session_state.show_stats = not st.session_state.show_stats

with col4:
    if st.button("🔄 Дастурни янгилаш", use_container_width=True, help="Барча параметрларни тозалаш"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# САЙДБАР - БЕМОР МАЪЛУМОТЛАРИ
with st.sidebar:
    st.markdown('<div class="sidebar-header"><h3>👤 БЕМОР МАЪЛУМОТЛАРИ</h3></div>', unsafe_allow_html=True)
    
    # Бемор ID
    st.info(f"**🎫 Бемор ID:** {st.session_state.patient_id}")
    
    # 1. ШАХСИЙ МАЪЛУМОТЛАР
    with st.expander("📋 Шахсий маълумотлар", expanded=True):
        patient_name = st.text_input("Фамилия Исм Шариф", 
                                   placeholder="Мадина Алиева", 
                                   help="Беморнинг тўлиқ исми")
        
        col_a, col_b = st.columns(2)
        with col_a:
            patient_age = st.number_input("Ёши", 15, 55, 30, 
                                        help="Беморнинг ёши (15-55)")
        with col_b:
            gestational_age = st.number_input("Хомилалик (ҳафта)", 5, 42, 12,
                                            help="Хомилалик даври (5-42 ҳафта)")
        
        parity = st.selectbox("Туғишлар сони", 
                            ["0 - биринчи хомилалик", "1", "2", "3", "4", "5 ёки кўп"],
                            index=0)
        
        blood_group = st.selectbox("Қон гуруҳи", 
                                 ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Аник эмас"],
                                 index=8)
        
        registration_date = st.date_input("Рўйҳатга олиш санаси", date.today())
    
    # 2. ОИЛАВИЙ ТАРИХ
    with st.expander("👨‍👩‍👧‍👦 Оилавий тарих", expanded=True):
        st.markdown("**Ирсий касалликлар:**")
        family_history = st.multiselect(
            "Оила аъзоларидаги касалликлар (бир нечтасини танланг)",
            [
                "Даун синдроми (трисомия 21)",
                "Эдвардс синдроми (трисомия 18)",
                "Патау синдроми (трисомия 13)",
                "Спина бифида",
                "Юрак аномалиялари",
                "Мускул дистрофияси",
                "Кистоз фиброз",
                "Гемофилия",
                "Фенилкетонурия",
                "Нейрофиброматоз",
                "Хромосома ўзгаришлари",
                "Метаболик касалликлар",
                "Йўқ"
            ],
            default=["Йўқ"]
        )
        
        consanguinity = st.radio("Қариндошлик никоҳи", 
                               ["Ҳа", "Йўқ"], 
                               index=1,
                               help="Ота-она қариндош бўлса")
        
        if consanguinity == "Ҳа":
            consanguinity_degree = st.selectbox("Қариндошлик даражаси",
                                              ["Бир аммаки/таға", 
                                               "Иккиламчи қариндош", 
                                               "Учинчи даража",
                                               "Турли даражада"],
                                              index=0)
    
    # 3. МЕДИЦИН ТАРИХ
    with st.expander("🏥 Медицин тарих", expanded=True):
        chronic_diseases = st.multiselect(
            "Мавжуд касалликлар",
            [
                "Сахар диабети (1-тип)",
                "Сахар диабети (2-тип)",
                "Гестацион диабет",
                "Артериал гипертония",
                "Гипертония хомилаликда",
                "Эпилепсия",
                "Аутоиммун касалликлар",
                "Буғум касалликлари",
                "Қалқонсимон без касалликлари",
                "Бронхиал астма",
                "Юрак-Қон томир касалликлари",
                "Бўйрак касалликлари",
                "Йўқ"
            ],
            default=["Йўқ"]
        )
        
        previous_pregnancies = st.selectbox("Хомилалик сони",
                                          ["1 (биринчи)", "2", "3", "4", "5", "6 ёки кўп"],
                                          index=0)
        
        previous_abnormalities = st.radio("Олдин аномалияли болалар туғилганми?",
                                        ["Ҳа", "Йўқ", "Аник эмас"],
                                        index=1)
        
        if previous_abnormalities == "Ҳа":
            abnormality_type = st.text_area("Аномалия тури ва тафсилотлари",
                                          placeholder="Каерда, қачон, қандай аномалия...")
        
        medications = st.text_area("Ҳозирги вақтда олинаётган дорулар",
                                 placeholder="Дору номи, доза, қанча вақтдан бери...",
                                 height=80)
        
        allergies = st.text_input("Аллергик реакциялар", 
                                placeholder="Доругга, овқатга аллергия...")
    
    # 4. УЛЧАШЛАР ВА ТЕСТ НАТИЖАЛАРИ
    with st.expander("📏 Улчашлар ва тестлар", expanded=True):
        col_h, col_w = st.columns(2)
        with col_h:
            height = st.number_input("Бўй (см)", 140, 200, 165, 
                                   help="Бўй баландлиги сантиметрда")
        with col_w:
            weight = st.number_input("Вазн (кг)", 40, 150, 65,
                                   help="Вазн килограммда")
        
        # BMI ҳисоблаш ва кўрсатиш
        if height > 0:
            bmi = calculate_bmi(weight, height)
            bmi_category = "Норма" if 18.5 <= bmi < 25 else "Огирлик" if bmi < 18.5 else "Ортиқча вазн"
            st.metric("📊 BMI (Тана вазни индексси)", f"{bmi:.1f}", delta=bmi_category)
        
        st.markdown("**🩸 Қон босими:**")
        bp_col1, bp_col2 = st.columns(2)
        with bp_col1:
            bp_systolic = st.number_input("Систолик (юкори)", 80, 200, 120)
        with bp_col2:
            bp_diastolic = st.number_input("Диастолик (паст)", 50, 120, 80)
        
        st.markdown("**🔬 Ультратовуш натижалари:**")
        nt_measurement = st.slider("Бўйин териси қалинлиги (NT) мм", 
                                 0.5, 10.0, 1.8, 0.1,
                                 help="Норма: 2.5 мм дан кам")
        nasal_bone = st.radio("Бурун суяги мавжудлиги",
                            ["Ҳа - норма", "Йўқ - аномалия", "Аник эмас"],
                            index=0)
        
        st.markdown("**🧪 Биохимик маркерлар:**")
        col_p, col_h = st.columns(2)
        with col_p:
            papp_a = st.number_input("PAPP-A (мЕд/мл)", 0.1, 20.0, 1.0, 0.1,
                                   help="Норма: 0.4-2.5 мЕд/мл")
        with col_h:
            free_beta_hcg = st.number_input("Эркин β-hCG (нг/мл)", 0.1, 50.0, 1.0, 0.1,
                                          help="Норма: 0.5-2.0 MoM")
    
    # 5. ҲАЁТ ТАРЗИ ВА СКРИНИНГ
    with st.expander("🌿 Ҳаёт тарзи ва скрининг", expanded=True):
        lifestyle_factors = st.multiselect(
            "Ҳаёт тарзи омиллари",
            [
                "Чекма (ҳа)",
                "Спиртли ичимликлар (ҳа)",
                "Наркотиклар (ҳа)",
                "Жисмоний фаоллик паст",
                "Туғри эмас овқатланиш",
                "Стрессли иш шароити",
                "Экология ноқулай",
                "Йўқ - барчаси норма"
            ],
            default=["Йўқ - барчаси норма"]
        )
        
        lifestyle_factor = 1.0
        if "Йўқ - барчаси норма" not in lifestyle_factors:
            lifestyle_factor = 1.3
        
        test_type = st.selectbox(
            "Ишлатилган скрининг тести",
            [
                "Life Cecly - Комплекс скрининг",
                "Astarea - Генетик таҳлил",
                "FMD - Фетал мониторинг дастури",
                "Prisca - Хавф бахолаш тизими",
                "Комбинация скрининг (бир нечтаси)",
                "Локал скрининг",
                "Тест ўтказилмаган"
            ],
            index=0
        )
        
        test_date = st.date_input("Тест санаси", date.today())
        
        if "Life Cecly" in test_type:
            risk_factor = st.slider("Life Cecly хавф коэффициенти", 0.1, 5.0, 1.0, 0.1)
        elif "Astarea" in test_type:
            risk_factor = st.slider("Astarea генетик коэффициенти", 0.1, 5.0, 1.0, 0.1)
        elif "FMD" in test_type:
            risk_factor = st.slider("FMD мониторинг коэффициенти", 0.1, 5.0, 1.0, 0.1)
        elif "Prisca" in test_type:
            risk_factor = st.slider("Prisca хавф коэффициенти", 0.1, 5.0, 1.0, 0.1)
        else:
            risk_factor = 1.0
    
    # ХАВФНИ ҲИСОБЛАШ ТУГМАСИ
    st.markdown("---")
    calculate_btn = st.button("🚀 ХАВФНИ ҲИСОБЛАШ", 
                            type="primary", 
                            use_container_width=True,
                            help="Барча маълумотларни киритиб бўлгандан сўнг босинг")

# ==================== АСОСИЙ КОНТЕНТ ====================

# ТАБЛАР
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎯 Хавф бахолаш", "📊 Таҳлиллар", "📋 Ҳисобот", "💾 Маълумотлар", "ℹ️ Ёрдам"])

with tab1:
    if calculate_btn:
        if not patient_name:
            st.warning("⚠️ Илтимос, беморнинг исмини киритинг!")
        else:
            # BMI ҳисоблаш
            bmi = calculate_bmi(weight, height)
            
            # Хавф параметрлари
            risk_params = {
                'age': patient_age,
                'bmi': bmi,
                'family_history': family_history,
                'nt': nt_measurement,
                'papp_a': papp_a,
                'hcg': free_beta_hcg,
                'consanguinity': consanguinity,
                'consanguinity_degree': consanguinity_degree if consanguinity == "Ҳа" else None,
                'previous_abnormalities': previous_abnormalities,
                'chronic_diseases': chronic_diseases,
                'lifestyle_factor': lifestyle_factor,
                'risk_factor': risk_factor
            }
            
            # Хавфни ҳисоблаш
            with st.spinner("Хавф бахолаш жараёнида..."):
                risk_score, risk_factors = calculate_genetic_risk_advanced(risk_params)
            
            # Хавф категорияси
            risk_category, risk_class, risk_color = get_risk_category_detailed(risk_score)
            
            # Сессияда сақлаш
            st.session_state.current_patient = {
                'id': st.session_state.patient_id,
                'name': patient_name,
                'age': patient_age,
                'gestational_age': gestational_age,
                'bmi': bmi,
                'risk_score': risk_score,
                'risk_category': risk_category,
                'risk_factors': risk_factors,
                'timestamp': datetime.now().isoformat()
            }
            
            st.session_state.patients_data.append(st.session_state.current_patient)
            st.session_state.risk_history.append({
                'patient': patient_name,
                'score': risk_score,
                'category': risk_category,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            
            # НАТИЖАЛАРНИ КӨРСАТИШ
            st.success(f"✅ {patient_name} учун хавф бахолаш тугади!")
            
            # АСОСИЙ МЕТРИКАЛАР
            st.markdown("### 📊 Асосий натижалар")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("👤 Бемор", patient_name)
            with col2:
                age_delta = f"+{patient_age-35}" if patient_age > 35 else None
                st.metric("🎂 Ёши", f"{patient_age} йош", delta=age_delta)
            with col3:
                st.metric("🤰 Хомилалик", f"{gestational_age} ҳафта")
            with col4:
                risk_display = f"1:{int(1/risk_score)}" if risk_score > 0 else "1:∞"
                st.metric("📈 Хавф нисбати", risk_display)
            
            # ХАВФ КАТЕГОРИЯСИ
            st.markdown("### 🎯 Хавф категорияси")
            st.markdown(f'<div class="{risk_class}">{risk_category}</div>', unsafe_allow_html=True)
            
            # ХАВФ ИНДИКАТОРИ
            st.markdown("### 📊 Хавф даражаси индикатори")
            progress_value = min(risk_score * 100, 100)
            st.progress(progress_value / 100)
            st.caption(f"Хавф даражаси: {risk_score:.6f} ({risk_display})")
            
            # ГРАФИКЛАР
            col_graph1, col_graph2 = st.columns(2)
            
            with col_graph1:
                # Хавф омиллари графиги
                st.markdown("#### 📈 Хавф омиллари таҳсири")
                factors_df = pd.DataFrame({
                    'Омил': list(risk_factors.keys()),
                    'Кўпайтирувчи': list(risk_factors.values())
                })
                
                fig_factors = px.bar(factors_df, x='Омил', y='Кўпайтирувчи',
                                    color='Кўпайтирувчи',
                                    color_continuous_scale='RdYlGn_r',
                                    title="Хавф омиллари таҳсири",
                                    labels={'Кўпайтирувчи': 'Кўпайтирувчи'})
                
                fig_factors.update_layout(height=400)
                st.plotly_chart(fig_factors, use_container_width=True)
            
            with col_graph2:
                # Гейдж график
                st.markdown("#### 🎚️ Хавф даражаси кўрсаткичи")
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=risk_score * 1000,
                    title={'text': "Хавф даражаси (1:1000 шкаласи)", 'font': {'size': 20}},
                    delta={'reference': 1, 'increasing': {'color': "red"}},
                    gauge={
                        'axis': {'range': [0, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': "darkblue"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [0, 1], 'color': 'green'},
                            {'range': [1, 3], 'color': 'lightgreen'},
                            {'range': [3, 5], 'color': 'yellow'},
                            {'range': [5, 7], 'color': 'orange'},
                            {'range': [7, 10], 'color': 'red'}
                        ],
                        'threshold': {
                            'line': {'color': "black", 'width': 4},
                            'thickness': 0.75,
                            'value': risk_score * 1000
                        }
                    }
                ))
                
                fig_gauge.update_layout(height=400)
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            # ТАВСИЯЛАР
            st.markdown("### 💡 Тавсия ва Таклифлар")
            recommendations = get_recommendations_by_risk(risk_category)
            
            with st.expander("#### 🏥 Тиббий тавсиялар", expanded=True):
                st.markdown(f"**Даркорлик даражаси:** {recommendations['urgency']}")
                st.markdown(f"**Назорат жиҳати:** {recommendations['monitoring']}")
                
                st.markdown("**Зурур тадбирлар:**")
                for i, action in enumerate(recommendations['actions'], 1):
                    st.markdown(f"{i}. {action}")
                
                st.markdown("**Маслаҳат берадиган мутахассислар:**")
                st.markdown(", ".join(recommendations['specialists']))
            
            # ҚОШИМЧА ТАВСИЯЛАР
            with st.expander("#### 🌿 Қўшимча тавсиялар"):
                st.markdown("""
                **Парвардалик бўйича:**
                1. Мутахассис кўрсатмасида парвардалик
                2. Мунтазам тиббий кўриқув
                3. Даво-профилактика витаминлари
                4. Соглом овқатланиш режими
                5. Ўртача жисмоний фаоллик
                
                **Эхтиёт чоралари:**
                1. Стрессдан сақланиш
                2. Ўз-ўзини даволашдан қочиш
                3. Шифокор кўрсатмасига қатъий риоя
                4. Ҳар қандай норинҷийликда дастурки шифокорга мурожаат
                """)
            
            # ДЕТАЛЛИ ТАҲЛИЛ
            with st.expander("#### 🔍 Деталли таҳлил", expanded=False):
                st.markdown("**📋 Хавф ҳисоблаш параметрлари:**")
                
                col_details1, col_details2 = st.columns(2)
                
                with col_details1:
                    st.markdown("**Асосий омиллар:**")
                    st.markdown(f"- Ёш омили: {risk_factors['age']:.2f}x")
                    st.markdown(f"- BMI омили: {risk_factors['bmi']:.2f}x")
                    st.markdown(f"- Оилавий тарих: {risk_factors['family']:.2f}x")
                    st.markdown(f"- NT қалинлиги: {risk_factors['nt']:.2f}x")
                    st.markdown(f"- Биохимик маркерлар: {risk_factors['biochemical']:.2f}x")
                
                with col_details2:
                    st.markdown("**Қўшимча омиллар:**")
                    st.markdown(f"- Қариндошлик никоҳи: {risk_factors['consanguinity']:.2f}x")
                    st.markdown(f"- Олдинги аномалиялар: {risk_factors['previous']:.2f}x")
                    st.markdown(f"- Сурункарон касалликлар: {risk_factors['chronic']:.2f}x")
                    st.markdown(f"- Ҳаёт тарзи: {risk_factors['lifestyle']:.2f}x")
                    st.markdown(f"- Скрининг тести: {risk_factors['test']:.2f}x")
                
                st.markdown(f"**Умумий кўпайтирувчи:** {np.prod(list(risk_factors.values())):.2f}x")
                st.markdown(f"**Асосий хавф:** 1:1250")
                st.markdown(f"**Хисобланган хавф:** 1:{int(1/risk_score)} ({risk_score:.8f})")
    
    else:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Хавф бахолаш бўлимига хуш келибсиз!")
        st.markdown("""
        **Дастурни ишлатиш учун:**
        1. Чеп томондаги панелда барча маълумотларни тўлдиринг
        2. **«ХАВФНИ ҲИСОБЛАШ»** тугмасини босинг
        3. Натижаларни кўринг ва тавсияларга амал қилинг
        
        **Диққат:** Барча маълумотлар конфиденциальдир ва фақат тиббий мақсадлар учун ишлатилади.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("## 📊 Статистика ва таҳлиллар")
    
    if st.session_state.patients_data:
        # Маълумотларни DataFrame га айлантириш
        df = pd.DataFrame(st.session_state.patients_data)
        
        # Умумий статистика
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            st.metric("👥 Жами беморлар", len(df))
        with col_stat2:
            avg_age = df['age'].mean() if not df.empty else 0
            st.metric("📊 Ўртача ёш", f"{avg_age:.1f} йош")
        with col_stat3:
            high_risk = len([p for p in st.session_state.patients_data 
                           if p.get('risk_category') in ['КРИТИК', 'ЖУДА ЮҚОРИ', 'ЮҚОРИ']])
            st.metric("⚠️ Юқори хавфли", high_risk)
        with col_stat4:
            low_risk = len([p for p in st.session_state.patients_data 
                          if p.get('risk_category') in ['ПАСТ', 'ПАСТ-ЎРТАЧА']])
            st.metric("✅ Паст хавфли", low_risk)
        
        # Хавф категориялари бўйича тақсимот
        st.markdown("### 🎯 Хавф категориялари тақсимоти")
        
        if not df.empty:
            category_counts = df['risk_category'].value_counts()
            
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                # Пай чарт
                fig_pie = px.pie(values=category_counts.values, 
                               names=category_counts.index,
                               title="Хавф категориялари (%)",
                               color_discrete_sequence=px.colors.sequential.RdBu)
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col_chart2:
                # Бар чарт
                fig_bar = px.bar(x=category_counts.index, y=category_counts.values,
                               title="Хавф категориялари (сони)",
                               labels={'x': 'Категория', 'y': 'Сони'},
                               color=category_counts.values,
                               color_continuous_scale='Viridis')
                st.plotly_chart(fig_bar, use_container_width=True)
        
        # Ёш бўйича хавф таҳлили
        st.markdown("### 📈 Ёшга қараб хавф ўзгариши")
        
        if not df.empty:
            fig_age = px.scatter(df, x='age', y='risk_score',
                               color='risk_category',
                               size='risk_score',
                               hover_data=['name'],
                               title="Ёш ва хавф даражаси богликлиги",
                               labels={'age': 'Ёш', 'risk_score': 'Хавф даражаси'})
            
            # 35 йош чизиғи
            fig_age.add_vline(x=35, line_dash="dash", line_color="red",
                            annotation_text="35 йош", 
                            annotation_position="top right")
            
            st.plotly_chart(fig_age, use_container_width=True)
        
        # Вакт бўйича хавф ўзгариши
        st.markdown("### ⏳ Вакт бўйича хавфлар тарихи")
        
        if st.session_state.risk_history:
            history_df = pd.DataFrame(st.session_state.risk_history)
            history_df['date'] = pd.to_datetime(history_df['date'])
            
            fig_history = px.line(history_df, x='date', y='score',
                                color='patient',
                                markers=True,
                                title="Беморлар бўйича хавф даражаси ўзгариши",
                                labels={'date': 'Сана', 'score': 'Хавф даражаси', 'patient': 'Бемор'})
            
            st.plotly_chart(fig_history, use_container_width=True)
        
        # Омиллар таҳлили
        st.markdown("### 🔬 Хавф омиллари таҳлили")
        
        if not df.empty and len(df) > 1:
            # Сонли маълумотларни олиш
            numeric_factors = ['age', 'bmi'] if 'bmi' in df.columns else ['age']
            
            for factor in numeric_factors:
                if factor in df.columns:
                    fig_factor = px.box(df, y=factor, 
                                      title=f"{factor.upper()} бўйича тақсимот")
                    st.plotly_chart(fig_factor, use_container_width=True)
    
    else:
        st.info("📊 Статистикани кўриш учун аввал камида битта бемор учун хавфни ҳисобланг.")

with tab3:
    st.markdown("## 📋 Ҳисобот генератор")
    
    if 'current_patient' in st.session_state and st.session_state.current_patient:
        patient = st.session_state.current_patient
        
        # Ҳисобот параметрлари
        st.markdown("### 🖋️ Ҳисобот параметрлари")
        
        col_report1, col_report2 = st.columns(2)
        
        with col_report1:
            report_language = st.selectbox("Ҳисобот тили", 
                                         ["Ўзбекча", "Русча", "Инглизча", "Ҳамма тилда"],
                                         index=0)
            
            hospital_name = st.text_input("Шифохона номи", 
                                        "Марказий Тиббийот Маркази")
            
            doctor_name = st.text_input("Шифокор исми", 
                                      "Др. Алиев Абдураҳмон")
            
            doctor_position = st.selectbox("Шифокор лавозими",
                                         ["Акушер-гинеколог", 
                                          "Генетик", 
                                          "Перинатолог",
                                          "Тиббий генетик",
                                          "Даволаш шифокори"])
        
        with col_report2:
            include_details = st.checkbox("Батафсил маълумотларни қўшиш", value=True)
            include_charts = st.checkbox("Диаграммаларни қўшиш", value=True)
            include_recommendations = st.checkbox("Тавсияларни қўшиш", value=True)
            add_signature = st.checkbox("Имзо майдони қўшиш", value=True)
        
        # Ҳисобот яратиш
        if st.button("🖨️ Ҳисоботни Яратиш ва Юклаб Олиш", use_container_width=True):
            with st.spinner("Ҳисобот яратилмоқда..."):
                # Тавсияларни олиш
                recommendations = get_recommendations_by_risk(patient['risk_category'])
                
                # Ҳисобот контентарини яратиш
                report_content = f"""
ТИББИЙ ГЕНЕТИК ХАВФ БАХОЛАШ ҲИСОБОТИ
========================================

ШИФОХОНА МАЪЛУМОТЛАРИ:
----------------------
Шифохона: {hospital_name}
Шифокор: {doctor_name}
Лавозими: {doctor_position}
Ҳисобот ID: {patient['id']}
Саналди: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

БЕМОР МАЪЛУМОТЛАРИ:
------------------
ФИО: {patient['name']}
Ёши: {patient['age']} йош
Хомилалик даври: {patient.get('gestational_age', 'N/A')} ҳафта
Бемор ID: {patient['id']}
Рўйҳатга олиш санаси: {datetime.now().strftime('%Y-%m-%d')}

ХАВФ БАХОЛАШ НАТИЖАЛАРИ:
-----------------------
Хавф даражаси: 1:{int(1/patient['risk_score'])}
Хавф категорияси: {patient['risk_category']}
Хавф қиймати: {patient['risk_score']:.8f}

ТАВСИЯ ВА ТАКЛИФЛАР:
-------------------
Даркорлик даражаси: {recommendations['urgency']}
Назорат жиҳати: {recommendations['monitoring']}

Зурур тадбирлар:
{chr(10).join([f"{i+1}. {action}" for i, action in enumerate(recommendations['actions'])])}

Маслаҳат берадиган мутахассислар: {', '.join(recommendations['specialists'])}

ШАХСИЙ ЭСЛАТМАЛАР:
-----------------
{doctor_name} томонидан берилган изоҳлар ва қўшимча тавсиялар...

ҲУЖЖАТ МАЪНОСИ:
--------------
Бу ҳисобот фақат тиббий мақсадлар учун ишлаб чиқилган.
Ҳар қандай тадбир қабул қилишдан олдин тиббий мутахассисга мурожаат қилинг.

ИМЗО ВА МУҲР:
------------
Шифокор: ____________________
Сана: ____________________
МҲҲ: ____________________
"""
                
                # Ҳисоботни кўрсатиш
                st.markdown("### 📄 Яратилган ҳисобот:")
                st.text_area("Ҳисобот мазмуни", report_content, height=400)
                
                # Юклаб олиш имконияти
                st.markdown("### 📥 Ҳисоботни юклаб олиш")
                
                col_download1, col_download2, col_download3 = st.columns(3)
                
                with col_download1:
                    # TXT форматида
                    b64_txt = base64.b64encode(report_content.encode()).decode()
                    href_txt = f'<a href="data:file/txt;base64,{b64_txt}" download="hisobot_{patient["id"]}.txt">📄 .TXT форматида</a>'
                    st.markdown(href_txt, unsafe_allow_html=True)
                
                with col_download2:
                    # JSON форматида
                    report_json = json.dumps(patient, ensure_ascii=False, indent=2)
                    b64_json = base64.b64encode(report_json.encode()).decode()
                    href_json = f'<a href="data:file/json;base64,{b64_json}" download="hisobot_{patient["id"]}.json">📊 .JSON форматида</a>'
                    st.markdown(href_json, unsafe_allow_html=True)
                
                with col_download3:
                    # CSV форматида (қисқа)
                    report_csv = f"Бемор,Хавф даражаси,Категория\n{patient['name']},{patient['risk_score']:.6f},{patient['risk_category']}"
                    b64_csv = base64.b64encode(report_csv.encode()).decode()
                    href_csv = f'<a href="data:file/csv;base64,{b64_csv}" download="hisobot_{patient["id"]}.csv">📈 .CSV форматида</a>'
                    st.markdown(href_csv, unsafe_allow_html=True)
                
                st.success("✅ Ҳисобот муваффақиятли яратилди!")
    
    else:
        st.info("📋 Ҳисобот яратиш учун аввал бемор маълумотларини киритиб, хавфни ҳисобланг.")

with tab4:
    st.markdown("## 💾 Маълумотлар бошқаруви")
    
    # Маълумотлар импорт/экспорт
    col_data1, col_data2 = st.columns(2)
    
    with col_data1:
        st.markdown("### 📤 Маълумотларни экспорт қилиш")
        
        if st.button("📊 JSON форматида экспорт", use_container_width=True):
            if st.session_state.patients_data:
                data_str = json.dumps(st.session_state.patients_data, ensure_ascii=False, indent=2)
                b64 = base64.b64encode(data_str.encode()).decode()
                href = f'<a href="data:file/json;base64,{b64}" download="genetic_risk_data.json">💾 JSON файлини юклаб олиш</a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                st.warning("Экспорт қилиш учун маълумотлар мавжуд эмас")
    
    with col_data2:
        st.markdown("### 📥 Маълумотларни импорт қилиш")
        
        uploaded_file = st.file_uploader("JSON файл юклаш", type=['json'])
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                if isinstance(data, list):
                    st.session_state.patients_data = data
                    st.success(f"✅ {len(data)} та бемор маълумотлари юкланди!")
                else:
                    st.error("❌ Файл тузилиши нотўғри!")
            except Exception as e:
                st.error(f"❌ Файлни ўқишда хатолик: {e}")
    
    # Маълумотлар жадвали
    st.markdown("### 📋 Беморлар рўйхати")
    
    if st.session_state.patients_data:
        # DataFrame га айлантириш
        df_display = pd.DataFrame(st.session_state.patients_data)
        
        # Керакли устунларни танлаш
        display_cols = ['name', 'age', 'gestational_age', 'risk_score', 'risk_category']
        display_cols = [col for col in display_cols if col in df_display.columns]
        
        if display_cols:
            df_display = df_display[display_cols]
            
            # Хавф даражасини форматлаш
            if 'risk_score' in df_display.columns:
                def format_risk_score(score):
                    if score > 0:
                        return f"1:{int(1/score)}"
                    return "1:∞"
                
                df_display['risk_score'] = df_display['risk_score'].apply(format_risk_score)
            
            # Жадвални кўрсатиш
            st.dataframe(df_display, 
                        use_container_width=True,
                        column_config={
                            "name": st.column_config.TextColumn("Бемор исми", width="medium"),
                            "age": st.column_config.NumberColumn("Ёши", format="%d йош"),
                            "gestational_age": st.column_config.NumberColumn("Хомилалик", format="%d ҳафта"),
                            "risk_score": st.column_config.TextColumn("Хавф даражаси"),
                            "risk_category": st.column_config.TextColumn("Хавф категорияси")
                        })
            
            # Жадвални юклаб олиш
            csv = df_display.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Жадвални CSV форматида юклаб олиш",
                data=csv,
                file_name="bemorlar_royxati.csv",
                mime="text/csv"
            )
        else:
            st.info("Кўрсатиш учун маълумотлар мавжуд эмас")
    else:
        st.info("📭 Ҳали бемор маълумотлари киритилмаган")

with tab5:
    st.markdown("## ℹ️ Дастур Қўлланмаси ва Ёрдам")
    
    col_help1, col_help2 = st.columns(2)
    
    with col_help1:
        st.markdown("""
        ### 🎯 Дастур мақсади
        
        **Тиббий генетик хавф бахолаш дастури** хомиладор аёлларда 
        ирсий касалликлар хавфини комплекс бахолаш ва таҳлил қилиш учун 
        ишлаб чиқилган.
        
        ### 📋 Асосий имкониятлар
        
        1. **Бемор маълумотларини киритиш** - тўлиқ тиббий анкета
        2. **Хавфни ҳисоблаш** - кўп омилли алгоритм
        3. **График ва таҳлиллар** - визуал таҳлил
        4. **Ҳисобот генерацияси** - тиббий ҳужжатлар
        5. **Маълумотлар бошқаруви** - импорт/экспорт
        
        ### 🔬 Ишлатиладиган параметрлар
        
        - **Демографик**: ёш, BMI, қон гуруҳи
        - **Оилавий**: ирсий касалликлар, қариндошлик
        - **Медицин**: касалликлар, олдинги хомилаликлар
        - **Биохимик**: PAPP-A, β-hCG, NT
        - **Ҳаёт тарзи**: чекма, овқатланиш, стресс
        """)
    
    with col_help2:
        st.markdown("""
        ### ⚠️ Диққат этиш керак
        
        1. **Дастур тиббий қарор қабул қилиш воситаси эмас**
        2. **Барча натижалар шифокор таҳлили талаб қилади**
        3. **Маълумотлар аник ва яқин вактда олинган бўлиши керак**
        4. **Шубхали ҳолатда генетик мутахассисга мурожаат**
        
        ### 🏥 Хавф категориялари
        
        - **ПАСТ**: 1:1000 дан кам - стандарт парвардалик
        - **ЎРТАЧА**: 1:1000-1:200 - қўшимча кўриқув
        - **ЮҚОРИ**: 1:100-1:20 - деталли текширув
        - **КРИТИК**: 1:20 дан юкори - шошилинч тадбир
        
        ### 📞 Контакт маълумотлари
        
        **Техник ёрдам:**
        - Email: support@genetic-risk.uz
        - Телефон: +998 71 123 45 67
        
        **Тиббий масалаҳат:**
        - Марказий генетик марказ
        - Респубдика перинатология маркази
        """)
    
    # ТИЗИМ ТАЛАБЛАРИ
    st.markdown("---")
    st.markdown("### 💻 Тизим талаблари")
    
    col_sys1, col_sys2, col_sys3 = st.columns(3)
    
    with col_sys1:
        st.markdown("""
        **Операцион тизимлар:**
        - Windows 10/11
        - macOS 10.15+
        - Linux Ubuntu 18.04+
        """)
    
    with col_sys2:
        st.markdown("""
        **Браузерлар:**
        - Chrome 80+
        - Firefox 75+
        - Safari 13+
        - Edge 80+
        """)
    
    with col_sys3:
        st.markdown("""
        **Минимал талаблар:**
        - CPU: 2 ядро
        - RAM: 4 GB
        - Storage: 500 MB
        - Internet: 5 Mbps
        """)
    
    # ВЕРСИЯ МАЪЛУМОТЛАРИ
    st.markdown("---")
    st.markdown("""
    **Дастур версияси:** 3.0.1 (Тўлиқ локал версия)
    **Сўнги янгилаш:** 2024 йил
    **Ишлаб чиқувчи:** Тиббий информатика ва аналитика маркази
    **Лицензия:** Фойдаланувчи лицензияси (учебно-тиббий)
    """)

# ==================== ФУТЕР ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 25px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 15px;'>
    <p style='font-size: 1.2rem; font-weight: bold; margin-bottom: 10px;'>
        © 2024 ТИББИЙ ГЕНЕТИК ХАВФ БАХОЛАШ ДАСТУРИ
    </p>
    <p style='font-size: 1rem; margin-bottom: 5px;'>
        Life Cecly • Astarea • FMD • Prisca скрининг тизимлари асосида ишлайди
    </p>
    <p style='font-size: 0.9rem; margin-top: 10px; color: #e74c3c;'>
        <strong>⚕️ ТИББИЙ ОГОҲЛАНТИРИШ:</strong> 
        Бу дастур фақат ёрдамчи восита сифатида ишлатилади. 
        Ҳар қандай тиббий қарор қабул қилишдан олдин мутахассис шифокорга мурожаат қилинг. 
        Барча маълумотлар конфиденциальдир ва тиббий мақсадлар учун сақланади.
    </p>
    <p style='font-size: 0.8rem; margin-top: 15px; color: #95a5a6;'>
        Версия: 3.0.1 | Локал ишлаш учун мослаштирилган | Барча ҳуқуқлар ҳимояланган
    </p>
</div>
""", unsafe_allow_html=True)

# ==================== ЛОКАЛ САҚЛАШ ТЕКШИРИШИ ====================
# Автомат сақлаш (ихтиёрий)
if st.session_state.patients_data and len(st.session_state.patients_data) % 5 == 0:
    try:
        with open("autosave_patients.json", "w", encoding='utf-8') as f:
            json.dump(st.session_state.patients_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        pass
