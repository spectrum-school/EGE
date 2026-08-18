import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import io
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Прогресс ЕГЭ", layout="wide")

# CSS и JavaScript с localStorage
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
    if score >= 80: return "Отлично", "🌟"
    elif score >= 60: return "Хорошо", "👍"
    elif score >= 40: return "Средне", "📊"
    else: return "Требует внимания", "⚠️"

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

# ==================== РАБОТА С localStorage ====================

# Инициализация session_state
if 'selected_student' not in st.session_state:
    st.session_state.selected_student = None

# JavaScript для работы с localStorage (вставляем в HTML)
st.markdown("""
<script>
    // Функция для сохранения в localStorage
    function saveStudent(name) {
        try {
            localStorage.setItem('ege_selected_student', name);
            console.log('✅ Сохранён:', name);
            return true;
        } catch(e) {
            console.log('❌ Ошибка сохранения:', e);
            return false;
        }
    }
    
    // Функция для загрузки из localStorage
    function loadStudent() {
        try {
            const name = localStorage.getItem('ege_selected_student');
            console.log('📥 Загружен из localStorage:', name);
            return name;
        } catch(e) {
            console.log('❌ Ошибка загрузки:', e);
            return null;
        }
    }
    
    // При загрузке страницы отправляем сохранённое значение в Streamlit
    function sendSavedStudent() {
        const saved = loadStudent();
        if (saved) {
            // Создаём скрытый элемент для передачи данных
            const input = document.createElement('input');
            input.type = 'hidden';
            input.id = 'saved_student';
            input.value = saved;
            document.body.appendChild(input);
            
            // Отправляем событие
            const event = new CustomEvent('student_loaded', { 
                detail: { student: saved } 
            });
            document.dispatchEvent(event);
        }
    }
    
    // Выполняем при загрузке
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', sendSavedStudent);
    } else {
        sendSavedStudent();
    }
    
    // Функция для сохранения при выборе ученика
    window.saveSelectedStudent = function(name) {
        saveStudent(name);
        // Отправляем событие в Streamlit через URL параметр
        const url = new URL(window.location);
        url.searchParams.set('student', encodeURIComponent(name));
        window.history.replaceState({}, '', url);
        // Перезагружаем страницу для применения
        setTimeout(() => {
            window.location.reload();
        }, 200);
    };
</script>
""", unsafe_allow_html=True)

# Проверяем параметры URL для восстановления
query_params = st.query_params
saved_from_url = query_params.get('student', None)

# Проверяем session_state
if saved_from_url and saved_from_url in students_list:
    st.session_state.selected_student = saved_from_url
    st.query_params.clear()  # Очищаем параметры после использования

# Если в session_state ничего нет, берём первого
if st.session_state.selected_student is None or st.session_state.selected_student not in students_list:
    st.session_state.selected_student = students_list[0] if students_list else None

# ==================== ВЫБОР УЧЕНИКА ====================

st.sidebar.markdown("---")
st.sidebar.subheader("👤 Ученик")

# Определяем индекс для selectbox
try:
    current_index = students_list.index(st.session_state.selected_student)
except ValueError:
    current_index = 0
    st.session_state.selected_student = students_list[0] if students_list else None

selected_student = st.sidebar.selectbox(
    "Выберите ученика",
    students_list,
    index=current_index,
    label_visibility="collapsed"
)

# Если выбор изменился - сохраняем
if selected_student != st.session_state.selected_student:
    st.session_state.selected_student = selected_student
    # Сохраняем в localStorage через JavaScript с перезагрузкой
    st.markdown(f"""
    <script>
        try {{
            localStorage.setItem('ege_selected_student', '{selected_student}');
            console.log('✅ Сохранён ученик:', '{selected_student}');
            // Перезагружаем страницу с параметром
            const url = new URL(window.location);
            url.searchParams.set('student', encodeURIComponent('{selected_student}'));
            window.location.href = url.toString();
        }} catch(e) {{
            console.log('❌ Ошибка сохранения:', e);
        }}
    </script>
    """, unsafe_allow_html=True)

student_row = students_df[students_df[student_name_col] == selected_student]
if student_row.empty:
    st.error("Ученик не найден")
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

# Уровень успеваемости
level_text, level_icon = get_score_level(secondary_score)

# ==================== ОСНОВНАЯ СТРАНИЦА ====================

# Заголовок
st.markdown(f"""
<div>
    <h1 style="margin: 0; color: #1f2937;">{selected_student}</h1>
    <p style="color: #6b7280; margin: 0;">{level_icon} Уровень: {level_text}</p>
    <p style="color: #9ca3af; font-size: 14px; margin: 4px 0 0 0;">
        📅 {all_dates[-1] if all_dates else 'Нет данных'}
    </p>
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
    
    # Создаём цветную карту заданий
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
    
    st.plotly_chart(fig, use_container_width=True, config=config)
    
    # Легенда
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
    
    # Детальная таблица
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
    st.dataframe(df_details, use_container_width=True, hide_index=True)

# ==================== TAB 2: ПРОГРЕСС ====================
with tab2:
    st.markdown('<h3 style="color: #1f2937;">📈 Динамика обучения</h3>', unsafe_allow_html=True)
    
    if len(student_tasks) > 1:
        # График прогресса во времени
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
            
            st.plotly_chart(fig_progress, use_container_width=True, config=config)
            
            # Дополнительная статистика
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
    
    # 1. Слабые задания
    weak_tasks = [
        (num, prob) for num, prob, status in zip(task_numbers, probabilities, task_statuses)
        if status == 'studied' and prob < 60
    ]
    
    # 2. Неизученные задания
    not_studied = [
        num for num, status in zip(task_numbers, task_statuses)
        if status == 'not_studied'
    ]
    
    # 3. Задания для улучшения (близкие к следующему уровню)
    improving_tasks = [
        (num, prob) for num, prob, status in zip(task_numbers, probabilities, task_statuses)
        if status == 'studied' and 60 <= prob < 80
    ]
    
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        if weak_tasks:
            st.markdown("""
            <div class="rec-warning">
                <h4 style="color: #dc2626; margin: 0 0 8px 0;">🔴 Требуют внимания</h4>
            """, unsafe_allow_html=True)
            
            weak_sorted = sorted(weak_tasks, key=lambda x: x[1])[:5]
            for num, prob in weak_sorted:
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 4px 0;">
                    <span style="font-weight: 600; color: #1f2937;">Задание {num}</span>
                    <span style="color: #dc2626;">{prob:.0f}%</span>
                </div>
                <div class="status-bar">
                    <div class="status-bar-fill" style="width: {prob}%; background: #ef4444;"></div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"<p class='rec-text'>Рекомендуется повторить тему и решить дополнительные задачи</p>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.success("✅ Все изученные задания освоены на достаточном уровне!")
    
    with col_rec2:
        if not_studied:
            st.markdown("""
            <div class="rec-info">
                <h4 style="color: #2563eb; margin: 0 0 8px 0;">📚 Неизученные задания</h4>
            """, unsafe_allow_html=True)
            
            for num in not_studied[:5]:
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 4px 0;">
                    <span style="font-weight: 600; color: #1f2937;">Задание {num}</span>
                    <span style="color: #9ca3af;">⏳ Не начато</span>
                </div>
                """, unsafe_allow_html=True)
            
            if len(not_studied) > 5:
                st.markdown(f"<p style='color: #9ca3af;'>... и ещё {len(not_studied) - 5} заданий</p>", unsafe_allow_html=True)
            
            st.markdown("""
            <p class='rec-text'>💡 Рекомендуется начать с простых заданий и постепенно переходить к сложным</p>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.success("🎉 Все задания изучены!")
    
    # Задания для улучшения
    if improving_tasks:
        st.markdown("""
        <div class="rec-improve">
            <h4 style="color: #d97706; margin: 0 0 8px 0;">⭐ Задания для улучшения</h4>
        """, unsafe_allow_html=True)
        
        improving_sorted = sorted(improving_tasks, key=lambda x: x[1], reverse=True)[:5]
        for num, prob in improving_sorted:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 4px 0;">
                <span style="font-weight: 600; color: #1f2937;">Задание {num}</span>
                <span style="color: #d97706;">{prob:.0f}%</span>
            </div>
            <div class="status-bar">
                <div class="status-bar-fill" style="width: {prob}%; background: #f59e0b;"></div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"<p class='rec-text'>Цель: достичь 80% для отличного результата</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== TAB 4: СРАВНЕНИЕ ====================
with tab4:
    st.markdown('<h3 style="color: #1f2937;">🏅 Сравнение с классом</h3>', unsafe_allow_html=True)
    
    # Подготовка данных для сравнения
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
        
        # Определяем цвет для текущего ученика
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
        
        st.plotly_chart(fig_rank, use_container_width=True, config=config)
        
        # Статистика
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
        
        # Позиция в рейтинге
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
