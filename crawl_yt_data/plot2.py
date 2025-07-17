import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


#set page configuration
st.set_page_config(page_title="PHÂN TÍCH KÊNH ĐỐI THỦ", layout = 'wide')

#load csv
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

#stop if df is empty
if df is None:
    st.stop()


st.title('Trực quan hóa dữ liệu kênh youtube')

st.sidebar.header('Chọn Kênh')
channel_names = df['channel_name'].unique()
selected_channel = st.sidebar.selectbox('Chọn một kênh', channel_names)

channel_data = df[df['channel_name'] == selected_channel]

st.header(f'Kênh: {selected_channel}')
st.subheader("Thống Kê Cơ Bản")
col1, col2, col3 = st.columns(3)
col1.metric("Tổng Videos", len(channel_data))
col2.metric("Tổng Lượt Xem", f"{channel_data['view_count'].sum():,}")
col3.metric("Tổng Lượt Thích", f"{channel_data['like_count'].sum():,}")

# visualize1
st.subheader("Lượng Views và Likes")
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(
    go.Scatter(
        x=channel_data['published_at'],
        y=channel_data['view_count'],
        name="Lượt Xem",
        line=dict(color = '#02acf5'),
        hovertemplate='%{y:,d} Views',
    ),
    secondary_y=False,
)

fig1.add_trace(
    go.Scatter(
        x=channel_data['published_at'],
        y=channel_data['like_count'],
        name="Lượt Thích",
        line=dict(color = '#f54302'),
        hovertemplate= '%{y:,d} Likes',
    ),
    secondary_y=True, #choose likes data to be second y axis
)

fig1.update_layout(
    title = "Lượt Xem Và Lượt Thích Theo Từng Video",
    xaxis_title = "Thời Gian Published",
    yaxis_title = "Lượt Xem",
    yaxis2_title="Lượt Thích",
    template='plotly_dark',
    hovermode = 'x unified',
)
st.plotly_chart(fig1, use_container_width=True)

#visualization 2
st.subheader("Top 10 Videos Nhiều Lượt Xem Nhất")
top_vids = channel_data.nlargest(10, 'view_count')[['video_title','view_count']]
fig2 = px.bar(
    top_vids,
    x='view_count',
    y='video_title',
    orientation='h',
    title="Top 10 Videos Nhiều Lượt Xem Nhất",
    template='plotly_dark',
    color_discrete_sequence=['#0277f5'],

)
fig2.update_layout(yaxis={'tickmode': 'linear'},
                    xaxis_tickformat=',d',
                    showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

#visualization 3
st.subheader("Lượt Xem và Lượt Thích")
fig3 = px.scatter(
    channel_data,
    x="view_count",
    y="like_count",
    hover_data=['video_title','published_at'],
    title = 'Lượt Xem và Lượt Thích',
    template='plotly_dark',
    color_discrete_sequence= ['#a802f5'],
)
fig3.update_layout(xaxis_tickformat=',d', yaxis_tickformat=',d')
st.plotly_chart(fig3, use_container_width=True)


if st.checkbox("Hiển thị dữ liệu gốc"):
    st.subheader("Dữ liệu gốc")
    st.dataframe(channel_data)
