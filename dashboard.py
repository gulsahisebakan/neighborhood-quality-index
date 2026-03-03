import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

# ── 1. PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Neighborhood Quality-of-Life Index",
    page_icon="🏙️",
    layout="wide"
)

# ── 2. LOAD DATA ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("neighborhoods.csv")

df = load_data()

# Factor definitions — used throughout the dashboard
FACTORS = {
    "crime_safety":   "🔒 Crime Safety",
    "school_quality": "🎓 School Quality",
    "transit_access": "🚌 Transit Access",
    "air_quality":    "💨 Air Quality",
    "walkability":    "🚶 Walkability",
    "green_space":    "🌳 Green Space",
}

# ── 3. HEADER ─────────────────────────────────────────────────────────────────
st.title("🏙️ Neighborhood Quality-of-Life Index")
st.markdown("*Compare neighborhoods across safety, schools, transit, air quality, walkability and green space*")
st.divider()

# ── 4. SIDEBAR — WEIGHT CUSTOMIZER ───────────────────────────────────────────
# This is the standout feature — users can adjust how much each factor matters
st.sidebar.title("⚖️ Customize Your Priorities")
st.sidebar.markdown("*Adjust weights to match what matters most to you*")

weights = {}
for factor, label in FACTORS.items():
    weights[factor] = st.sidebar.slider(
        label,
        min_value=0.0,
        max_value=1.0,
        value=0.25 if factor == "crime_safety" else
              0.20 if factor == "school_quality" else
              0.15,
        step=0.05
    )

# Recalculate livability scores based on user weights
def recalculate_scores(df, weights):
    total_weight = sum(weights.values())
    if total_weight == 0:
        return df.copy()
    # Normalize weights so they always add up to 1
    normalized = {k: v / total_weight for k, v in weights.items()}
    df = df.copy()
    df["livability_score"] = df.apply(
        lambda row: round(sum(row[f] * w for f, w in normalized.items()), 1),
        axis=1
    )
    df["rank"] = df["livability_score"].rank(ascending=False).astype(int)
    return df.sort_values("livability_score", ascending=False).reset_index(drop=True)

df_weighted = recalculate_scores(df, weights)

st.sidebar.divider()
st.sidebar.markdown("**Total weight:** " + str(round(sum(weights.values()), 2)))
st.sidebar.markdown("*Weights are automatically normalized*")

# ── 5. KPI CARDS ──────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Neighborhoods Analyzed", len(df_weighted))
col2.metric("🏆 Best Neighborhood",   df_weighted.iloc[0]["neighborhood"])
col3.metric("📊 Avg Livability Score", f"{df_weighted['livability_score'].mean():.1f}")
col4.metric("⚠️ Lowest Score",        f"{df_weighted['livability_score'].min():.1f}")

st.divider()

# ── 6. INTERACTIVE MAP ────────────────────────────────────────────────────────
st.subheader("🗺️ Neighborhood Map")
st.markdown("*Circle size and color represent livability score — click any marker for details*")

# Create folium map centered on our city
m = folium.Map(
    location=[41.88, -87.65],
    zoom_start=11,
    tiles="CartoDB dark_matter"
)

# Add a circle marker for each neighborhood
for _, row in df_weighted.iterrows():
    # Color based on score: red=low, yellow=medium, green=high
    if row["livability_score"] >= 70:
        color = "#2ecc71"    # green
    elif row["livability_score"] >= 55:
        color = "#f39c12"    # orange
    else:
        color = "#e74c3c"    # red

    # Circle size based on score
    radius = int(row["livability_score"] * 0.4)

    # Popup shows full neighborhood details when clicked
    popup_html = f"""
    <div style='font-family: Arial; min-width: 200px'>
        <h4 style='color: {color}; margin: 0'>{row['neighborhood']}</h4>
        <hr style='margin: 5px 0'>
        <b>🏆 Livability Score: {row['livability_score']}</b><br>
        <b>Rank: #{row['rank']} of {len(df_weighted)}</b><br><br>
        🔒 Crime Safety: {row['crime_safety']}<br>
        🎓 School Quality: {row['school_quality']}<br>
        🚌 Transit Access: {row['transit_access']}<br>
        💨 Air Quality: {row['air_quality']}<br>
        🚶 Walkability: {row['walkability']}<br>
        🌳 Green Space: {row['green_space']}<br><br>
        🏠 Median Home Price: ${row['median_home_price']:,}
    </div>
    """

    folium.CircleMarker(
        location=[row["lat"], row["lng"]],
        radius=radius,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=f"{row['neighborhood']} — Score: {row['livability_score']}"
    ).add_to(m)

# Display map in Streamlit
st_folium(m, width=None, height=500)

st.divider()

# ── 7. RANKINGS CHART ─────────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🏆 Livability Rankings")
    fig_rank = px.bar(
        df_weighted,
        x="livability_score",
        y="neighborhood",
        orientation="h",
        color="livability_score",
        color_continuous_scale="RdYlGn",
        labels={"livability_score": "Score", "neighborhood": ""},
        text="livability_score"
    )
    fig_rank.update_traces(texttemplate="%{text}", textposition="outside")
    fig_rank.update_layout(
        coloraxis_showscale=False,
        yaxis={"categoryorder": "total ascending"},
        height=500
    )
    st.plotly_chart(fig_rank, use_container_width=True)

with col_right:
    st.subheader("📊 Factor Breakdown")
    # Let user select a neighborhood to see its radar chart
    selected_hood = st.selectbox(
        "Select neighborhood to inspect:",
        df_weighted["neighborhood"].tolist()
    )

    hood_data = df_weighted[df_weighted["neighborhood"] == selected_hood].iloc[0]

    # Radar chart showing all 6 factors
    factor_scores = [hood_data[f] for f in FACTORS.keys()]
    factor_labels = list(FACTORS.values())

    fig_radar = go.Figure(data=go.Scatterpolar(
        r=factor_scores + [factor_scores[0]],
        theta=factor_labels + [factor_labels[0]],
        fill="toself",
        fillcolor="rgba(46, 204, 113, 0.3)",
        line=dict(color="#2ecc71", width=2),
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=400,
        title=f"{selected_hood} — Factor Profile"
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # Show home price
    st.metric(
        "🏠 Median Home Price",
        f"${hood_data['median_home_price']:,}"
    )

st.divider()

# ── 8. NEIGHBORHOOD COMPARISON ────────────────────────────────────────────────
st.subheader("⚖️ Compare Two Neighborhoods")

col_a, col_b = st.columns(2)
with col_a:
    hood_a = st.selectbox("Neighborhood A", df_weighted["neighborhood"].tolist(), index=0)
with col_b:
    hood_b = st.selectbox("Neighborhood B", df_weighted["neighborhood"].tolist(), index=1)

data_a = df_weighted[df_weighted["neighborhood"] == hood_a].iloc[0]
data_b = df_weighted[df_weighted["neighborhood"] == hood_b].iloc[0]

# Build comparison bar chart
factors_list = list(FACTORS.keys())
labels_list  = list(FACTORS.values())

fig_compare = go.Figure()
fig_compare.add_trace(go.Bar(
    name=hood_a,
    x=labels_list,
    y=[data_a[f] for f in factors_list],
    marker_color="#3498db"
))
fig_compare.add_trace(go.Bar(
    name=hood_b,
    x=labels_list,
    y=[data_b[f] for f in factors_list],
    marker_color="#e74c3c"
))
fig_compare.update_layout(
    barmode="group",
    yaxis=dict(range=[0, 100], title="Score"),
    height=400
)
st.plotly_chart(fig_compare, use_container_width=True)

# Winner summary
st.markdown(f"""
| Factor | {hood_a} | {hood_b} | Winner |
|--------|---------|---------|--------|
| 🔒 Crime Safety | {data_a['crime_safety']} | {data_b['crime_safety']} | {'✅ ' + hood_a if data_a['crime_safety'] > data_b['crime_safety'] else '✅ ' + hood_b} |
| 🎓 School Quality | {data_a['school_quality']} | {data_b['school_quality']} | {'✅ ' + hood_a if data_a['school_quality'] > data_b['school_quality'] else '✅ ' + hood_b} |
| 🚌 Transit Access | {data_a['transit_access']} | {data_b['transit_access']} | {'✅ ' + hood_a if data_a['transit_access'] > data_b['transit_access'] else '✅ ' + hood_b} |
| 💨 Air Quality | {data_a['air_quality']} | {data_b['air_quality']} | {'✅ ' + hood_a if data_a['air_quality'] > data_b['air_quality'] else '✅ ' + hood_b} |
| 🚶 Walkability | {data_a['walkability']} | {data_b['walkability']} | {'✅ ' + hood_a if data_a['walkability'] > data_b['walkability'] else '✅ ' + hood_b} |
| 🌳 Green Space | {data_a['green_space']} | {data_b['green_space']} | {'✅ ' + hood_a if data_a['green_space'] > data_b['green_space'] else '✅ ' + hood_b} |
| 🏠 Home Price | ${data_a['median_home_price']:,} | ${data_b['median_home_price']:,} | {'✅ ' + hood_a if data_a['median_home_price'] < data_b['median_home_price'] else '✅ ' + hood_b} |
""")

st.divider()

# ── 9. RAW DATA TABLE ─────────────────────────────────────────────────────────
st.subheader("📋 Full Neighborhood Data")
st.dataframe(
    df_weighted[[
        "rank", "neighborhood", "livability_score",
        "crime_safety", "school_quality", "transit_access",
        "air_quality", "walkability", "green_space", "median_home_price"
    ]],
    use_container_width=True,
    height=400
)