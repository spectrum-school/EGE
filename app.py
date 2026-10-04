import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import io
import numpy as np
from datetime import datetime
import random

st.set_page_config(page_title="Прогресс ЕГЭ", layout="wide")

# CSS
st.markdown("""
<style>
    /* ==================== ЦВЕТОВАЯ ПАЛИТРА ====================
       Primary:   #4F46E5 (индиго) — основной акцент
       Secondary: #7C3AED (фиолетовый)
       
       Уровни:
       - Отлично:  #059669 (зелёный)
       - Хорошо:   #10B981 (светло-зелёный)
       - Средне:   #D97706 (оранжевый)
       - Низкий:   #DC2626 (красный)
    ========================================================= */
    
    /* ==================== БАЗА ==================== */
    .stApp, .stApp > div, .main, .block-container {
        background-color: #F9FAFB !important;
        color: #1F2937 !important;
    }
    
    /* ==================== КАРТОЧКИ ==================== */
    .card {
        background: #FFFFFF !important;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
        margin-bottom: 16px;
        border: 2px solid #E5E7EB !important;
        transition: box-shadow 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
    }
    
    .card:hover {
        box-shadow: 0 4px 16px rgba(79, 70, 229, 0.10) !important;
        transform: translateY(-2px);
    }
    
    /* Цветные варианты карточек */
    .card-excellent {
        border-color: #A7F3D0 !important;
        background: linear-gradient(180deg, #FFFFFF 0%, #F0FDF4 100%) !important;
    }
    .card-excellent:hover {
        border-color: #059669 !important;
        box-shadow: 0 6px 20px rgba(5, 150, 105, 0.15) !important;
    }
    
    .card-good {
        border-color: #BBF7D0 !important;
        background: linear-gradient(180deg, #FFFFFF 0%, #F0FDF4 100%) !important;
    }
    .card-good:hover {
        border-color: #10B981 !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.15) !important;
    }
    
    .card-medium {
        border-color: #FED7AA !important;
        background: linear-gradient(180deg, #FFFFFF 0%, #FFFBEB 100%) !important;
    }
    .card-medium:hover {
        border-color: #D97706 !important;
        box-shadow: 0 6px 20px rgba(217, 119, 6, 0.15) !important;
    }
    
    .card-low {
        border-color: #FECACA !important;
        background: linear-gradient(180deg, #FFFFFF 0%, #FEF2F2 100%) !important;
    }
    .card-low:hover {
        border-color: #DC2626 !important;
        box-shadow: 0 6px 20px rgba(220, 38, 38, 0.15) !important;
    }
    
    .card-primary {
        border-color: #C7D2FE !important;
        background: linear-gradient(180deg, #FFFFFF 0%, #EEF2FF 100%) !important;
    }
    .card-primary:hover {
        border-color: #4F46E5 !important;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.15) !important;
    }
    
    .card-title {
        font-size: 13px;
        font-weight: 600;
        color: #6B7280 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 14px;
    }
    
    .card-value {
        font-size: 38px;
        font-weight: 700;
        color: #1F2937 !important;
        line-height: 1.1;
    }
    
    .card-sub {
        font-size: 14px;
        color: #6B7280 !important;
        margin-top: 6px;
    }
    
    .card-stats {
        display: flex;
        justify-content: space-around;
        padding: 12px 0 0 0;
        border-top: 1px solid #F3F4F6;
        margin-top: 14px;
    }
    
    .card-stats-item { text-align: center; }
    .card-stats-item .stat-value { font-size: 20px; font-weight: 700; color: #4F46E5; }
    .card-stats-item .stat-label { font-size: 12px; color: #9CA3AF; margin-top: 2px; }
    
    /* ==================== УРОВЕНЬ (БЕЙДЖ) ==================== */
    .level-container {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 12px 26px;
        border-radius: 12px;
        font-size: 20px !important;
        font-weight: 600 !important;
        margin: 5px 0;
        min-width: 220px;
        justify-content: center;
        border: 2px solid transparent;
    }
    
    .level-excellent {
        background: #ECFDF5 !important;
        color: #047857 !important;
        border-color: #059669 !important;
        box-shadow: 0 0 0 4px rgba(5, 150, 105, 0.08);
    }
    
    .level-good {
        background: #F0FDF4 !important;
        color: #047857 !important;
        border-color: #10B981 !important;
        box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.08);
    }
    
    .level-medium {
        background: #FFFBEB !important;
        color: #B45309 !important;
        border-color: #D97706 !important;
        box-shadow: 0 0 0 4px rgba(217, 119, 6, 0.08);
    }
    
    .level-low {
        background: #FEF2F2 !important;
        color: #B91C1C !important;
        border-color: #DC2626 !important;
        box-shadow: 0 0 0 4px rgba(220, 38, 38, 0.08);
    }
    
    .level-text {
        font-size: 20px !important;
        font-weight: 700 !important;
        letter-spacing: 0.01em;
    }
    
    /* ==================== ДОМАШНЕЕ ЗАДАНИЕ ==================== */
    .hw-container {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 18px 22px;
        border: 2px solid #E5E7EB;
        border-left: 6px solid #4F46E5;
        margin-top: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 14px;
    }
    
    .hw-done {
        border-color: #A7F3D0 !important;
        border-left-color: #059669 !important;
        background: #F0FDF4 !important;
    }
    
    .hw-not-done {
        border-color: #FECACA !important;
        border-left-color: #DC2626 !important;
        background: #FEF2F2 !important;
    }
    
    .hw-link {
        color: #4F46E5 !important;
        text-decoration: none !important;
        font-weight: 600;
        font-size: 15px;
        padding: 8px 16px;
        background: #EEF2FF;
        border-radius: 8px;
        border: 2px solid #C7D2FE;
        transition: all 0.2s;
    }
    
    .hw-link:hover {
        background: #E0E7FF !important;
        border-color: #A5B4FC;
    }
    
    .hw-status {
        font-weight: 700;
        font-size: 14px;
        padding: 6px 16px;
        border-radius: 20px;
        display: inline-block;
        letter-spacing: 0.02em;
        border: 2px solid transparent;
    }
    
    .hw-status-done {
        color: #047857;
        background: #D1FAE5;
        border-color: #059669;
    }
    
    .hw-status-not-done {
        color: #B91C1C;
        background: #FEE2E2;
        border-color: #DC2626;
    }
    
    .hw-label {
        font-weight: 600;
        font-size: 15px;
        color: #1F2937;
    }
    
    /* ==================== СТАТУС-БАРЫ ==================== */
    .status-bar {
        height: 10px;
        border-radius: 5px;
        background: #F3F4F6;
        margin: 10px 0;
        overflow: hidden;
        border: 1px solid #E5E7EB;
    }
    
    .status-bar-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.6s ease;
    }
    
    /* ==================== ТЕКСТ ==================== */
    h1, h2, h3, h4, h5, h6 { color: #1F2937 !important; }
    h1 { font-size: 32px !important; font-weight: 700 !important; letter-spacing: -0.02em; }
    h3 { font-size: 22px !important; font-weight: 600 !important; letter-spacing: -0.01em; }
    p, div, span, label { color: #1F2937 !important; }
    
    /* ==================== ТАБЛИЦЫ ==================== */
    .stDataFrame { border-radius: 12px; overflow: hidden; border: 2px solid #E5E7EB; }
    .stDataFrame table { color: #1F2937 !important; }
    .stDataFrame thead tr th {
        background-color: #F9FAFB !important;
        color: #4F46E5 !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 0.05em;
        border-bottom: 2px solid #E5E7EB !important;
    }
    .stDataFrame tbody tr td { background-color: #FFFFFF !important; color: #1F2937 !important; }
    .stDataFrame tbody tr:hover td { background-color: #F9FAFB !important; }
    
    /* ==================== САЙДБАР ==================== */
    .stSidebar {
        background-color: #FFFFFF !important;
        border-right: 2px solid #E5E7EB !important;
    }
    
    .stSidebar h1, .stSidebar h2, .stSidebar h3,
    .stSidebar p, .stSidebar div { color: #1F2937 !important; }
    
    /* ==================== SELECTBOX ==================== */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 2px solid #E5E7EB !important;
        border-radius: 10px !important;
    }
    .stSelectbox div[data-baseweb="select"] input { color: #1F2937 !important; }
    .stSelectbox div[data-baseweb="select"]:focus-within {
        border-color: #4F46E5 !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12) !important;
    }
    
    /* ==================== КНОПКИ ==================== */
    .stButton button {
        background-color: #FFFFFF !important;
        border: 2px solid #E5E7EB !important;
        color: #1F2937 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
        padding: 10px 16px !important;
    }
    
    .stButton button:hover {
        background-color: #EEF2FF !important;
        border-color: #4F46E5 !important;
        color: #4F46E5 !important;
        transform: translateY(-1px);
    }
    
    .stButton button:active {
        transform: translateY(0);
    }
    
    /* ==================== ВКЛАДКИ ==================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #F9FAFB !important;
        border-radius: 12px;
        padding: 4px;
        border: 2px solid #E5E7EB;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #6B7280 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        border: none !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #4F46E5 !important;
        box-shadow: 0 1px 3px rgba(79, 70, 229, 0.15) !important;
        font-weight: 700 !important;
    }
    
    /* ==================== ALERT ==================== */
    .stAlert {
        background-color: #FFFFFF !important;
        border: 2px solid #E5E7EB !important;
        border-left: 6px solid #4F46E5 !important;
        border-radius: 10px !important;
        color: #1F2937 !important;
    }
    
    /* ==================== RADIO (в сайдбаре) ==================== */
    .stRadio > div { gap: 8px; }
    .stRadio label {
        background: #FFFFFF;
        border: 2px solid #E5E7EB;
        border-radius: 10px;
        padding: 10px 14px;
        transition: all 0.2s;
        font-weight: 600;
    }
    
    .stRadio label:hover {
        border-color: #4F46E5;
        background: #EEF2FF;
    }
    
    /* ==================== ИНФО-БЛОКИ ==================== */
    .info-block {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 18px 20px;
        border: 2px solid #E5E7EB;
        border-left: 6px solid #4F46E5;
        margin-bottom: 12px;
    }
    
    .info-block-green {
        border-color: #A7F3D0 !important;
        border-left-color: #059669 !important;
        background: #F0FDF4 !important;
    }
    
    .info-block-orange {
        border-color: #FED7AA !important;
        border-left-color: #D97706 !important;
        background: #FFFBEB !important;
    }
    
    .info-block-red {
        border-color: #FECACA !important;
        border-left-color: #DC2626 !important;
        background: #FEF2F2 !important;
    }
    
    .info-block-blue {
        border-color: #C7D2FE !important;
        border-left-color: #4F46E5 !important;
        background: #EEF2FF !important;
    }
    
    /* ==================== АДАПТИВНОСТЬ ==================== */
    @media only screen and (max-width: 768px) {
        .card { padding: 16px; margin-bottom: 12px; }
        .card-value { font-size: 28px; }
        .card-title { font-size: 12px; }
        .level-container { font-size: 16px !important; padding: 8px 16px; min-width: 160px; }
        .level-text { font-size: 16px !important; }
        .hw-container { flex-direction: column; align-items: stretch !important; text-align: center; padding: 14px; }
        .stTabs [data-baseweb="tab"] { font-size: 13px; padding: 8px 12px; }
        h1 { font-size: 24px !important; }
        h3 { font-size: 18px !important; }
    }
    
    @media only screen and (max-width: 480px) {
        .card { padding: 14px; }
        .card-value { font-size: 24px; }
        .card-title { font-size: 11px; }
        .level-container { font-size: 14px !important; padding: 6px 12px; min-width: 140px; }
        .level-text { font-size: 14px !important; }
    }
</style>
""", unsafe_allow_html=True)

SHEET_ID = "1GkNVYBZqLkZPEEnRbB2CZKzsFb5ZrkKfjs4pMObD-YY"

@st.cache_data(ttl=60)
def load_sheet(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.content.decode('utf-8-sig')
        df = pd.read_csv(io.StringIO(content))
        return df
    except Exception as e:
        st.sidebar.error(f"Ошибка загрузки: {str(e)[:100]}")
        return pd.DataFrame()

def get_task_status(value):
    if pd.isna(value) or value == '' or value == '-' or value == '—' or value == '–':
        return 'not_studied'
    try:
        val = float(value)
        if val == 0: return 'wrong'
        elif val == 1: return 'correct'
        elif val == 2: return 'correct'
        else: return 'invalid'
    except:
        return 'invalid'

def convert_to_secondary(primary_score):
    conversion_table = {
        0: 0, 1: 7, 2: 14, 3: 20, 4: 27, 5: 34,
        6: 40, 7: 43, 8: 46, 9: 48, 10: 51,
        11: 54, 12: 56, 13: 59, 14: 62, 15: 64,
        16: 67, 17: 70, 18: 72, 19: 75, 20: 78,
        21: 80, 22: 83, 23: 85, 24: 88, 25: 90,
        26: 93, 27: 95, 28: 98, 29: 100
    }
    primary_rounded = max(0, min(round(primary_score), 29))
    return conversion_table.get(primary_rounded, primary_rounded)

def get_score_level(score):
    if score >= 80: return "Отлично", "level-excellent", "card-excellent"
    elif score >= 60: return "Хорошо", "level-good", "card-good"
    elif score >= 40: return "Средне", "level-medium", "card-medium"
    else: return "Требует внимания", "level-low", "card-low"

def calculate_forecast(scores_history):
    if not scores_history or len(scores_history) == 0:
        return 0
    n = len(scores_history)
    if n == 1:
        return scores_history[0]
    alpha = 0.7
    weights = [alpha ** (n - 1 - i) for i in range(n)]
    total_weight = sum(weights)
    if total_weight > 0:
        weights = [w / total_weight for w in weights]
    return sum(weights[i] * s for i, s in enumerate(scores_history))

def calculate_student_forecast(student_tasks, task_cols, max_attempts=5):
    if student_tasks.empty:
        return {'forecast_primary': 0, 'forecast_secondary': 0,
                'current_primary': 0, 'current_secondary': 0,
                'best_primary': 0, 'best_secondary': 0,
                'scores_history': [], 'task_stats': {}}
    
    recent_tasks = student_tasks.tail(max_attempts).copy()
    
    scores_history = []
    task_stats = {}
    
    for col in task_cols:
        num = col.replace('task_', '').replace('задание', '').replace('_', '')
        task_stats[num] = {'correct': 0, 'wrong': 0, 'total': 0, 'not_studied': 0}
    
    for _, row in recent_tasks.iterrows():
        primary = 0
        for col in task_cols:
            num = col.replace('task_', '').replace('задание', '').replace('_', '')
            task_num_int = int(num) if num.isdigit() else 0
            weight = 2 if task_num_int in [26, 27] else 1
            value = row[col]
            if not pd.isna(value) and value != '' and value != '-' and value != '—' and value != '–':
                try:
                    val = float(value)
                    primary += val * weight
                    if val > 0:
                        task_stats[num]['correct'] += 1
                    else:
                        task_stats[num]['wrong'] += 1
                    task_stats[num]['total'] += 1
                except:
                    pass
            else:
                task_stats[num]['not_studied'] += 1
        scores_history.append(primary)
    
    forecast_primary = calculate_forecast(scores_history)
    
    all_scores = []
    for _, row in student_tasks.iterrows():
        primary = 0
        for col in task_cols:
            num = col.replace('task_', '').replace('задание', '').replace('_', '')
            task_num_int = int(num) if num.isdigit() else 0
            weight = 2 if task_num_int in [26, 27] else 1
            value = row[col]
            if not pd.isna(value) and value != '' and value != '-' and value != '—' and value != '–':
                try:
                    primary += float(value) * weight
                except:
                    pass
        all_scores.append(primary)
    
    current_primary = all_scores[-1] if all_scores else 0
    best_primary = max(all_scores) if all_scores else 0
    
    return {
        'forecast_primary': forecast_primary,
        'forecast_secondary': convert_to_secondary(round(forecast_primary)),
        'current_primary': current_primary,
        'current_secondary': convert_to_secondary(round(current_primary)),
        'best_primary': best_primary,
        'best_secondary': convert_to_secondary(round(best_primary)),
        'scores_history': all_scores,
        'recent_scores': scores_history,
        'task_stats': task_stats
    }

# ==================== ЗАГРУЗКА ДАННЫХ ====================
st.sidebar.markdown('<h2 style="margin: 0 0 4px 0; font-size: 20px;">Прогресс ЕГЭ</h2>', unsafe_allow_html=True)
st.sidebar.markdown('<p style="color: #6B7280; font-size: 13px; margin: 0 0 16px 0;">Панель управления</p>', unsafe_allow_html=True)

if st.sidebar.button("Обновить данные", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

students_df = load_sheet("Ученики")
tasks_df = load_sheet("Задания")

if students_df.empty: students_df = load_sheet("Sheet1")
if tasks_df.empty: tasks_df = load_sheet("Sheet2")

if students_df.empty or tasks_df.empty:
    st.error("Не удалось загрузить данные")
    st.stop()

student_id_col = 'id' if 'id' in students_df.columns else students_df.columns[0]
student_name_col = 'ФИО' if 'ФИО' in students_df.columns else students_df.columns[1]

hw_link_col = 'Домашнее задание' if 'Домашнее задание' in students_df.columns else None
hw_status_col = 'Отметка о выполнении' if 'Отметка о выполнении' in students_df.columns else None

task_id_col = 'id' if 'id' in tasks_df.columns else tasks_df.columns[0]
task_cols = [c for c in tasks_df.columns if c != task_id_col and c != 'date']

students_list = students_df[student_name_col].tolist()

# ==================== РАСЧЁТ ДАННЫХ ПО КЛАССУ ====================
class_data = []
for _, row in students_df.iterrows():
    sid = row[student_id_col]
    name = row[student_name_col]
    s_tasks = tasks_df[tasks_df[task_id_col] == sid].copy()
    
    if not s_tasks.empty:
        s_tasks['date_parsed'] = pd.to_datetime(s_tasks['date'], dayfirst=True, errors='coerce')
        s_tasks = s_tasks.sort_values('date_parsed', na_position='first')
        
        forecast = calculate_student_forecast(s_tasks, task_cols)
        
        hw_link = row[hw_link_col] if hw_link_col else None
        hw_status = row[hw_status_col] if hw_status_col else None
        hw_done = False
        if hw_status and isinstance(hw_status, str) and hw_status.strip().lower() in ['да', 'yes', '+', 'true', '1']:
            hw_done = True
        
        last_date = s_tasks.iloc[-1]['date'] if not s_tasks.empty else None
        
        latest = s_tasks.iloc[-1]
        task_columns = [c for c in latest.index if c.startswith('task_')]
        studied = 0
        for col in task_columns:
            v = latest[col]
            if not pd.isna(v) and v != '' and v != '-' and v != '—' and v != '–':
                studied += 1
        total = len(task_columns)
        
        class_data.append({
            'name': name,
            'forecast_secondary': forecast['forecast_secondary'],
            'current_secondary': forecast['current_secondary'],
            'best_secondary': forecast['best_secondary'],
            'attempts': len(forecast['scores_history']),
            'studied': studied,
            'total_tasks': total,
            'progress': (studied / total * 100) if total > 0 else 0,
            'hw_done': hw_done,
            'hw_link': hw_link,
            'last_date': last_date,
            'forecast_data': forecast
        })

class_df = pd.DataFrame(class_data)

if class_df.empty:
    st.error("Нет данных по ученикам")
    st.stop()

class_df_sorted = class_df.sort_values('forecast_secondary', ascending=False).reset_index(drop=True)

# ==================== САЙДБАР: ВЫБОР ====================
st.sidebar.markdown("---")
st.sidebar.markdown('<p style="color: #6B7280; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700; margin-bottom: 8px;">Раздел</p>', unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = "Обзор класса"
if 'selected_student_from_class' not in st.session_state:
    st.session_state.selected_student_from_class = None

pages_list = ["Обзор класса", "Ученик"]

try:
    page_index = pages_list.index(st.session_state.page)
except ValueError:
    page_index = 0

page = st.sidebar.radio(
    "Раздел",
    pages_list,
    index=page_index,
    label_visibility="collapsed"
)

st.session_state.page = page

selected_student = None
if page == "Ученик":
    st.sidebar.markdown("---")
    st.sidebar.markdown('<p style="color: #6B7280; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700; margin-bottom: 8px;">Ученик</p>', unsafe_allow_html=True)
    
    student_options = class_df_sorted['name'].tolist()
    
    if st.session_state.selected_student_from_class and st.session_state.selected_student_from_class in student_options:
        default_index = student_options.index(st.session_state.selected_student_from_class)
        st.session_state.selected_student_from_class = None
    else:
        default_index = 0
    
    selected_student = st.sidebar.selectbox(
        "Ученик",
        student_options,
        index=default_index,
        label_visibility="collapsed"
    )

# ==================== СТРАНИЦА: ОБЗОР КЛАССА ====================
if page == "Обзор класса":
    st.markdown('<h1 style="margin: 0;">Обзор класса</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #6B7280; font-size: 14px; margin-top: 4px;">{datetime.now().strftime("%d.%m.%Y")} · {len(class_df)} учеников</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    class_avg = class_df['forecast_secondary'].mean()
    class_max = class_df['forecast_secondary'].max()
    class_min = class_df['forecast_secondary'].min()
    class_avg_progress = class_df['progress'].mean()
    
    top_student = class_df_sorted.iloc[0]
    bottom_student = class_df_sorted.iloc[-1]
    
    avg_level_text, _, avg_card_class = get_score_level(class_avg)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="card {avg_card_class}">
            <div class="card-title">Средний прогноз</div>
            <div class="card-value">{class_avg:.0f}</div>
            <div class="card-sub">{avg_level_text}</div>
            <div class="card-stats">
                <div class="card-stats-item">
                    <div class="stat-value">{class_max:.0f}</div>
                    <div class="stat-label">макс</div>
                </div>
                <div class="card-stats-item">
                    <div class="stat-value">{class_min:.0f}</div>
                    <div class="stat-label">мин</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="card card-primary">
            <div class="card-title">Прогресс изучения</div>
            <div class="card-value">{class_avg_progress:.0f}%</div>
            <div class="card-sub">заданий изучено в среднем</div>
            <div class="status-bar">
                <div class="status-bar-fill" style="width: {class_avg_progress}%; background: linear-gradient(90deg, #4F46E5, #7C3AED);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="card card-excellent">
            <div class="card-title">Лучший результат</div>
            <div class="card-value" style="color: #047857;">{top_student['forecast_secondary']:.0f}</div>
            <div class="card-sub" style="font-size: 14px; color: #1F2937; font-weight: 600;">{top_student['name']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="card card-low">
            <div class="card-title">Требует внимания</div>
            <div class="card-value" style="color: #B91C1C;">{bottom_student['forecast_secondary']:.0f}</div>
            <div class="card-sub" style="font-size: 14px; color: #1F2937; font-weight: 600;">{bottom_student['name']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<h3>Распределение по уровням</h3>', unsafe_allow_html=True)
    
    excellent = len(class_df[class_df['forecast_secondary'] >= 80])
    good = len(class_df[(class_df['forecast_secondary'] >= 60) & (class_df['forecast_secondary'] < 80)])
    medium = len(class_df[(class_df['forecast_secondary'] >= 40) & (class_df['forecast_secondary'] < 60)])
    low = len(class_df[class_df['forecast_secondary'] < 40])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="card card-excellent">
            <div class="card-title">Отлично (80+)</div>
            <div class="card-value" style="color: #047857;">{excellent}</div>
            <div class="card-sub">{excellent/len(class_df)*100:.0f}% класса</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="card card-good">
            <div class="card-title">Хорошо (60-79)</div>
            <div class="card-value" style="color: #047857;">{good}</div>
            <div class="card-sub">{good/len(class_df)*100:.0f}% класса</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="card card-medium">
            <div class="card-title">Средне (40-59)</div>
            <div class="card-value" style="color: #B45309;">{medium}</div>
            <div class="card-sub">{medium/len(class_df)*100:.0f}% класса</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="card card-low">
            <div class="card-title">Внимание (&lt;40)</div>
            <div class="card-value" style="color: #B91C1C;">{low}</div>
            <div class="card-sub">{low/len(class_df)*100:.0f}% класса</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.markdown('<h3>Рейтинг класса</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #6B7280; font-size: 13px; margin-bottom: 12px;">Нажмите на имя ученика, чтобы открыть его статистику</p>', unsafe_allow_html=True)
        
        # Генерируем CSS для каждой кнопки по имени (используем data-атрибут через key)
        # Streamlit добавляет класс st-key-{key} к обёртке, key = f"rank_btn_{i}"
        css_rank = "<style>"
        for idx, row in class_df_sorted.iterrows():
            score = row['forecast_secondary']
            
            if score >= 80:
                bg, border, text, hover = "#F0FDF4", "#059669", "#047857", "#DCFCE7"
            elif score >= 60:
                bg, border, text, hover = "#F0FDF4", "#10B981", "#047857", "#DCFCE7"
            elif score >= 40:
                bg, border, text, hover = "#FFFBEB", "#D97706", "#B45309", "#FEF3C7"
            else:
                bg, border, text, hover = "#FEF2F2", "#DC2626", "#B91C1C", "#FEE2E2"
            
            css_rank += f"""
        .st-key-rank_btn_{idx} button {{
            background: {bg} !important;
            border: 2px solid {border} !important;
            color: {text} !important;
            text-align: left !important;
            justify-content: flex-start !important;
            padding: 14px 18px !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            transition: all 0.2s !important;
            box-shadow: none !important;
        }}
        .st-key-rank_btn_{idx} button:hover {{
            background: {hover} !important;
            border-color: {border} !important;
            color: {text} !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
        }}
        .st-key-rank_btn_{idx} button:focus {{
            background: {bg} !important;
            border-color: {border} !important;
            color: {text} !important;
            box-shadow: 0 0 0 3px {border}33 !important;
        }}
        """
        css_rank += "</style>"
        st.markdown(css_rank, unsafe_allow_html=True)
        
        for idx, row in class_df_sorted.iterrows():
            student_name = row['name']
            score = row['forecast_secondary']
            level_text, _, _ = get_score_level(score)
            
            if score >= 80:
                text_color = "#047857"
                chip_bg = "#F0FDF4"
                chip_border = "#059669"
            elif score >= 60:
                text_color = "#047857"
                chip_bg = "#F0FDF4"
                chip_border = "#10B981"
            elif score >= 40:
                text_color = "#B45309"
                chip_bg = "#FFFBEB"
                chip_border = "#D97706"
            else:
                text_color = "#B91C1C"
                chip_bg = "#FEF2F2"
                chip_border = "#DC2626"
            
            c1, c2 = st.columns([5, 2])
            
            with c1:
                if st.button(
                    f"{idx+1}.  {student_name}",
                    key=f"rank_btn_{idx}",
                    use_container_width=True
                ):
                    st.session_state.selected_student_from_class = student_name
                    st.session_state.page = "Ученик"
                    st.rerun()
            
            with c2:
                # Единый блок с баллом и уровнем одинакового размера
                st.markdown(f"""
                <div style="
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                    background: {chip_bg};
                    border: 2px solid {chip_border};
                    border-radius: 10px;
                    padding: 12px 14px;
                    height: 52px;
                    box-sizing: border-box;
                ">
                    <span style="font-size: 20px; font-weight: 700; color: {text_color}; line-height: 1;">
                        {score:.0f}
                    </span>
                    <span style="
                        font-size: 10px;
                        font-weight: 700;
                        color: {text_color};
                        text-transform: uppercase;
                        letter-spacing: 0.03em;
                        line-height: 1.2;
                        text-align: left;
                    ">
                        {level_text}
                    </span>
                </div>
                """, unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<h3>Домашние задания</h3>', unsafe_allow_html=True)
        
        hw_done_count = class_df['hw_done'].sum()
        hw_total = len(class_df)
        hw_percent = (hw_done_count / hw_total * 100) if hw_total > 0 else 0
        
        hw_card_class = "card-excellent" if hw_percent >= 80 else "card-medium" if hw_percent >= 50 else "card-low"
        
        st.markdown(f"""
        <div class="card {hw_card_class}">
            <div class="card-title">Выполнено</div>
            <div class="card-value" style="color: #047857;">{hw_done_count} / {hw_total}</div>
            <div class="card-sub">{hw_percent:.0f}% класса выполнили домашнее задание</div>
            <div class="status-bar">
                <div class="status-bar-fill" style="width: {hw_percent}%; background: linear-gradient(90deg, #059669, #10B981);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        not_done = class_df[~class_df['hw_done']]['name'].tolist()
        
        if not_done:
            items_html = ''.join(f'<div style="color: #1F2937; font-size: 14px; padding: 8px 0; border-bottom: 1px solid #FECACA; font-weight: 500;">{n}</div>' for n in not_done)
            st.markdown(f"""
            <div style="background: #FEF2F2; border-radius: 12px; padding: 18px 20px; border: 2px solid #FECACA; border-left: 6px solid #DC2626;">
                <p style="margin: 0 0 10px 0; font-weight: 700; color: #B91C1C; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em;">Не выполнили ({len(not_done)})</p>
                <div>{items_html}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #F0FDF4; border-radius: 12px; padding: 18px 20px; border: 2px solid #A7F3D0; border-left: 6px solid #059669;">
                <p style="margin: 0; font-weight: 700; color: #047857; font-size: 15px;">Все выполнили домашнее задание</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<h3>Сводная таблица</h3>', unsafe_allow_html=True)
    
    table_data = []
    for _, row in class_df_sorted.iterrows():
        level_text, _, _ = get_score_level(row['forecast_secondary'])
        hw_status_text = "Выполнено" if row['hw_done'] else "Не выполнено"
        
        table_data.append({
            "№": len(table_data) + 1,
            "Ученик": row['name'],
            "Прогноз": f"{row['forecast_secondary']:.0f}",
            "Уровень": level_text,
            "Прогресс": f"{row['progress']:.0f}%",
            "Попыток": row['attempts'],
            "ДЗ": hw_status_text
        })
    
    df_table = pd.DataFrame(table_data)
    st.dataframe(df_table, use_container_width=True, hide_index=True)

# ==================== СТРАНИЦА: УЧЕНИК ====================
else:
    student_row = students_df[students_df[student_name_col] == selected_student]
    if student_row.empty:
        st.error("Ученик не найден")
        st.stop()

    student_id = student_row[student_id_col].iloc[0]

    hw_link = student_row[hw_link_col].iloc[0] if hw_link_col else None
    hw_status = student_row[hw_status_col].iloc[0] if hw_status_col else None

    target_score = None
    if 'Целевой балл' in students_df.columns:
        try:
            target_score = float(student_row['Целевой балл'].iloc[0])
        except:
            pass

    student_tasks = tasks_df[tasks_df[task_id_col] == student_id].copy()
    student_tasks['date_parsed'] = pd.to_datetime(student_tasks['date'], dayfirst=True, errors='coerce')
    student_tasks = student_tasks.sort_values('date_parsed', na_position='first')

    if student_tasks.empty:
        st.warning(f"Нет данных для {selected_student}")
        st.stop()

    forecast_data = calculate_student_forecast(student_tasks, task_cols)

    forecast_secondary = forecast_data['forecast_secondary']
    current_secondary = forecast_data['current_secondary']
    best_secondary = forecast_data['best_secondary']
    forecast_primary = forecast_data['forecast_primary']
    current_primary = forecast_data['current_primary']
    best_primary = forecast_data['best_primary']
    scores_history = forecast_data['scores_history']
    task_stats = forecast_data['task_stats']

    prev_secondary = 0
    if len(scores_history) > 1:
        prev_secondary = convert_to_secondary(round(scores_history[-2]))

    studied_count = 0
    not_studied_count = 0
    latest = student_tasks.iloc[-1]

    task_columns = [col for col in latest.index if col.startswith('task_')]
    task_columns_sorted = sorted(task_columns, key=lambda x: int(x.replace('task_', '')))

    for col in task_columns_sorted:
        value = latest[col]
        if pd.isna(value) or value == '' or value == '-' or value == '—' or value == '–':
            not_studied_count += 1
        else:
            studied_count += 1

    total_tasks = len(task_columns_sorted)
    progress_percent = (studied_count / total_tasks * 100) if total_tasks > 0 else 0

    level_text, level_class, level_card_class = get_score_level(forecast_secondary)

    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
        <div>
            <h1 style="margin: 0;">{selected_student}</h1>
            <p style="color: #6B7280; font-size: 14px; margin: 6px 0 0 0;">
                Последнее обновление: {student_tasks.iloc[-1]['date'] if not student_tasks.empty else 'Нет данных'}
                &nbsp;·&nbsp;
                Всего попыток: {len(scores_history)}
            </p>
        </div>
        <div class="level-container {level_class}">
            <span class="level-text">{level_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if hw_link and isinstance(hw_link, str) and hw_link.strip() != '' and not pd.isna(hw_link):
        if hw_status and isinstance(hw_status, str) and hw_status.strip().lower() in ['да', 'yes', '+', 'true', '1']:
            hw_status_text = "Выполнено"
            hw_status_class = "hw-status-done"
            hw_container_class = "hw-done"
        else:
            hw_status_text = "Не выполнено"
            hw_status_class = "hw-status-not-done"
            hw_container_class = "hw-not-done"

        st.markdown(f"""
        <div class="hw-container {hw_container_class}">
            <div style="display: flex; align-items: center; gap: 16px; flex-wrap: wrap;">
                <span class="hw-label">Домашнее задание</span>
                <a href="{hw_link}" target="_blank" class="hw-link">Перейти к заданию</a>
            </div>
            <div>
                <span class="hw-status {hw_status_class}">{hw_status_text}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="hw-container" style="background: #F9FAFB; border-left-color: #D1D5DB;">
            <div style="display: flex; align-items: center; gap: 16px;">
                <span class="hw-label" style="color: #9CA3AF;">Домашнее задание</span>
                <span style="color: #9CA3AF; font-size: 15px;">Не задано</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Определяем цвет для карточки прогноза
    if forecast_secondary >= 80: forecast_bar = "#059669"
    elif forecast_secondary >= 60: forecast_bar = "#10B981"
    elif forecast_secondary >= 40: forecast_bar = "#D97706"
    else: forecast_bar = "#DC2626"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if len(scores_history) > 1:
            prev_secondary = convert_to_secondary(round(scores_history[-2]))
            delta = forecast_secondary - prev_secondary if prev_secondary else None
            if delta is not None:
                delta_color = "#059669" if delta > 0 else "#DC2626" if delta < 0 else "#6B7280"
                delta_html = f'<div style="color: {delta_color}; font-size: 15px; font-weight: 700; margin-top: 6px;">{delta:+.0f} баллов</div>'
            else:
                delta_html = ''
        else:
            delta_html = '<div style="color: #9CA3AF; font-size: 13px; margin-top: 6px;">Первая попытка</div>'

        current_secondary = convert_to_secondary(round(scores_history[-1])) if scores_history else 0
        best_secondary = convert_to_secondary(round(max(scores_history))) if scores_history else 0

        st.markdown(f"""
        <div class="card {level_card_class}">
            <div class="card-title">Прогноз баллов</div>
            <div class="card-value" style="color: {forecast_bar};">{forecast_secondary}</div>
            <div class="card-sub">{forecast_primary:.1f} первичных</div>
            {delta_html}
            <div class="card-stats">
                <div class="card-stats-item">
                    <div class="stat-value">{current_secondary}</div>
                    <div class="stat-label">последний</div>
                </div>
                <div class="card-stats-item">
                    <div class="stat-value">{best_secondary}</div>
                    <div class="stat-label">лучший</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if target_score:
            diff = forecast_secondary - target_score
            color = "#059669" if diff >= 0 else "#DC2626"
            status = "Достигнут" if diff >= 0 else "Осталось"
            target_card = "card-excellent" if diff >= 0 else "card-low"

            st.markdown(f"""
            <div class="card {target_card}">
                <div class="card-title">Целевой балл</div>
                <div class="card-value">{target_score:.0f}</div>
                <div class="card-sub" style="color: {color}; font-weight: 700;">{diff:+.0f} баллов</div>
                <div style="font-size: 13px; color: #6B7280; margin-top: 4px; font-weight: 600;">{status}</div>
                <div class="card-stats">
                    <div class="card-stats-item">
                        <div class="stat-value">{((forecast_secondary / target_score) * 100):.0f}%</div>
                        <div class="stat-label">выполнение</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">Целевой балл</div>
                <div class="card-value" style="color: #9CA3AF;">—</div>
                <div class="card-sub">Не указан</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card card-primary">
            <div class="card-title">Прогресс изучения</div>
            <div class="card-value">{studied_count}/{total_tasks}</div>
            <div class="card-sub">{progress_percent:.0f}% заданий изучено</div>
            <div class="status-bar">
                <div class="status-bar-fill" style="width: {progress_percent}%; background: linear-gradient(90deg, #4F46E5, #7C3AED);"></div>
            </div>
            <div class="card-stats">
                <div class="card-stats-item">
                    <div class="stat-value">{len(scores_history)}</div>
                    <div class="stat-label">всего попыток</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        all_students_scores = []
        for _, row in students_df.iterrows():
            sid = row[student_id_col]
            s_tasks = tasks_df[tasks_df[task_id_col] == sid]
            if not s_tasks.empty:
                s_forecast = calculate_student_forecast(s_tasks, task_cols)
                all_students_scores.append((row[student_name_col], s_forecast['forecast_secondary']))

        all_students_scores.sort(key=lambda x: x[1], reverse=True)
        rank = next((i+1 for i, (name, _) in enumerate(all_students_scores) if name == selected_student), None)

        st.markdown(f"""
        <div class="card card-primary">
            <div class="card-title">Рейтинг</div>
            <div class="card-value" style="color: #4F46E5;">#{rank if rank else '—'}</div>
            <div class="card-sub">из {len(all_students_scores)} учеников</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Результаты",
        "Динамика",
        "Рекомендации",
        "Сравнение"
    ])

    # ==================== TAB 1: РЕЗУЛЬТАТЫ ====================
    with tab1:
        st.markdown('<h3 style="margin-bottom: 4px;">Карта вероятностей и последний пробник</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #6B7280; font-size: 13px; margin-bottom: 16px;">Верхняя полоса — вероятность правильного решения по последним 5 попыткам. Нижняя — результат последнего пробника.</p>', unsafe_allow_html=True)

        probabilities_list = []
        for col in task_columns_sorted:
            num = col.replace('task_', '')
            if num in task_stats:
                stats = task_stats[num]
                correct = stats['correct']
                total = stats['total']
                prob = correct / total * 100 if total > 0 else None
            else:
                prob = None
            probabilities_list.append(prob)

        prob_colors = []
        prob_labels = []
        for prob in probabilities_list:
            if prob is None:
                prob_colors.append('#E5E7EB'); prob_labels.append('—')
            elif prob >= 80:
                prob_colors.append('#059669'); prob_labels.append(f'{prob:.0f}%')
            elif prob >= 60:
                prob_colors.append('#10B981'); prob_labels.append(f'{prob:.0f}%')
            elif prob >= 40:
                prob_colors.append('#D97706'); prob_labels.append(f'{prob:.0f}%')
            elif prob >= 20:
                prob_colors.append('#EA580C'); prob_labels.append(f'{prob:.0f}%')
            else:
                prob_colors.append('#DC2626'); prob_labels.append(f'{prob:.0f}%')

        last_colors = []
        last_labels = []
        for col in task_columns_sorted:
            num = col.replace('task_', '')
            task_num_int = int(num)
            max_score = 2 if task_num_int in [26, 27] else 1
            value = latest[col]
            status = get_task_status(value)

            if status == 'not_studied':
                last_colors.append('#E5E7EB'); last_labels.append('—')
            elif status == 'wrong':
                last_colors.append('#DC2626'); last_labels.append('0')
            else:
                try:
                    val = float(value)
                    if val == 0:
                        last_colors.append('#DC2626'); last_labels.append('0')
                    elif val == max_score:
                        last_colors.append('#059669'); last_labels.append(f'{val:.0f}')
                    elif val > 0:
                        last_colors.append('#D97706'); last_labels.append(f'{val:.0f}')
                    else:
                        last_colors.append('#E5E7EB'); last_labels.append('—')
                except:
                    last_colors.append('#E5E7EB'); last_labels.append('—')

        def hex_to_rgba(hex_color, alpha=0.25):
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return f'rgba({r}, {g}, {b}, {alpha})'

        prob_colors_rgba = [hex_to_rgba(c, 0.25) for c in prob_colors]
        last_colors_rgba = [hex_to_rgba(c, 0.25) for c in last_colors]

        task_numbers = [col.replace('task_', '') for col in task_columns_sorted]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=task_numbers,
            y=[0.55] * len(task_numbers),
            base=[0.55] * len(task_numbers),
            name='Вероятность решения',
            marker=dict(color=prob_colors_rgba, line=dict(color=prob_colors, width=2)),
            text=prob_labels,
            textposition='inside',
            textfont=dict(size=11, color='#1F2937', family='system-ui'),
            showlegend=False,
            width=0.8,
            hovertemplate='Задание %{x}<br>Вероятность: %{text}<extra></extra>'
        ))

        fig.add_trace(go.Bar(
            x=task_numbers,
            y=[0.55] * len(task_numbers),
            base=[0.0] * len(task_numbers),
            name='Последний пробник',
            marker=dict(color=last_colors_rgba, line=dict(color=last_colors, width=2)),
            text=last_labels,
            textposition='inside',
            textfont=dict(size=11, color='#1F2937', family='system-ui'),
            showlegend=False,
            width=0.8,
            hovertemplate='Задание %{x}<br>Последний пробник: %{text}<extra></extra>'
        ))

        fig.add_shape(type="rect", xref="paper", yref="y",
                     x0=0, x1=1, y0=0.57, y1=1.15,
                     fillcolor="rgba(79, 70, 229, 0.04)",
                     line=dict(color="rgba(79, 70, 229, 0.5)", width=2),
                     layer="below")

        fig.add_shape(type="rect", xref="paper", yref="y",
                     x0=0, x1=1, y0=-0.02, y1=0.53,
                     fillcolor="rgba(124, 58, 237, 0.04)",
                     line=dict(color="rgba(124, 58, 237, 0.5)", width=2),
                     layer="below")

        fig.add_annotation(xref="paper", yref="y", x=1.02, y=0.86,
                          text="Вероятность", showarrow=False,
                          font=dict(size=11, color="#4F46E5", family='system-ui'), align="left", xanchor="left")

        fig.add_annotation(xref="paper", yref="y", x=1.02, y=0.27,
                          text="Пробник", showarrow=False,
                          font=dict(size=11, color="#7C3AED", family='system-ui'), align="left", xanchor="left")

        fig.update_layout(
            height=300, barmode='overlay', bargap=0.3,
            xaxis=dict(title=dict(text="Номер задания", font=dict(size=13, color='#6B7280')),
                      tickfont=dict(size=12, color='#6B7280'), tickmode='linear', tick0=1, dtick=1),
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[-0.1, 1.2]),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=100, t=10, b=40),
            font=dict(family='system-ui, -apple-system, sans-serif'),
            dragmode=False,
            modebar=dict(remove=['zoomIn2d', 'zoomOut2d', 'pan2d', 'resetScale2d', 'autoScale2d'])
        )

        config = {
            'displayModeBar': True,
            'modeBarButtonsToRemove': ['zoomIn2d', 'zoomOut2d', 'pan2d', 'resetScale2d', 'autoScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian'],
            'displaylogo': False,
            'scrollZoom': False
        }

        st.plotly_chart(fig, use_container_width=True, config=config)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div style="background: #EEF2FF; border-radius: 12px; padding: 16px 18px; border: 2px solid #C7D2FE; border-left: 6px solid #4F46E5;">
                <p style="margin: 0 0 10px 0; font-weight: 700; color: #4F46E5; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em;">Вероятность решения (верхняя полоса)</p>
                <div style="display: flex; flex-direction: column; gap: 6px; font-size: 13px; color: #4B5563;">
                    <span><b style="color: #059669;">80-100%</b> — отлично</span>
                    <span><b style="color: #10B981;">60-79%</b> — хорошо</span>
                    <span><b style="color: #D97706;">40-59%</b> — средне</span>
                    <span><b style="color: #EA580C;">20-39%</b> — слабо</span>
                    <span><b style="color: #DC2626;">0-19%</b> — очень слабо</span>
                    <span><b style="color: #9CA3AF;">Серый</b> — не решалось</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="background: #F5F3FF; border-radius: 12px; padding: 16px 18px; border: 2px solid #DDD6FE; border-left: 6px solid #7C3AED;">
                <p style="margin: 0 0 10px 0; font-weight: 700; color: #7C3AED; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em;">Последний пробник (нижняя полоса)</p>
                <div style="display: flex; flex-direction: column; gap: 6px; font-size: 13px; color: #4B5563;">
                    <span><b style="color: #059669;">Максимум</b> — полностью верно</span>
                    <span><b style="color: #D97706;">Частично</b> — неполный балл (26-27)</span>
                    <span><b style="color: #DC2626;">0</b> — неверно</span>
                    <span><b style="color: #9CA3AF;">Серый</b> — не изучалось</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<h3>Детальная информация по заданиям</h3>', unsafe_allow_html=True)

        details_data = []
        for col in task_columns_sorted:
            num = col.replace('task_', '')
            task_num_int = int(num)
            max_score = 2 if task_num_int in [26, 27] else 1

            if num in task_stats:
                stats = task_stats[num]
                correct = stats['correct']
                wrong = stats['wrong']
                total_attempts = stats['total']
                prob_display = f"{(correct/total_attempts*100):.0f}%" if total_attempts > 0 else "—"
            else:
                correct = 0; wrong = 0; total_attempts = 0
                prob_display = "—"

            latest_value = latest[col]
            latest_status = get_task_status(latest_value)

            if latest_status == 'not_studied':
                latest_display = "—"
            elif latest_status == 'wrong':
                latest_display = "0"
            else:
                try:
                    val = float(latest_value)
                    if val == max_score: latest_display = f"{val:.0f} (макс)"
                    elif val > 0: latest_display = f"{val:.0f} (частично)"
                    else: latest_display = "0"
                except:
                    latest_display = "—"

            details_data.append({
                "Задание": f"№{num}",
                "Вес": max_score,
                "Правильно": correct,
                "Неправильно": wrong,
                "Вероятность": prob_display,
                "Последний пробник": latest_display
            })

        df_details = pd.DataFrame(details_data)
        st.dataframe(df_details, use_container_width=True, hide_index=True)

    # ==================== TAB 2: ДИНАМИКА ====================
    with tab2:
        st.markdown('<h3>Динамика результатов</h3>', unsafe_allow_html=True)

        if len(student_tasks) > 1:
            dates = []
            primary_scores = []
            secondary_scores = []

            for idx, (_, row) in enumerate(student_tasks.iterrows()):
                primary = 0
                for col in task_columns_sorted:
                    num = col.replace('task_', '')
                    task_num_int = int(num)
                    weight = 2 if task_num_int in [26, 27] else 1
                    value = row[col]
                    if not pd.isna(value) and value != '' and value != '-' and value != '—' and value != '–':
                        try:
                            primary += float(value) * weight
                        except:
                            pass
                dates.append(row['date'])
                primary_scores.append(round(primary))
                secondary_scores.append(convert_to_secondary(round(primary)))

            if len(dates) > 1:
                fig_progress = go.Figure()

                fig_progress.add_trace(go.Scatter(
                    x=dates, y=secondary_scores,
                    mode='lines+markers', name='Результат',
                    line=dict(color='#4F46E5', width=4),
                    marker=dict(size=10, color='#4F46E5', line=dict(color='#FFFFFF', width=2)),
                    hovertemplate='%{x}<br>%{y} баллов<extra></extra>'
                ))

                if forecast_secondary > 0:
                    fig_progress.add_hline(y=forecast_secondary, line_dash="dash",
                                          line_color="#7C3AED", line_width=2,
                                          annotation_text=f"Прогноз: {forecast_secondary:.0f}",
                                          annotation_position="top right",
                                          annotation_font=dict(size=11, color="#7C3AED"))

                if target_score:
                    fig_progress.add_hline(y=target_score, line_dash="dash",
                                          line_color="#DC2626", line_width=2,
                                          annotation_text=f"Цель: {target_score:.0f}",
                                          annotation_position="bottom right",
                                          annotation_font=dict(size=11, color="#DC2626"))

                fig_progress.update_layout(
                    height=400,
                    xaxis=dict(title=dict(text="Дата", font=dict(size=13, color='#6B7280')),
                              tickfont=dict(size=11, color='#6B7280'), gridcolor='#F3F4F6'),
                    yaxis=dict(title=dict(text="Тестовый балл", font=dict(size=13, color='#6B7280')),
                              range=[0, max(100, max(secondary_scores) + 10)],
                              tickfont=dict(size=11, color='#6B7280'), gridcolor='#F3F4F6'),
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified', showlegend=False,
                    font=dict(family='system-ui, -apple-system, sans-serif'),
                    dragmode=False,
                    modebar=dict(remove=['zoomIn2d', 'zoomOut2d', 'pan2d', 'resetScale2d', 'autoScale2d'])
                )

                st.plotly_chart(fig_progress, use_container_width=True, config=config)

                col1, col2, col3 = st.columns(3)

                with col1:
                    progress_delta = secondary_scores[-1] - secondary_scores[0] if len(secondary_scores) > 1 else 0
                    if progress_delta > 0:
                        color = "#059669"; card_class = "card-excellent"
                    elif progress_delta < 0:
                        color = "#DC2626"; card_class = "card-low"
                    else:
                        color = "#6B7280"; card_class = ""
                    st.markdown(f"""
                    <div class="card {card_class}">
                        <div class="card-title">Общий прогресс</div>
                        <div class="card-value" style="color: {color};">{progress_delta:+.0f}</div>
                        <div class="card-sub">баллов</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    best_score = max(secondary_scores) if secondary_scores else 0
                    _, _, best_card = get_score_level(best_score)
                    st.markdown(f"""
                    <div class="card {best_card}">
                        <div class="card-title">Лучший результат</div>
                        <div class="card-value">{best_score}</div>
                        <div class="card-sub">баллов</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    last_change = secondary_scores[-1] - secondary_scores[-2] if len(secondary_scores) > 1 else 0
                    if last_change > 0:
                        color = "#059669"; card_class = "card-excellent"
                    elif last_change < 0:
                        color = "#DC2626"; card_class = "card-low"
                    else:
                        color = "#6B7280"; card_class = ""
                    st.markdown(f"""
                    <div class="card {card_class}">
                        <div class="card-title">Последнее изменение</div>
                        <div class="card-value" style="color: {color};">{last_change:+.0f}</div>
                        <div class="card-sub">баллов</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Недостаточно данных для отображения динамики")
        else:
            st.info("Добавьте больше записей для отслеживания динамики")

    # ==================== TAB 3: РЕКОМЕНДАЦИИ ====================
    with tab3:
        st.markdown('<h3>Рекомендации по улучшению</h3>', unsafe_allow_html=True)

        weak_tasks = []
        medium_tasks = []
        not_studied_tasks = []

        for num, stats in task_stats.items():
            total_attempts = stats['total']
            correct = stats['correct']
            not_studied = stats['not_studied']

            if total_attempts > 0:
                success_rate = correct / total_attempts * 100
                if success_rate < 40:
                    weak_tasks.append((num, success_rate, correct, total_attempts))
                elif success_rate < 70:
                    medium_tasks.append((num, success_rate, correct, total_attempts))
            elif not_studied > 0 and stats['not_studied'] >= len(student_tasks):
                not_studied_tasks.append(num)
            else:
                if total_attempts == 0 and not_studied < len(student_tasks):
                    medium_tasks.append((num, 0, 0, 0))

        st.markdown("""
        <div style="background: linear-gradient(135deg, #EEF2FF, #F5F3FF); padding: 22px; border-radius: 14px; margin-bottom: 20px; border: 2px solid #C7D2FE;">
            <p style="font-size: 16px; font-weight: 600; margin: 0; color: #1F2937; text-align: center; line-height: 1.6;">
                Каждый результат — это сигнал. Анализируй ошибки, исправляй их и двигайся вперёд.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if weak_tasks:
            st.markdown("""
            <div style="background: #FEF2F2; border-radius: 14px; padding: 20px; border: 2px solid #FECACA; margin-bottom: 16px;">
                <h4 style="color: #B91C1C; margin: 0 0 14px 0; font-size: 18px; text-transform: uppercase; letter-spacing: 0.05em;">Требуют внимания</h4>
            """, unsafe_allow_html=True)

            weak_sorted = sorted(weak_tasks, key=lambda x: x[1])[:5]
            for num, success_rate, correct, total in weak_sorted:
                st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 18px 20px; margin-bottom: 10px; border: 2px solid #FECACA; border-left: 6px solid #DC2626;">
                    <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 10px;">
                        <span style="background: #DC2626; color: white; border-radius: 8px; padding: 5px 14px; font-weight: 700; font-size: 14px;">Задание {num}</span>
                        <span style="font-weight: 700; color: #B91C1C; font-size: 18px;">{success_rate:.0f}%</span>
                        <span style="color: #9CA3AF; font-size: 13px;">({correct}/{total} верно)</span>
                    </div>
                    <p style="font-size: 14px; line-height: 1.6; color: #4B5563; margin: 0;">
                        Ошибки — это возможность понять, куда направить усилия. Разбери решение и попробуй ещё раз.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        if medium_tasks:
            st.markdown("""
            <div style="background: #FFFBEB; border-radius: 14px; padding: 20px; border: 2px solid #FED7AA; margin-bottom: 16px;">
                <h4 style="color: #B45309; margin: 0 0 14px 0; font-size: 18px; text-transform: uppercase; letter-spacing: 0.05em;">Потенциал к улучшению</h4>
            """, unsafe_allow_html=True)

            medium_sorted = sorted(medium_tasks, key=lambda x: x[1], reverse=True)[:3]
            for num, success_rate, correct, total in medium_sorted:
                st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 18px 20px; margin-bottom: 10px; border: 2px solid #FED7AA; border-left: 6px solid #D97706;">
                    <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 10px;">
                        <span style="background: #D97706; color: white; border-radius: 8px; padding: 5px 14px; font-weight: 700; font-size: 14px;">Задание {num}</span>
                        <span style="font-weight: 700; color: #B45309; font-size: 18px;">{success_rate:.0f}%</span>
                        <span style="color: #9CA3AF; font-size: 13px;">({correct}/{total} верно)</span>
                    </div>
                    <p style="font-size: 14px; line-height: 1.6; color: #4B5563; margin: 0;">
                        Уже хороший результат. Осталось довести решение до совершенства.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        if not_studied_tasks:
            st.markdown("""
            <div style="background: #EEF2FF; border-radius: 14px; padding: 20px; border: 2px solid #C7D2FE; margin-bottom: 16px;">
                <h4 style="color: #4F46E5; margin: 0 0 14px 0; font-size: 18px; text-transform: uppercase; letter-spacing: 0.05em;">Неизученные задания</h4>
            """, unsafe_allow_html=True)

            for num in not_studied_tasks[:5]:
                st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 18px 20px; margin-bottom: 10px; border: 2px solid #C7D2FE; border-left: 6px solid #4F46E5;">
                    <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 10px;">
                        <span style="background: #4F46E5; color: white; border-radius: 8px; padding: 5px 14px; font-weight: 700; font-size: 14px;">Задание {num}</span>
                        <span style="font-weight: 700; color: #4F46E5; font-size: 14px;">Новое</span>
                    </div>
                    <p style="font-size: 14px; line-height: 1.6; color: #4B5563; margin: 0;">
                        Начни с изучения теории, затем попробуй решить. Каждое новое задание — шаг вперёд.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        total_studied = studied_count
        total_all = total_tasks

        if total_studied == total_all:
            stage_message = "Все задания изучены. Теперь задача — довести каждый результат до максимума."
            stage_card = "card-excellent"
        elif total_studied / total_all >= 0.8:
            stage_message = "Почти все задания изучены. Осталось совсем немного до полного освоения материала."
            stage_card = "card-excellent"
        elif total_studied / total_all >= 0.5:
            stage_message = "Половина пути пройдена. Продолжай двигаться вперёд — результат придёт."
            stage_card = "card-medium"
        else:
            stage_message = "Путь начинается с первого шага. Каждое изученное задание — это твоя победа."
            stage_card = "card-low"

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div class="card {stage_card}" style="text-align: center; padding: 26px;">
                <h4 style="color: #1F2937; margin: 0 0 14px 0; font-size: 18px;">Прогресс: {total_studied} / {total_all} заданий</h4>
                <div class="status-bar" style="max-width: 300px; margin: 10px auto;">
                    <div class="status-bar-fill" style="width: {(total_studied/total_all*100) if total_all > 0 else 0}%; background: linear-gradient(90deg, #4F46E5, #7C3AED);"></div>
                </div>
                <p style="font-size: 15px; line-height: 1.6; color: #4B5563; margin: 14px 0 0 0;">
                    {stage_message}
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ==================== TAB 4: СРАВНЕНИЕ ====================
    with tab4:
        st.markdown('<h3>Сравнение с классом</h3>', unsafe_allow_html=True)

        all_scores = []
        for _, row in students_df.iterrows():
            sid = row[student_id_col]
            name = row[student_name_col]
            s_tasks = tasks_df[tasks_df[task_id_col] == sid]

            if not s_tasks.empty:
                s_forecast = calculate_student_forecast(s_tasks, task_cols)
                all_scores.append((name, s_forecast['forecast_secondary']))

        if all_scores:
            all_scores.sort(key=lambda x: x[1], reverse=True)

            colors_scores = []
            for name, score in all_scores:
                if name == selected_student:
                    colors_scores.append('#4F46E5')
                else:
                    if score >= 80: colors_scores.append('#A7F3D0')
                    elif score >= 60: colors_scores.append('#BBF7D0')
                    elif score >= 40: colors_scores.append('#FED7AA')
                    else: colors_scores.append('#FECACA')

            fig_rank = go.Figure()

            fig_rank.add_trace(go.Bar(
                x=[name for name, _ in all_scores],
                y=[score for _, score in all_scores],
                marker=dict(color=colors_scores, line=dict(color='#FFFFFF', width=1)),
                text=[f'{score:.0f}' for _, score in all_scores],
                textposition='outside',
                textfont=dict(size=11, color='#1F2937'),
                hovertemplate='%{x}<br>%{y:.0f} баллов<extra></extra>'
            ))

            fig_rank.update_layout(
                height=max(400, len(all_scores) * 30),
                xaxis=dict(title=dict(text="Ученик", font=dict(size=13, color='#6B7280')),
                          tickfont=dict(size=10, color='#6B7280'), tickangle=-45),
                yaxis=dict(title=dict(text="Прогнозируемый балл", font=dict(size=13, color='#6B7280')),
                          range=[0, max(100, max([s for _, s in all_scores]) + 10)],
                          tickfont=dict(size=11, color='#6B7280'), gridcolor='#F3F4F6'),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                font=dict(family='system-ui, -apple-system, sans-serif'),
                dragmode=False,
                modebar=dict(remove=['zoomIn2d', 'zoomOut2d', 'pan2d', 'resetScale2d', 'autoScale2d'])
            )

            st.plotly_chart(fig_rank, use_container_width=True, config=config)

            col1, col2, col3, col4 = st.columns(4)

            current_score = next((s for n, s in all_scores if n == selected_student), 0)
            max_score = max([s for _, s in all_scores]) if all_scores else 0
            avg_score = sum([s for _, s in all_scores]) / len(all_scores) if all_scores else 0
            min_score = min([s for _, s in all_scores]) if all_scores else 0

            _, _, current_card = get_score_level(current_score)
            _, _, max_card = get_score_level(max_score)
            _, _, avg_card = get_score_level(avg_score)
            _, _, min_card = get_score_level(min_score)

            with col1:
                st.markdown(f"""
                <div class="card {current_card}">
                    <div class="card-title">Ваш прогноз</div>
                    <div class="card-value">{current_score:.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="card {max_card}">
                    <div class="card-title">Лучший прогноз</div>
                    <div class="card-value">{max_score:.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="card {avg_card}">
                    <div class="card-title">Средний прогноз</div>
                    <div class="card-value">{avg_score:.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class="card {min_card}">
                    <div class="card-title">Минимальный</div>
                    <div class="card-value">{min_score:.0f}</div>
                </div>
                """, unsafe_allow_html=True)

            rank = next((i+1 for i, (n, _) in enumerate(all_scores) if n == selected_student), None)
            total = len(all_scores)
            
            students_below = total - rank if rank else 0
            other_students = total - 1
            percentile = (students_below / other_students * 100) if other_students > 0 else 100

            st.markdown(f"""
            <div class="card card-primary" style="margin-top: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
                    <div>
                        <h4 style="margin: 0; color: #6B7280; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em;">Позиция</h4>
                        <p style="font-size: 28px; font-weight: 700; margin: 6px 0 0 0; color: #1F2937;">#{rank} из {total}</p>
                    </div>
                    <div style="text-align: right;">
                        <h4 style="margin: 0; color: #6B7280; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em;">Выше чем</h4>
                        <p style="font-size: 28px; font-weight: 700; color: #4F46E5; margin: 6px 0 0 0;">{percentile:.0f}%</p>
                    </div>
                </div>
                <div class="status-bar" style="margin-top: 16px;">
                    <div class="status-bar-fill" style="width: {percentile}%; background: linear-gradient(90deg, #4F46E5, #7C3AED);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Нет данных для сравнения")
