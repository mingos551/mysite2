import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
from streamlit_folium import folium_static
from PIL import Image
import math
import base64

image = Image.open('DWELL_MATCHO.jpg')
st.set_page_config(
    page_title="DWELL MATCHO",
    page_icon=image,)

# 背景画像の指定
def add_bg_from_file():
    image_path = "DWELL_MATCHO.jpg"
    bg_color = f"background-image: url('data:image/png;base64,{base64.b64encode(open(image_path, 'rb').read()).decode()}');"
    bg_style = f"""
        <style>
        .stApp {{
            {bg_color}
            background-repeat: no-repeat;
            background-position: right center;
            background-attachment: fixed;
            background-size: contain;
        }}
        </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

add_bg_from_file()

# ジムの情報をcsvファイルから読み込む
gyms = pd.read_csv('ptT3.csv', encoding='utf-8')

# 物件のダミー情報をcsvファイルから読み込む
properties = pd.read_csv('ochiai02.csv', encoding='shift_jis')

# 地図を作成 (中野区の中心を初期表示)
m = folium.Map(location=[35.7060, 139.6650], zoom_start=15)

# サイドバーでタンニングマシーンが必要かどうかを選択
tanning_required = st.sidebar.checkbox("Tanning Machine Required")

# タンニングマシーンが必要な場合、リストをフィルタリング
if tanning_required:
    gyms = gyms[gyms['tanning'] == 1]

# ジムを選択するためのドロップダウンメニュー
selected_gym = st.selectbox("Select a Gym:", gyms['店舗名'].tolist(), key='gym_selectbox')


# 選択されたジムの情報を取得
gym_info = gyms[gyms['店舗名'] == selected_gym].iloc[0]

# 選択されたジムを青色のピンで表示
folium.Marker(
    location=[gym_info['緯度'], gym_info['経度']],
    popup=folium.Popup(f"<b>{gym_info['店舗名']}</b><br>{gym_info['住所']}", parse_html=True),
    icon=folium.Icon(color="blue")
).add_to(m)

# サイドバーで家賃の範囲を調節
rent_range = st.sidebar.slider("Rent Range (in 10,000 yen units):", min_value=0.0, max_value=30.0, value=(0.0, 30.0), step=0.1)

# サイドバーで徒歩圏内を選択 (5分=0.4km, 10分=0.8km, 15分=1.2km)
walking_distance = st.sidebar.selectbox("Walking Distance:", ["5 minutes", "10 minutes", "15 minutes"])
walking_distance_km = {"5 minutes": 0.4, "10 minutes": 0.8, "15 minutes": 1.2}[walking_distance]

# 周囲の物件を赤色のピンで表示
def haversine(lat1, lon1, lat2, lon2):
    # 地球の半径 (km)
    R = 6371
    # 緯度、経度をラジアンに変換
    try:
        lat1, lon1, lat2, lon2 = map(math.radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    except ValueError:
        st.error("Error converting latitude and longitude to numbers. Please check the data.")
        return 0
    # haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    return distance

for index, row in properties.iterrows():
    try:
        lat = float(row['Latitude'])
        lon = float(row['Longitude'])
        rent = float(row['Rent'])
    except ValueError:
        st.error("Error converting latitude, longitude, or rent to numbers in property data.")
        continue

    name = row['PropertyName']
    address = row['Address']
    layout = row['Arrangement']
    url = row['URL']

    # 徒歩圏内かつ家賃が範囲内の物件のみ表示
    if haversine(lat, lon, gym_info['緯度'], gym_info['経度']) < walking_distance_km and rent_range[0] <= rent <= rent_range[1]:
        folium.Marker(
            location=[lat, lon],
            # 家賃を小数点第一位まで表示
            popup=folium.Popup(f'<b>{name}</b><br>{address}<br>{layout}<br>{rent:.1f}万円<br><a href="{url}" target="_blank">View Property</a>', parse_html=True),
            icon=folium.Icon(color="red")
        ).add_to(m)

# 地図を表示
folium_static(m)
