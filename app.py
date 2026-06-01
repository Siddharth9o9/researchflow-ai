import streamlit as st
import time
from pipeline import run_research_pipeline

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent AI Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #0a0a0f;
    --surface:   #111118;
    --border:    #1e1e2e;
    --accent:    #00e5ff;
    --accent2:   #7c3aed;
    --warn:      #f59e0b;
    --success:   #10b981;
    --text:      #e2e8f0;
    --muted:     #64748b;
    --mono:      'Space Mono', monospace;
    --sans:      'Syne', sans-serif;
}

/* ── Global resets ── */
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1100px; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 1rem 2.5rem;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(0,229,255,0.07) 0%, transparent 70%);
    pointer-events: none;
}
.hero-label {
    font-family: var(--mono);
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.hero h1 {
    font-family: var(--sans) !important;
    font-size: clamp(2rem, 5vw, 3.4rem) !important;
    font-weight: 800 !important;
    line-height: 1.1 !important;
    background: linear-gradient(135deg, #fff 30%, var(--accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 !important;
}
.hero-sub {
    margin-top: 1rem;
    color: var(--muted);
    font-size: 0.95rem;
    letter-spacing: 0.02em;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1.5rem 0;
}

/* ── Input card ── */
.input-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
}

/* ── Override Streamlit text input ── */
.stTextInput > div > div > input {
    background: #0d0d16 !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color .2s;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,229,255,0.08) !important;
}
.stTextInput label { color: var(--muted) !important; font-size: 0.8rem !important; letter-spacing: .08em; text-transform: uppercase; }

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent2), #4f46e5) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: var(--sans) !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: .04em;
    padding: 0.7rem 2.2rem !important;
    transition: opacity .2s, transform .15s !important;
    width: 100%;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── Pipeline step cards ── */
.step-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: border-color .3s;
}
.step-card.active  { border-color: var(--accent);  box-shadow: 0 0 16px rgba(0,229,255,.1); }
.step-card.done    { border-color: var(--success); }
.step-card.pending { opacity: 0.45; }

.step-icon {
    width: 38px; height: 38px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
}
.step-icon.active  { background: rgba(0,229,255,.12);  }
.step-icon.done    { background: rgba(16,185,129,.12); }
.step-icon.pending { background: rgba(100,116,139,.08); }

.step-meta { flex: 1; }
.step-name {
    font-family: var(--sans);
    font-weight: 700;
    font-size: 0.9rem;
    margin: 0;
}
.step-desc {
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--muted);
    margin-top: 2px;
}
.step-badge {
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: .06em;
    padding: 3px 10px;
    border-radius: 20px;
}
.badge-active  { background: rgba(0,229,255,.12);  color: var(--accent);  }
.badge-done    { background: rgba(16,185,129,.12); color: var(--success); }
.badge-pending { background: rgba(100,116,139,.08); color: var(--muted); }

/* ── Result tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 10px 10px 0 0 !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
    padding: 0 0.5rem !important;
}
.stTabs [data-baseweb="tab"] {
    color: var(--muted) !important;
    font-family: var(--sans) !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: .04em !important;
    padding: 0.75rem 1.2rem !important;
    border-radius: 0 !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom-color: var(--accent) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    padding: 1.5rem !important;
}

/* ── Content boxes ── */
.content-box {
    background: #0d0d16;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    font-family: var(--mono);
    font-size: 0.8rem;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 420px;
    overflow-y: auto;
    color: #cbd5e1;
}
.content-box::-webkit-scrollbar { width: 4px; }
.content-box::-webkit-scrollbar-track { background: transparent; }
.content-box::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

/* ── Report box ── */
.report-box {
    background: #0d0d16;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.8rem 2rem;
    font-family: var(--sans);
    font-size: 0.92rem;
    line-height: 1.8;
    color: var(--text);
    max-height: 520px;
    overflow-y: auto;
}
.report-box::-webkit-scrollbar { width: 4px; }
.report-box::-webkit-scrollbar-track { background: transparent; }
.report-box::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

/* ── Feedback box ── */
.feedback-box {
    background: rgba(245,158,11,.04);
    border: 1px solid rgba(245,158,11,.2);
    border-radius: 8px;
    padding: 1.4rem 1.6rem;
    font-family: var(--sans);
    font-size: 0.9rem;
    line-height: 1.75;
    color: #fde68a;
    max-height: 420px;
    overflow-y: auto;
}

/* ── Stat strip ── */
.stat-strip {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}
.stat-pill {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--muted);
    display: flex; align-items: center; gap: 0.5rem;
}
.stat-val { color: var(--accent); font-weight: 700; }

/* ── Error box ── */
.error-box {
    background: rgba(239,68,68,.05);
    border: 1px solid rgba(239,68,68,.25);
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    color: #fca5a5;
    font-family: var(--mono);
    font-size: 0.82rem;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────
STEPS = [
    ("🔍", "Search Agent",  "Retrieving recent, reliable information from the web"),
    ("📄", "Reader Agent",  "Scraping the most relevant URL for deep content"),
    ("✍️",  "Writer Chain", "Drafting a structured research report"),
    ("🧠", "Critic Chain",  "Reviewing and scoring the report quality"),
]

def render_pipeline(active: int):
    """Render the 4-step pipeline tracker. active=-1 means all pending."""
    for i, (icon, name, desc) in enumerate(STEPS):
        if active == -1:
            state_cls, badge_cls, badge_txt = "pending", "badge-pending", "WAITING"
        elif i < active:
            state_cls, badge_cls, badge_txt = "done",    "badge-done",    "DONE ✓"
        elif i == active:
            state_cls, badge_cls, badge_txt = "active",  "badge-active",  "RUNNING…"
        else:
            state_cls, badge_cls, badge_txt = "pending", "badge-pending", "WAITING"

        st.markdown(f"""
        <div class="step-card {state_cls}">
            <div class="step-icon {state_cls}">{icon}</div>
            <div class="step-meta">
                <p class="step-name">{name}</p>
                <p class="step-desc">{desc}</p>
            </div>
            <span class="step-badge {badge_cls}">{badge_txt}</span>
        </div>
        """, unsafe_allow_html=True)


def run_with_progress(topic: str):
    """Run pipeline and stream step-by-step progress into the UI."""
    from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

    state = {}
    pipeline_slot = st.empty()
    status_slot   = st.empty()

    def update(step, msg=""):
        with pipeline_slot.container():
            render_pipeline(step)
        if msg:
            status_slot.markdown(
                f'<p style="font-family:var(--mono);font-size:0.72rem;color:var(--muted);margin-top:.4rem">⟶ {msg}</p>',
                unsafe_allow_html=True
            )

    # Step 0 — Search
    update(0, "Sending query to search agent…")
    search_agent  = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = search_result["messages"][-1].content
    update(0, "Search complete.")
    time.sleep(0.3)

    # Step 1 — Reader
    update(1, "Picking top URL and scraping…")
    reader_agent  = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"Pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search results:\n{state['search_results'][:800]}"
        )]
    })
    state["scraped_content"] = reader_result["messages"][-1].content
    update(1, "Scraping complete.")
    time.sleep(0.3)

    # Step 2 — Writer
    update(2, "Drafting full research report…")
    research_combined = (
        f"Search Results:\n{state['search_results']}\n\n"
        f"Detailed Scraped Content:\n{state['scraped_content']}"
    )
    state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})
    update(2, "Report drafted.")
    time.sleep(0.3)

    # Step 3 — Critic
    update(3, "Running critic review…")
    state["feedback"] = critic_chain.invoke({"report": state["report"]})
    update(3, "Review complete.")
    time.sleep(0.3)

    # All done
    with pipeline_slot.container():
        for i, (icon, name, desc) in enumerate(STEPS):
            st.markdown(f"""
            <div class="step-card done">
                <div class="step-icon done">{icon}</div>
                <div class="step-meta">
                    <p class="step-name">{name}</p>
                    <p class="step-desc">{desc}</p>
                </div>
                <span class="step-badge badge-done">DONE ✓</span>
            </div>
            """, unsafe_allow_html=True)
    status_slot.empty()

    return state


# ── Layout ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <p class="hero-label">// An Autonomous Multi-Agent AI Research System</p>
    <h1>ResearchFlow.AI </h1>
    <p class="hero-sub">Search → Scrape → Write → Critique &nbsp;|&nbsp; Powered by LangChain agents</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.6], gap="large")

with col_left:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing in drug discovery",
        key="topic_input",
    )
    run_btn = st.button("🚀  Launch Pipeline", key="run_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("#### Pipeline Steps")
    pipeline_placeholder = st.empty()
    with pipeline_placeholder.container():
        render_pipeline(-1)

with col_right:
    results_placeholder = st.empty()

    if not st.session_state.get("results"):
        with results_placeholder.container():
            st.markdown("""
            <div style="height:340px;display:flex;flex-direction:column;align-items:center;
                        justify-content:center;background:var(--surface);border:1px solid var(--border);
                        border-radius:12px;color:var(--muted);text-align:center;gap:0.7rem;">
                <span style="font-size:2.5rem">🔬</span>
                <p style="font-family:var(--mono);font-size:0.75rem;letter-spacing:.08em;">
                    AWAITING TOPIC INPUT
                </p>
                <p style="font-size:0.8rem;max-width:280px;line-height:1.6;">
                    Enter a research topic on the left and launch the pipeline to see results here.
                </p>
            </div>
            """, unsafe_allow_html=True)

# ── Run pipeline ─────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic before launching.")
    else:
        # Clear old results
        st.session_state["results"] = None
        results_placeholder.empty()

        with col_left:
            # Replace static pipeline with live tracker
            pipeline_placeholder.empty()
            try:
                results = run_with_progress(topic.strip())
                st.session_state["results"] = results
                st.session_state["topic"]   = topic.strip()
                st.session_state["elapsed"] = True
            except Exception as e:
                st.markdown(f'<div class="error-box">❌ Pipeline error: {e}</div>', unsafe_allow_html=True)

# ── Display results ───────────────────────────────────────────────────────────
results = st.session_state.get("results")
if results:
    saved_topic = st.session_state.get("topic", topic)

    with col_right:
        results_placeholder.empty()
        word_count  = len(results.get("report", "").split())
        search_len  = len(results.get("search_results", ""))
        scraped_len = len(results.get("scraped_content", ""))

        st.markdown(f"""
        <div class="stat-strip">
            <div class="stat-pill">📝 Report words <span class="stat-val">{word_count:,}</span></div>
            <div class="stat-pill">🔍 Search chars <span class="stat-val">{search_len:,}</span></div>
            <div class="stat-pill">📄 Scraped chars <span class="stat-val">{scraped_len:,}</span></div>
        </div>
        """, unsafe_allow_html=True)

        tab_report, tab_search, tab_scraped, tab_feedback = st.tabs(
            ["📋 Final Report", "🔍 Search Results", "📄 Scraped Content", "🧠 Critic Feedback"]
        )

        with tab_report:
            st.markdown(
                f'<div class="report-box">{results.get("report", "No report generated.")}</div>',
                unsafe_allow_html=True,
            )
            st.download_button(
                "⬇  Download Report",
                data=results.get("report", ""),
                file_name=f"report_{saved_topic[:30].replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with tab_search:
            st.markdown(
                f'<div class="content-box">{results.get("search_results", "No search results.")}</div>',
                unsafe_allow_html=True,
            )

        with tab_scraped:
            st.markdown(
                f'<div class="content-box">{results.get("scraped_content", "No scraped content.")}</div>',
                unsafe_allow_html=True,
            )

        with tab_feedback:
            st.markdown(
                f'<div class="feedback-box">{results.get("feedback", "No feedback available.")}</div>',
                unsafe_allow_html=True,
            )