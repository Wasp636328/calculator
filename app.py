"""
Student CGPA & Attendance Tracker
Smart Academic Performance Monitoring System
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CGPA & Attendance Tracker",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS  —  dark premium academic theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Google Fonts ── */
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

  /* ── Root palette ── */
  :root {
    --bg-deep:    #0b0f1a;
    --bg-card:    #111827;
    --bg-raised:  #1a2236;
    --border:     #1f2d45;
    --accent:     #4f9cf9;
    --accent2:    #a78bfa;
    --accent3:    #34d399;
    --warn:       #f59e0b;
    --danger:     #ef4444;
    --text-hi:    #f1f5f9;
    --text-mid:   #94a3b8;
    --text-lo:    #475569;
    --font-head:  'DM Serif Display', serif;
    --font-body:  'DM Sans', sans-serif;
    --font-mono:  'JetBrains Mono', monospace;
  }

  /* ── Base overrides ── */
  html, body, [class*="css"] {
    font-family: var(--font-body);
    background-color: var(--bg-deep);
    color: var(--text-hi);
  }
  .block-container { padding: 2rem 2.5rem 4rem; max-width: 1400px; }

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }

  /* ── Hero banner ── */
  .hero {
    background: linear-gradient(135deg, #0d1b2e 0%, #162032 50%, #0b0f1a 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: '';
    position: absolute; top: -80px; right: -80px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(79,156,249,.18) 0%, transparent 70%);
    border-radius: 50%;
  }
  .hero::after {
    content: '';
    position: absolute; bottom: -60px; left: 30%;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(167,139,250,.12) 0%, transparent 70%);
    border-radius: 50%;
  }
  .hero-title {
    font-family: var(--font-head);
    font-size: 2.8rem;
    color: var(--text-hi);
    margin: 0 0 .4rem;
    line-height: 1.1;
  }
  .hero-title span { color: var(--accent); }
  .hero-subtitle {
    font-size: 1.05rem;
    color: var(--text-mid);
    font-weight: 300;
    letter-spacing: .04em;
  }
  .hero-badge {
    display: inline-block;
    background: rgba(79,156,249,.12);
    border: 1px solid rgba(79,156,249,.3);
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: .72rem;
    padding: .25rem .75rem;
    border-radius: 20px;
    margin-top: 1rem;
    letter-spacing: .08em;
  }

  /* ── Section headers ── */
  .section-header {
    font-family: var(--font-head);
    font-size: 1.55rem;
    color: var(--text-hi);
    border-left: 3px solid var(--accent);
    padding-left: .85rem;
    margin: 2rem 0 1.2rem;
  }

  /* ── Cards ── */
  .card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    transition: border-color .2s;
  }
  .card:hover { border-color: rgba(79,156,249,.4); }

  /* ── Subject card ── */
  .subject-card {
    background: var(--bg-raised);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: .8rem;
  }
  .subject-label {
    font-family: var(--font-mono);
    font-size: .78rem;
    color: var(--accent);
    letter-spacing: .1em;
    margin-bottom: .3rem;
  }

  /* ── Metric overrides ── */
  [data-testid="metric-container"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
  }
  [data-testid="metric-container"] label { color: var(--text-mid) !important; font-size: .82rem; }
  [data-testid="metric-container"] [data-testid="stMetricValue"] { color: var(--text-hi) !important; font-size: 2rem; font-weight: 700; }

  /* ── Buttons ── */
  .stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #3b82f6);
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: .55rem 1.6rem;
    font-family: var(--font-body);
    font-weight: 600;
    font-size: .9rem;
    cursor: pointer;
    transition: opacity .2s, transform .15s;
    letter-spacing: .03em;
  }
  .stButton > button:hover { opacity: .88; transform: translateY(-1px); }
  .stButton > button:active { transform: translateY(0); }

  /* ── Inputs ── */
  .stTextInput > div > div > input,
  .stNumberInput > div > div > input,
  .stSelectbox > div > div {
    background: var(--bg-raised) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-hi) !important;
    font-family: var(--font-body) !important;
  }
  .stTextInput > div > div > input:focus,
  .stNumberInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(79,156,249,.15) !important;
  }

  /* ── Alerts ── */
  .alert-warn {
    background: rgba(245,158,11,.1);
    border: 1px solid rgba(245,158,11,.35);
    border-radius: 8px;
    padding: .8rem 1rem;
    color: var(--warn);
    font-size: .88rem;
    margin: .4rem 0;
  }
  .alert-danger {
    background: rgba(239,68,68,.1);
    border: 1px solid rgba(239,68,68,.35);
    border-radius: 8px;
    padding: .8rem 1rem;
    color: var(--danger);
    font-size: .88rem;
    margin: .4rem 0;
  }
  .alert-success {
    background: rgba(52,211,153,.1);
    border: 1px solid rgba(52,211,153,.35);
    border-radius: 8px;
    padding: .8rem 1rem;
    color: var(--accent3);
    font-size: .88rem;
    margin: .4rem 0;
  }

  /* ── Grade badges ── */
  .grade-S  { color: #fbbf24; font-weight: 700; }
  .grade-A  { color: #34d399; font-weight: 700; }
  .grade-B  { color: #60a5fa; font-weight: 700; }
  .grade-C  { color: #a78bfa; font-weight: 700; }
  .grade-D  { color: #fb923c; font-weight: 700; }
  .grade-E  { color: #f87171; font-weight: 700; }
  .grade-F  { color: #ef4444; font-weight: 700; }

  /* ── Dataframe ── */
  .stDataFrame { border-radius: 10px; overflow: hidden; }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: var(--bg-card);
    border-right: 1px solid var(--border);
  }
  [data-testid="stSidebar"] * { color: var(--text-hi) !important; }

  /* ── Dividers ── */
  hr { border-color: var(--border); margin: 1.5rem 0; }

  /* ── Expander ── */
  .streamlit-expanderHeader { color: var(--accent) !important; font-weight: 600; }

  /* ── Top subject highlight ── */
  .top-subject-badge {
    display: inline-flex; align-items: center; gap: .5rem;
    background: rgba(251,191,36,.1);
    border: 1px solid rgba(251,191,36,.3);
    border-radius: 8px;
    padding: .5rem 1rem;
    color: #fbbf24;
    font-weight: 600;
    font-size: .9rem;
    margin-bottom: 1rem;
  }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# GRADING CONSTANTS
# ─────────────────────────────────────────────
GRADE_SCALE = [
    (90, "S", 10),
    (80, "A",  9),
    (70, "B",  8),
    (60, "C",  7),
    (50, "D",  6),
    (40, "E",  5),
    ( 0, "F",  0),
]

GRADE_COLORS = {
    "S": "#fbbf24", "A": "#34d399", "B": "#60a5fa",
    "C": "#a78bfa", "D": "#fb923c", "E": "#f87171", "F": "#ef4444",
}

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(17,24,39,0.6)",
    font=dict(family="DM Sans", color="#94a3b8"),
    xaxis=dict(gridcolor="#1f2d45", zerolinecolor="#1f2d45"),
    yaxis=dict(gridcolor="#1f2d45", zerolinecolor="#1f2d45"),
)

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────
def get_grade(percentage: float) -> tuple[str, int]:
    for threshold, grade, gp in GRADE_SCALE:
        if percentage >= threshold:
            return grade, gp
    return "F", 0


def calc_total_percentage(internal: float, external: float) -> float:
    """Convert internal/50 + external/100 → aggregate percentage /100."""
    total = (internal / 50) * 50 + external
    return round((total / 150) * 100, 2)


def marks_needed_for_grade(internal: float, target_threshold: float) -> float | None:
    """Return external marks needed to reach target_threshold% overall."""
    # total% = ((internal/50)*50 + ext) / 150 * 100 >= target_threshold
    # ext >= (target_threshold * 150 / 100) - internal
    needed = (target_threshold * 150 / 100) - internal
    if needed <= 0:
        return 0.0
    if needed > 100:
        return None   # impossible
    return round(needed, 1)


def build_required_marks(internal: float, current_pct: float) -> str:
    """Return a human-readable string of what external score is needed for next grade."""
    thresholds = [90, 80, 70, 60, 50, 40]
    for t in thresholds:
        if current_pct < t:
            needed = marks_needed_for_grade(internal, t)
            grade, _ = get_grade(t)
            if needed is None:
                return f"Grade {grade} not achievable with current internal marks."
            return f"Need {needed}/100 in external to reach Grade {grade} ({t}%)"
    return "Already at maximum grade (S)."


def process_subjects(subjects: list[dict]) -> pd.DataFrame:
    """Build results DataFrame from raw subject input dicts."""
    rows = []
    for s in subjects:
        pct = calc_total_percentage(s["internal"], s["external"])
        grade, gp = get_grade(pct)
        att_pct = round((s["attended"] / s["total_classes"]) * 100, 1) if s["total_classes"] > 0 else 0.0
        required = build_required_marks(s["internal"], pct)
        rows.append({
            "Subject":        s["name"],
            "Credits":        s["credits"],
            "Internal (/50)": s["internal"],
            "External (/100)": s["external"],
            "Total %":        pct,
            "Grade":          grade,
            "Grade Point":    gp,
            "Attended":       s["attended"],
            "Total Classes":  s["total_classes"],
            "Attendance %":   att_pct,
            "Required Marks": required,
            "Status":         "✅ Pass" if grade != "F" else "❌ Fail",
        })
    return pd.DataFrame(rows)


def calc_cgpa(df: pd.DataFrame) -> float:
    total_credits = df["Credits"].sum()
    if total_credits == 0:
        return 0.0
    weighted = (df["Grade Point"] * df["Credits"]).sum()
    return round(weighted / total_credits, 2)


def calc_overall_attendance(df: pd.DataFrame) -> float:
    total_attended = df["Attended"].sum()
    total_classes  = df["Total Classes"].sum()
    if total_classes == 0:
        return 0.0
    return round((total_attended / total_classes) * 100, 1)


# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
if "num_subjects" not in st.session_state:
    st.session_state.num_subjects = 3
if "results" not in st.session_state:
    st.session_state.results = None

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:.5rem 0 1rem'>
      <div style='font-family:"DM Serif Display",serif;font-size:1.4rem;color:#f1f5f9'>🎓 AcadTrack</div>
      <div style='font-size:.78rem;color:#475569;letter-spacing:.08em'>SMART PERFORMANCE MONITOR</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("**📌 Navigation**")
    page = st.radio(
        "",
        ["📝 Enter Marks", "📊 Dashboard", "ℹ️ About"],
        label_visibility="collapsed",
    )
    st.markdown("---")

    # Live summary if results exist
    if st.session_state.results is not None:
        df = st.session_state.results
        cgpa     = calc_cgpa(df)
        att_pct  = calc_overall_attendance(df)
        passed   = (df["Grade"] != "F").sum()
        failed   = (df["Grade"] == "F").sum()

        st.markdown("**📋 Quick Summary**")
        st.markdown(f"""
        <div style='font-size:.88rem;line-height:2'>
          <span style='color:#94a3b8'>CGPA</span>&nbsp;&nbsp;
          <span style='color:#4f9cf9;font-weight:700;font-size:1.1rem'>{cgpa}</span><br>
          <span style='color:#94a3b8'>Attendance</span>&nbsp;&nbsp;
          <span style='color:{"#34d399" if att_pct>=75 else "#ef4444"};font-weight:700'>{att_pct}%</span><br>
          <span style='color:#94a3b8'>Subjects</span>&nbsp;&nbsp;
          <span style='color:#f1f5f9;font-weight:600'>{len(df)}</span><br>
          <span style='color:#94a3b8'>Passed</span>&nbsp;&nbsp;
          <span style='color:#34d399;font-weight:600'>{passed}</span> &nbsp;
          <span style='color:#94a3b8'>Failed</span>&nbsp;&nbsp;
          <span style='color:#ef4444;font-weight:600'>{failed}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

    if st.button("🔄 Reset All"):
        st.session_state.num_subjects = 3
        st.session_state.results      = None
        st.rerun()

    st.markdown(f"""
    <div style='font-size:.72rem;color:#334155;margin-top:2rem;text-align:center'>
      v1.0 · {datetime.now().strftime("%B %Y")}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class='hero'>
  <div class='hero-title'>Student <span>CGPA</span> & Attendance Tracker</div>
  <div class='hero-subtitle'>Smart Academic Performance Monitoring System</div>
  <div class='hero-badge'>✦ PRECISION ANALYTICS FOR STUDENTS ✦</div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE: ENTER MARKS
# ═══════════════════════════════════════════════
if "Enter" in page:

    st.markdown("<div class='section-header'>📚 Subject Entry</div>", unsafe_allow_html=True)
    st.caption("Fill in details for each subject. Click **+ Add Subject** to expand the list.")

    col_add, col_remove, _ = st.columns([1, 1, 5])
    with col_add:
        if st.button("＋ Add Subject"):
            st.session_state.num_subjects += 1
            st.rerun()
    with col_remove:
        if st.session_state.num_subjects > 1:
            if st.button("－ Remove Last"):
                st.session_state.num_subjects -= 1
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Subject input forms
    subject_data = []
    DEFAULT_NAMES = [
        "Mathematics", "Physics", "Chemistry", "Data Structures",
        "Operating Systems", "Networks", "DBMS", "Software Engineering",
    ]

    for i in range(st.session_state.num_subjects):
        default_name = DEFAULT_NAMES[i] if i < len(DEFAULT_NAMES) else f"Subject {i+1}"
        st.markdown(f"<div class='subject-label'>▸ SUBJECT {i+1}</div>", unsafe_allow_html=True)

        with st.container():
            c1, c2, c3, c4, c5, c6 = st.columns([2.5, 1, 1.2, 1.5, 1.5, 1.5])
            with c1:
                name = st.text_input("Subject Name", value=default_name, key=f"name_{i}", label_visibility="collapsed", placeholder="Subject Name")
            with c2:
                credits = st.number_input("Credits", min_value=1, max_value=6, value=4, key=f"cred_{i}", label_visibility="collapsed")
            with c3:
                internal = st.number_input("Internal /50", min_value=0.0, max_value=50.0, value=35.0, step=0.5, key=f"int_{i}", label_visibility="collapsed")
            with c4:
                external = st.number_input("External /100", min_value=0.0, max_value=100.0, value=60.0, step=0.5, key=f"ext_{i}", label_visibility="collapsed")
            with c5:
                attended = st.number_input("Classes Attended", min_value=0, max_value=300, value=55, key=f"att_{i}", label_visibility="collapsed")
            with c6:
                total_cls = st.number_input("Total Classes", min_value=1, max_value=300, value=72, key=f"tot_{i}", label_visibility="collapsed")

        subject_data.append({
            "name": name, "credits": credits, "internal": internal,
            "external": external, "attended": attended, "total_classes": total_cls,
        })

    # Column headers legend
    st.markdown("""
    <div style='display:flex;gap:1rem;font-size:.72rem;color:#475569;font-family:"JetBrains Mono",monospace;
                margin-top:.2rem;padding-left:.2rem;letter-spacing:.06em'>
      <span style='flex:2.5'>SUBJECT NAME</span>
      <span style='flex:1'>CREDITS</span>
      <span style='flex:1.2'>INTERNAL /50</span>
      <span style='flex:1.5'>EXTERNAL /100</span>
      <span style='flex:1.5'>ATTENDED</span>
      <span style='flex:1.5'>TOTAL CLASSES</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CALCULATE BUTTON ──
    if st.button("⚡ Calculate Performance", use_container_width=True):
        with st.spinner("Processing academic data..."):
            import time; time.sleep(0.6)  # brief UX delay
            df = process_subjects(subject_data)
            st.session_state.results = df
            st.success("✅ Calculation complete! Switch to **📊 Dashboard** to see results.")


# ═══════════════════════════════════════════════
# PAGE: DASHBOARD
# ═══════════════════════════════════════════════
elif "Dashboard" in page:

    if st.session_state.results is None:
        st.markdown("""
        <div class='card' style='text-align:center;padding:3rem'>
          <div style='font-size:3rem'>📊</div>
          <div style='font-size:1.2rem;color:#94a3b8;margin-top:.8rem'>No data yet</div>
          <div style='color:#475569;margin-top:.4rem'>Go to <b>📝 Enter Marks</b> and click <b>Calculate</b>.</div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    df = st.session_state.results

    # ── KPI METRICS ──
    cgpa        = calc_cgpa(df)
    att_pct     = calc_overall_attendance(df)
    total_cred  = df["Credits"].sum()
    passed      = int((df["Grade"] != "F").sum())
    failed      = int((df["Grade"] == "F").sum())
    top_subject = df.loc[df["Total %"].idxmax(), "Subject"]
    top_score   = df["Total %"].max()

    st.markdown("<div class='section-header'>📊 Performance Overview</div>", unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🎓 CGPA", f"{cgpa}", delta=f"{'Good' if cgpa>=7 else 'Needs Work'}")
    k2.metric("📅 Overall Attendance", f"{att_pct}%", delta=f"{'Above 75%' if att_pct>=75 else 'Below 75%'}")
    k3.metric("📚 Total Credits", total_cred)
    k4.metric("✅ Pass / ❌ Fail", f"{passed} / {failed}")

    # ── ALERTS ──
    st.markdown("<br>", unsafe_allow_html=True)
    low_att = df[df["Attendance %"] < 75]
    failed_subs = df[df["Grade"] == "F"]

    if not low_att.empty:
        for _, row in low_att.iterrows():
            st.markdown(f"<div class='alert-warn'>⚠️ <b>{row['Subject']}</b> — Attendance {row['Attendance %']}% is below the 75% threshold.</div>", unsafe_allow_html=True)

    if not failed_subs.empty:
        for _, row in failed_subs.iterrows():
            st.markdown(f"<div class='alert-danger'>❌ <b>{row['Subject']}</b> — Failed (Grade F). Immediate attention required.</div>", unsafe_allow_html=True)

    if low_att.empty and failed_subs.empty:
        st.markdown("<div class='alert-success'>✨ All subjects cleared with adequate attendance. Keep it up!</div>", unsafe_allow_html=True)

    # Top subject
    st.markdown(f"<div class='top-subject-badge'>🏆 Top Subject: {top_subject} — {top_score}%</div>", unsafe_allow_html=True)

    # ── SUBJECT TABLE ──
    st.markdown("<div class='section-header'>📋 Subject-wise Breakdown</div>", unsafe_allow_html=True)

    display_df = df[[
        "Subject", "Credits", "Internal (/50)", "External (/100)",
        "Total %", "Grade", "Grade Point", "Attendance %", "Status", "Required Marks"
    ]].copy()

    st.dataframe(
        display_df.style
            .background_gradient(subset=["Total %"], cmap="Blues")
            .background_gradient(subset=["Attendance %"], cmap="Greens")
            .applymap(lambda v: f"color: {GRADE_COLORS.get(v, '#f1f5f9')}; font-weight:700" if v in GRADE_COLORS else "", subset=["Grade"])
            .set_properties(**{"background-color": "#111827", "color": "#f1f5f9"}),
        use_container_width=True,
        height=300,
    )

    # ── CHARTS ──
    st.markdown("<div class='section-header'>📈 Visual Analytics</div>", unsafe_allow_html=True)

    ch1, ch2 = st.columns(2)

    # Bar — subject marks
    with ch1:
        fig_bar = px.bar(
            df, x="Subject", y="Total %",
            color="Grade",
            color_discrete_map=GRADE_COLORS,
            title="Subject-wise Total Marks (%)",
            text="Total %",
        )
        fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_bar.update_layout(**PLOTLY_THEME, title_font_size=14, showlegend=True, height=380)
        fig_bar.add_hline(y=40, line_dash="dash", line_color="#ef4444", annotation_text="Pass Line (40%)")
        st.plotly_chart(fig_bar, use_container_width=True)

    # Pie — grade distribution
    with ch2:
        grade_counts = df["Grade"].value_counts().reset_index()
        grade_counts.columns = ["Grade", "Count"]
        fig_pie = px.pie(
            grade_counts, names="Grade", values="Count",
            color="Grade", color_discrete_map=GRADE_COLORS,
            title="Grade Distribution",
            hole=0.45,
        )
        fig_pie.update_layout(**PLOTLY_THEME, title_font_size=14, height=380)
        fig_pie.update_traces(textinfo="percent+label", textfont_size=13)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Attendance line/bar
    fig_att = px.bar(
        df, x="Subject", y="Attendance %",
        color="Attendance %",
        color_continuous_scale=[[0,"#ef4444"],[0.75,"#f59e0b"],[1,"#34d399"]],
        title="Attendance % per Subject",
        text="Attendance %",
    )
    fig_att.update_traces(texttemplate="%{text}%", textposition="outside")
    fig_att.add_hline(y=75, line_dash="dot", line_color="#f59e0b", annotation_text="75% Min Required")
    fig_att.update_layout(**PLOTLY_THEME, title_font_size=14, coloraxis_showscale=False, height=350)
    st.plotly_chart(fig_att, use_container_width=True)

    # Radar — subject performance
    radar_fig = go.Figure()
    radar_fig.add_trace(go.Scatterpolar(
        r=df["Total %"].tolist() + [df["Total %"].iloc[0]],
        theta=df["Subject"].tolist() + [df["Subject"].iloc[0]],
        fill="toself",
        fillcolor="rgba(79,156,249,.15)",
        line=dict(color="#4f9cf9", width=2),
        name="Marks %"
    ))
    radar_fig.add_trace(go.Scatterpolar(
        r=df["Attendance %"].tolist() + [df["Attendance %"].iloc[0]],
        theta=df["Subject"].tolist() + [df["Subject"].iloc[0]],
        fill="toself",
        fillcolor="rgba(52,211,153,.1)",
        line=dict(color="#34d399", width=2),
        name="Attendance %"
    ))
    radar_fig.update_layout(
        **PLOTLY_THEME,
        polar=dict(
            bgcolor="rgba(17,24,39,.6)",
            radialaxis=dict(visible=True, range=[0, 100], color="#475569", gridcolor="#1f2d45"),
            angularaxis=dict(color="#94a3b8", gridcolor="#1f2d45"),
        ),
        title=dict(text="Performance Radar", font_size=14, font_color="#94a3b8"),
        showlegend=True,
        height=450,
    )
    st.plotly_chart(radar_fig, use_container_width=True)

    # ── REQUIRED MARKS PREDICTOR ──
    st.markdown("<div class='section-header'>🎯 Required Marks Predictor</div>", unsafe_allow_html=True)
    pred_df = df[["Subject", "Total %", "Grade", "Required Marks"]].copy()
    for _, row in pred_df.iterrows():
        col_icon = "✅" if row["Grade"] not in ("F","E","D") else "⚠️"
        grade_color = GRADE_COLORS.get(row["Grade"], "#94a3b8")
        st.markdown(f"""
        <div class='card' style='padding:.9rem 1.2rem;margin-bottom:.5rem'>
          <span style='font-weight:600;color:#f1f5f9'>{col_icon} {row['Subject']}</span>
          <span style='color:{grade_color};font-weight:700;margin-left:1rem'>Grade {row['Grade']}</span>
          <span style='color:#475569;margin-left:.5rem'>({row['Total %']}%)</span>
          <div style='color:#94a3b8;font-size:.85rem;margin-top:.3rem'>{row['Required Marks']}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── DOWNLOAD ──
    st.markdown("<div class='section-header'>💾 Export Report</div>", unsafe_allow_html=True)
    dl1, dl2, _ = st.columns([1.5, 1.5, 5])

    with dl1:
        csv_buf = io.StringIO()
        df.to_csv(csv_buf, index=False)
        st.download_button(
            "⬇ Download CSV",
            data=csv_buf.getvalue(),
            file_name=f"cgpa_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
    with dl2:
        txt_lines = [
            "STUDENT CGPA & ATTENDANCE REPORT",
            f"Generated: {datetime.now().strftime('%d %B %Y %H:%M')}",
            "=" * 50,
            f"Overall CGPA      : {calc_cgpa(df)}",
            f"Overall Attendance: {calc_overall_attendance(df)}%",
            f"Total Credits     : {df['Credits'].sum()}",
            f"Passed Subjects   : {(df['Grade']!='F').sum()}",
            f"Failed Subjects   : {(df['Grade']=='F').sum()}",
            "=" * 50,
        ]
        for _, row in df.iterrows():
            txt_lines += [
                f"\nSubject : {row['Subject']}",
                f"  Credits     : {row['Credits']}",
                f"  Internal    : {row['Internal (/50)']}/50",
                f"  External    : {row['External (/100)']}/100",
                f"  Total %     : {row['Total %']}",
                f"  Grade       : {row['Grade']} (GP: {row['Grade Point']})",
                f"  Attendance  : {row['Attendance %']}%",
                f"  Status      : {row['Status']}",
                f"  Predictor   : {row['Required Marks']}",
            ]
        st.download_button(
            "⬇ Download TXT",
            data="\n".join(txt_lines),
            file_name=f"cgpa_report_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
        )

    # ── FUTURE SCOPE ──
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🚀 Future Scope & Roadmap", expanded=False):
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            **🔗 Integration & Sync**
            - Integration with University ERP systems
            - Automated timetable sync via LMS API
            - Push notifications for low attendance

            **📆 Planning Tools**
            - AI-powered exam preparation planner
            - Smart study scheduler with Pomodoro mode
            """)
        with col_b:
            st.markdown("""
            **📚 History & Analytics**
            - Multi-semester CGPA history tracking
            - Cumulative performance trend charts
            - Peer percentile comparison (anonymized)

            **🤖 AI Enhancements**
            - Grade prediction using ML models
            - Personalised improvement recommendations
            """)


# ═══════════════════════════════════════════════
# PAGE: ABOUT
# ═══════════════════════════════════════════════
elif "About" in page:
    st.markdown("<div class='section-header'>ℹ️ About This Project</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
      <p style='font-size:1.05rem;line-height:1.8;color:#cbd5e1'>
        <b style='color:#f1f5f9'>Student CGPA & Attendance Tracker</b> is a data-driven academic monitoring
        tool that helps students stay on top of their performance in real time. It combines
        <b>Education Management</b>, <b>Data Analysis</b>, and <b>Software Development</b>
        to provide actionable insights at a glance.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='section-header'>⚙️ Grading Scale Used</div>
    """, unsafe_allow_html=True)

    scale_data = {
        "Marks Range": ["90 – 100", "80 – 89", "70 – 79", "60 – 69", "50 – 59", "40 – 49", "Below 40"],
        "Grade":       ["S", "A", "B", "C", "D", "E", "F"],
        "Grade Point": [10, 9, 8, 7, 6, 5, 0],
        "Status":      ["Outstanding", "Excellent", "Very Good", "Good", "Average", "Marginal Pass", "Fail"],
    }
    st.dataframe(
        pd.DataFrame(scale_data)
          .style.set_properties(**{"background-color": "#111827", "color": "#f1f5f9"}),
        use_container_width=True, hide_index=True,
    )

    st.markdown("""
    <div class='section-header'>🧮 Calculation Method</div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class='card'>
      <ul style='color:#94a3b8;line-height:2.2;font-size:.95rem'>
        <li><b style='color:#f1f5f9'>Total %</b> = ((Internal/50)×50 + External) / 150 × 100</li>
        <li><b style='color:#f1f5f9'>CGPA</b> = Σ(Grade Point × Credits) / Σ Credits</li>
        <li><b style='color:#f1f5f9'>Attendance %</b> = (Classes Attended / Total Classes) × 100</li>
        <li><b style='color:#f1f5f9'>Required External</b> = (Target% × 150/100) − Internal</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center;color:#334155;font-size:.8rem;margin-top:3rem'>
      Built with ❤️ using Streamlit · Python · Plotly
    </div>
    """, unsafe_allow_html=True)
