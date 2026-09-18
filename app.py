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
    .stApp, .stApp > div, .main, .block-container,
    .element-container, .stMarkdown, .stTabs,
    div[data-testid="stTabs"], .stSidebar,
    .stSidebar .stMarkdown, .stSelectbox,
    .stButton, .stAlert, .stDataFrame,
    [data-testid="stMetric"] {
        background-color: #f8f9fa !important;
        color: #1f2937 !important;
    }
    
    .card {
        background: #ffffff !important;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
        margin-bottom: 16px;
        border: 1px solid #e5e7eb !important;
    }
    
    .card-title {
        font-size: 18px;
        font-weight: 600;
        color: #6b7280 !important;
        margin-bottom: 12px;
    }
    
    .card-value {
        font-size: 36px;
        font-weight: 700;
        color: #1f2937 !important;
    }
    
    .card-sub {
        font-size: 14px;
        color: #9ca3af !important;
        margin-top: 4px;
    }
    
    .card-stats {
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        border-top: 1px solid #e5e7eb;
        margin-top: 10px;
    }
    
    .card-stats-item { text-align: center; }
    .card-stats-item .stat-value { font-size: 20px; font-weight: 700; color: #1f2937; }
    .card-stats-item .stat-label { font-size: 12px; color: #9ca3af; }
    
    .level-container {
        display: inline-block;
        padding: 8px 20px;
        border-radius: 20px;
        font-size: 28px !important;
        font-weight: bold !important;
        margin: 5px 0;
        min-width: 200px;
        text-align: center;
    }
    
    .level-excellent { background: linear-gradient(135deg, #10b981, #059669) !important; color: white !important; box-shadow: 0 2px 8px rgba(16,185,129,0.3); }
    .level-good { background: linear-gradient(135deg, #34d399, #059669) !important; color: white !important; box-shadow: 0 2px 8px rgba(52,211,153,0.3); }
    .level-medium { background: linear-gradient(135deg, #fbbf24, #f59e0b) !important; color: #1f2937 !important; box-shadow: 0 2px 8px rgba(251,191,36,0.3); }
    .level-low { background: linear-gradient(135deg, #f87171, #dc2626) !important; color: white !important; box-shadow: 0 2px 8px rgba(248,113,113,0.3); }
    
    .level-icon { font-size: 32px !important; margin-right: 10px; }
    .level-text { font-size: 28px !important; font-weight: bold !important; }
    
    .hw-container {
        background: white;
        border-radius: 12px;
        padding: 16px 20px;
        border: 2px solid #e5e7eb;
        margin-top: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
    }
    
    .hw-done { background: #ecfdf5 !important; border-color: #10b981 !important; }
    .hw-not-done { background: #fef2f2 !important; border-color: #ef4444 !important; }
    
    .hw-link {
        color: #3b82f6 !important;
        text-decoration: none !important;
        font-weight: 600;
        font-size: 16px;
        padding: 6px 12px;
        background: #eff6ff;
        border-radius: 8px;
    }
    
    .hw-status { font-weight: 700; font-size: 16px; padding: 4px 16px; border-radius: 20px; display: inline-block; }
    .hw-status-done { color: #059669; background: #d1fae5; }
    .hw-status-not-done { color: #dc2626; background: #fee2e2; }
    .hw-label { font-weight: 600; font-size: 16px; color: #1f2937; }
    
    .status-bar { height: 8px; border-radius: 4px; background: #e5e7eb; margin: 8px 0; overflow: hidden; }
    .status-bar-fill { height: 100%; border-radius: 4px; transition: width 0.6s ease; }
    
    h1, h2, h3, h4, h5, h6 { color: #1f2937 !important; }
    p, div, span, label { color: #1f2937 !important; }
    
    .stDataFrame table { color: #1f2937 !important; }
    .stDataFrame thead tr th { background-color: #f3f4f6 !important; color: #1f2937 !important; }
    .stDataFrame tbody tr td { background-color: #ffffff !important; color: #1f2937 !important; }
    .stDataFrame tbody tr:hover td { background-color: #f3f4f6 !important; }
    
    .stSidebar { background-color: #f8f9fa !important; border-right: 1px solid #e5e7eb !important; }
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar p, .stSidebar div { color: #1f2937 !important; }
    
    .stSelectbox div[data-baseweb="select"] { background-color: #ffffff !important; border-color: #e5e7eb !important; }
    .stSelectbox div[data-baseweb="select"] input { color: #1f2937 !important; }
    
    .stButton button {
        background-color: #ffffff !important;
        border-color: #e5e7eb !important;
        color: #1f2937 !important;
    }
    .stButton button:hover { background-color: #f3f4f6 !important; }
    
    .stTabs [data-baseweb="tab"] { background-color: #f8f9fa !important; color: #6b7280 !important; border-color: #e5e7eb !important; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background-color: #ffffff !important; color: #1f2937 !important; border-bottom: 2px solid #3b82f6 !important; }
    
    .stAlert { background-color: #ffffff !important; border-color: #e5e7eb !important; color: #1f2937 !important; }
    
    @media only screen and (max-width: 768px) {
        .card { padding: 16px; margin-bottom: 12px; }
        .card-value { font-size: 28px; }
        .card-title { font-size: 16px; }
        .level-container { font-size: 20px !important; padding: 6px 16px; min-width: 150px; }
        .level-text { font-size: 20px !important; }
        .level-icon { font-size: 24px !important; }
        .hw-container { flex-direction: column; align-items: stretch !important; text-align: center; padding: 14px; }
        .stTabs [data-baseweb="tab"] { font-size: 14px; padding: 8px 12px; }
    }
    
    @media only screen and (max-width: 480px) {
        .card { padding: 12px; }
        .card-value { font-size: 24px; }
        .card-title { font-size: 14px; }
        .level-container { font-size: 16px !important; padding: 4px 12px; min-width: 120px; }
        .level-text { font-size: 16px !important; }
        .level-icon { font-size: 20px !important; }
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
    if score >= 80: return "Отлично", "🌟", "level-excellent"
    elif score >= 60: return "Хорошо", "👍", "level-good"
    elif score >= 40: return "Средне", "📊", "level-medium"
    else: return "Требует внимания", "⚠️", "level-low"

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

def calculate_student_forecast(student_tasks, task_cols):
    if student_tasks.empty:
        return {'forecast_primary': 0, 'forecast_secondary': 0,
                'current_primary': 0, 'current_secondary': 0,
                'best_primary': 0, 'best_secondary': 0,
                'scores_history': [], 'task_stats': {}}
    
    scores_history = []
    task_stats = {}
    
    for col in task_cols:
        num = col.replace('task_', '').replace('задание', '').replace('_', '')
        task_stats[num] = {'correct': 0, 'wrong': 0, 'total': 0, 'not_studied': 0}
    
    for _, row in student_tasks.iterrows():
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
    current_primary = scores_history[-1] if scores_history else 0
    best_primary = max(scores_history) if scores_history else 0
    
    return {
        'forecast_primary': forecast_primary,
        'forecast_secondary': convert_to_secondary(round(forecast_primary)),
        'current_primary': current_primary,
        'current_secondary': convert_to_secondary(round(current_primary)),
        'best_primary': best_primary,
        'best_secondary': convert_to_secondary(round(best_primary)),
        'scores_history': scores_history,
        'task_stats': task_stats
    }

# ==================== ЗАГРУЗКА ДАННЫХ ====================
st.sidebar.title("🎓 Прогресс ЕГЭ")

if st.sidebar.button("🔄 Обновить данные"):
    st.cache_data.clear()
    st.rerun()

students_df = load_sheet("Ученики")
tasks_df = load_sheet("Задания")

if students_df.empty: students_df = load_sheet("Sheet1")
if tasks_df.empty: tasks_df = load_sheet("Sheet2")

if students_df.empty or tasks_df.empty:
    st.error("❌ Не удалось загрузить данные")
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
    s_tasks = tasks_df[tasks_df[task_id_col] == sid]
    
    if not s_tasks.empty:
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
st.sidebar.subheader("📊 Отображение")

# Инициализация session_state для страницы и ученика
if 'page' not in st.session_state:
    st.session_state.page = "🏫 Обзор класса"
if 'selected_student_from_class' not in st.session_state:
    st.session_state.selected_student_from_class = None

# Определяем список страниц
pages_list = ["🏫 Обзор класса", "👤 Ученик"]

# Определяем индекс текущей страницы
try:
    page_index = pages_list.index(st.session_state.page)
except ValueError:
    page_index = 0

page = st.sidebar.radio(
    "Выберите страницу:",
    pages_list,
    index=page_index,
    label_visibility="collapsed"
)

# Синхронизируем session_state
st.session_state.page = page

selected_student = None
if page == "👤 Ученик":
    st.sidebar.markdown("---")
    st.sidebar.subheader("👤 Выберите ученика")
    
    # Определяем индекс для selectbox
    student_options = class_df_sorted['name'].tolist()
    
    # Если был клик по имени из рейтинга - используем его
    if st.session_state.selected_student_from_class and st.session_state.selected_student_from_class in student_options:
        default_index = student_options.index(st.session_state.selected_student_from_class)
        # Сбрасываем после использования
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
if page == "🏫 Обзор класса":
    st.markdown('<h1 style="margin: 0; color: #1f2937;">🏫 Обзор класса</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #9ca3af; font-size: 14px;">📅 {datetime.now().strftime("%d.%m.%Y")} • 👥 {len(class_df)} учеников</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    class_avg = class_df['forecast_secondary'].mean()
    class_max = class_df['forecast_secondary'].max()
    class_min = class_df['forecast_secondary'].min()
    class_avg_progress = class_df['progress'].mean()
    
    top_student = class_df_sorted.iloc[0]
    bottom_student = class_df_sorted.iloc[-1]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        level_text, level_icon, level_class = get_score_level(class_avg)
        st.markdown(f"""
        <div class="card">
            <div class="card-title">📊 Средний прогноз класса</div>
            <div class="card-value">{class_avg:.0f}</div>
            <div class="card-sub">{level_icon} {level_text}</div>
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
        <div class="card">
            <div class="card-title">📚 Прогресс изучения</div>
            <div class="card-value">{class_avg_progress:.0f}%</div>
            <div class="card-sub">заданий изучено в среднем</div>
            <div class="status-bar">
                <div class="status-bar-fill" style="width: {class_avg_progress}%; background: #3b82f6;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">🏆 Лучший результат</div>
            <div class="card-value">{top_student['forecast_secondary']:.0f}</div>
            <div class="card-sub" style="font-size: 14px; color: #1f2937; font-weight: 500;">{top_student['name']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">📉 Требует внимания</div>
            <div class="card-value">{bottom_student['forecast_secondary']:.0f}</div>
            <div class="card-sub" style="font-size: 14px; color: #1f2937; font-weight: 500;">{bottom_student['name']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<h3 style="color: #1f2937;">📊 Распределение по уровням подготовки</h3>', unsafe_allow_html=True)
    
    excellent = len(class_df[class_df['forecast_secondary'] >= 80])
    good = len(class_df[(class_df['forecast_secondary'] >= 60) & (class_df['forecast_secondary'] < 80)])
    medium = len(class_df[(class_df['forecast_secondary'] >= 40) & (class_df['forecast_secondary'] < 60)])
    low = len(class_df[class_df['forecast_secondary'] < 40])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="card" style="border-left: 6px solid #10b981;">
            <div class="card-title">🌟 Отлично (80+)</div>
            <div class="card-value" style="color: #10b981;">{excellent}</div>
            <div class="card-sub">{excellent/len(class_df)*100:.0f}% класса</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="card" style="border-left: 6px solid #34d399;">
            <div class="card-title">👍 Хорошо (60-79)</div>
            <div class="card-value" style="color: #34d399;">{good}</div>
            <div class="card-sub">{good/len(class_df)*100:.0f}% класса</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="card" style="border-left: 6px solid #f59e0b;">
            <div class="card-title">📊 Средне (40-59)</div>
            <div class="card-value" style="color: #f59e0b;">{medium}</div>
            <div class="card-sub">{medium/len(class_df)*100:.0f}% класса</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="card" style="border-left: 6px solid #ef4444;">
            <div class="card-title">⚠️ Внимание (&lt;40)</div>
            <div class="card-value" style="color: #ef4444;">{low}</div>
            <div class="card-sub">{low/len(class_df)*100:.0f}% класса</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ==================== РЕЙТИНГ КЛАССА С КЛИКАБЕЛЬНЫМИ ИМЕНАМИ ====================
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.markdown('<h3 style="color: #1f2937;">🏆 Рейтинг класса</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #9ca3af; font-size: 13px; margin-bottom: 12px;">👆 Нажмите на имя ученика, чтобы открыть его статистику</p>', unsafe_allow_html=True)
        
        # Кнопки перехода к ученику
        for idx, row in class_df_sorted.iterrows():
            student_name = row['name']
            score = row['forecast_secondary']
            level_text, level_icon, _ = get_score_level(score)
            
            # Медаль для топ-3
            if idx == 0:
                medal = "🥇"
            elif idx == 1:
                medal = "🥈"
            elif idx == 2:
                medal = "🥉"
            else:
                medal = f"#{idx+1}"
            
            # Цвет полосы прогресса
            if score >= 80: bar_color = "#10b981"
            elif score >= 60: bar_color = "#34d399"
            elif score >= 40: bar_color = "#f59e0b"
            else: bar_color = "#ef4444"
            
            # Создаём колонки для строки
            c1, c2, c3 = st.columns([5, 2, 1])
            
            with c1:
                # Кликабельная кнопка-имя
                if st.button(
                    f"{medal}  {student_name}",
                    key=f"goto_{student_name}",
                    use_container_width=True
                ):
                    st.session_state.selected_student_from_class = student_name
                    st.session_state.page = "👤 Ученик"
                    st.rerun()
            
            with c2:
                st.markdown(f"""
                <div style="text-align: center; padding-top: 6px;">
                    <span style="font-size: 20px; font-weight: 700; color: {bar_color};">{score:.0f}</span>
                    <span style="font-size: 14px; color: #9ca3af;"> баллов</span>
                </div>
                """, unsafe_allow_html=True)
            
            with c3:
                st.markdown(f"""
                <div style="text-align: center; padding-top: 6px; font-size: 22px;">
                    {level_icon}
                </div>
                """, unsafe_allow_html=True)
        
        # Дополнительно: общий график рейтинга
        st.markdown("---")
        st.markdown('<h4 style="color: #1f2937;">📊 Визуальный рейтинг</h4>', unsafe_allow_html=True)
        
        colors_rank = []
        for score in class_df_sorted['forecast_secondary']:
            if score >= 80: colors_rank.append('#10b981')
            elif score >= 60: colors_rank.append('#34d399')
            elif score >= 40: colors_rank.append('#f59e0b')
            else: colors_rank.append('#ef4444')
        
        fig_rank = go.Figure()
        fig_rank.add_trace(go.Bar(
            x=class_df_sorted['forecast_secondary'],
            y=class_df_sorted['name'],
            orientation='h',
            marker_color=colors_rank,
            text=[f'{s:.0f}' for s in class_df_sorted['forecast_secondary']],
            textposition='outside',
            hovertemplate='%{y}<br>Прогноз: %{x:.0f} баллов<extra></extra>'
        ))
        
        fig_rank.update_layout(
            height=max(300, len(class_df_sorted) * 35),
            xaxis=dict(
                title=dict(text="Прогнозируемый балл", font=dict(size=14)),
                range=[0, 105],
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                tickfont=dict(size=13),
                autorange='reversed'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=40, t=10, b=40),
            dragmode=False,
            modebar=dict(remove=['zoomIn2d', 'zoomOut2d', 'pan2d', 'resetScale2d', 'autoScale2d'])
        )
        
        config = {
            'displayModeBar': False,
            'displaylogo': False,
            'scrollZoom': False
        }
        
        st.plotly_chart(fig_rank, use_container_width=True, config=config)
    
    with col_right:
        st.markdown('<h3 style="color: #1f2937;">📝 Домашние задания</h3>', unsafe_allow_html=True)
        
        hw_done_count = class_df['hw_done'].sum()
        hw_total = len(class_df)
        hw_percent = (hw_done_count / hw_total * 100) if hw_total > 0 else 0
        
        st.markdown(f"""
        <div class="card">
            <div class="card-title">✅ Выполнено</div>
            <div class="card-value" style="color: #10b981;">{hw_done_count}/{hw_total}</div>
            <div class="card-sub">{hw_percent:.0f}% класса выполнили домашнее задание</div>
            <div class="status-bar">
                <div class="status-bar-fill" style="width: {hw_percent}%; background: #10b981;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        not_done = class_df[~class_df['hw_done']]['name'].tolist()
        
        if not_done:
            st.markdown(f"""
            <div style="background: #fef2f2; border-radius: 12px; padding: 16px; border: 2px solid #fecaca;">
                <p style="margin: 0 0 8px 0; font-weight: 600; color: #dc2626; font-size: 15px;">❌ Не выполнили ({len(not_done)})</p>
                <div style="display: flex; flex-direction: column; gap: 6px;">
                    {''.join(f'<span style="color: #1f2937; font-size: 14px;">• {n}</span>' for n in not_done)}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #ecfdf5; border-radius: 12px; padding: 16px; border: 2px solid #10b981;">
                <p style="margin: 0; font-weight: 600; color: #059669; font-size: 15px;">🎉 Все выполнили домашнее задание!</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<h3 style="color: #1f2937;">📋 Сводная таблица по классу</h3>', unsafe_allow_html=True)
    
    table_data = []
    for _, row in class_df_sorted.iterrows():
        level_text, level_icon, _ = get_score_level(row['forecast_secondary'])
        hw_status_text = "✅ Выполнено" if row['hw_done'] else "❌ Не выполнено"
        
        table_data.append({
            "№": len(table_data) + 1,
            "Ученик": row['name'],
            "🔮 Прогноз": f"{row['forecast_secondary']:.0f}",
            "📊 Уровень": f"{level_icon} {level_text}",
            "📚 Прогресс": f"{row['progress']:.0f}%",
            "📝 Попыток": row['attempts'],
            "📖 ДЗ": hw_status_text
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

    student_tasks = tasks_df[tasks_df[task_id_col] == student_id].sort_values('date')

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

    level_text, level_icon, level_class = get_score_level(forecast_secondary)

    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
        <div>
            <h1 style="margin: 0; color: #1f2937;">📊 {selected_student}</h1>
            <p style="color: #9ca3af; font-size: 14px; margin: 4px 0 0 0;">
                📅 Последнее обновление: {student_tasks.iloc[-1]['date'] if not student_tasks.empty else 'Нет данных'}
            </p>
            <p style="color: #9ca3af; font-size: 13px; margin: 2px 0 0 0;">
                📈 Всего попыток: {len(scores_history)}
            </p>
        </div>
        <div class="level-container {level_class}">
            <span class="level-icon">{level_icon}</span>
            <span class="level-text">{level_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if hw_link and isinstance(hw_link, str) and hw_link.strip() != '' and not pd.isna(hw_link):
        if hw_status and isinstance(hw_status, str) and hw_status.strip().lower() in ['да', 'yes', '+', 'true', '1']:
            hw_status_text = "✅ Выполнено"
            hw_status_class = "hw-status-done"
            hw_container_class = "hw-done"
        else:
            hw_status_text = "❌ Не выполнено"
            hw_status_class = "hw-status-not-done"
            hw_container_class = "hw-not-done"

        st.markdown(f"""
        <div class="hw-container {hw_container_class}">
            <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                <span class="hw-label">📚 Домашнее задание:</span>
                <a href="{hw_link}" target="_blank" class="hw-link">🔗 Перейти к заданию</a>
            </div>
            <div>
                <span class="hw-status {hw_status_class}">{hw_status_text}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="hw-container" style="background: #f9fafb; border-color: #e5e7eb;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span class="hw-label" style="color: #9ca3af;">📚 Домашнее задание:</span>
                <span style="color: #9ca3af; font-size: 15px;">Не задано</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if len(scores_history) > 1:
            prev_secondary = convert_to_secondary(round(scores_history[-2]))
            delta = forecast_secondary - prev_secondary if prev_secondary else None
            delta_html = f'<div style="color: {"green" if delta > 0 else "red" if delta < 0 else "gray"}; font-size: 16px;">{delta:+.0f} баллов</div>' if delta is not None else ''
        else:
            delta_html = '<div style="color: #9ca3af; font-size: 14px;">Первая попытка</div>'

        current_secondary = convert_to_secondary(round(scores_history[-1])) if scores_history else 0
        best_secondary = convert_to_secondary(round(max(scores_history))) if scores_history else 0

        st.markdown(f"""
        <div class="card">
            <div class="card-title">🔮 Прогноз баллов</div>
            <div class="card-value">{forecast_secondary}</div>
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
            color = "green" if diff >= 0 else "red"
            status = "✅ Достигнут" if diff >= 0 else "⬆️ Осталось"

            st.markdown(f"""
            <div class="card">
                <div class="card-title">🎯 Целевой балл</div>
                <div class="card-value">{target_score:.0f}</div>
                <div class="card-sub" style="color: {color};">{diff:+.0f} баллов</div>
                <div style="font-size: 14px; color: #9ca3af;">{status}</div>
                <div class="card-stats">
                    <div class="card-stats-item">
                        <div class="stat-value">{((forecast_secondary / target_score) * 100):.0f}%</div>
                        <div class="stat-label">выполнение цели</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">🎯 Целевой балл</div>
                <div class="card-value" style="color: #9ca3af;">—</div>
                <div class="card-sub">Не указан</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">📚 Прогресс изучения</div>
            <div class="card-value">{studied_count}/{total_tasks}</div>
            <div class="card-sub">{progress_percent:.0f}% заданий изучено</div>
            <div class="status-bar">
                <div class="status-bar-fill" style="width: {progress_percent}%; background: #3b82f6;"></div>
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
        <div class="card">
            <div class="card-title">🏆 Рейтинг</div>
            <div class="card-value">#{rank if rank else '—'}</div>
            <div class="card-sub">из {len(all_students_scores)} учеников</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Результаты",
        "📈 Динамика",
        "🎯 Рекомендации",
        "🏅 Сравнение"
    ])

    # ==================== TAB 1: РЕЗУЛЬТАТЫ ====================
    with tab1:
        st.markdown('<h3 style="margin-bottom: 12px; color: #1f2937;">🗺 Карта вероятностей и последний пробник</h3>', unsafe_allow_html=True)

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
                prob_colors.append('#e5e7eb'); prob_labels.append('—')
            elif prob >= 80:
                prob_colors.append('#10b981'); prob_labels.append(f'{prob:.0f}%')
            elif prob >= 60:
                prob_colors.append('#34d399'); prob_labels.append(f'{prob:.0f}%')
            elif prob >= 40:
                prob_colors.append('#fbbf24'); prob_labels.append(f'{prob:.0f}%')
            elif prob >= 20:
                prob_colors.append('#fb923c'); prob_labels.append(f'{prob:.0f}%')
            else:
                prob_colors.append('#ef4444'); prob_labels.append(f'{prob:.0f}%')

        last_colors = []
        last_labels = []
        for col in task_columns_sorted:
            num = col.replace('task_', '')
            task_num_int = int(num)
            max_score = 2 if task_num_int in [26, 27] else 1
            value = latest[col]
            status = get_task_status(value)

            if status == 'not_studied':
                last_colors.append('#e5e7eb'); last_labels.append('—')
            elif status == 'wrong':
                last_colors.append('#ef4444'); last_labels.append('0')
            else:
                try:
                    val = float(value)
                    if val == 0:
                        last_colors.append('#ef4444'); last_labels.append('0')
                    elif val == max_score:
                        last_colors.append('#10b981'); last_labels.append(f'{val:.0f}✓')
                    elif val > 0:
                        last_colors.append('#f59e0b'); last_labels.append(f'{val:.0f}')
                    else:
                        last_colors.append('#e5e7eb'); last_labels.append('—')
                except:
                    last_colors.append('#e5e7eb'); last_labels.append('—')

        def hex_to_rgba(hex_color, alpha=0.2):
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return f'rgba({r}, {g}, {b}, {alpha})'

        prob_colors_rgba = [hex_to_rgba(c, 0.2) for c in prob_colors]
        last_colors_rgba = [hex_to_rgba(c, 0.2) for c in last_colors]

        task_numbers = [col.replace('task_', '') for col in task_columns_sorted]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=task_numbers,
            y=[0.55] * len(task_numbers),
            base=[0.55] * len(task_numbers),
            name='Вероятность решения',
            marker=dict(color=prob_colors_rgba, line=dict(color=prob_colors, width=1.5)),
            text=prob_labels,
            textposition='inside',
            textfont=dict(size=12, color='black'),
            showlegend=False,
            width=0.8,
            hovertemplate='Задание %{x}<br>Вероятность: %{text}<extra></extra>'
        ))

        fig.add_trace(go.Bar(
            x=task_numbers,
            y=[0.55] * len(task_numbers),
            base=[0.0] * len(task_numbers),
            name='Последний пробник',
            marker=dict(color=last_colors_rgba, line=dict(color=last_colors, width=1.5)),
            text=last_labels,
            textposition='inside',
            textfont=dict(size=12, color='black'),
            showlegend=False,
            width=0.8,
            hovertemplate='Задание %{x}<br>Последний пробник: %{text}<extra></extra>'
        ))

        fig.add_shape(type="rect", xref="paper", yref="y",
                     x0=0, x1=1, y0=0.57, y1=1.15,
                     fillcolor="rgba(59, 130, 246, 0.08)",
                     line=dict(color="rgba(59, 130, 246, 0.6)", width=2),
                     layer="below")

        fig.add_shape(type="rect", xref="paper", yref="y",
                     x0=0, x1=1, y0=-0.02, y1=0.53,
                     fillcolor="rgba(139, 92, 246, 0.08)",
                     line=dict(color="rgba(139, 92, 246, 0.6)", width=2),
                     layer="below")

        fig.add_annotation(xref="paper", yref="y", x=1.02, y=0.86,
                          text="🎯 Вероятность<br>решения", showarrow=False,
                          font=dict(size=11, color="#3b82f6"), align="left", xanchor="left")

        fig.add_annotation(xref="paper", yref="y", x=1.02, y=0.27,
                          text="📝 Последний<br>пробник", showarrow=False,
                          font=dict(size=11, color="#8b5cf6"), align="left", xanchor="left")

        fig.update_layout(
            height=300, barmode='overlay', bargap=0.3,
            xaxis=dict(title=dict(text="Номер задания", font=dict(size=16)),
                      tickfont=dict(size=14), tickmode='linear', tick0=1, dtick=1),
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[-0.1, 1.2]),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=100, t=10, b=40),
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
            <div style="background: #eff6ff; border-radius: 12px; padding: 14px; border: 2px solid #3b82f6;">
                <p style="margin: 0 0 8px 0; font-weight: 600; color: #1f2937; font-size: 15px;">🎯 Вероятность решения (верхняя полоса)</p>
                <div style="display: flex; flex-direction: column; gap: 4px; font-size: 13px; color: #6b7280;">
                    <span>🟩 80-100% — отлично</span>
                    <span>🟢 60-79% — хорошо</span>
                    <span>🟨 40-59% — средне</span>
                    <span>🟧 20-39% — слабо</span>
                    <span>🟥 0-19% — очень слабо</span>
                    <span>⬜ — не решалось</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="background: #f5f3ff; border-radius: 12px; padding: 14px; border: 2px solid #8b5cf6;">
                <p style="margin: 0 0 8px 0; font-weight: 600; color: #1f2937; font-size: 15px;">📝 Последний пробник (нижняя полоса)</p>
                <div style="display: flex; flex-direction: column; gap: 4px; font-size: 13px; color: #6b7280;">
                    <span>🟩 Максимум — полностью верно</span>
                    <span>🟨 Частично — неполный балл (26-27)</span>
                    <span>🟥 0 — неверно</span>
                    <span>⬜ — не изучалось</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<h3 style="color: #1f2937;">📋 Детальная информация по заданиям</h3>', unsafe_allow_html=True)

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
                    if val == max_score: latest_display = f"{val:.0f} ✓"
                    elif val > 0: latest_display = f"{val:.0f} (частично)"
                    else: latest_display = "0"
                except:
                    latest_display = "—"

            details_data.append({
                "Задание": f"№{num}",
                "Вес": max_score,
                "✅ Правильно": correct,
                "❌ Неправильно": wrong,
                "🎯 Вероятность": prob_display,
                "📝 Последний пробник": latest_display
            })

        df_details = pd.DataFrame(details_data)
        st.dataframe(df_details, use_container_width=True, hide_index=True)

    # ==================== TAB 2: ДИНАМИКА ====================
    with tab2:
        st.markdown('<h3 style="color: #1f2937;">📈 Динамика результатов</h3>', unsafe_allow_html=True)

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
                    line=dict(color='#3b82f6', width=3),
                    marker=dict(size=8, color='#3b82f6')
                ))

                if forecast_secondary > 0:
                    fig_progress.add_hline(y=forecast_secondary, line_dash="dash",
                                          line_color="#8b5cf6",
                                          annotation_text=f"Прогноз: {forecast_secondary:.0f}",
                                          annotation_position="top right")

                if target_score:
                    fig_progress.add_hline(y=target_score, line_dash="dash",
                                          line_color="#ef4444",
                                          annotation_text=f"Цель: {target_score:.0f}",
                                          annotation_position="bottom right")

                fig_progress.update_layout(
                    height=400,
                    xaxis=dict(title=dict(text="Дата", font=dict(size=14)), tickfont=dict(size=12)),
                    yaxis=dict(title=dict(text="Тестовый балл", font=dict(size=14)),
                              range=[0, max(100, max(secondary_scores) + 10)], tickfont=dict(size=12)),
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified', legend=dict(font=dict(size=12)),
                    dragmode=False,
                    modebar=dict(remove=['zoomIn2d', 'zoomOut2d', 'pan2d', 'resetScale2d', 'autoScale2d'])
                )

                st.plotly_chart(fig_progress, use_container_width=True, config=config)

                col1, col2, col3 = st.columns(3)

                with col1:
                    progress_delta = secondary_scores[-1] - secondary_scores[0] if len(secondary_scores) > 1 else 0
                    color = "green" if progress_delta > 0 else "red" if progress_delta < 0 else "gray"
                    st.markdown(f"""
                    <div class="card">
                        <div class="card-title">📊 Общий прогресс</div>
                        <div class="card-value" style="color: {color};">{progress_delta:+.0f}</div>
                        <div class="card-sub">баллов</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    best_score = max(secondary_scores) if secondary_scores else 0
                    st.markdown(f"""
                    <div class="card">
                        <div class="card-title">🏆 Лучший результат</div>
                        <div class="card-value">{best_score}</div>
                        <div class="card-sub">баллов</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    last_change = secondary_scores[-1] - secondary_scores[-2] if len(secondary_scores) > 1 else 0
                    color = "green" if last_change > 0 else "red" if last_change < 0 else "gray"
                    st.markdown(f"""
                    <div class="card">
                        <div class="card-title">📈 Последнее изменение</div>
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
        st.markdown('<h3 style="color: #1f2937;">🎯 Рекомендации по улучшению</h3>', unsafe_allow_html=True)

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
        <div style="background: linear-gradient(135deg, #e0f2fe, #dbeafe); padding: 20px; border-radius: 16px; margin-bottom: 20px; border: 1px solid #bae6fd;">
            <p style="font-size: 20px; font-weight: 600; margin: 0; color: #1f2937; text-align: center;">
                💡 «Каждый результат — это сигнал. Анализируй ошибки, исправляй их и двигайся вперёд!»
            </p>
        </div>
        """, unsafe_allow_html=True)

        if weak_tasks:
            st.markdown("""
            <div style="background: #fef2f2; border-radius: 16px; padding: 20px; border: 1px solid #fecaca; margin-bottom: 16px;">
                <h4 style="color: #dc2626; margin: 0 0 12px 0; font-size: 22px;">🔴 Требуют внимания</h4>
            """, unsafe_allow_html=True)

            weak_sorted = sorted(weak_tasks, key=lambda x: x[1])[:5]
            for num, success_rate, correct, total in weak_sorted:
                st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #ef4444; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                        <span style="background: #ef4444; color: white; border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px;">{num}</span>
                        <span style="font-weight: 600; color: #dc2626; font-size: 18px;">{success_rate:.0f}%</span>
                        <span style="color: #9ca3af; font-size: 14px;">({correct}/{total} верно)</span>
                    </div>
                    <p style="font-size: 16px; line-height: 1.6; color: #1f2937; margin: 8px 0; font-style: italic;">
                        📚 «Ошибки — это не провал, а возможность понять, куда направить свои усилия. 
                        Задание {num} ждёт твоего второго шанса! Разбери решение и попробуй ещё раз. 
                        Ты справишься! 💪»
                    </p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        if medium_tasks:
            st.markdown("""
            <div style="background: #fef3c7; border-radius: 16px; padding: 20px; border: 1px solid #fde68a; margin-bottom: 16px;">
                <h4 style="color: #d97706; margin: 0 0 12px 0; font-size: 22px;">⭐ Потенциал к улучшению</h4>
            """, unsafe_allow_html=True)

            medium_sorted = sorted(medium_tasks, key=lambda x: x[1], reverse=True)[:3]
            for num, success_rate, correct, total in medium_sorted:
                st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #f59e0b; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                        <span style="background: #f59e0b; color: white; border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px;">{num}</span>
                        <span style="font-weight: 600; color: #d97706; font-size: 18px;">{success_rate:.0f}%</span>
                        <span style="color: #9ca3af; font-size: 14px;">({correct}/{total} верно)</span>
                    </div>
                    <p style="font-size: 16px; line-height: 1.6; color: #1f2937; margin: 8px 0; font-style: italic;">
                        🎯 «Ты уже на правильном пути! Задание {num} почти покорилось. 
                        Доведи решение до совершенства — и результат будет ещё лучше! ⚡»
                    </p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        if not_studied_tasks:
            st.markdown("""
            <div style="background: #eff6ff; border-radius: 16px; padding: 20px; border: 1px solid #bfdbfe; margin-bottom: 16px;">
                <h4 style="color: #2563eb; margin: 0 0 12px 0; font-size: 22px;">📚 Неизученные задания</h4>
            """, unsafe_allow_html=True)

            for num in not_studied_tasks[:5]:
                st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #3b82f6; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                        <span style="background: #3b82f6; color: white; border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px;">{num}</span>
                        <span style="font-weight: 600; color: #2563eb; font-size: 18px;">🚀 Новое</span>
                    </div>
                    <p style="font-size: 16px; line-height: 1.6; color: #1f2937; margin: 8px 0; font-style: italic;">
                        📖 «Каждое новое задание — это возможность пополнить свой арсенал знаний. 
                        Начни с задания {num}, изучи тему и попробуй решить. Ты обязательно сможешь! 🚀»
                    </p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        total_studied = studied_count
        total_all = total_tasks

        if total_studied == total_all:
            stage_message = random.choice([
                "🎊 Ты изучил все задания! Теперь задача — довести каждый результат до максимума!",
                "🏆 Отличная работа! Все задания изучены. Теперь твой фокус — на совершенствование!",
                "🚀 Ты прошёл все задания! Время шлифовать мастерство!"
            ])
        elif total_studied / total_all >= 0.8:
            stage_message = random.choice([
                "💪 Ты почти изучил все задания! Осталось совсем немного. Продолжай в том же духе!",
                "🌟 Отличный прогресс! Бóльшая часть заданий уже освоена. Ты на верном пути!",
                "🎯 Ты на финишной прямой! Остались последние шаги!"
            ])
        elif total_studied / total_all >= 0.5:
            stage_message = random.choice([
                "📈 Половина пути пройдена! Ты уже многое освоил. Продолжай двигаться вперёд!",
                "🌱 Твой прогресс впечатляет! Ты освоил половину заданий. Так держать!",
                "🔥 Ты в самом разгаре пути! Помни: дорогу осилит идущий!"
            ])
        else:
            stage_message = random.choice([
                "🚀 Путь начинается с первого шага! Ты уже сделал этот шаг. Продолжай!",
                "💫 Начало положено! Ты только начинаешь, но это самое важное. Вперёд!",
                "🌟 Ты уже в деле! Каждое изученное задание — это твоя победа!"
            ])

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #dbeafe, #e0e7ff); border-radius: 16px; padding: 24px; border: 1px solid #bae6fd; text-align: center;">
                <div style="font-size: 48px; margin-bottom: 8px;">🎯</div>
                <h4 style="color: #1f2937; margin: 0 0 8px 0; font-size: 20px;">Твой прогресс: {total_studied}/{total_all} заданий</h4>
                <div class="status-bar" style="max-width: 300px; margin: 8px auto;">
                    <div class="status-bar-fill" style="width: {(total_studied/total_all*100) if total_all > 0 else 0}%; background: linear-gradient(90deg, #3b82f6, #8b5cf6);"></div>
                </div>
                <p style="font-size: 18px; line-height: 1.6; color: #1f2937; margin: 12px 0 0 0; font-style: italic;">
                    {stage_message}
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ==================== TAB 4: СРАВНЕНИЕ ====================
    with tab4:
        st.markdown('<h3 style="color: #1f2937;">🏅 Сравнение с классом</h3>', unsafe_allow_html=True)

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

            colors_scores = ['#3b82f6' if name == selected_student else '#9ca3af' for name, _ in all_scores]

            fig_rank = go.Figure()

            fig_rank.add_trace(go.Bar(
                x=[name for name, _ in all_scores],
                y=[score for _, score in all_scores],
                marker_color=colors_scores,
                text=[f'{score:.0f}' for _, score in all_scores],
                textposition='outside'
            ))

            fig_rank.update_layout(
                height=max(400, len(all_scores) * 30),
                xaxis=dict(title=dict(text="Ученик", font=dict(size=14)),
                          tickfont=dict(size=11), tickangle=-45),
                yaxis=dict(title=dict(text="Прогнозируемый балл", font=dict(size=14)),
                          range=[0, max(100, max([s for _, s in all_scores]) + 10)],
                          tickfont=dict(size=12)),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False, dragmode=False,
                modebar=dict(remove=['zoomIn2d', 'zoomOut2d', 'pan2d', 'resetScale2d', 'autoScale2d'])
            )

            st.plotly_chart(fig_rank, use_container_width=True, config=config)

            col1, col2, col3, col4 = st.columns(4)

            current_score = next((s for n, s in all_scores if n == selected_student), 0)
            max_score = max([s for _, s in all_scores]) if all_scores else 0
            avg_score = sum([s for _, s in all_scores]) / len(all_scores) if all_scores else 0
            min_score = min([s for _, s in all_scores]) if all_scores else 0

            with col1:
                st.markdown(f"""
                <div class="card">
                    <div class="card-title">📊 Ваш прогноз</div>
                    <div class="card-value">{current_score:.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="card">
                    <div class="card-title">🏆 Лучший прогноз</div>
                    <div class="card-value">{max_score:.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="card">
                    <div class="card-title">📈 Средний прогноз</div>
                    <div class="card-value">{avg_score:.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class="card">
                    <div class="card-title">📉 Худший прогноз</div>
                    <div class="card-value">{min_score:.0f}</div>
                </div>
                """, unsafe_allow_html=True)

            rank = next((i+1 for i, (n, _) in enumerate(all_scores) if n == selected_student), None)
            total = len(all_scores)
            
            students_below = total - rank if rank else 0
            other_students = total - 1
            percentile = (students_below / other_students * 100) if other_students > 0 else 100

            st.markdown(f"""
            <div class="card" style="margin-top: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <h4 style="margin: 0; color: #6b7280;">Ваша позиция</h4>
                        <p style="font-size: 28px; font-weight: bold; margin: 4px 0; color: #1f2937;">#{rank} из {total}</p>
                    </div>
                    <div style="text-align: right;">
                        <h4 style="margin: 0; color: #6b7280;">Выше чем</h4>
                        <p style="font-size: 28px; font-weight: bold; color: #3b82f6; margin: 4px 0;">{percentile:.0f}%</p>
                    </div>
                </div>
                <div class="status-bar">
                    <div class="status-bar-fill" style="width: {percentile}%; background: linear-gradient(90deg, #3b82f6, #8b5cf6);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Нет данных для сравнения")
