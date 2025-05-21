# pip install -r requirements.txt
# streamlit run app.py
import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import locale
from babel.dates import format_date

# leer la data
df = pd.read_excel('Adidas.xlsx')
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top: 3rem;}</style>', unsafe_allow_html=True)
imagen = Image.open('logo-adidas-2.PNG')

col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image(imagen, width=150)

titulo_html = """
<style> .title-test { font-weight: bold; padding: 5px; border-radius: 6px } </style>
<center><h1 class="title-test">Dashboard Interactivo de Ventas</h1></center>

"""

with col2:
    st.markdown(titulo_html, unsafe_allow_html=True)

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

col3, col4, col5 = st.columns([0.1, 0.45, 0.45])
with col3:
    today = datetime.datetime.now()
    box_date = format_date(today, format='d MMMM y', locale='es')
    st.write(f"Actualizado el:  \n {box_date}")

with col4:
    fig = px.bar(df, x = 'Retailer', y = 'TotalSales', labels={'TotalSales': 'Total Ventas {$}', 'Retailer': 'Vendedor'},
                 title = "Total de Ventas por Vendedor", hover_data=['TotalSales'],
                 template='gridon', height=500)
    st.plotly_chart(fig, use_container_width=True)

_, view1, dwn1, view2, dwn2 = st.columns([0.15, 0.20, 0.20, 0.20, 0.20])

with view1:
    expander = st.expander('Detalles de Ventas por Vendedor')
    data = df[['Retailer', 'TotalSales']].groupby(by='Retailer')['TotalSales'].sum().reset_index()
    data['TotalSales'] = data['TotalSales'].map('{:,.0f}'.format)
    expander.write(data)
with dwn1: 
    st.download_button("Descargar CSV", data.to_csv().encode('utf-8'), "ventas_por_vendedor.csv", mime="text/csv")

df["Month_Year"] = df["InvoiceDate"].dt.strftime("%b/%y")
result = df.groupby(by = df['Month_Year'])['TotalSales'].sum().reset_index()

with col5:
    fig1 = px.line(result, x = 'Month_Year', y = 'TotalSales', labels={'TotalSales': 'Total Ventas {$}', 'Month_Year': 'Mes/Año'},
                     title = "Total de Ventas por Mes", template='gridon')
    st.plotly_chart(fig1, use_container_width=True)

with view2:
    expander = st.expander('Detalles de Ventas por Mes')
    data = result.copy()
    data['TotalSales'] = data['TotalSales'].map('{:,.0f}'.format)
    expander.write(data)
with dwn2:
    st.download_button("Descargar CSV", data = data.to_csv().encode('utf-8'), 
                       file_name="ventas_por_mes.csv", mime="text/csv")
    
st.divider()

result1 = df.groupby(by = "State")[["TotalSales", "UnitsSold"]].sum().reset_index()

# agregar como line chart
fig3 = go.Figure()
fig3.add_trace(go.Bar(x = result1['State'], y = result1['TotalSales'], name = 'Total Sales'))
fig3.add_trace(go.Scatter(x = result1['State'], y = result1['UnitsSold'], mode = 'lines',
                          name = 'Unidades Vendidas', yaxis = 'y2'))

fig3.update_layout(
    title = "Total de Ventas y Unidades Vendidas por Estado",
    xaxis = dict(title = 'Estado'),
    yaxis = dict(title = "Total Ventas {$}", showgrid = False),
    yaxis2 = dict(title = "Unidades Vendidas", overlaying = 'y',side = 'right'),
    template='gridon',
    legend = dict(x = 1, y = 1),
)

_, col6 = st.columns([0.1, 1])
with col6:
    st.plotly_chart(fig3, use_container_width=True)

_, view3, dwn3 = st.columns([0.5, 0.45, 0.45])
with view3:
    expander = st.expander('Detalles de Ventas y Unidades Vendidas por Estado')
    data = result1.copy()
    data['TotalSales'] = data['TotalSales'].map('{:,.0f}'.format)
    data['UnitsSold'] = data['UnitsSold'].map('{:,.0f}'.format)
    expander.write(data)

with dwn3:
    st.download_button("Descargar CSV", data = result1.to_csv().encode('utf-8'), 
                       file_name="ventas_y_unidades_por_estado.csv", mime="text/csv")
    
st.divider()

_, col7 = st.columns([0.1, 1])
treemap = df[['Region', 'City', 'TotalSales']].groupby(by = ['Region', 'City'])['TotalSales'].sum().reset_index()
def format_sales(value):
    if value >= 0:
        return '{:.2f} Lakh'.format(value / 1_000_00)

treemap['TotalSales (Formatted)'] = treemap['TotalSales'].apply(format_sales)
fig4 = px.treemap(treemap, path=['Region', 'City'], values='TotalSales',
                  hover_name = 'TotalSales (Formatted)',
                  hover_data = ['TotalSales (Formatted)'],
                  color = 'City', height = 700, width = 600)
fig4.update_traces(textinfo = 'label+value')

with col7:
    st.subheader("Treemap de Ventas por Ciudad y Región")
    st.plotly_chart(fig4, use_container_width=True)

_, view4, dwn4 = st.columns([0.5, 0.45, 0.45])
with view4:
    result2 = df[['Region', 'City', 'TotalSales']].groupby(by = ['Region', 'City'])['TotalSales'].sum()
    result2 = result2.apply(lambda x: '{:,.0f}'.format(x))  
    expander = st.expander('Detalles de Ventas por Ciudad y Región')
    expander.write(result2)
with dwn4:
    st.download_button("Descargar CSV", data = result2.to_csv().encode('utf-8'), 
                       file_name="ventas_por_region_y_ciudad.csv", mime="text/csv")
    
_, view5, dwn5 = st.columns([0.5, 0.45, 0.45])
with view5:
    expander = st.expander('Ver Datos Originales de Ventas')
    expander.write(df)
with dwn5:
    st.download_button("Descargar Datos Originales", data = df.to_csv().encode('utf-8'), 
                       file_name="datos_ventas_originales.csv", mime="text/csv")

st.divider()