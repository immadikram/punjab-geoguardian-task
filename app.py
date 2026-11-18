"""Punjab GeoGuardian – Streamlit dashboard.
Run:  streamlit run app.py   (put the Colab 'outputs' folder next to this file, or set GEOGUARDIAN_OUT)"""
import json, os
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

OUT = os.environ.get('GEOGUARDIAN_OUT', 'outputs')
st.set_page_config(page_title='Punjab GeoGuardian', page_icon='🛰️', layout='wide')

if not os.path.exists(f'{OUT}/config.json'):
    st.error(f'Folder "{OUT}" not found. Copy the Colab outputs folder here or set GEOGUARDIAN_OUT.'); st.stop()
cfg = json.load(open(f'{OUT}/config.json'))
y1, y2 = cfg['y1'], cfg['y2']

st.title('🛰️ Punjab GeoGuardian')
st.caption('AI-based monitoring of urban expansion and farmland loss using Sentinel-2. '
           'Learning prototype – not an official government system; all results are estimated / possible changes.')

st.sidebar.header('Area of Interest')
st.sidebar.write(f"**{cfg['aoi_name']}**")
st.sidebar.write(f"BBox: {cfg['bbox']}")
st.sidebar.write(f"Cloud filter: < {cfg['cloud_max']}%")
year = st.sidebar.selectbox('Year', [y1, y2], index=1)
st.sidebar.write('Date range:', cfg['dates'][str(year)])

def show(path, caption):
    p = f'{OUT}/maps/{path}.png'
    if os.path.exists(p): st.image(p, caption=caption, use_container_width=True)
    else: st.warning(f'{path}.png missing')

def read(name):
    p = f'{OUT}/{name}'
    return pd.read_csv(p) if os.path.exists(p) else None

tabs = st.tabs(['Maps', 'Change detection', 'Statistics', 'Validation', 'Interactive map', 'Observations'])

with tabs[0]:
    st.subheader(f'Satellite layers – {year}')
    a, b = st.columns(2)
    with a: show(f'rgb_{year}', f'RGB {year}')
    with b: show(f'class_{year}', f'Land cover {year}')
    c, d = st.columns(2)
    with c: show(f'ndvi_{year}', f'NDVI {year}')
    with d: show(f'ndbi_{year}', f'NDBI {year}')

with tabs[1]:
    st.subheader(f'Possible agriculture → urban conversion ({y1} → {y2})')
    a, b = st.columns([2, 1])
    with a: show('change', 'Red = possible conversion')
    with b:
        hs = read('hotspots.csv')
        if hs is not None: st.write('Top hotspot cells (1 sq km)'); st.dataframe(hs, hide_index=True)

with tabs[2]:
    st.subheader('Area statistics')
    s = read('area_stats.csv')
    if s is not None: st.dataframe(s, hide_index=True, use_container_width=True)
    show('area_chart', 'Area by class')

with tabs[3]:
    mp = f'{OUT}/metrics.json'
    if os.path.exists(mp):
        m = json.load(open(mp))
        c1, c2, c3, c4 = st.columns(4)
        c1.metric('Points checked', m['n']); c2.metric('Correct', m['correct'])
        c3.metric('Accuracy %', m['accuracy']); c4.metric('Kappa', m['kappa'])
    v = read('validation_results.csv')
    if v is not None: st.write('Validation table'); st.dataframe(v, hide_index=True, use_container_width=True)
    e = read('error_analysis.csv')
    if e is not None: st.write('Error analysis'); st.dataframe(e, hide_index=True, use_container_width=True)

with tabs[4]:
    p = f'{OUT}/interactive_map.html'
    if os.path.exists(p): components.html(open(p, encoding='utf-8').read(), height=650, scrolling=True)
    else: st.warning('interactive_map.html missing')

with tabs[5]:
    p = f'{OUT}/observations.md'
    st.markdown(open(p, encoding='utf-8').read() if os.path.exists(p) else 'No observations yet.')
