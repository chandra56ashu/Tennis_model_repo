# =========================================================
# TENNIS MATCH WINNER PREDICTION APP
# GRAND SLAM CLASSIC STREAMLIT DASHBOARD
# =========================================================

import streamlit as st
import pandas as pd
import joblib

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Tennis Match Winner Prediction",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# LOAD SAVED ARTIFACT
# =========================================================
@st.cache_resource
def load_artifact():
    return joblib.load("tennis_app_artifact.pkl")

artifact = load_artifact()
model = artifact["model"]
all_features = artifact["all_features"]
category_options = artifact["category_options"]

# =========================================================
# CUSTOM CSS - GRAND SLAM CLASSIC
# =========================================================
st.markdown("""
<style>
    :root {
        --bg-main: #0B0E14;
        --bg-card: #1C222D;
        --bg-soft: #111827;
        --primary: #005DAA;
        --secondary: #002D55;
        --accent: #E1FF00;
        --text-main: #F4F7F6;
        --text-soft: #C7D0D9;
        --border: rgba(255,255,255,0.08);
        --success: #35C759;
    }

    .stApp {
        background:
            radial-gradient(circle at top right, rgba(225,255,0,0.08), transparent 22%),
            radial-gradient(circle at top left, rgba(0,93,170,0.22), transparent 30%),
            linear-gradient(135deg, #0B0E14 0%, #111827 45%, #0B0E14 100%);
        color: var(--text-main);
    }

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1400px;
    }

    .hero-box {
        background: linear-gradient(135deg, rgba(0,45,85,0.98), rgba(0,93,170,0.96));
        border: 1px solid rgba(225,255,0,0.18);
        border-radius: 26px;
        padding: 1.7rem 1.8rem;
        margin-bottom: 1.35rem;
        box-shadow: 0 18px 40px rgba(0,0,0,0.32);
    }

    .main-title {
        font-size: 2.8rem;
        font-weight: 900;
        color: #FFFFFF;
        margin-bottom: 0.2rem;
        letter-spacing: 0.2px;
        line-height: 1.1;
    }

    .sub-text {
        font-size: 1.05rem;
        color: #EAF1F7;
        margin-bottom: 0.35rem;
        line-height: 1.5;
    }

    .tiny-note {
        color: #D6E1EA;
        font-size: 0.93rem;
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 800;
        margin-top: 0.85rem;
        margin-bottom: 0.8rem;
        color: var(--text-main);
    }

    .player-card {
        background: linear-gradient(180deg, rgba(28,34,45,0.98), rgba(17,24,39,0.98));
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 1.25rem;
        min-height: 430px;
        box-shadow: 0 14px 30px rgba(0,0,0,0.28);
    }

    .player-label {
        font-size: 0.86rem;
        color: #9CC8F0;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.2rem;
        font-weight: 800;
    }

    .player-name {
        font-size: 1.8rem;
        font-weight: 900;
        color: #FFFFFF;
        margin-bottom: 0.7rem;
    }

    .vs-box {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 430px;
    }

    .vs-pill {
        background: linear-gradient(135deg, var(--accent), #C4E800);
        color: #0B0E14;
        font-size: 1.55rem;
        font-weight: 900;
        padding: 1rem 1.4rem;
        border-radius: 999px;
        box-shadow: 0 12px 24px rgba(0,0,0,0.28);
        text-align: center;
        border: 2px solid rgba(255,255,255,0.08);
    }

    .context-card {
        background: linear-gradient(180deg, rgba(28,34,45,0.98), rgba(17,24,39,0.98));
        border: 1px solid var(--border);
        border-radius: 22px;
        padding: 1.2rem;
        margin-top: 1rem;
        box-shadow: 0 12px 24px rgba(0,0,0,0.22);
    }

    .result-card {
        background: linear-gradient(180deg, rgba(28,34,45,1), rgba(17,24,39,1));
        border: 1px solid rgba(225,255,0,0.16);
        border-left: 6px solid var(--accent);
        border-radius: 22px;
        padding: 1.4rem;
        margin-top: 1rem;
        box-shadow: 0 16px 34px rgba(0,0,0,0.3);
    }

    .result-title {
        font-size: 1.2rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 0.5rem;
    }

    .winner-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--accent), #C4E800);
        color: #0B0E14;
        font-weight: 900;
        font-size: 1rem;
        padding: 0.7rem 1rem;
        border-radius: 14px;
        margin: 0.45rem 0 0.9rem 0;
        box-shadow: 0 8px 18px rgba(0,0,0,0.2);
    }

    .stat-chip {
        display: inline-block;
        padding: 0.5rem 0.85rem;
        margin: 0.22rem 0.35rem 0.22rem 0;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 999px;
        color: var(--text-main);
        font-size: 0.92rem;
        font-weight: 600;
    }

    .footer-note {
        color: #B9C6D3;
        font-size: 0.92rem;
        margin-top: 1rem;
    }

    label, .stMarkdown, .stCaption, .stText, .stMetricLabel {
        color: var(--text-main) !important;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input {
        background-color: #0F1722 !important;
        color: #F4F7F6 !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 12px !important;
    }

    div[data-testid="stSelectbox"] > div {
        background-color: transparent !important;
        color: #F4F7F6 !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #0F1722 !important;
        color: #F4F7F6 !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 12px !important;
    }

    div.stButton > button {
        width: 100%;
        height: 3.2rem;
        font-size: 1rem;
        font-weight: 900;
        border-radius: 999px;
        border: none;
        color: #0B0E14;
        background: linear-gradient(135deg, var(--accent), #C4E800);
        box-shadow: 0 12px 24px rgba(0,0,0,0.24);
    }

    div.stButton > button:hover {
        filter: brightness(1.03);
        transform: translateY(-1px);
    }

    div[data-testid="metric-container"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        padding: 0.8rem 1rem !important;
        border-radius: 16px !important;
    }

    div[data-testid="metric-container"] * {
        color: #F4F7F6 !important;
    }

    div[data-testid="metric-container"] label,
    div[data-testid="metric-container"] p,
    div[data-testid="metric-container"] span {
        color: #F4F7F6 !important;
        opacity: 1 !important;
    }

    div[data-testid="metric-container"] > div {
        color: #F4F7F6 !important;
    }

    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #E1FF00 !important;
        font-weight: 900 !important;
        font-size: 2rem !important;
        line-height: 1.1 !important;
        opacity: 1 !important;
    }

    div[data-testid="metric-container"] [data-testid="stMetricLabel"] {
        color: #F4F7F6 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        opacity: 1 !important;
    }

    div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }

    div[data-testid="stCaptionContainer"] p,
    [data-testid="stCaptionContainer"] {
        color: #D6E1EA !important;
        opacity: 1 !important;
        font-size: 0.9rem !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        overflow: hidden;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0E1520 0%, #111827 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] * {
        color: #F4F7F6 !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero-box">
    <div class="main-title">🎾 Tennis Match Winner Prediction</div>
    <div class="sub-text">
         Tennis analytics dashboard for predicting the likely winner between two players before the match begins.
    </div>
    <div class="tiny-note">
        This app is for academic use only built for Dr. Vineet Agarwal by his students - S489801, S477223, S481517, S487932
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.header("Dashboard Info")
    st.write("""
This dashboard estimates the likely winner using:

- Player rankings
- ATP points
- Betting odds
- Indoor condition
- Surface
- Tournament series
- Match round
    """)
    st.markdown("---")
    st.write("**Prediction Labels**")
    st.write("- Class 1 = Player 1 wins")
    st.write("- Class 0 = Player 2 wins")
    st.markdown("---")
    st.caption("Built for academic demonstration and portfolio showcase.")

# =========================================================
# PLAYER INPUT AREA
# =========================================================
st.markdown('<div class="section-title">Enter Match Inputs</div>', unsafe_allow_html=True)

left, middle, right = st.columns([4, 1.15, 4], vertical_alignment="center")

with left:
    st.markdown("""
        <div class="player-label">Competitor A</div>
    """, unsafe_allow_html=True)

    player_1_name = st.text_input("Player 1 Name", value="Player 1")

    st.markdown(
        f'<div class="player-name">{player_1_name if player_1_name.strip() else "Player 1"}</div>',
        unsafe_allow_html=True
    )

    rank_1 = st.number_input(
        "Player 1 Rank",
        min_value=1,
        max_value=5000,
        value=50,
        step=1
    )

    pts_1 = st.number_input(
        "Player 1 ATP Points",
        min_value=0,
        max_value=50000,
        value=1000,
        step=10
    )

    odd_1 = st.number_input(
        "Player 1 Betting Odds",
        min_value=1.01,
        max_value=100.0,
        value=1.80,
        step=0.01,
        format="%.2f"
    )

    st.markdown("</div>", unsafe_allow_html=True)

with middle:
    st.markdown("""
    <div class="vs-box">
        <div class="vs-pill">VS</div>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
        <div class="player-label">Competitor B</div>
    """, unsafe_allow_html=True)

    player_2_name = st.text_input("Player 2 Name", value="Player 2")

    st.markdown(
        f'<div class="player-name">{player_2_name if player_2_name.strip() else "Player 2"}</div>',
        unsafe_allow_html=True
    )

    rank_2 = st.number_input(
        "Player 2 Rank",
        min_value=1,
        max_value=5000,
        value=60,
        step=1
    )

    pts_2 = st.number_input(
        "Player 2 ATP Points",
        min_value=0,
        max_value=50000,
        value=900,
        step=10
    )

    odd_2 = st.number_input(
        "Player 2 Betting Odds",
        min_value=1.01,
        max_value=100.0,
        value=2.10,
        step=0.01,
        format="%.2f"
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# MATCH CONTEXT
# =========================================================
st.markdown('<div class="section-title">Match Context</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    is_indoor = st.selectbox(
        "Indoor Match",
        options=[0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )

with c2:
    surface = st.selectbox(
        "Surface",
        options=category_options["Surface"]
    )

with c3:
    series = st.selectbox(
        "Tournament Series",
        options=category_options["Series"]
    )

with c4:
    round_name = st.selectbox(
        "Match Round",
        options=category_options["Round"]
    )

# =========================================================
# BACKEND FEATURE ENGINEERING
# =========================================================
rank_diff = rank_2 - rank_1
pts_diff = pts_1 - pts_2
odd_diff = odd_2 - odd_1

input_df = pd.DataFrame([{
    "Rank_Diff": rank_diff,
    "Pts_Diff": pts_diff,
    "Odd_Diff": odd_diff,
    "Is_Indoor": is_indoor,
    "Surface": surface,
    "Series": series,
    "Round": round_name
}])

input_df = input_df[all_features]

player_1_display = player_1_name.strip() if player_1_name.strip() else "Player 1"
player_2_display = player_2_name.strip() if player_2_name.strip() else "Player 2"

# =========================================================
# QUICK PREVIEW STRIP
# =========================================================
st.markdown('<div class="section-title">Computed Match Indicators</div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <span class="stat-chip">{player_1_display}</span>
    <span class="stat-chip">{player_2_display}</span>
    <span class="stat-chip">Rank_Diff: {rank_diff}</span>
    <span class="stat-chip">Pts_Diff: {pts_diff}</span>
    <span class="stat-chip">Odd_Diff: {odd_diff:.2f}</span>
    <span class="stat-chip">Indoor: {'Yes' if is_indoor == 1 else 'No'}</span>
    <span class="stat-chip">Surface: {surface}</span>
    <span class="stat-chip">Series: {series}</span>
    <span class="stat-chip">Round: {round_name}</span>
    """,
    unsafe_allow_html=True
)

# =========================================================
# PREDICTION BUTTON
# =========================================================
predict_btn = st.button("Predict Match Winner")

# =========================================================
# PREDICTION OUTPUT
# =========================================================
if predict_btn:
    prediction = model.predict(input_df)[0]
    prediction_proba = model.predict_proba(input_df)[0]

    prob_player2 = float(prediction_proba[0])
    prob_player1 = float(prediction_proba[1])

    predicted_winner = player_1_display if prediction == 1 else player_2_display

    st.markdown("""
    <div class="result-card">
        <div class="result-title">Prediction Result</div>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="winner-badge">Predicted Winner: {predicted_winner}</div>',
        unsafe_allow_html=True
    )

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(f"{player_1_display} Win Probability", f"{prob_player1:.2%}")
    with m2:
        st.metric(f"{player_2_display} Win Probability", f"{prob_player2:.2%}")
    with m3:
        st.metric("Confidence Gap", f"{abs(prob_player1 - prob_player2):.2%}")

    st.progress(int(prob_player1 * 100))
    st.caption(f"Progress bar represents {player_1_display} win probability.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Prediction Interpretation</div>', unsafe_allow_html=True)

    if abs(prob_player1 - prob_player2) < 0.08:
        st.info(
            f"This looks like a closely balanced match between {player_1_display} and {player_2_display}. "
            "The model sees only a small gap between the two players."
        )
    elif prediction == 1:
        st.success(
            f"The model favors {player_1_display} based on the combined effect of rankings, ATP points, betting odds, and match context."
        )
    else:
        st.success(
            f"The model favors {player_2_display} based on the combined effect of rankings, ATP points, betting odds, and match context."
        )

    t1, t2 = st.columns(2)

    with t1:
        st.markdown("### User Input Summary")
        summary_df = pd.DataFrame({
            "Input Variable": [
                "Player 1 Name", "Player 2 Name",
                "Player 1 Rank", "Player 2 Rank",
                "Player 1 ATP Points", "Player 2 ATP Points",
                "Player 1 Betting Odds", "Player 2 Betting Odds",
                "Indoor Match", "Surface", "Tournament Series", "Match Round"
            ],
            "Value": [
                player_1_display, player_2_display,
                rank_1, rank_2,
                pts_1, pts_2,
                odd_1, odd_2,
                "Yes" if is_indoor == 1 else "No",
                surface, series, round_name
            ]
        })
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

    with t2:
        st.markdown("### Engineered Features Used by Model")
        engineered_df = pd.DataFrame({
            "Feature": ["Rank_Diff", "Pts_Diff", "Odd_Diff", "Is_Indoor", "Surface", "Series", "Round"],
            "Value": [rank_diff, pts_diff, odd_diff, is_indoor, surface, series, round_name]
        })
        st.dataframe(engineered_df, use_container_width=True, hide_index=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.markdown(
    """
    <div class="footer-note">
        This dashboard is intended for academic demonstration only.
        It showcases how a machine learning model can be deployed in a user-facing sports analytics application.
    </div>
    """,
    unsafe_allow_html=True
)
