import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_loader import (
    load_all_data, get_summary, get_expense_summary,
    get_expense_detail, ingest_file,
)

st.set_page_config(
    page_title="Revenue Management Console",
    page_icon="▣",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'IBM Plex Sans', sans-serif !important;
}
.stApp { background: #edf0f4; }
.main .block-container { padding: 0 !important; max-width: 100% !important; }

/* SIDEBAR */
[data-testid="stSidebar"], [data-testid="stSidebar"] > div,
[data-testid="stSidebar"] > div > div,
section[data-testid="stSidebar"],
.css-1d391kg, .css-6qob1r, .css-qrbaxs,
.st-emotion-cache-1d391kg, .st-emotion-cache-6qob1r,
.st-emotion-cache-eczf1x, .st-emotion-cache-1gwvy71,
.st-emotion-cache-16txtl3, .st-emotion-cache-qrbaxs {
    background: #101828 !important;
    background-color: #101828 !important;
}
[data-testid="stSidebar"] { border-right: 2px solid #1e2f4a !important; }
[data-testid="stSidebar"] * { color: #8fa8c8 !important; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] label { font-size: 11px !important; }
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"],
[data-testid="stSidebar"] [data-testid="stFileUploader"] section {
    background: #172038 !important;
    border: 1px dashed #2a3f60 !important;
    border-radius: 4px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #172038 !important;
    border: 1px solid #2a3f60 !important;
    color: #c0d4ec !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: #1e3a5f !important;
    border: 1px solid #2a5080 !important;
}
[data-testid="stSidebar"] button {
    background: #172038 !important;
    border: 1px solid #2a3f60 !important;
    color: #8fa8c8 !important;
    border-radius: 3px !important;
}
[data-testid="stSidebar"] hr { border-color: #1e2f4a !important; }
[data-testid="stSidebar"] [data-baseweb="select"] svg { fill: #4a6a9a !important; }

.sb-logo {
    display:flex; align-items:center; gap:10px;
    padding:16px 0 14px; border-bottom:1px solid #1e2f4a; margin-bottom:4px;
}
.sb-logo-box {
    width:30px; height:30px; background:#1a56db; border-radius:3px;
    display:flex; align-items:center; justify-content:center;
    font-family:'IBM Plex Mono',monospace; font-size:15px; font-weight:500; color:#fff !important;
}
.sb-logo-name { font-size:13px !important; font-weight:600 !important; color:#e0eaf8 !important; }
.sb-logo-sub  { font-size:9px !important; color:#3d5a80 !important; font-family:'IBM Plex Mono',monospace; letter-spacing:0.08em; text-transform:uppercase; }
.sb-section   { font-family:'IBM Plex Mono',monospace; font-size:9px; letter-spacing:0.14em; text-transform:uppercase; color:#3d5a80 !important; padding:14px 0 6px; border-bottom:1px solid #1e2f4a; margin-bottom:10px; }
.sb-label     { color:#5a7a9a !important; font-size:10px; letter-spacing:0.06em; text-transform:uppercase; margin-bottom:4px; font-family:'IBM Plex Mono',monospace; }
.sb-stat      { font-size:10px !important; color:#3d5a80 !important; font-family:'IBM Plex Mono',monospace; }

/* HEADER */
.ent-header {
    background:linear-gradient(135deg,#0a1628 0%,#0f2044 100%);
    border-bottom:3px solid #1a56db;
    padding:20px 32px 16px; display:flex; align-items:flex-end; justify-content:space-between;
}
.ent-breadcrumb { font-family:'IBM Plex Mono',monospace; font-size:9px; letter-spacing:0.14em; text-transform:uppercase; color:#3d5a80; margin-bottom:5px; }
.ent-title { font-size:22px; font-weight:300; color:#e8f0fc; letter-spacing:-0.3px; }
.ent-title strong { font-weight:600; color:#fff; }
.ent-header-right { display:flex; align-items:center; gap:14px; }
.ent-badge { background:#172038; border:1px solid #2a3f60; border-radius:3px; padding:5px 14px; font-family:'IBM Plex Mono',monospace; font-size:10px; color:#6a8ab8; }
.ent-badge strong { color:#a0c4f0; font-weight:500; }

/* KPI */
.kpi-strip { background:#f8f9fb; border-bottom:1px solid #cdd2de; display:flex; }
.kpi-item  { flex:1; padding:18px 24px 14px; border-right:1px solid #cdd2de; position:relative; }
.kpi-item:last-child { border-right:none; }
.kpi-item::after { content:''; position:absolute; top:0; left:0; right:0; height:3px; }
.kpi-item.c-blue::after   { background:#1a56db; }
.kpi-item.c-green::after  { background:#0e9f6e; }
.kpi-item.c-amber::after  { background:#c27803; }
.kpi-item.c-purple::after { background:#6c2bd9; }
.kpi-item.c-red::after    { background:#e02424; }
.kpi-item.c-teal::after   { background:#0694a2; }
.kpi-lbl  { font-family:'IBM Plex Mono',monospace; font-size:9px; letter-spacing:0.12em; text-transform:uppercase; color:#6b7a99; margin-bottom:6px; }
.kpi-val  { font-size:27px; font-weight:300; color:#111928; letter-spacing:-0.8px; line-height:1; margin-bottom:5px; }
.kpi-delta     { font-family:'IBM Plex Mono',monospace; font-size:10px; }
.kpi-delta.pos { color:#0e9f6e; }
.kpi-delta.neg { color:#e02424; }
.kpi-delta.neu { color:#9aa4b8; }

/* TOP-LEVEL MODULE TABS */
.stTabs [data-baseweb="tab-list"] {
    background:#ffffff !important; border-bottom:2px solid #cdd2de !important;
    padding:0 32px !important; gap:0 !important;
}
.stTabs [data-baseweb="tab"] {
    background:transparent !important; border:none !important;
    border-bottom:3px solid transparent !important; padding:14px 24px !important;
    font-family:'IBM Plex Sans',sans-serif !important; font-size:12px !important;
    font-weight:500 !important; color:#6b7a99 !important; margin-bottom:-2px !important;
    border-radius:0 !important;
}
.stTabs [aria-selected="true"] { color:#1a56db !important; border-bottom-color:#1a56db !important; }
.stTabs [data-baseweb="tab-panel"] { padding:28px 32px !important; background:#edf0f4; }

/* PANELS */
.panel { background:#fff; border:1px solid #cdd2de; border-top:3px solid #1a56db; border-radius:0 0 4px 4px; padding:20px 24px 24px; margin-bottom:16px; }
.panel.red    { border-top-color:#e02424; }
.panel.amber  { border-top-color:#c27803; }
.panel.green  { border-top-color:#0e9f6e; }
.panel.teal   { border-top-color:#0694a2; }
.panel-title  { font-size:13px; font-weight:600; color:#111928; margin-bottom:3px; }
.panel-sub    { font-family:'IBM Plex Mono',monospace; font-size:9px; letter-spacing:0.1em; text-transform:uppercase; color:#9aa4b8; margin-bottom:16px; padding-bottom:12px; border-bottom:1px solid #e8ebf2; }

/* BUCKET BADGES */
.bucket-badge { display:inline-block; padding:2px 8px; border-radius:2px; font-family:'IBM Plex Mono',monospace; font-size:10px; font-weight:500; }
.bucket-loe      { background:#dbeafe; color:#1e40af; }
.bucket-leasehold{ background:#fef3c7; color:#92400e; }
.bucket-capital  { background:#f3e8ff; color:#5b21b6; }
.bucket-workover { background:#fee2e2; color:#991b1b; }

/* SUMMARY ROWS */
.sum-row  { display:flex; gap:12px; margin:18px 0 4px; }
.sum-cell { flex:1; background:#f4f6fa; border:1px solid #cdd2de; border-left:3px solid #1a56db; padding:14px 18px; border-radius:0 3px 3px 0; }
.sum-cell.green { border-left-color:#0e9f6e; }
.sum-cell.amber { border-left-color:#c27803; }
.sum-cell.red   { border-left-color:#e02424; }
.sum-cell.teal  { border-left-color:#0694a2; }
.sum-cell.purple{ border-left-color:#6c2bd9; }
.sum-lbl  { font-family:'IBM Plex Mono',monospace; font-size:9px; letter-spacing:0.1em; text-transform:uppercase; color:#6b7a99; margin-bottom:5px; }
.sum-val  { font-size:19px; font-weight:400; color:#111928; letter-spacing:-0.4px; }
.sum-note { font-family:'IBM Plex Mono',monospace; font-size:9px; color:#9aa4b8; margin-top:3px; }

div[data-testid="metric-container"] { display:none; }
.stExpander { background:#fff !important; border:1px solid #cdd2de !important; border-radius:3px !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
      <div class="sb-logo-box">R</div>
      <div>
        <div class="sb-logo-name">RevConsole</div>
        <div class="sb-logo-sub">Oil &amp; Gas · GL Analytics</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Data Source</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(" ", type=["xlsx", "xls", "csv"], label_visibility="collapsed")

    if uploaded:
        res = ingest_file(uploaded)
        if res["status"] == "ok":
            st.success(f"✓ {res['rows']:,} rows · {res['months']} period(s) · {res['wells']} wells")
            st.rerun()
        elif res["status"] == "duplicate":
            st.info("Already loaded — no duplicate data added.")
        else:
            st.error(res.get("message", "Unknown error"))

    st.divider()

    _raw = load_all_data()
    if _raw is None or _raw.empty:
        st.warning("No data loaded. Upload a GL export above.")
        st.stop()

    df = _raw.copy()
    for col in ["Well", "Period", "SubAcctNum"]:
        if col not in df.columns:
            df[col] = "Unknown"
    df["Well"]      = df["Well"].fillna("Unknown").astype(str)
    df["SubAcctNum"] = df["SubAcctNum"].fillna("Unknown").astype(str)

    st.markdown('<div class="sb-section">Filters</div>', unsafe_allow_html=True)

    valid_mask = (df["Well"].notna() & (df["Well"].str.strip() != "") & (df["Well"].str.strip().str.lower() != "unknown"))
    valid      = df.loc[valid_mask, ["SubAcctNum", "Well"]].drop_duplicates().sort_values(["SubAcctNum", "Well"])
    all_nums   = sorted(valid["SubAcctNum"].unique().tolist()) if not valid.empty else []
    all_descs  = sorted(valid["Well"].unique().tolist())      if not valid.empty else []

    st.markdown('<div class="sb-label">Sub Account</div>', unsafe_allow_html=True)
    sel_nums = st.multiselect("_nums", options=all_nums, default=[], placeholder="All sub accounts…", label_visibility="collapsed")

    avail_descs = sorted(valid.loc[valid["SubAcctNum"].isin(sel_nums), "Well"].unique().tolist()) if sel_nums else all_descs
    st.markdown('<div class="sb-label" style="margin-top:10px">Well Name</div>', unsafe_allow_html=True)
    sel_descs = st.multiselect("_descs", options=avail_descs, default=[], placeholder="All wells…", label_visibility="collapsed")

    selected_wells = sel_descs if sel_descs else (avail_descs if sel_nums else [])
    all_months     = sorted([m for m in df["Period"].dropna().astype(str).unique().tolist() if m != ""])

    st.markdown('<div class="sb-label" style="margin-top:10px">Period Range</div>', unsafe_allow_html=True)
    if len(all_months) >= 2:
        month_range = st.select_slider("_period", options=all_months, value=(all_months[0], all_months[-1]), label_visibility="collapsed")
    elif len(all_months) == 1:
        month_range = (all_months[0], all_months[0])
    else:
        month_range = (None, None)

    st.divider()
    st.markdown(f'<div class="sb-stat">{df["Period"].nunique()} periods · {df["Well"].nunique()} wells loaded</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FILTER
# ═══════════════════════════════════════════════════════════════════════════════
dff = df.copy()
if selected_wells:
    dff = dff[dff["Well"].isin(selected_wells)]
if month_range[0] and month_range[1]:
    dff = dff[(dff["Period"] >= month_range[0]) & (dff["Period"] <= month_range[1])]

summary     = get_summary(dff)
exp_summary = get_expense_summary(dff)

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
PF   = "IBM Plex Sans, sans-serif"
MF   = "IBM Plex Mono, monospace"
GRID = "#e8ebf2"
BG   = "#ffffff"
C = {
    "oil":    "#1a56db", "gas":    "#0e9f6e", "plant":  "#c27803",
    "ded":    "#e02424", "net":    "#6c2bd9", "dshade": "rgba(224,36,36,0.10)",
    "loe":    "#1a56db", "leasehold": "#c27803",
    "capital":"#6c2bd9", "workover":  "#e02424", "total_exp": "#374151",
}
BUCKET_COLORS = {"LOE": C["loe"], "Leasehold": C["leasehold"], "Capital": C["capital"], "Workover": C["workover"]}

def fmt(v):
    if abs(v) >= 1_000_000: return f"${v/1e6:.2f}M"
    if abs(v) >= 1_000:     return f"${v/1e3:.1f}K"
    return f"${v:,.0f}"

def delta_html(cur, prev, lbl=""):
    if prev and prev != 0:
        d  = (cur - prev) / abs(prev) * 100
        cl = "pos" if d >= 0 else "neg"
        return f'<span class="kpi-delta {cl}">{"+" if d >= 0 else ""}{d:.1f}% vs {lbl}</span>'
    return '<span class="kpi-delta neu">—</span>'

def bl(**kw):
    base = {
        "font": dict(family=PF, size=12, color="#374151"),
        "paper_bgcolor": BG, "plot_bgcolor": BG,
        "margin": dict(t=16, b=40, l=12, r=12),
        "hovermode": "x unified",
        "hoverlabel": dict(bgcolor="#111928", font_color="#e8f0fc", font_family=MF, font_size=11),
        "legend": dict(orientation="h", yanchor="bottom", y=1.02, x=0,
                       font=dict(family=MF, size=10), bgcolor="rgba(0,0,0,0)", borderwidth=0),
    }
    base.update(kw)
    return base

def sax(fig):
    tf = dict(family=MF, size=10, color="#9aa4b8")
    fig.update_xaxes(showgrid=False, showline=True, linecolor="#cdd2de", tickfont=tf, ticks="outside", ticklen=3)
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=tf)
    return fig

months_sorted = sorted(dff["Period"].dropna().astype(str).unique().tolist())
last_m = months_sorted[-1] if months_sorted else None
prev_m = months_sorted[-2] if len(months_sorted) >= 2 else None

last_gross = summary.loc[summary["Period"] == last_m, "Gross_Revenue"].sum()  if (last_m and not summary.empty) else 0
prev_gross = summary.loc[summary["Period"] == prev_m, "Gross_Revenue"].sum()  if (prev_m and not summary.empty) else 0
last_net   = summary.loc[summary["Period"] == last_m, "Net_Revenue"].sum()    if (last_m and not summary.empty) else 0
prev_net   = summary.loc[summary["Period"] == prev_m, "Net_Revenue"].sum()    if (prev_m and not summary.empty) else 0
last_deds  = summary.loc[summary["Period"] == last_m, "Total_Deductions"].sum() if (last_m and not summary.empty) else 0
ded_rate   = last_deds / last_gross * 100 if last_gross else 0
total_gross= summary["Gross_Revenue"].sum() if not summary.empty else 0
total_net  = summary["Net_Revenue"].sum()   if not summary.empty else 0

last_exp   = exp_summary.loc[exp_summary["Period"] == last_m, "Amount"].sum() if (last_m and not exp_summary.empty) else 0
total_exp  = exp_summary["Amount"].sum() if not exp_summary.empty else 0
n_wells    = df["Well"].nunique()

wlbl = f"{len(selected_wells)} of {n_wells} wells" if selected_wells else f"All {dff['Well'].nunique()} wells"
plbl = f"{month_range[0]} – {month_range[1]}" if month_range and month_range[0] != month_range[1] else (month_range[0] if month_range else "")

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER + KPI STRIP
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="ent-header">
  <div>
    <div class="ent-breadcrumb">Revenue Management &rsaquo; GL Analytics</div>
    <div class="ent-title">Integrated P&amp;L &nbsp;<strong>{wlbl}</strong></div>
  </div>
  <div class="ent-header-right">
    <div class="ent-badge">Period &nbsp;<strong>{plbl}</strong></div>
    <div class="ent-badge">Latest &nbsp;<strong>{last_m or "—"}</strong></div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="kpi-strip">
  <div class="kpi-item c-blue">
    <div class="kpi-lbl">Gross Revenue ({last_m or "—"})</div>
    <div class="kpi-val">{fmt(last_gross)}</div>
    {delta_html(last_gross, prev_gross, prev_m or "")}
  </div>
  <div class="kpi-item c-green">
    <div class="kpi-lbl">Net Revenue ({last_m or "—"})</div>
    <div class="kpi-val">{fmt(last_net)}</div>
    {delta_html(last_net, prev_net, prev_m or "")}
  </div>
  <div class="kpi-item c-red">
    <div class="kpi-lbl">Total Expenses ({last_m or "—"})</div>
    <div class="kpi-val">{fmt(last_exp)}</div>
    <span class="kpi-delta neu">operating costs</span>
  </div>
  <div class="kpi-item c-teal">
    <div class="kpi-lbl">Net Income ({last_m or "—"})</div>
    <div class="kpi-val">{fmt(last_net - last_exp)}</div>
    <span class="kpi-delta neu">net rev minus opex</span>
  </div>
  <div class="kpi-item c-amber">
    <div class="kpi-lbl">Deduction Rate</div>
    <div class="kpi-val">{ded_rate:.1f}%</div>
    <span class="kpi-delta neu">of gross revenue</span>
  </div>
  <div class="kpi-item c-purple">
    <div class="kpi-lbl">Cumul. Net Revenue</div>
    <div class="kpi-val">{fmt(total_net)}</div>
    <span class="kpi-delta neu">{len(months_sorted)} period(s)</span>
  </div>
  <div class="kpi-item c-red">
    <div class="kpi-lbl">Cumul. Expenses</div>
    <div class="kpi-val">{fmt(total_exp)}</div>
    <span class="kpi-delta neu">{len(months_sorted)} period(s)</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE TABS
# ═══════════════════════════════════════════════════════════════════════════════
rev_tab, exp_tab = st.tabs(["📈  Revenue", "💰  Expenses"])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# REVENUE MODULE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with rev_tab:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Revenue Trend", "Commodity Mix", "Deduction Bridge", "Well Rankings", "Volumes",
    ])

    # ── Tab 1: Revenue Trend ──────────────────────────────────────────────────
    with tab1:
        trend = (
            summary.groupby("Period")
            .agg(Oil=("Oil_Gross","sum"), Gas=("Gas_Gross","sum"), Plant=("Plant_Gross","sum"),
                 Deductions=("Total_Deductions","sum"), Net=("Net_Revenue","sum"))
            .reset_index().sort_values("Period")
        )
        st.markdown('<div class="panel"><div class="panel-title">Revenue Trend by Commodity</div><div class="panel-sub">Monthly gross — oil · gas · plant/NGL · net overlay</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_bar(x=trend["Period"], y=trend["Oil"],   name="Oil",        marker_color=C["oil"],    marker_line_width=0)
        fig.add_bar(x=trend["Period"], y=trend["Gas"],   name="Gas",        marker_color=C["gas"],    marker_line_width=0)
        fig.add_bar(x=trend["Period"], y=trend["Plant"], name="Plant/NGL",  marker_color=C["plant"],  marker_line_width=0)
        fig.add_bar(x=trend["Period"], y=(-trend["Deductions"]).tolist(), name="Deductions", marker_color=C["dshade"], marker_line_width=0)
        fig.add_scatter(x=trend["Period"], y=trend["Net"], name="Net Revenue",
                        line=dict(color=C["net"], width=2.5), mode="lines+markers",
                        marker=dict(size=6, color=C["net"], line=dict(color="#fff", width=1.5)))
        fig.update_layout(**bl(barmode="relative", height=380, yaxis=dict(tickprefix="$", tickformat=",.0f")))
        sax(fig)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        with st.expander("Data table"):
            td = trend.copy()
            for c in ["Oil","Gas","Plant","Deductions","Net"]:
                td[c] = td[c].apply(lambda v: f"${v:,.0f}")
            st.dataframe(td, use_container_width=True, hide_index=True)

    # ── Tab 2: Commodity Mix ──────────────────────────────────────────────────
    with tab2:
        mix = (summary.groupby("Period").agg(Oil=("Oil_Gross","sum"), Gas=("Gas_Gross","sum"), Plant=("Plant_Gross","sum"))
               .reset_index().sort_values("Period"))
        tot_o = summary["Oil_Gross"].sum()  if not summary.empty else 0
        tot_g = summary["Gas_Gross"].sum()  if not summary.empty else 0
        tot_p = summary["Plant_Gross"].sum() if not summary.empty else 0
        L, R  = st.columns([3, 2], gap="medium")
        with L:
            st.markdown('<div class="panel"><div class="panel-title">Monthly Revenue Stack</div><div class="panel-sub">Gross by commodity per period</div>', unsafe_allow_html=True)
            f2 = go.Figure()
            f2.add_bar(x=mix["Period"], y=mix["Oil"],   name="Oil",       marker_color=C["oil"],   marker_line_width=0)
            f2.add_bar(x=mix["Period"], y=mix["Gas"],   name="Gas",       marker_color=C["gas"],   marker_line_width=0)
            f2.add_bar(x=mix["Period"], y=mix["Plant"], name="Plant/NGL", marker_color=C["plant"], marker_line_width=0)
            f2.update_layout(**bl(barmode="stack", height=340, yaxis=dict(tickprefix="$", tickformat=",.0f")))
            sax(f2)
            st.plotly_chart(f2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with R:
            st.markdown('<div class="panel"><div class="panel-title">Cumulative Mix</div><div class="panel-sub">All selected periods</div>', unsafe_allow_html=True)
            f3 = go.Figure(go.Pie(
                labels=["Oil","Gas","Plant/NGL"], values=[tot_o, tot_g, tot_p], hole=0.62,
                marker=dict(colors=[C["oil"], C["gas"], C["plant"]], line=dict(color="#fff", width=2.5)),
                textinfo="label+percent", textfont=dict(family=MF, size=10),
                hovertemplate="%{label}: $%{value:,.0f}<extra></extra>", insidetextorientation="radial",
            ))
            f3.update_layout(height=340, showlegend=False, paper_bgcolor=BG, margin=dict(t=10,b=10,l=20,r=20),
                annotations=[dict(text=f"<b>{fmt(tot_o+tot_g+tot_p)}</b>", x=0.5, y=0.5, showarrow=False,
                                  font=dict(family=PF, size=18, color="#111928"))])
            st.plotly_chart(f3, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 3: Deduction Bridge ───────────────────────────────────────────────
    with tab3:
        sc, cc = st.columns([1, 4], gap="medium")
        with sc:
            st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
            bp_period = st.selectbox("Period", months_sorted[::-1] if months_sorted else ["—"], index=0)
        bp    = summary[summary["Period"] == bp_period].sum(numeric_only=True) if not summary.empty else pd.Series(dtype=float)
        gross = bp.get("Gross_Revenue", 0.0)
        net   = bp.get("Net_Revenue", 0.0)
        di    = [(l,v,c) for l,v,c in [
            ("Oil Prod. Tax",    bp.get("Oil_Tax",      0.0), "#c81e1e"),
            ("Gas Prod. Tax",    bp.get("Gas_Tax",      0.0), "#c81e1e"),
            ("Plant Prod. Tax",  bp.get("Plant_Tax",    0.0), "#c81e1e"),
            ("Compression",      bp.get("Gas_Comp",     0.0), "#b45309"),
            ("Low Vol. Fee",     bp.get("Gas_LowVol",   0.0), "#b45309"),
            ("Plant Deduction",  bp.get("Plant_Deduct", 0.0), "#b45309"),
            ("Rejected Load Fee",bp.get("Rejected_Fee", 0.0), "#d97706"),
        ] if v > 0.01]
        labels = ["Gross Revenue"] + [i[0] for i in di] + ["Net Revenue"]
        bclrs  = ["#1a56db"] + [i[2] for i in di] + ["#6c2bd9"]
        bases, bvals = [], []
        running = gross
        for idx in range(len(labels)):
            if idx == 0:          bases.append(0);       bvals.append(gross)
            elif idx == len(labels)-1: bases.append(0);  bvals.append(net)
            else:
                dv = di[idx-1][1]; bases.append(running - dv); bvals.append(dv); running -= dv
        dvals = [gross] + [-i[1] for i in di] + [net]
        with cc:
            st.markdown('<div class="panel"><div class="panel-title">Revenue Deduction Waterfall</div><div class="panel-sub">Gross → taxes → fees → net</div>', unsafe_allow_html=True)
            f4 = go.Figure()
            f4.add_bar(x=labels, y=bases, marker_color="rgba(0,0,0,0)", showlegend=False, hoverinfo="skip")
            f4.add_bar(x=labels, y=bvals, marker_color=bclrs, marker_line_width=0,
                       text=[fmt(v) for v in dvals], textposition="outside",
                       textfont=dict(family=MF, size=10, color="#374151"), showlegend=False,
                       hovertemplate="%{x}: $%{y:,.0f}<extra></extra>")
            f4.update_layout(**bl(barmode="stack", height=400, yaxis=dict(tickprefix="$", tickformat=",.0f")))
            sax(f4)
            st.plotly_chart(f4, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        ded_total = gross - net
        st.markdown(f"""
        <div class="sum-row">
          <div class="sum-cell"><div class="sum-lbl">Gross Revenue</div><div class="sum-val">{fmt(gross)}</div><div class="sum-note">Before any deductions</div></div>
          <div class="sum-cell amber"><div class="sum-lbl">Total Deductions</div><div class="sum-val">{fmt(ded_total)}</div><div class="sum-note">{f"{ded_total/gross*100:.1f}% of gross" if gross else "—"}</div></div>
          <div class="sum-cell green"><div class="sum-lbl">Net Revenue</div><div class="sum-val">{fmt(net)}</div><div class="sum-note">{f"{net/gross*100:.1f}% retained" if gross else "—"}</div></div>
        </div>""", unsafe_allow_html=True)

    # ── Tab 4: Well Rankings ──────────────────────────────────────────────────
    with tab4:
        ctrl, cc = st.columns([1, 4], gap="medium")
        with ctrl:
            st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
            top_n = st.slider("Top N wells", 5, 50, 15)
            rp    = st.selectbox("Period", ["All periods"] + (months_sorted[::-1] if months_sorted else []))
            rm    = st.radio("Metric", ["Gross Revenue","Net Revenue"])
        rdf = dff[dff["Period"] == rp].copy() if rp != "All periods" else dff.copy()
        mc  = "Gross_Revenue" if rm == "Gross Revenue" else "Net_Revenue"
        ws  = get_summary(rdf)
        wr  = ws.groupby("Well")[mc].sum().sort_values(ascending=False).head(top_n).reset_index() if not ws.empty else pd.DataFrame(columns=["Well", mc])
        with cc:
            st.markdown(f'<div class="panel"><div class="panel-title">Top {top_n} Wells — {rm}</div><div class="panel-sub">{rp}</div>', unsafe_allow_html=True)
            f5 = go.Figure(go.Bar(
                x=wr[mc] if not wr.empty else [], y=wr["Well"] if not wr.empty else [],
                orientation="h", marker_color=C["oil"] if rm=="Gross Revenue" else C["net"],
                marker_line_width=0, text=wr[mc].apply(fmt) if not wr.empty else [],
                textposition="outside", textfont=dict(family=MF, size=10),
                hovertemplate="%{y}: $%{x:,.0f}<extra></extra>",
            ))
            f5.update_layout(**bl(height=max(380, top_n*30), xaxis=dict(tickprefix="$", tickformat=",.0f"),
                                  yaxis=dict(autorange="reversed"), margin=dict(t=16,b=40,l=230,r=90)))
            sax(f5)
            st.plotly_chart(f5, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with st.expander("Full well-by-period detail"):
            ws2 = get_summary(dff)
            if ws2.empty:
                st.dataframe(pd.DataFrame(), use_container_width=True, hide_index=True)
            else:
                tbl = ws2.pivot_table(index="Well", columns="Period", values=mc, aggfunc="sum", fill_value=0).reset_index()
                tbl["Total"] = tbl.iloc[:,1:].sum(axis=1)
                tbl = tbl.sort_values("Total", ascending=False)
                for col in tbl.columns[1:]:
                    tbl[col] = tbl[col].apply(lambda v: f"${v:,.0f}" if v != 0 else "—")
                st.dataframe(tbl, use_container_width=True, hide_index=True)

    # ── Tab 5: Volumes ────────────────────────────────────────────────────────
    with tab5:
        vol = (summary.groupby("Period")
               .agg(Oil_BBL=("Oil_BBL","sum"), Gas_MCF=("Gas_MCF","sum"), Plant_GAL=("Plant_GAL","sum"))
               .reset_index().sort_values("Period"))
        st.markdown('<div class="panel"><div class="panel-title">Production Volumes</div><div class="panel-sub">Oil (BBL) · Gas (MCF) · Plant/NGL (GAL — secondary axis)</div>', unsafe_allow_html=True)
        f6 = make_subplots(specs=[[{"secondary_y": True}]])
        f6.add_bar(x=vol["Period"], y=vol["Oil_BBL"], name="Oil (BBL)", marker_color=C["oil"],  marker_line_width=0, secondary_y=False)
        f6.add_bar(x=vol["Period"], y=vol["Gas_MCF"], name="Gas (MCF)", marker_color=C["gas"],  marker_line_width=0, secondary_y=False)
        f6.add_scatter(x=vol["Period"], y=vol["Plant_GAL"], name="Plant/NGL (GAL)",
                       line=dict(color=C["plant"], width=2.5), mode="lines+markers",
                       marker=dict(size=6, color=C["plant"], line=dict(color="#fff", width=1.5)), secondary_y=True)
        f6.update_layout(**bl(barmode="group", height=380))
        tf2 = dict(family=MF, size=10, color="#9aa4b8")
        f6.update_xaxes(showgrid=False, showline=True, linecolor="#cdd2de", tickfont=tf2)
        f6.update_yaxes(title_text="BBL / MCF", showgrid=True, gridcolor=GRID, tickfont=tf2, secondary_y=False)
        f6.update_yaxes(title_text="GAL (Plant/NGL)", showgrid=False, tickfont=tf2, secondary_y=True)
        st.plotly_chart(f6, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        with st.expander("Implied realized prices"):
            rp2 = (summary.groupby("Period").agg(Oil_Rev=("Oil_Gross","sum"), Oil_BBL=("Oil_BBL","sum"),
                    Gas_Rev=("Gas_Gross","sum"), Gas_MCF=("Gas_MCF","sum")).reset_index())
            rp2["Oil $/BBL"] = (rp2["Oil_Rev"] / rp2["Oil_BBL"].replace(0, float("nan"))).round(2)
            rp2["Gas $/MCF"] = (rp2["Gas_Rev"] / rp2["Gas_MCF"].replace(0, float("nan"))).round(2)
            disp = rp2[["Period","Oil $/BBL","Gas $/MCF"]].copy()
            for col in ["Oil $/BBL","Gas $/MCF"]:
                disp[col] = disp[col].apply(lambda v: f"${v:.2f}" if pd.notna(v) else "—")
            st.dataframe(disp, use_container_width=True, hide_index=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXPENSE MODULE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with exp_tab:
    etab1, etab2, etab3, etab4 = st.tabs([
        "Expense Trend", "Bucket Breakdown", "Well Deep-Dive", "Well Rankings",
    ])

    if exp_summary.empty:
        for t in [etab1, etab2, etab3, etab4]:
            with t:
                st.info("No expense data found in the loaded GL export.")
    else:
        # ── Precompute pivot ──────────────────────────────────────────────────
        exp_trend = (exp_summary.groupby(["Period","Bucket"])["Amount"]
                     .sum().reset_index().sort_values("Period"))
        exp_period = (exp_trend.pivot_table(index="Period", columns="Bucket", values="Amount", fill_value=0)
                      .reset_index().sort_values("Period"))
        for bk in ["LOE","Leasehold","Capital","Workover"]:
            if bk not in exp_period.columns:
                exp_period[bk] = 0.0
        exp_period["Total"] = exp_period[["LOE","Leasehold","Capital","Workover"]].sum(axis=1)

        # ── Etab 1: Expense Trend ─────────────────────────────────────────────
        with etab1:
            st.markdown('<div class="panel red"><div class="panel-title">Total Expense Trend by Bucket</div><div class="panel-sub">Monthly LOE · Leasehold · Capital · Workover · total overlay</div>', unsafe_allow_html=True)
            fe1 = go.Figure()
            for bk in ["LOE","Leasehold","Capital","Workover"]:
                fe1.add_bar(x=exp_period["Period"], y=exp_period[bk], name=bk,
                            marker_color=BUCKET_COLORS[bk], marker_line_width=0)
            fe1.add_scatter(x=exp_period["Period"], y=exp_period["Total"], name="Total Expenses",
                            line=dict(color="#111928", width=2.5), mode="lines+markers",
                            marker=dict(size=6, color="#111928", line=dict(color="#fff", width=1.5)))
            fe1.update_layout(**bl(barmode="stack", height=380, yaxis=dict(tickprefix="$", tickformat=",.0f")))
            sax(fe1)
            st.plotly_chart(fe1, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Summary tiles
            loe_tot = exp_period["LOE"].sum()
            lh_tot  = exp_period["Leasehold"].sum()
            cap_tot = exp_period["Capital"].sum()
            wo_tot  = exp_period["Workover"].sum()
            all_tot = loe_tot + lh_tot + cap_tot + wo_tot
            st.markdown(f"""
            <div class="sum-row">
              <div class="sum-cell"><div class="sum-lbl">LOE (9000–9099)</div><div class="sum-val">{fmt(loe_tot)}</div><div class="sum-note">{f"{loe_tot/all_tot*100:.1f}% of total" if all_tot else "—"}</div></div>
              <div class="sum-cell amber"><div class="sum-lbl">Leasehold (9100–9199)</div><div class="sum-val">{fmt(lh_tot)}</div><div class="sum-note">{f"{lh_tot/all_tot*100:.1f}% of total" if all_tot else "—"}</div></div>
              <div class="sum-cell purple"><div class="sum-lbl">Capital (9200–9399)</div><div class="sum-val">{fmt(cap_tot)}</div><div class="sum-note">{f"{cap_tot/all_tot*100:.1f}% of total" if all_tot else "—"}</div></div>
              <div class="sum-cell red"><div class="sum-lbl">Workover (9500–9598)</div><div class="sum-val">{fmt(wo_tot)}</div><div class="sum-note">{f"{wo_tot/all_tot*100:.1f}% of total" if all_tot else "—"}</div></div>
              <div class="sum-cell teal"><div class="sum-lbl">Grand Total</div><div class="sum-val">{fmt(all_tot)}</div><div class="sum-note">{len(months_sorted)} period(s)</div></div>
            </div>""", unsafe_allow_html=True)

            with st.expander("Period data table"):
                disp = exp_period.copy()
                for col in ["LOE","Leasehold","Capital","Workover","Total"]:
                    disp[col] = disp[col].apply(lambda v: f"${v:,.0f}")
                st.dataframe(disp, use_container_width=True, hide_index=True)

        # ── Etab 2: Bucket Breakdown ──────────────────────────────────────────
        with etab2:
            ctrl2, body2 = st.columns([1, 4], gap="medium")
            with ctrl2:
                st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
                e2_period = st.selectbox("Period", ["All periods"] + (months_sorted[::-1] if months_sorted else []), key="e2p")
                e2_bucket = st.selectbox("Bucket", ["All buckets","LOE","Leasehold","Capital","Workover"], key="e2b")

            e2_df = exp_summary.copy()
            if e2_period != "All periods":
                e2_df = e2_df[e2_df["Period"] == e2_period]
            if e2_bucket != "All buckets":
                e2_df = e2_df[e2_df["Bucket"] == e2_bucket]

            # Account-level detail from raw
            e2_raw = dff[dff["Bucket"] != "Revenue"].copy()
            if e2_period != "All periods":
                e2_raw = e2_raw[e2_raw["Period"] == e2_period]
            if e2_bucket != "All buckets":
                e2_raw = e2_raw[e2_raw["Bucket"] == e2_bucket]

            acct_roll = (e2_raw.groupby(["Account","AccountDesc","Bucket"])["AmountAdj"]
                         .sum().reset_index().sort_values("AmountAdj", ascending=False))
            acct_roll = acct_roll[acct_roll["AmountAdj"].abs() > 0.01]

            with body2:
                # Pie by bucket
                L2, R2 = st.columns(2, gap="medium")
                with L2:
                    bucket_tots = e2_df.groupby("Bucket")["Amount"].sum().reset_index()
                    st.markdown('<div class="panel red"><div class="panel-title">Spend by Bucket</div><div class="panel-sub">Selected period / filter</div>', unsafe_allow_html=True)
                    fp1 = go.Figure(go.Pie(
                        labels=bucket_tots["Bucket"], values=bucket_tots["Amount"], hole=0.55,
                        marker=dict(colors=[BUCKET_COLORS.get(b,"#888") for b in bucket_tots["Bucket"]],
                                    line=dict(color="#fff", width=2)),
                        textinfo="label+percent", textfont=dict(family=MF, size=10),
                        hovertemplate="%{label}: $%{value:,.0f}<extra></extra>",
                    ))
                    tot_sel = bucket_tots["Amount"].sum()
                    fp1.update_layout(height=300, showlegend=False, paper_bgcolor=BG, margin=dict(t=8,b=8,l=16,r=16),
                        annotations=[dict(text=f"<b>{fmt(tot_sel)}</b>", x=0.5, y=0.5, showarrow=False,
                                          font=dict(family=PF, size=16, color="#111928"))])
                    st.plotly_chart(fp1, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                with R2:
                    # Top accounts bar
                    st.markdown('<div class="panel red"><div class="panel-title">Top GL Accounts</div><div class="panel-sub">By total spend</div>', unsafe_allow_html=True)
                    top_accts = acct_roll.head(15)
                    acct_labels = top_accts.apply(lambda r: f"{int(r['Account'])} – {r['AccountDesc']}" if r['AccountDesc'] else str(int(r['Account'])), axis=1)
                    fp2 = go.Figure(go.Bar(
                        x=top_accts["AmountAdj"], y=acct_labels,
                        orientation="h",
                        marker_color=[BUCKET_COLORS.get(b, "#888") for b in top_accts["Bucket"]],
                        marker_line_width=0,
                        text=top_accts["AmountAdj"].apply(fmt), textposition="outside",
                        textfont=dict(family=MF, size=10),
                        hovertemplate="%{y}: $%{x:,.0f}<extra></extra>",
                    ))
                    fp2.update_layout(**bl(height=300, xaxis=dict(tickprefix="$", tickformat=",.0f"),
                                          yaxis=dict(autorange="reversed"), margin=dict(t=8,b=32,l=200,r=80)))
                    sax(fp2)
                    st.plotly_chart(fp2, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Full account table
                with st.expander("Full GL account detail"):
                    disp2 = acct_roll.copy()
                    disp2["Amount"] = disp2["AmountAdj"].apply(lambda v: f"${v:,.0f}")
                    disp2 = disp2[["Bucket","Account","AccountDesc","Amount"]].rename(columns={"AccountDesc":"Description","AmountAdj":"_drop"})
                    disp2 = disp2.drop(columns=["_drop"], errors="ignore")
                    st.dataframe(disp2, use_container_width=True, hide_index=True)

        # ── Etab 3: Well Deep-Dive ────────────────────────────────────────────
        with etab3:
            all_exp_wells = sorted(exp_summary["Well"].unique().tolist())
            ctrl3, body3  = st.columns([1, 4], gap="medium")
            with ctrl3:
                st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
                sel_well   = st.selectbox("Well", all_exp_wells, key="e3w")
                e3_period  = st.selectbox("Period", ["All periods"] + (months_sorted[::-1] if months_sorted else []), key="e3p")

            well_exp = dff[(dff["Bucket"] != "Revenue") & (dff["Well"] == sel_well)].copy()
            if e3_period != "All periods":
                well_exp = well_exp[well_exp["Period"] == e3_period]

            with body3:
                if well_exp.empty:
                    st.info(f"No expense data for **{sel_well}** in the selected period.")
                else:
                    # Bucket totals for this well
                    wb_tots = well_exp.groupby("Bucket")["AmountAdj"].sum().reset_index()
                    wb_tot  = wb_tots["AmountAdj"].sum()

                    # KPI row for the well
                    loe_w  = wb_tots.loc[wb_tots["Bucket"]=="LOE",       "AmountAdj"].sum()
                    lh_w   = wb_tots.loc[wb_tots["Bucket"]=="Leasehold", "AmountAdj"].sum()
                    cap_w  = wb_tots.loc[wb_tots["Bucket"]=="Capital",   "AmountAdj"].sum()
                    wo_w   = wb_tots.loc[wb_tots["Bucket"]=="Workover",  "AmountAdj"].sum()

                    st.markdown(f"""
                    <div class="sum-row">
                      <div class="sum-cell"><div class="sum-lbl">LOE</div><div class="sum-val">{fmt(loe_w)}</div></div>
                      <div class="sum-cell amber"><div class="sum-lbl">Leasehold</div><div class="sum-val">{fmt(lh_w)}</div></div>
                      <div class="sum-cell purple"><div class="sum-lbl">Capital</div><div class="sum-val">{fmt(cap_w)}</div></div>
                      <div class="sum-cell red"><div class="sum-lbl">Workover</div><div class="sum-val">{fmt(wo_w)}</div></div>
                      <div class="sum-cell teal"><div class="sum-lbl">Total</div><div class="sum-val">{fmt(wb_tot)}</div></div>
                    </div>""", unsafe_allow_html=True)

                    # Stacked bar by period (if multi-period)
                    if e3_period == "All periods":
                        st.markdown('<div class="panel red"><div class="panel-title">Expense Trend — ' + sel_well + '</div><div class="panel-sub">Monthly by bucket</div>', unsafe_allow_html=True)
                        wp_trend = (well_exp.groupby(["Period","Bucket"])["AmountAdj"]
                                    .sum().reset_index().sort_values("Period"))
                        wp_piv = wp_trend.pivot_table(index="Period", columns="Bucket", values="AmountAdj", fill_value=0).reset_index()
                        for bk in ["LOE","Leasehold","Capital","Workover"]:
                            if bk not in wp_piv.columns: wp_piv[bk] = 0.0
                        fw1 = go.Figure()
                        for bk in ["LOE","Leasehold","Capital","Workover"]:
                            fw1.add_bar(x=wp_piv["Period"], y=wp_piv[bk], name=bk,
                                        marker_color=BUCKET_COLORS[bk], marker_line_width=0)
                        fw1.update_layout(**bl(barmode="stack", height=300, yaxis=dict(tickprefix="$", tickformat=",.0f")))
                        sax(fw1)
                        st.plotly_chart(fw1, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                    # Account-level line items
                    st.markdown('<div class="panel red"><div class="panel-title">GL Line Items</div><div class="panel-sub">Every charge for this well · selected period</div>', unsafe_allow_html=True)
                    acct_detail = (well_exp.groupby(["Bucket","Account","AccountDesc"])["AmountAdj"]
                                   .sum().reset_index().sort_values(["Bucket","AmountAdj"], ascending=[True,False]))
                    acct_detail = acct_detail[acct_detail["AmountAdj"].abs() > 0.01]

                    fw2 = go.Figure(go.Bar(
                        x=acct_detail["AmountAdj"],
                        y=acct_detail.apply(lambda r: f"{int(r['Account'])} – {r['AccountDesc']}" if r['AccountDesc'] else str(int(r['Account'])), axis=1),
                        orientation="h",
                        marker_color=[BUCKET_COLORS.get(b,"#888") for b in acct_detail["Bucket"]],
                        marker_line_width=0,
                        text=acct_detail["AmountAdj"].apply(fmt), textposition="outside",
                        textfont=dict(family=MF, size=10),
                        hovertemplate="%{y}: $%{x:,.0f}<extra></extra>",
                    ))
                    fw2.update_layout(**bl(height=max(320, len(acct_detail)*28),
                                          xaxis=dict(tickprefix="$", tickformat=",.0f"),
                                          yaxis=dict(autorange="reversed"),
                                          margin=dict(t=8, b=32, l=260, r=90)))
                    sax(fw2)
                    st.plotly_chart(fw2, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                    with st.expander("Raw line-item table"):
                        tbl3 = acct_detail.copy()
                        tbl3["Amount"] = tbl3["AmountAdj"].apply(lambda v: f"${v:,.0f}")
                        tbl3 = tbl3[["Bucket","Account","AccountDesc","Amount"]].rename(columns={"AccountDesc":"Description"})
                        st.dataframe(tbl3, use_container_width=True, hide_index=True)

        # ── Etab 4: Well Rankings (Expenses) ──────────────────────────────────
        with etab4:
            ctrl4, body4 = st.columns([1, 4], gap="medium")
            with ctrl4:
                st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
                e4_top   = st.slider("Top N wells", 5, 50, 15, key="e4n")
                e4_period= st.selectbox("Period", ["All periods"] + (months_sorted[::-1] if months_sorted else []), key="e4p")
                e4_bucket= st.selectbox("Bucket", ["All buckets","LOE","Leasehold","Capital","Workover"], key="e4b")

            e4_df = exp_summary.copy()
            if e4_period != "All periods":
                e4_df = e4_df[e4_df["Period"] == e4_period]
            if e4_bucket != "All buckets":
                e4_df = e4_df[e4_df["Bucket"] == e4_bucket]

            well_rank = (e4_df.groupby("Well")["Amount"].sum()
                         .sort_values(ascending=False).head(e4_top).reset_index())

            with body4:
                st.markdown(f'<div class="panel red"><div class="panel-title">Top {e4_top} Wells by Expense</div><div class="panel-sub">{e4_period} · {e4_bucket}</div>', unsafe_allow_html=True)
                if well_rank.empty:
                    st.info("No data for selected filters.")
                else:
                    fw3 = go.Figure(go.Bar(
                        x=well_rank["Amount"], y=well_rank["Well"],
                        orientation="h", marker_color=C["ded"], marker_line_width=0,
                        text=well_rank["Amount"].apply(fmt), textposition="outside",
                        textfont=dict(family=MF, size=10),
                        hovertemplate="%{y}: $%{x:,.0f}<extra></extra>",
                    ))
                    fw3.update_layout(**bl(height=max(380, e4_top*30),
                                          xaxis=dict(tickprefix="$", tickformat=",.0f"),
                                          yaxis=dict(autorange="reversed"),
                                          margin=dict(t=16,b=40,l=230,r=90)))
                    sax(fw3)
                    st.plotly_chart(fw3, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

                with st.expander("Full well-by-period expense detail"):
                    e4_full = exp_summary.copy()
                    if e4_bucket != "All buckets":
                        e4_full = e4_full[e4_full["Bucket"] == e4_bucket]
                    if e4_full.empty:
                        st.dataframe(pd.DataFrame(), use_container_width=True, hide_index=True)
                    else:
                        tbl4 = e4_full.pivot_table(index="Well", columns="Period", values="Amount",
                                                   aggfunc="sum", fill_value=0).reset_index()
                        tbl4["Total"] = tbl4.iloc[:,1:].sum(axis=1)
                        tbl4 = tbl4.sort_values("Total", ascending=False)
                        for col in tbl4.columns[1:]:
                            tbl4[col] = tbl4[col].apply(lambda v: f"${v:,.0f}" if v != 0 else "—")
                        st.dataframe(tbl4, use_container_width=True, hide_index=True)
