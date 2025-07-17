import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.set_page_config(page_title="PHÂN TÍCH KÊNH ĐỐI THỦ", layout='wide')

@st.cache_data
def load_data(path):
    try:
        df = pd.read_csv(path)
        df['published_at'] = pd.to_datetime(df['published_at'])
        return df
    except Exception as e:
        print(f'Error when load csv: {e}')
        return None

file_path = 'latest_videos.csv'
df = load_data(file_path)

if df is None:
    st.stop()

st.title('Trực quan hóa dữ liệu kênh YouTube')

st.sidebar.header('Chọn Kênh')
channel_names = df['channel_name'].unique()
selected_channels = st.sidebar.multiselect('Chọn một hoặc nhiều kênh', channel_names, default=[channel_names[0]])

channel_data = df[df['channel_name'].isin(selected_channels)]

if not selected_channels:
    st.warning("Vui lòng chọn ít nhất một kênh.")
    st.stop()


st.header(f'Kênh: {", ".join(selected_channels)}')
st.subheader("Thống Kê Cơ Bản")
cols = st.columns(len(selected_channels))
for i, channel in enumerate(selected_channels):
    channel_subset = channel_data[channel_data['channel_name'] == channel]
    with cols[i]:
        st.metric(f"Tổng Videos ({channel})", len(channel_subset))
        st.metric(f"Tổng Lượt Xem ({channel})", f"{channel_subset['view_count'].sum():,}")
        st.metric(f"Tổng Lượt Thích ({channel})", f"{channel_subset['like_count'].sum():,}")

st.subheader("Lượng Views và Likes Theo Thời Gian")
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

colors = ['#02acf5', '#f54302', '#00cc96', '#ff6692']  
for i, channel in enumerate(selected_channels):
    channel_subset = channel_data[channel_data['channel_name'] == channel]
    fig1.add_trace(
        go.Scatter(
            x=channel_subset['published_at'],
            y=channel_subset['view_count'],
            name=f"Lượt Xem ({channel})",
            line=dict(color=colors[i % len(colors)]),
            hovertemplate=f'%{{y:,d}} Views',
        ),
        secondary_y=False,
    )
    fig1.add_trace(
        go.Scatter(
            x=channel_subset['published_at'],
            y=channel_subset['like_count'],
            name=f"Lượt Thích ({channel})",
            line=dict(color=colors[(i + 1) % len(colors)], dash='dash'),
            hovertemplate=f'%{{y:,d}} Likes',
        ),
        secondary_y=True,
    )

fig1.update_layout(
    title="Lượt Xem và Lượt Thích Theo Từng Video",
    xaxis_title="Thời Gian Published",
    yaxis_title="Lượt Xem",
    yaxis2_title="Lượt Thích",
    template='plotly_dark',
    hovermode='x unified',
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Top 10 Videos Nhiều Lượt Xem Nhất")
top_vids = channel_data.nlargest(10, 'view_count')[['video_title', 'view_count', 'channel_name']]
fig2 = px.bar(
    top_vids,
    x='view_count',
    y='video_title',
    color='channel_name',
    orientation='h',
    title="Top 10 Videos Nhiều Lượt Xem Nhất",
    template='plotly_dark',
    color_discrete_sequence=colors,
)
fig2.update_layout(
    yaxis={'tickmode': 'linear'},
    xaxis_tickformat=',d',
    showlegend=True,
    legend_title_text="Kênh"
)
st.plotly_chart(fig2, use_container_width=True)


st.subheader("Lượt Xem và Lượt Thích")
fig3 = px.scatter(
    channel_data,
    x="view_count",
    y="like_count",
    color="channel_name",
    hover_data=['video_title', 'published_at'],
    title='Lượt Xem và Lượt Thích',
    template='plotly_dark',
    color_discrete_sequence=colors,
)
fig3.update_layout(
    xaxis_tickformat=',d',
    yaxis_tickformat=',d',
    legend_title_text="Kênh"
)
st.plotly_chart(fig3, use_container_width=True)

if st.checkbox("Hiển thị dữ liệu gốc"):
    st.subheader("Dữ liệu gốc")
    st.dataframe(channel_data)