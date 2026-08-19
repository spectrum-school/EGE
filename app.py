import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import io
import numpy as np
from datetime import datetime
import hashlib
import base64

st.set_page_config(page_title="Прогресс ЕГЭ", layout="wide")

# CSS для светлой темы и стилей уровня
st.markdown("""
<style>
    /* Принудительно светлая тема для всех элементов */
    .stApp, .stApp > div, .main, .block-container,
    .element-container, .stMarkdown, .stTabs,
    div[data-testid="stTabs"], .stSidebar,
    .stSidebar .stMarkdown, .stSelectbox,
    .stButton, .stAlert, .stDataFrame,
    [data-testid="stMetric"] {
        background-color: #f8f9fa !important;
        color: #1f2937 !important;
    }
    
    /* Принудительно светлая тема для карточек */
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
        display: flex;
        align-items: center;
        gap: 8px;
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
    
    /* Стили для уровня успеваемости с цветовой градацией */
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
    
    .level-excellent {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }
    
    .level-good {
        background: linear-gradient(135deg, #34d399, #059669) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(52, 211, 153, 0.3);
    }
    
    .level-medium {
        background: linear-gradient(135deg, #fbbf24, #f59e0b) !important;
        color: #1f2937 !important;
        box-shadow: 0 2px 8px rgba(251, 191, 36, 0.3);
    }
    
    .level-low {
        background: linear-gradient(135deg, #f87171, #dc2626) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(248, 113, 113, 0.3);
    }
    
    .level-icon {
        font-size: 32px !important;
        margin-right: 10px;
    }
    
    /* Увеличенный шрифт для уровня */
    .level-text {
        font-size: 28px !important;
        font-weight: bold !important;
    }
    
    /* Статус-бары */
    .status-bar {
        height: 8px;
        border-radius: 4px;
        background: #e5e7eb;
        margin: 8px 0;
        overflow: hidden;
    }
    
    .status-bar-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.6s ease;
    }
    
    /* Стили для рекомендаций */
    .rec-warning {
        background: #ffffff !important;
        border-left: 4px solid #ef4444;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 16px;
        border: 1px solid #e5e7eb !important;
    }
    
    .rec-info {
        background: #ffffff !important;
        border-left: 4px solid #3b82f6;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 16px;
        border: 1px solid #e5e7eb !important;
    }
    
    .rec-improve {
        background: #ffffff !important;
        border-left: 4px solid #f59e0b;
        padding: 16px;
        border-radius: 8px;
        margin-top: 16px;
        border: 1px solid #e5e7eb !important;
    }
    
    .rec-title {
        color: #1f2937 !important;
        margin: 0 0 8px 0;
    }
    
    .rec-text {
        color: #6b7280 !important;
        font-size: 14px;
        margin-top: -4px;
    }
    
    /* Стили для заголовков и текста */
    h1, h2, h3, h4, h5, h6 {
        color: #1f2937 !important;
    }
    
    p, div, span, label {
        color: #1f2937 !important;
    }
    
    /* Стили для таблиц */
    .stDataFrame table {
        color: #1f2937 !important;
    }
    
    .stDataFrame thead tr th {
        background-color: #f3f4f6 !important;
        color: #1f2937 !important;
    }
    
    .stDataFrame tbody tr td {
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    .stDataFrame tbody tr:hover td {
        background-color: #f3f4f6 !important;
    }
    
    /* Стили для боковой панели */
    .stSidebar {
        background-color: #f8f9fa !important;
        border-right: 1px solid #e5e7eb !important;
    }
    
    .stSidebar h1, .stSidebar h2, .stSidebar h3,
    .stSidebar p, .stSidebar div {
        color: #1f2937 !important;
    }
    
    /* Стили для selectbox */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border-color: #e5e7eb !important;
    }
    
    .stSelectbox div[data-baseweb="select"] input {
        color: #1f2937 !important;
    }
    
    /* Стили для кнопок */
    .stButton button {
        background-color: #ffffff !important;
        border-color: #e5e7eb !important;
        color: #1f2937 !important;
    }
    
    .stButton button:hover {
        background-color: #f3f4f6 !important;
    }
    
    /* Стили для метрик */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #1f2937 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #6b7280 !important;
    }
    
    /* Стили для вкладок */
    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa !important;
        color: #6b7280 !important;
        border-color: #e5e7eb !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #ffffff !important;
        color: #1f2937 !important;
        border-bottom: 2px solid #3b82f6 !important;
    }
    
    /* Стили для прогресс-баров */
    .stProgress > div > div {
        background-color: #e5e7eb !important;
    }
    
    .stAlert {
        background-color: #ffffff !important;
        border-color: #e5e7eb !important;
        color: #1f2937 !important;
    }
    
    /* Адаптивность */
    @media only screen and (max-width: 768px) {
        .card {
            padding: 16px;
            margin-bottom: 12px;
        }
        
        .card-value {
            font-size: 28px;
        }
        
        .card-title {
            font-size: 16px;
        }
        
        .level-container {
            font-size: 20px !important;
            padding: 6px 16px;
            min-width: 150px;
        }
        
        .level-text {
            font-size: 20px !important;
        }
        
        .level-icon {
            font-size: 24px !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 14px;
            padding: 8px 12px;
        }
    }
    
    @media only screen and (max-width: 480px) {
        .card {
            padding: 12px;
        }
        
        .card-value {
            font-size: 24px;
        }
        
        .card-title {
            font-size: 14px;
        }
        
        .level-container {
            font-size: 16px !important;
            padding: 4px 12px;
            min-width: 120px;
        }
        
        .level-text {
            font-size: 16px !important;
        }
        
        .level-icon {
            font-size: 20px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ID вашей таблицы
SHEET_ID = "1GkNVYBZqLkZPEEnRbB2CZKzsFb5ZrkKfjs4pMObD-YY"

# Функции загрузки
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
        if 0 <= val <= 100:
            return 'studied'
        return 'invalid'
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
    if score >= 80: 
        return "Отлично", "🌟", "level-excellent"
    elif score >= 60: 
        return "Хорошо", "👍", "level-good"
    elif score >= 40: 
        return "Средне", "📊", "level-medium"
    else: 
        return "Требует внимания", "⚠️", "level-low"

# Загрузка данных
st.sidebar.title("🎓 Панель")
if st.sidebar.button("🔄 Обновить"):
    st.cache_data.clear()
    st.rerun()

students_df = load_sheet("Ученики")
tasks_df = load_sheet("Задания")

if students_df.empty:
    students_df = load_sheet("Sheet1")
if tasks_df.empty:
    tasks_df = load_sheet("Sheet2")

if students_df.empty or tasks_df.empty:
    st.error("❌ Не удалось загрузить данные")
    st.stop()

# Определяем колонки
student_id_col = 'id' if 'id' in students_df.columns else students_df.columns[0]
student_name_col = 'ФИО' if 'ФИО' in students_df.columns else students_df.columns[1]

task_id_col = 'id' if 'id' in tasks_df.columns else tasks_df.columns[0]
task_cols = [c for c in tasks_df.columns if c != task_id_col and c != 'date']

# Получаем список учеников
students_list = students_df[student_name_col].tolist()

# ==================== СИСТЕМА АУТЕНТИФИКАЦИИ ====================

# Инициализация session_state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.current_user = None

# Функция для входа
def login(student_name):
    if student_name in students_list:
        st.session_state.authenticated = True
        st.session_state.current_user = student_name
        return True
    return False

# Функция для выхода
def logout():
    st.session_state.authenticated = False
    st.session_state.current_user = None
    st.rerun()

# Проверяем сохранённый логин из cookies (через параметры URL)
query_params = st.query_params
saved_user = query_params.get('user', None)
if saved_user and not st.session_state.authenticated:
    try:
        decoded = base64.b64decode(saved_user.encode()).decode()
        if decoded in students_list:
            login(decoded)
            st.query_params.clear()
            st.rerun()
    except:
        pass

# ==================== СТРАНИЦА ВХОДА ====================

if not st.session_state.authenticated:
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px;">
        <h1 style="font-size: 48px; margin-bottom: 20px;">📊 Прогресс ЕГЭ</h1>
        <p style="font-size: 20px; color: #6b7280; margin-bottom: 30px;">
            Введите ФИО ученика для доступа к данным
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.markdown("### 🔑 Вход в систему")
        
        student_search = st.text_input(
            "Введите ФИО ученика",
            placeholder="Например: Иванов Иван Иванович",
            help="Введите полное ФИО ученика, как в списке"
        )
        
        remember_me = st.checkbox("Запомнить меня на этом устройстве", value=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button("🔓 Войти", use_container_width=True)
        
        if submitted and student_search:
            if student_search in students_list:
                login(student_search)
                if remember_me:
                    encoded = base64.b64encode(student_search.encode()).decode()
                    st.query_params.user = encoded
                st.rerun()
            else:
                similar = [s for s in students_list if student_search.lower() in s.lower()]
                if similar:
                    st.warning(f"❌ Ученик не найден. Возможно, вы имели в виду:\n" + "\n".join(f"- {s}" for s in similar[:3]))
                else:
                    st.error("❌ Ученик с таким ФИО не найден. Проверьте правильность ввода.")
        elif submitted:
            st.warning("⚠️ Введите ФИО ученика")
    
    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-top: 20px;">
        <p style="margin: 0; color: #6b7280;">
            💡 <b>Подсказка:</b> Введите полное ФИО ученика (например: Иванов Иван Иванович). 
            ФИО должно точно совпадать с указанным в списке.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# ==================== ОСНОВНАЯ СТРАНИЦА (ДЛЯ АВТОРИЗОВАННЫХ) ====================

selected_student = st.session_state.current_user

# Кнопка выхода в боковой панели
st.sidebar.markdown("---")
st.sidebar.markdown(f"👤 **{selected_student}**")
if st.sidebar.button("🚪 Выйти"):
    if 'user' in st.query_params:
        del st.query_params.user
    logout()

# Получаем данные ученика
student_row = students_df[students_df[student_name_col] == selected_student]
if student_row.empty:
    st.error("Ученик не найден. Возможно, данные были изменены.")
    logout()
    st.stop()

student_id = student_row[student_id_col].iloc[0]

# Целевой балл
target_score = None
if 'Целевой балл' in students_df.columns:
    try:
        target_score = float(student_row['Целевой балл'].iloc[0])
    except:
        pass

# Загрузка данных ученика
student_tasks = tasks_df[tasks_df[task_id_col] == student_id].sort_values('date')

if student_tasks.empty:
    st.warning(f"Нет данных для {selected_student}")
    st.stop()

# Последние данные
latest = student_tasks.iloc[-1]
previous = student_tasks.iloc[-2] if len(student_tasks) > 1 else None
all_dates = student_tasks['date'].tolist()

# Анализ заданий
probabilities = []
task_numbers = []
task_statuses = []
task_weights = []

for col in task_cols:
    num = col.replace('task_', '').replace('задание', '').replace('_', '')
    value = latest[col]
    status = get_task_status(value)
    
    task_num_int = int(num) if num.isdigit() else 0
    weight = 2 if task_num_int in [26, 27] else 1
    
    if status == 'studied':
        probabilities.append(float(value))
        task_numbers.append(num)
        task_statuses.append('studied')
        task_weights.append(weight)
    elif status == 'not_studied':
        probabilities.append(0)
        task_numbers.append(num)
        task_statuses.append('not_studied')
        task_weights.append(weight)

# Расчёт баллов
primary_score = sum((p/100) * w for p, w in zip(probabilities, task_weights))
primary_rounded = round(primary_score)
secondary_score = convert_to_secondary(primary_rounded)

# Предыдущий расчёт
prev_secondary = None
if previous is not None:
    prev_probs = []
    prev_weights = []
    for col in task_cols:
        num = col.replace('task_', '').replace('задание', '').replace('_', '')
        value = previous[col]
        status = get_task_status(value)
        task_num_int = int(num) if num.isdigit() else 0
        weight = 2 if task_num_int in [26, 27] else 1
        if status == 'studied':
            prev_probs.append(float(value))
            prev_weights.append(weight)
        elif status == 'not_studied':
            prev_probs.append(0)
            prev_weights.append(weight)
    if prev_probs:
        prev_primary = sum((p/100) * w for p, w in zip(prev_probs, prev_weights))
        prev_secondary = convert_to_secondary(round(prev_primary))

# Статистика
studied_count = sum(1 for s in task_statuses if s == 'studied')
total_tasks = len(probabilities)
max_primary = sum(task_weights)
progress_percent = (studied_count / total_tasks * 100) if total_tasks > 0 else 0

# Уровень успеваемости с цветом
level_text, level_icon, level_class = get_score_level(secondary_score)

# ==================== ОСНОВНАЯ СТРАНИЦА ====================

# Заголовок с цветным уровнем
st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
    <div>
        <h1 style="margin: 0; color: #1f2937;">📊 {selected_student}</h1>
        <p style="color: #9ca3af; font-size: 14px; margin: 4px 0 0 0;">
            📅 {all_dates[-1] if all_dates else 'Нет данных'}
        </p>
    </div>
    <div class="level-container {level_class}">
        <span class="level-icon">{level_icon}</span>
        <span class="level-text">{level_text}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==================== ВЕРХНИЕ МЕТРИКИ ====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    delta_html = ""
    if prev_secondary:
        delta = secondary_score - prev_secondary
        color = "green" if delta > 0 else "red" if delta < 0 else "gray"
        delta_html = f'<div style="color: {color}; font-size: 16px;">{delta:+.0f} баллов</div>'
    
    st.markdown(f"""
    <div class="card">
        <div class="card-title">🎯 Текущий балл</div>
        <div class="card-value">{secondary_score}</div>
        <div class="card-sub">{primary_rounded} первичных</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

with col2:
    if target_score:
        diff = secondary_score - target_score
        color = "green" if diff >= 0 else "red"
        status = "✅ Достигнут" if diff >= 0 else "⬆️ Осталось"
        
        st.markdown(f"""
        <div class="card">
            <div class="card-title">🎯 Целевой балл</div>
            <div class="card-value">{target_score:.0f}</div>
            <div class="card-sub" style="color: {color};">{diff:+.0f} баллов</div>
            <div style="font-size: 14px; color: #9ca3af;">{status}</div>
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
        <div class="card-title">📚 Прогресс</div>
        <div class="card-value">{studied_count}/{total_tasks}</div>
        <div class="card-sub">{progress_percent:.0f}% заданий изучено</div>
        <div class="status-bar">
            <div class="status-bar-fill" style="width: {progress_percent}%; background: #3b82f6;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    # Рейтинг среди учеников
    all_students_scores = []
    for _, row in students_df.iterrows():
        sid = row[student_id_col]
        s_tasks = tasks_df[tasks_df[task_id_col] == sid]
        if not s_tasks.empty:
            s_latest = s_tasks.iloc[-1]
            s_probs = []
            s_weights = []
            for col in task_cols:
                num = col.replace('task_', '').replace('задание', '').replace('_', '')
                val = s_latest[col]
                status = get_task_status(val)
                task_num_int = int(num) if num.isdigit() else 0
                weight = 2 if task_num_int in [26, 27] else 1
                if status == 'studied':
                    s_probs.append(float(val))
                    s_weights.append(weight)
                elif status == 'not_studied':
                    s_probs.append(0)
                    s_weights.append(weight)
            if s_probs:
                s_primary = sum((p/100) * w for p, w in zip(s_probs, s_weights))
                s_secondary = convert_to_secondary(round(s_primary))
                all_students_scores.append((row[student_name_col], s_secondary))
    
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

# ==================== ВКЛАДКИ ====================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Успеваемость", 
    "📈 Прогресс", 
    "🎯 Рекомендации",
    "🏅 Сравнение"
])

# ==================== TAB 1: УСПЕВАЕМОСТЬ ====================
with tab1:
    st.markdown('<h3 style="margin-bottom: 12px; color: #1f2937;">🗺 Карта знаний</h3>', unsafe_allow_html=True)
    
    colors = []
    labels = []
    for prob, status in zip(probabilities, task_statuses):
        if status == 'not_studied':
            colors.append('#e5e7eb')
            labels.append('—')
        elif prob >= 80:
            colors.append('#10b981')
            labels.append(f'{prob:.0f}%')
        elif prob >= 60:
            colors.append('#34d399')
            labels.append(f'{prob:.0f}%')
        elif prob >= 40:
            colors.append('#fbbf24')
            labels.append(f'{prob:.0f}%')
        elif prob >= 20:
            colors.append('#fb923c')
            labels.append(f'{prob:.0f}%')
        else:
            colors.append('#f87171')
            labels.append(f'{prob:.0f}%')
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=task_numbers,
        y=[1] * len(task_numbers),
        marker_color=colors,
        text=labels,
        textposition='auto',
        textfont=dict(size=14, color='black'),
        showlegend=False,
        width=0.8
    ))
    
    fig.update_layout(
        height=200,
        xaxis=dict(
            title=dict(text="Номер задания", font=dict(size=16)),
            tickfont=dict(size=14),
            tickmode='linear',
            tick0=1,
            dtick=1
        ),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=40),
        dragmode=False,
        modebar=dict(
            remove=['zoomIn2d', 'zoomOut2d', 'pan2d', 'resetScale2d', 'autoScale2d']
        )
    )
    
    config = {
        'displayModeBar': True,
        'modeBarButtonsToRemove': ['zoomIn2d', 'zoomOut2d', 'pan2d', 'resetScale2d', 'autoScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian'],
        'displaylogo': False,
        'scrollZoom': False
    }
    
    st.plotly_chart(fig, width='stretch', config=config)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("🟩 **80-100%** — отлично")
    with col2:
        st.markdown("🟨 **60-79%** — хорошо")
    with col3:
        st.markdown("🟧 **40-59%** — средне")
    with col4:
        st.markdown("🟥 **0-39%** — слабо")
    with col5:
        st.markdown("⬜ **—** — не изучалось")
    
    st.markdown("---")
    
    st.markdown('<h3 style="color: #1f2937;">📋 Детальная информация</h3>', unsafe_allow_html=True)
    
    details_data = []
    for num, prob, status, weight in zip(task_numbers, probabilities, task_statuses, task_weights):
        status_text = "✅ Изучено" if status == 'studied' else "⏳ Не изучалось"
        details_data.append({
            "Задание": f"№{num}",
            "Вес": weight,
            "Прогресс": f"{prob:.0f}%" if status == 'studied' else "—",
            "Статус": status_text
        })
    
    df_details = pd.DataFrame(details_data)
    st.dataframe(df_details, width='stretch', hide_index=True)

# ==================== TAB 2: ПРОГРЕСС ====================
with tab2:
    st.markdown('<h3 style="color: #1f2937;">📈 Динамика обучения</h3>', unsafe_allow_html=True)
    
    if len(student_tasks) > 1:
        dates = []
        scores = []
        primaries = []
        
        for idx, (_, row) in enumerate(student_tasks.iterrows()):
            probs = []
            weights = []
            for col in task_cols:
                num = col.replace('task_', '').replace('задание', '').replace('_', '')
                val = row[col]
                status = get_task_status(val)
                task_num_int = int(num) if num.isdigit() else 0
                weight = 2 if task_num_int in [26, 27] else 1
                if status == 'studied':
                    probs.append(float(val))
                    weights.append(weight)
                elif status == 'not_studied':
                    probs.append(0)
                    weights.append(weight)
            
            if probs:
                primary = sum((p/100) * w for p, w in zip(probs, weights))
                secondary = convert_to_secondary(round(primary))
                dates.append(row['date'])
                scores.append(secondary)
                primaries.append(round(primary))
        
        if len(dates) > 1:
            fig_progress = go.Figure()
            
            fig_progress.add_trace(go.Scatter(
                x=dates,
                y=scores,
                mode='lines+markers',
                name='Тестовый балл',
                line=dict(color='#3b82f6', width=3),
                marker=dict(size=8, color='#3b82f6')
            ))
            
            if target_score:
                fig_progress.add_hline(
                    y=target_score, 
                    line_dash="dash", 
                    line_color="#ef4444",
                    annotation_text=f"Цель: {target_score:.0f}",
                    annotation_position="top right"
                )
            
            fig_progress.update_layout(
                height=400,
                xaxis=dict(
                    title=dict(text="Дата", font=dict(size=14)),
                    tickfont=dict(size=12)
                ),
                yaxis=dict(
                    title=dict(text="Тестовый балл", font=dict(size=14)),
                    range=[0, max(100, max(scores) + 10)],
                    tickfont=dict(size=12)
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified',
                legend=dict(font=dict(size=12)),
                dragmode=False,
                modebar=dict(
                    remove=['zoomIn2d', 'zoomOut2d', 'pan2d', 'resetScale2d', 'autoScale2d']
                )
            )
            
            config = {
                'displayModeBar': True,
                'modeBarButtonsToRemove': ['zoomIn2d', 'zoomOut2d', 'pan2d', 'resetScale2d', 'autoScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian'],
                'displaylogo': False,
                'scrollZoom': False
            }
            
            st.plotly_chart(fig_progress, width='stretch', config=config)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                progress_delta = scores[-1] - scores[0] if len(scores) > 1 else 0
                color = "green" if progress_delta > 0 else "red" if progress_delta < 0 else "gray"
                st.markdown(f"""
                <div class="card">
                    <div class="card-title">📊 Общий прогресс</div>
                    <div class="card-value" style="color: {color};">{progress_delta:+.0f}</div>
                    <div class="card-sub">баллов</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                best_score = max(scores) if scores else 0
                st.markdown(f"""
                <div class="card">
                    <div class="card-title">🏆 Лучший результат</div>
                    <div class="card-value">{best_score}</div>
                    <div class="card-sub">баллов</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                last_change = scores[-1] - scores[-2] if len(scores) > 1 else 0
                color = "green" if last_change > 0 else "red" if last_change < 0 else "gray"
                st.markdown(f"""
                <div class="card">
                    <div class="card-title">📈 Последнее изменение</div>
                    <div class="card-value" style="color: {color};">{last_change:+.0f}</div>
                    <div class="card-sub">баллов</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Недостаточно данных для отображения прогресса")
    else:
        st.info("Добавьте больше записей для отслеживания прогресса")

# ==================== TAB 3: РЕКОМЕНДАЦИИ ====================
with tab3:
    st.markdown('<h3 style="color: #1f2937;">🎯 Персональные рекомендации</h3>', unsafe_allow_html=True)
    
    # Определяем слабые, средние и сильные задания
    weak_tasks = [
        (num, prob) for num, prob, status in zip(task_numbers, probabilities, task_statuses)
        if status == 'studied' and prob < 40
    ]
    
    medium_tasks = [
        (num, prob) for num, prob, status in zip(task_numbers, probabilities, task_statuses)
        if status == 'studied' and 40 <= prob < 70
    ]
    
    strong_tasks = [
        (num, prob) for num, prob, status in zip(task_numbers, probabilities, task_statuses)
        if status == 'studied' and prob >= 70
    ]
    
    not_studied = [
        num for num, status in zip(task_numbers, task_statuses)
        if status == 'not_studied'
    ]
    
    # ==================== МОТИВИРУЮЩИЕ СООБЩЕНИЯ ====================
    
    import random
    from datetime import datetime
    
    # Банк мотивирующих сообщений для разных ситуаций
    motivation_messages = {
        'weak': [
            "💪 «Ты уже сделал первый шаг — начал решать! Осталось совсем немного, чтобы закрепить успех. Задание {num} — отличная возможность показать, на что ты способен. Давай, ты справишься!»",
            "🚀 «Знаешь, что общего у всех великих? Они не боялись ошибаться на пути к успеху! Задание {num} — твой следующий рубеж. Ты уже близко к прорыву!»",
            "🌟 «Каждое задание — это кирпичик в твоём фундаменте знаний. Задание {num} ждёт тебя, чтобы стать ещё одним прочным кирпичом. Ты можешь больше, чем думаешь!»",
            "🔥 «Твой прогресс виден невооружённым глазом! Задание {num} — идеальный кандидат для улучшения. Представь, как возрастёт твой балл, когда ты его освоишь!»",
            "🎯 «Помни: чем сложнее задание, тем слаще победа! Задание {num} — твой персональный вызов. Прими его и докажи себе, что ты способен на большее!»",
            "⚡ «Знаешь, как прокачивают мышцы? Через преодоление! Задание {num} — это твой тренажёр для мозга. Поработай над ним — и результат не заставит себя ждать!»",
            "🏆 «Победители не те, кто никогда не падает, а те, кто всегда поднимается. Задание {num} — твой шанс подняться ещё выше! Ты уже на правильном пути.»",
            "💫 «Каждое новое задание — это шаг к мечте. Задание {num} приближает тебя к цели быстрее, чем ты думаешь. Не останавливайся на достигнутом!»",
            "🌈 «Ты уже столько всего освоил! Задание {num} — это просто следующий уровень. Ты точно сможешь его пройти, ведь у тебя всё получается!»",
            "🎖️ «Настоящий герой не боится трудностей. Задание {num} — твой шанс проявить характер и показать, на что ты способен. Вперёд, к победе!»"
        ],
        'medium': [
            "🎉 «Ты уже хорошо справляешься! Задание {num} — отличная возможность закрепить успех и перейти на новый уровень. Ты на правильном пути!»",
            "📈 «Прогресс очевиден! Задание {num} — это та вершина, которую осталось чуть-чуть покорить. Ещё немного — и ты будешь на высоте!»",
            "⭐ «Ты уже почти там! Задание {num} требует всего лишь небольшого усилия, чтобы стать твоим сильным местом. Давай, финишная прямая!»",
            "🌱 «Твой рост вдохновляет! Задание {num} — это следующая ступенька на пути к совершенству. Ты уже заложил отличную основу, теперь осталось доделать!»",
            "✨ «У тебя есть все шансы сделать это задание идеальным! {num} — твой шанс блеснуть. Ты уже знаешь почти всё, осталось лишь отточить мастерство!»"
        ],
        'strong': [
            "🏅 «Ты настоящий мастер! Задание {num} ты освоил на отлично. Почему бы не помочь другим или не усложнить себе задачу? Ты готов к новым свершениям!»",
            "🌟 «Твой результат по заданию {num} впечатляет! Ты доказал, что способен на многое. Продолжай в том же духе — ты на верном пути к сотне!»",
            "🎯 «Ты уже профи в задании {num}! Так держать! Твои успехи вдохновляют окружающих. Осталось совсем немного до абсолютного совершенства!»"
        ],
        'all_done': [
            "🎊 «Поздравляю! Ты прошёл все задания! Ты — настоящий герой своего обучения. Твой упорство и труд принесли плоды. Гордись собой!»",
            "🏆 «Удивительно! Ты освоил все задания. Ты — пример для подражания! Твоя целеустремлённость заслуживает самых высоких похвал!»",
            "🚀 «Ты сделал это! Все задания позади. Теперь ты готов к любым вызовам. Помни: с таким подходом ты покоришь любые вершины!»"
        ],
        'no_weak': [
            "💪 «Отлично! У тебя нет слабых мест — все задания на хорошем уровне. Теперь твоя задача — превратить хорошие результаты в идеальные. Ты сможешь!»",
            "🌟 «Твой результат впечатляет! Все задания освоены на достойном уровне. Теперь пора поднимать планку ещё выше. Ты готов к новому уровню!»",
            "🎯 «Ты уже достиг отличных результатов по всем заданиям! Это говорит о твоей целеустремлённости. Продолжай в том же духе — и сотня будет твоей!»"
        ],
        'weak_improvement': [
            "📈 «Отличный прогресс! Ты уже начал улучшать свои результаты. Помни: даже маленький шаг вперёд — это уже победа. Продолжай двигаться!»",
            "🔥 «Ты на правильном пути! С каждым разом ты становишься лучше. Не сбавляй обороты — у тебя всё получится!»"
        ]
    }
    
    # Функция для получения мотивирующего сообщения с уникальностью
    def get_motivation_message(task_num, category, used_messages, prob=None):
        messages = motivation_messages.get(category, motivation_messages['weak'])
        
        # Фильтруем уже использованные сообщения
        available = [m for m in messages if m not in used_messages]
        
        if not available:
            # Если все сообщения использованы, берём из резерва
            available = messages.copy()
            used_messages.clear()
        
        # Выбираем случайное сообщение
        msg_template = random.choice(available)
        used_messages.add(msg_template)
        
        # Форматируем с номером задания
        return msg_template.format(num=task_num), used_messages
    
    # Отображаем рекомендации
    st.markdown("""
    <div style="background: linear-gradient(135deg, #e0f2fe, #dbeafe); padding: 20px; border-radius: 16px; margin-bottom: 20px; border: 1px solid #bae6fd;">
        <p style="font-size: 22px; font-weight: 600; margin: 0; color: #1f2937; text-align: center;">
            💡 «Успех — это не финальная точка, это путь, который ты проходишь каждый день. 
            Каждое решённое задание — шаг к твоей мечте!»
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Используем session_state для хранения использованных сообщений
    if 'used_messages' not in st.session_state:
        st.session_state.used_messages = set()
    
    # === 1. Слабые задания ===
    if weak_tasks:
        weak_sorted = sorted(weak_tasks, key=lambda x: x[1])[:3]
        
        st.markdown("""
        <div style="background: #fef2f2; border-radius: 16px; padding: 20px; border: 1px solid #fecaca; margin-bottom: 16px;">
            <h4 style="color: #dc2626; margin: 0 0 12px 0; font-size: 22px;">🔴 Зона роста</h4>
            <p style="color: #6b7280; margin-bottom: 12px; font-size: 16px;">
                Эти задания требуют твоего внимания. Но помни: именно преодоление трудностей делает нас сильнее!
            </p>
        """, unsafe_allow_html=True)
        
        for num, prob in weak_sorted:
            msg, st.session_state.used_messages = get_motivation_message(
                num, 'weak', st.session_state.used_messages, prob
            )
            
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #ef4444; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <span style="background: #ef4444; color: white; border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px;">{num}</span>
                    <span style="font-weight: 600; color: #dc2626; font-size: 18px;">{prob:.0f}%</span>
                    <span style="color: #9ca3af; font-size: 14px;">выполнено</span>
                </div>
                <div class="status-bar" style="margin: 8px 0 12px 0;">
                    <div class="status-bar-fill" style="width: {prob}%; background: linear-gradient(90deg, #ef4444, #f87171);"></div>
                </div>
                <p style="font-size: 16px; line-height: 1.6; color: #1f2937; margin: 0; font-style: italic;">
                    {msg}
                </p>
                <div style="margin-top: 8px; display: flex; gap: 8px; flex-wrap: wrap;">
                    <span style="background: #f3f4f6; color: #6b7280; font-size: 13px; padding: 3px 10px; border-radius: 12px;">📚 Повтори тему</span>
                    <span style="background: #f3f4f6; color: #6b7280; font-size: 13px; padding: 3px 10px; border-radius: 12px;">✍️ Реши 5 задач</span>
                    <span style="background: #f3f4f6; color: #6b7280; font-size: 13px; padding: 3px 10px; border-radius: 12px;">🎯 Цель: 80%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # === 2. Средние задания ===
    if medium_tasks:
        medium_sorted = sorted(medium_tasks, key=lambda x: x[1], reverse=True)[:2]
        
        st.markdown("""
        <div style="background: #fef3c7; border-radius: 16px; padding: 20px; border: 1px solid #fde68a; margin-bottom: 16px;">
            <h4 style="color: #d97706; margin: 0 0 12px 0; font-size: 22px;">⭐ Потенциал к росту</h4>
            <p style="color: #6b7280; margin-bottom: 12px; font-size: 16px;">
                Ты уже хорошо справляешься! Эти задания — отличная возможность для рывка вперёд.
            </p>
        """, unsafe_allow_html=True)
        
        for num, prob in medium_sorted:
            msg, st.session_state.used_messages = get_motivation_message(
                num, 'medium', st.session_state.used_messages, prob
            )
            
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #f59e0b; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <span style="background: #f59e0b; color: white; border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px;">{num}</span>
                    <span style="font-weight: 600; color: #d97706; font-size: 18px;">{prob:.0f}%</span>
                    <span style="color: #9ca3af; font-size: 14px;">выполнено</span>
                </div>
                <div class="status-bar" style="margin: 8px 0 12px 0;">
                    <div class="status-bar-fill" style="width: {prob}%; background: linear-gradient(90deg, #f59e0b, #fbbf24);"></div>
                </div>
                <p style="font-size: 16px; line-height: 1.6; color: #1f2937; margin: 0; font-style: italic;">
                    {msg}
                </p>
                <div style="margin-top: 8px; display: flex; gap: 8px; flex-wrap: wrap;">
                    <span style="background: #f3f4f6; color: #6b7280; font-size: 13px; padding: 3px 10px; border-radius: 12px;">📈 Закрепи материал</span>
                    <span style="background: #f3f4f6; color: #6b7280; font-size: 13px; padding: 3px 10px; border-radius: 12px;">✍️ Реши 3 задачи</span>
                    <span style="background: #f3f4f6; color: #6b7280; font-size: 13px; padding: 3px 10px; border-radius: 12px;">🎯 Цель: 90%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # === 3. Неизученные задания ===
    if not_studied:
        st.markdown("""
        <div style="background: #eff6ff; border-radius: 16px; padding: 20px; border: 1px solid #bfdbfe; margin-bottom: 16px;">
            <h4 style="color: #2563eb; margin: 0 0 12px 0; font-size: 22px;">📚 Неизученные задания</h4>
            <p style="color: #6b7280; margin-bottom: 12px; font-size: 16px;">
                Эти задания ждут тебя! Начни с самых простых и постепенно двигайся к сложным.
            </p>
        """, unsafe_allow_html=True)
        
        # Берём первые 5 неизученных
        not_studied_list = not_studied[:5]
        for num in not_studied_list:
            # Специальные сообщения для неизученных
            msg, st.session_state.used_messages = get_motivation_message(
                num, 'medium', st.session_state.used_messages
            )
            
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid #3b82f6; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <span style="background: #3b82f6; color: white; border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px;">{num}</span>
                    <span style="font-weight: 600; color: #2563eb; font-size: 18px;">🚀 Новое</span>
                    <span style="color: #9ca3af; font-size: 14px;">ждёт тебя</span>
                </div>
                <p style="font-size: 16px; line-height: 1.6; color: #1f2937; margin: 0; font-style: italic;">
                    «Каждое новое задание — это возможность открыть что-то удивительное! Задание {num} станет твоим следующим достижением. Ты готов? Вперёд!»
                </p>
                <div style="margin-top: 8px; display: flex; gap: 8px; flex-wrap: wrap;">
                    <span style="background: #f3f4f6; color: #6b7280; font-size: 13px; padding: 3px 10px; border-radius: 12px;">📖 Изучи теорию</span>
                    <span style="background: #f3f4f6; color: #6b7280; font-size: 13px; padding: 3px 10px; border-radius: 12px;">✍️ Попробуй решить</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if len(not_studied) > 5:
            st.markdown(f"""
            <div style="text-align: center; color: #6b7280; padding: 8px;">
                <span style="font-size: 14px;">... и ещё {len(not_studied) - 5} заданий ждут тебя! 🚀</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # === 4. Мотивирующий итог ===
    st.markdown("---")
    
    # Считаем прогресс
    total_studied = studied_count
    total_all = total_tasks
    
    # Определяем этап обучения
    if total_studied == total_all:
        stage_message = random.choice([
            "🎊 Ты покорил все вершины! Это невероятное достижение! Ты — пример для подражания. Помни: ты способен на всё, к чему приложишь усилия!",
            "🏆 Браво! Ты прошёл все задания. Твой путь был долгим, но ты справился! Теперь ты готов к самым сложным вызовам. Гордись собой!",
            "🚀 Удивительный результат! Все задания освоены. Ты показал характер и упорство. Теперь ты знаешь: ты способен на большее, чем думал!"
        ])
    elif total_studied / total_all >= 0.8:
        stage_message = random.choice([
            "💪 Ты почти у цели! Осталось совсем немного. Твой прогресс впечатляет! Продолжай в том же духе — ты на финишной прямой!",
            "🌟 Ты уже освоил бóльшую часть заданий! Это отличный результат. Ещё чуть-чуть — и ты будешь непобедим!",
            "🎯 Ты на финишной прямой! Остались последние шаги к совершенству. Твой упорство достойно уважения!"
        ])
    elif total_studied / total_all >= 0.5:
        stage_message = random.choice([
            "📈 Ты уже на полпути! Отличный темп. Продолжай двигаться вперёд, и ты обязательно достигнешь цели!",
            "🌱 Твой прогресс очевиден! Ты освоил половину заданий. Это важный этап на пути к успеху. Так держать!",
            "🔥 Ты в самом разгаре пути! Уже много сделано, но ещё больше ждёт впереди. Помни: дорогу осилит идущий!"
        ])
    else:
        stage_message = random.choice([
            "🚀 Путь начинается с первого шага! Ты уже сделал этот шаг. Каждое новое задание приближает тебя к цели. Не останавливайся!",
            "💫 Начало положено! Ты только начинаешь свой путь, но это самое важное. Помни: даже великие начинали с малого!",
            "🌟 Ты уже в деле! Каждое решённое задание — это твоя победа. Продолжай двигаться вперёд, и ты увидишь, на что способен!"
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
            s_latest = s_tasks.iloc[-1]
            s_probs = []
            s_weights = []
            for col in task_cols:
                num = col.replace('task_', '').replace('задание', '').replace('_', '')
                val = s_latest[col]
                status = get_task_status(val)
                task_num_int = int(num) if num.isdigit() else 0
                weight = 2 if task_num_int in [26, 27] else 1
                if status == 'studied':
                    s_probs.append(float(val))
                    s_weights.append(weight)
                elif status == 'not_studied':
                    s_probs.append(0)
                    s_weights.append(weight)
            
            if s_probs:
                s_primary = sum((p/100) * w for p, w in zip(s_probs, s_weights))
                s_secondary = convert_to_secondary(round(s_primary))
                all_scores.append((name, s_secondary))
    
    if all_scores:
        all_scores.sort(key=lambda x: x[1], reverse=True)
        df_ranking = pd.DataFrame(all_scores, columns=['Ученик', 'Балл'])
        
        colors_scores = ['#3b82f6' if name == selected_student else '#9ca3af' for name, _ in all_scores]
        
        fig_rank = go.Figure()
        
        fig_rank.add_trace(go.Bar(
            x=[name for name, _ in all_scores[:10]],
            y=[score for _, score in all_scores[:10]],
            marker_color=colors_scores[:10],
            text=[f'{score} баллов' for _, score in all_scores[:10]],
            textposition='outside'
        ))
        
        fig_rank.update_layout(
            height=400,
            xaxis=dict(
                title=dict(text="Ученик", font=dict(size=14)),
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title=dict(text="Тестовый балл", font=dict(size=14)),
                range=[0, max(100, max([s for _, s in all_scores]) + 10)],
                tickfont=dict(size=12)
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            dragmode=False,
            modebar=dict(
                remove=['zoomIn2d', 'zoomOut2d', 'pan2d', 'resetScale2d', 'autoScale2d']
            )
        )
        
        config = {
            'displayModeBar': True,
            'modeBarButtonsToRemove': ['zoomIn2d', 'zoomOut2d', 'pan2d', 'resetScale2d', 'autoScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian'],
            'displaylogo': False,
            'scrollZoom': False
        }
        
        st.plotly_chart(fig_rank, width='stretch', config=config)
        
        col1, col2, col3, col4 = st.columns(4)
        
        current_score = next((s for n, s in all_scores if n == selected_student), 0)
        max_score = max([s for _, s in all_scores]) if all_scores else 0
        avg_score = sum([s for _, s in all_scores]) / len(all_scores) if all_scores else 0
        min_score = min([s for _, s in all_scores]) if all_scores else 0
        
        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">📊 Ваш балл</div>
                <div class="card-value">{current_score:.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">🏆 Лучший</div>
                <div class="card-value">{max_score:.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">📈 Средний</div>
                <div class="card-value">{avg_score:.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">📉 Худший</div>
                <div class="card-value">{min_score:.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        rank = next((i+1 for i, (n, _) in enumerate(all_scores) if n == selected_student), None)
        total = len(all_scores)
        percentile = ((total - rank) / total * 100) if rank else 0
        
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
