import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(page_title="YouTube Channel Data Visualizer", layout="wide")

# Load the CSV file
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        # Convert published_at to datetime
        df['published_at'] = pd.to_datetime(df['published_at'])
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return None

# File path to your CSV
file_path = "latest_videos.csv"  # Update with your file path if needed
df = load_data(file_path)

# Check if data loaded successfully
if df is None:
    st.stop()

# App title
st.title("YouTube Channel Data Visualizer")

# Sidebar for channel selection
st.sidebar.header("Select Channel")
channel_names = df['channel_name'].unique()
selected_channel = st.sidebar.selectbox("Choose a channel", channel_names)

# Filter data for the selected channel
channel_data = df[df['channel_name'] == selected_channel]

# Display basic stats
st.header(f"Channel: {selected_channel}")
st.subheader("Basic Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Videos", len(channel_data))
col2.metric("Total Views", f"{channel_data['view_count'].sum():,}")
col3.metric("Total Likes", f"{channel_data['like_count'].sum():,}")

# Visualization 1: Views and Likes over Time
st.subheader("Views and Likes Over Time")
fig1 = make_subplots(specs=[[{"secondary_y": True}]])
fig1.add_trace(
    go.Scatter(
        x=channel_data['published_at'],
        y=channel_data['view_count'],
        name="Views",
        line=dict(color="#1f77b4"),
    ),
    secondary_y=False,
)
fig1.add_trace(
    go.Scatter(
        x=channel_data['published_at'],
        y=channel_data['like_count'],
        name="Likes",
        line=dict(color="#ff7f0e"),
    ),
    secondary_y=True,
)
fig1.update_layout(
    title="Views and Likes Over Time",
    xaxis_title="Published Date",
    yaxis_title="Views",
    yaxis2_title="Likes",
    template="plotly_dark",
    hovermode="x unified",
)
st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Top 5 Videos by Views
st.subheader("Top 5 Videos by Views")
top_videos = channel_data.nlargest(5, 'view_count')[['video_title', 'view_count']]
fig2 = px.bar(
    top_videos,
    x='view_count',
    y='video_title',
    orientation='h',
    title="Top 5 Videos by Views",
    template="plotly_dark",
    color_discrete_sequence=["#1f77b4"],
)
fig2.update_layout(yaxis={'tickmode': 'linear'}, showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

# Visualization 3: Views vs Likes Scatter Plot
st.subheader("Views vs Likes")
fig3 = px.scatter(
    channel_data,
    x='view_count',
    y='like_count',
    hover_data=['video_title', 'published_at'],
    title="Views vs Likes",
    template="plotly_dark",
    color_discrete_sequence=["#1f77b4"],
)
st.plotly_chart(fig3, use_container_width=True)

# Display raw data (optional)
if st.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.dataframe(channel_data)