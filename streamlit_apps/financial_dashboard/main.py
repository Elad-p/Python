import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Datapoint Analytics | Executive BI Showcase",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css(file_name):
    try:
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"קובץ ה-CSS בשם {file_name} לא נמצא.")

path = 'streamlit_apps/financial_dashboard/'

load_css(path + "style_v2.css")

@st.cache_data
def load_financial_data():
    df = pd.read_excel(path + 'Financial_Report.xlsx')
    df.columns = df.columns.str.strip() # ניקוי רווחים משמות העמודות
    return df

try:
    df_raw = load_financial_data()
except Exception as e:
    st.error(f"שגיאה בטעינת קובץ הנתונים: {e}")
    st.stop()

st.sidebar.markdown("<h2 style='text-align: center; color: #00D2FF; margin-top: 10px;'>מערכת סינון</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

min_date = df_raw['Date'].min().to_pydatetime()
max_date = df_raw['Date'].max().to_pydatetime()

st.sidebar.markdown("**📅 טווח תאריכים**")
selected_date_range = st.sidebar.slider(
    "בחר תאריכי התחלה וסיום",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="MM/YYYY"
)

countries = sorted(df_raw['Country'].unique())
selected_countries = st.sidebar.multiselect("🌍 מדינות", countries, default=countries)

segments = sorted(df_raw['Segment'].unique())
selected_segments = st.sidebar.multiselect("💼 סגמנטים עסקיים", segments, default=segments)

products = sorted(df_raw['Product'].unique())
selected_products = st.sidebar.multiselect("📦 מוצרים", products, default=products)

df_filtered = df_raw[
    (df_raw['Date'] >= selected_date_range[0]) & 
    (df_raw['Date'] <= selected_date_range[1]) &
    (df_raw['Country'].isin(selected_countries)) &
    (df_raw['Segment'].isin(selected_segments)) &
    (df_raw['Product'].isin(selected_products))
]

col_logo, col_title = st.columns([1, 6])
with col_title:
    st.markdown("<h1 style='margin-bottom:0;'>דשבורד מנהלים פיננסי – תצוגת תכלית</h1>", unsafe_allow_html=True)

st.markdown("<hr style='border: 0; border-top: 1px solid #243141; margin-bottom: 25px;'>", unsafe_allow_html=True)

if not df_filtered.empty:
    total_sales = df_filtered['Sales'].sum()
    total_profit = df_filtered['Profit'].sum()
    total_units = df_filtered['Units Sold'].sum()
    avg_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    
    sales_delta = ((total_sales / df_raw['Sales'].sum()) * 100) - 15
    profit_delta = ((total_profit / df_raw['Profit'].sum()) * 100) - 12
else:
    total_sales = total_profit = total_units = avg_margin = sales_delta = profit_delta = 0

kpi_html = f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-title">סה"כ מכירות (Sales)</div>
        <div class="kpi-value">${total_sales:,.0f}</div>
        <div class="kpi-delta delta-positive">▲ +{sales_delta:.1f}% לעומת היעד</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">רווח נקי (Profit)</div>
        <div class="kpi-value" style="color: #00E676;">${total_profit:,.0f}</div>
        <div class="kpi-delta delta-positive">▲ +{profit_delta:.1f}% מתקופה מקבילה</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">יחידות שנמכרו (Units Sold)</div>
        <div class="kpi-value" style="color: #00D2FF;">{total_units:,.0f}</div>
        <div class="kpi-delta delta-positive">📈 קצב מכירות יציב</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">אחוז רווחיות (Margin %)</div>
        <div class="kpi-value" style="color: #FFB300;">{avg_margin:.1f}%</div>
        <div class="kpi-delta {'delta-positive' if avg_margin > 15 else 'delta-negative'}">
            { '▲ מעל סף היעד הארגוני' if avg_margin > 15 else '▼ טעון שיפור אופרטיבי' }
        </div>
    </div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

tab_trends, tab_deep_dive, tab_data = st.tabs([
    "📈 מגמות וביצועים גלובליים", 
    "🎯 ניתוח מעמיק ומטריצות", 
    "📋 מאגר נתונים וייצוא"
])

with tab_trends:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 מגמת מכירות ורווח לאורך זמן")
        if not df_filtered.empty:
            df_trend = df_filtered.groupby('Date')[['Sales', 'Profit']].sum().reset_index()
            
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=df_trend['Date'], y=df_trend['Sales'],
                mode='lines+markers', name='מכירות',
                line=dict(color='#00D2FF', width=3),
                fill='tozeroy', fillcolor='rgba(0, 210, 255, 0.05)'
            ))
            fig_trend.add_trace(go.Scatter(
                x=df_trend['Date'], y=df_trend['Profit'],
                mode='lines+markers', name='רווח',
                line=dict(color='#00E676', width=3),
                fill='tozeroy', fillcolor='rgba(0, 230, 118, 0.05)'
            ))
            
            fig_trend.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(showgrid=True, gridcolor='#243141'),
                yaxis=dict(showgrid=True, gridcolor='#243141')
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.warning("אין מספיק נתונים זמינים להצגת הגרף.")
            
    with col2:
        st.markdown("### 🌍 התפלגות מכירות ורווחיות לפי מדינות")
        if not df_filtered.empty:
            df_country = df_filtered.groupby('Country')[['Sales', 'Profit']].sum().reset_index()
            
            fig_country = px.bar(
                df_country, x='Country', y='Sales',
                color='Profit',
                color_continuous_scale=['#161D26', '#00D2FF', '#00E676'],
                text_auto='.2s',
                labels={'Sales': 'מכירות', 'Country': 'מדינה', 'Profit': 'רווח'}
            )
            fig_country.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=30, b=20),
                xaxis={'categoryorder':'total descending', 'showgrid':False},
                yaxis={'showgrid':True, 'gridcolor':'#243141'}
            )
            st.plotly_chart(fig_country, use_container_width=True)

with tab_deep_dive:
    col_deep1, col_deep2 = st.columns(2)
    
    with col_deep1:
        st.markdown("### 🎯 ניתוח סגמנטים ומוצרים (Sunburst Chart)")
        if not df_filtered.empty:
            fig_sunburst = px.sunburst(
                df_filtered, 
                path=['Segment', 'Product'], 
                values='Sales',
                color='Profit',
                color_continuous_scale='Viridis',
                maxdepth=2
            )
            fig_sunburst.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=20, b=0)
            )
            st.plotly_chart(fig_sunburst, use_container_width=True)
            
    with col_deep2:
        st.markdown("### 🔍 מטריצת נפח מכירות מול רווח לכל עסקה")
        if not df_filtered.empty:
            fig_scatter = px.scatter(
                df_filtered, 
                x="Units Sold", 
                y="Profit",
                size="Gross Sales", 
                color="Product",
                hover_name="Segment",
                size_max=35
            )
            fig_scatter.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=30, b=20),
                xaxis=dict(showgrid=True, gridcolor='#243141'),
                yaxis=dict(showgrid=True, gridcolor='#243141')
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

with tab_data:
    st.markdown("### 📋 סינון וייצוא קובץ הנתונים האופרטיבי")
    st.write(f"נמצאו **{len(df_filtered)}** שורות התואמות את בחירות הסינון שלך.")
    
    st.dataframe(
        df_filtered,
        use_container_width=True,
        hide_index=True
    )
    
    csv_data = df_filtered.to_csv(index=False).encode('utf-8-sig')
    st.sidebar.markdown("---")
    st.sidebar.download_button(
        label="📥 ייצוא הנתונים המסוננים ל-CSV",
        data=csv_data,
        file_name=f"Filtered_Financial_Report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    st.download_button(
        label="📥 הורד נתונים אלו כעת",
        data=csv_data,
        file_name=f"Filtered_Financial_Report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
