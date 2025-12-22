import streamlit as st
import os
import random
import time
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Product Pulse | Ethereal",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# 2. SUBTLE LUXURY CSS ENGINE
# =====================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&family=Inter:wght@300;400;600&display=swap');

    /* --- GLOBAL THEME: Deep Charcoal & Champagne --- */
    :root {
        --bg-deep: #0f1115;
        --bg-card: rgba(255, 255, 255, 0.03);
        --accent: #d4c5a8; /* Champagne Gold */
        --accent-glow: rgba(212, 197, 168, 0.3);
        --text-main: #e6e6e6;
        --text-muted: #8c8c8c;
    }

    body {
        background-color: var(--bg-deep);
        color: var(--text-main);
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1a1d26 0%, #0f1115 100%);
        background-attachment: fixed;
    }

    /* --- ANIMATED STARDUST BACKGROUND --- */
    .stApp::before {
        content: "";
        position: absolute;
        width: 100%; height: 100%;
        background-image: 
            radial-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px);
        background-size: 40px 40px;
        opacity: 0.4;
        z-index: 0;
        animation: floatStars 100s linear infinite;
        pointer-events: none;
    }

    @keyframes floatStars {
        0% { transform: translateY(0); }
        100% { transform: translateY(-100px); }
    }

    /* --- HEADERS --- */
    h1, h2, h3, h4 {
        font-family: 'Outfit', sans-serif;
        font-weight: 300;
        letter-spacing: 1px;
        color: var(--accent) !important;
    }

    /* --- ETHEREAL GLASS CARDS --- */
    .ethereal-card {
        background: var(--bg-card);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 0;
        margin-bottom: 24px;
        transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }

    .ethereal-card:hover {
        transform: translateY(-6px);
        border-color: var(--accent);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4), 0 0 20px var(--accent-glow);
    }

    /* --- SOFT SHINE EFFECT --- */
    .ethereal-card::after {
        content: "";
        position: absolute;
        top: 0; left: -100%;
        width: 50%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
        transform: skewX(-25deg);
        transition: 0.6s;
        pointer-events: none;
    }

    .ethereal-card:hover::after {
        left: 150%;
        transition: 0.8s ease-in-out;
    }

    /* --- IMAGES --- */
    .card-img {
        width: 100%;
        height: 200px;
        object-fit: cover;
        opacity: 0.85;
        transition: 0.4s;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .ethereal-card:hover .card-img {
        opacity: 1;
        transform: scale(1.03);
    }

    /* --- CONTENT & TYPOGRAPHY --- */
    .card-content { padding: 18px; }
    
    .card-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        color: white;
        margin-bottom: 8px;
    }
    
    .card-price {
        font-family: 'Outfit', sans-serif;
        font-size: 1.25rem;
        color: var(--accent);
        font-weight: 400;
    }

    /* --- BUTTONS --- */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: var(--text-main);
        font-family: 'Outfit', sans-serif;
        font-weight: 400;
        letter-spacing: 0.5px;
        transition: 0.4s;
        border-radius: 8px;
    }
    
    div.stButton > button:hover {
        background: var(--accent);
        color: #0f1115 !important;
        border-color: var(--accent);
        box-shadow: 0 0 15px var(--accent-glow);
    }

    /* --- CUSTOM SCROLLBAR --- */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0f1115; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent); }

    /* --- METRICS --- */
    [data-testid="stMetricValue"] {
        color: var(--accent) !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 300;
    }
    [data-testid="stMetricLabel"] { color: var(--text-muted); }

    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. INITIALIZATION
# =====================================================
if 'booted' not in st.session_state:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
        <div style='height:80vh; display:flex; flex-direction:column; justify-content:center; align-items:center;'>
            <h2 style='color:#d4c5a8; letter-spacing:4px; font-weight:300;'>PRODUCT PULSE</h2>
            <div style='width:100px; height:1px; background:#333; margin:20px 0; overflow:hidden;'>
                <div style='width:100%; height:100%; background:#d4c5a8; animation: shimmer 2s infinite;'></div>
            </div>
            <p style='color:#666; font-size:0.8rem; letter-spacing:2px;'>ESTABLISHING SECURE CONNECTION</p>
        </div>
        <style> @keyframes shimmer { 0% {transform:translateX(-100%)} 100% {transform:translateX(100%)} } </style>
        """, unsafe_allow_html=True)
        time.sleep(2.0)
        placeholder.empty()
        st.session_state.booted = True

# =====================================================
# 4. DATA LOGIC
# =====================================================
PRODUCTS_DIR = "images_processed/products"
CATEGORIES_DIR = "images_processed/categories"

CATEGORY_KEYWORDS = {
    "accessories": ["wallet", "wine", "jewellery"], "art_supplies": ["sketch", "tattoo", "craft"],
    "audio": ["headphone", "speaker"], "automotive": ["car", "tire", "scanner", "mount"],
    "baby": ["baby"], "beauty": ["hair", "face"], "books": ["book", "novel"],
    "clothing": ["tshirt", "jeans", "sweatshirt"], "electronics": ["laptop", "smartphone", "tablet", "air_fryer", "charging"],
    "fitness": ["dumbbell", "yoga", "band"], "food": ["coffee", "honey", "protein"],
    "furniture": ["desk", "chair"], "gaming": ["gaming"], "health": ["thermo", "pressure"],
    "home_kitchen": ["cookware", "mixer", "kettle"], "lighting": ["lamp", "light"],
    "office_supplies": ["desk_organizer", "memory"], "outdoor": ["camping", "hiking"],
    "personal_care": ["toothbrush", "groom"], "pet_supplies": ["pet", "dog"],
    "photography": ["dslr", "tripod"], "security": ["cctv", "lock"], "storage": ["packing", "storage"],
    "tools": ["screwdriver", "drone"], "toys": ["toy", "chess", "remote"],
    "travel": ["travel", "bag"], "wearable_tech": ["watch"]
}

REVIEWS = ["Exceptional quality.", "Elegant design.", "Highly refined.", "Premium experience.", "Worth the investment.", "Flawless finish.", "Top tier utility.", "Aesthetic perfection.", "Smooth performance.", "Durable build."]

@st.cache_data(ttl=3600)
def load_data():
    products = []
    pid = 1
    if not os.path.exists(PRODUCTS_DIR): os.makedirs(PRODUCTS_DIR)
    if not os.path.exists(CATEGORIES_DIR): os.makedirs(CATEGORIES_DIR)
    files = sorted([f for f in os.listdir(PRODUCTS_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    
    for file in files:
        fname = file.lower()
        category = "general" 
        for cat, keys in CATEGORY_KEYWORDS.items():
            if any(k in fname for k in keys): category = cat; break
        
        stock = random.randint(5, 150)
        sales = random.randint(50, 1000)
        products.append({
            "id": pid, "name": file.replace("_", " ").replace(".jpg", "").title(),
            "category": category, "image": f"{PRODUCTS_DIR}/{file}",
            "price": random.randint(499, 9999), "stock": stock, "sales": sales,
            "rating": round(random.uniform(4.2, 5.0), 1), "review": random.choice(REVIEWS),
            "stock_level": "High" if stock > 100 else "Medium" if stock > 30 else "Low",
            "is_bestseller": sales > 750
        })
        pid += 1
    return pd.DataFrame(products)

@st.cache_data(ttl=3600)
def get_categories():
    return sorted([f.replace(".jpg", "").replace(".png", "") for f in os.listdir(CATEGORIES_DIR) if f.lower().endswith(('.jpg', '.png'))])

df = load_data()
CATEGORIES = get_categories()

def format_name(name): return name.replace("_", " ").title()
def get_trend_data(base_sales):
    dates = [datetime.today() - timedelta(days=i) for i in range(30)][::-1]
    daily_sales = [int(base_sales/30 * random.uniform(0.8, 1.2)) for _ in range(30)]
    return pd.DataFrame({'Date': dates, 'Sales': daily_sales})

# =====================================================
# 5. UI COMPONENTS
# =====================================================

def render_hero():
    st.markdown("""
    <div style='text-align:center; padding: 50px 0 30px 0; margin-bottom: 30px; border-bottom: 1px solid rgba(255,255,255,0.05);'>
        <h1 style='font-size: 3rem; margin:0; text-shadow: 0 0 30px rgba(212, 197, 168, 0.2);'>❖ PRODUCT PULSE</h1>
        <p style='color: #8c8c8c; font-family: "Outfit"; font-size: 1rem; letter-spacing: 3px; margin-top:10px;'>
            INTELLIGENCE DASHBOARD
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    def btn_type(v): return "primary" if st.session_state.view == v else "secondary"
    with c1: 
        if st.button("CATALOG", use_container_width=True, type=btn_type('categories')):
            st.session_state.view = 'categories'; st.rerun()
    with c2: 
        if st.button("ANALYTICS", use_container_width=True, type=btn_type('analytics')):
            st.session_state.view = 'analytics'; st.rerun()
    with c3: 
        if st.button("DASHBOARD", use_container_width=True, type=btn_type('dashboard')):
            st.session_state.view = 'dashboard'; st.rerun()

def render_category_card(cat_name):
    is_sel = st.session_state.selected_category == cat_name
    active_style = "border-color: #d4c5a8; box-shadow: 0 0 30px rgba(212, 197, 168, 0.1);" if is_sel else ""
    
    st.markdown(f"<div class='ethereal-card' style='{active_style}'>", unsafe_allow_html=True)
    try: st.image(f"{CATEGORIES_DIR}/{cat_name}.jpg", use_container_width=True)
    except: pass
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button(f"{format_name(cat_name)}", key=f"btn_{cat_name}", use_container_width=True):
        st.session_state.selected_category = cat_name
        st.session_state.selected_product = None
        st.rerun()

def render_product_card(row):
    st.markdown(f"<div class='ethereal-card'>", unsafe_allow_html=True)
    try: st.image(row['image'], use_container_width=True)
    except: pass
    
    badges = ""
    if row['is_bestseller']: badges += f"<span style='color:#d4c5a8; border:1px solid #d4c5a8; padding:2px 8px; font-size:0.65em; margin-right:6px; border-radius:12px; font-family:Outfit;'>★ PREMIER</span>"
    if row['stock_level'] == 'Low': badges += f"<span style='color:#e57373; border:1px solid #e57373; padding:2px 8px; font-size:0.65em; border-radius:12px; font-family:Outfit;'>⚠ LIMITED</span>"

    st.markdown(f"""
        <div class='card-content'>
            <div class='card-title'>{row['name']}</div>
            <div style='margin: 8px 0;'>{badges}</div>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <span class='card-price'>₹{row['price']:,}</span>
                <span style='color:#8c8c8c; font-size:0.9rem'>★ {row['rating']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Details", key=f"p_{row['id']}", use_container_width=True):
        st.session_state.selected_product = row.to_dict()

def render_details():
    p = st.session_state.selected_product
    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.1); border-radius:16px; padding:24px; position:sticky; top:20px; backdrop-filter:blur(20px);'>
    """, unsafe_allow_html=True)
    
    if p is not None:
        st.markdown(f"<h3 style='margin:0; font-family:Outfit; font-weight:300;'>{p['name']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='color:#d4c5a8; font-size:2.2rem; margin:10px 0 20px 0; font-family:Outfit; font-weight:300;'>₹{p['price']:,}</h1>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: st.metric("Stock", f"{p['stock']}")
        with c2: st.metric("Sales", f"{p['sales']}")
        
        st.markdown("<hr style='border-color:rgba(255,255,255,0.05)'>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#a0a0a0; font-style:italic; font-family:Outfit;'>\"{p['review']}\"</div>", unsafe_allow_html=True)
        
        revenue = p['price'] * p['sales']
        st.markdown(f"<div style='margin-top:20px; padding:12px; border:1px solid #d4c5a8; border-radius:8px; text-align:center; color:#d4c5a8; letter-spacing:1px; font-family:Outfit;'>REVENUE: ₹{revenue:,}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align:center; padding:60px 20px; color:#555; letter-spacing:1px;'>SELECT ITEM</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# 6. MAIN LOGIC
# =====================================================
if 'view' not in st.session_state: st.session_state.view = 'categories'
if 'selected_category' not in st.session_state: st.session_state.selected_category = None
if 'selected_product' not in st.session_state: st.session_state.selected_product = None

render_hero()

# --- CATEGORIES VIEW ---
if st.session_state.view == 'categories':
    st.markdown("### SECTORS")
    cols = st.columns(3)
    for i, cat in enumerate(CATEGORIES):
        with cols[i % 3]: render_category_card(cat)

    if st.session_state.selected_category:
        st.markdown("---")
        st.markdown(f"### VIEWING: {format_name(st.session_state.selected_category)}")
        
        c1, c2 = st.columns([3, 1])
        with c1: search = st.text_input("SEARCH", placeholder="Filter by name...")
        with c2: sort_opt = st.selectbox("SORT", ["Relevance", "Price: High", "Price: Low"])
        
        cat_df = df[df['category'] == st.session_state.selected_category]
        if search: cat_df = cat_df[cat_df['name'].str.contains(search, case=False)]
        if sort_opt == "Price: High": cat_df = cat_df.sort_values('price', ascending=False)
        elif sort_opt == "Price: Low": cat_df = cat_df.sort_values('price')

        l, r = st.columns([2, 1])
        with l:
            if cat_df.empty: st.info("No items found.")
            else:
                p_cols = st.columns(3)
                for idx, (i, row) in enumerate(cat_df.iterrows()):
                    with p_cols[idx % 3]: render_product_card(row)
        with r: render_details()

# --- ANALYTICS VIEW ---
elif st.session_state.view == 'analytics':
    cat_options = {format_name(c): c for c in CATEGORIES}
    target_cat = cat_options[st.selectbox("SELECT SECTOR", list(cat_options.keys()))]
    
    if target_cat:
        cat_df = df[df['category'] == target_cat]
        
        st.markdown("""
        <style>
            .metric-box { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 20px; text-align: center; border-radius: 12px; }
            .metric-val { font-size: 2rem; font-weight: 300; color: #d4c5a8; font-family: 'Outfit'; }
            .metric-lbl { color: #666; letter-spacing: 2px; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 5px; }
        </style>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='metric-box'><div class='metric-lbl'>Units Sold</div><div class='metric-val'>{int(cat_df['sales'].sum())}</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='metric-box'><div class='metric-lbl'>Gross Revenue</div><div class='metric-val'>₹{int((cat_df['price']*cat_df['sales']).sum()):,}</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-box'><div class='metric-lbl'>Avg Rating</div><div class='metric-val'>{round(cat_df['rating'].mean(), 1)}</div></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.subheader("VELOCITY TREND")
        trend_df = get_trend_data(int(cat_df['sales'].sum()))
        
        # [FIXED ERROR] Changed 'fill_color' to 'fillcolor'
        fig_trend = px.area(trend_df, x='Date', y='Sales', template='plotly_dark')
        fig_trend.update_traces(line_color='#d4c5a8', fillcolor='rgba(212, 197, 168, 0.1)')
        fig_trend.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family='Outfit')
        st.plotly_chart(fig_trend, use_container_width=True)

# --- DASHBOARD VIEW ---
elif st.session_state.view == 'dashboard':
    st.markdown("### OBJECTIVES")
    
    total_rev = int((df['sales']*df['price']).sum())
    target_rev = int(total_rev * 1.2)
    progress = min(total_rev/target_rev, 1.0)
    
    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.05); padding:24px; border-radius:16px;'>
        <div style='display:flex; justify-content:space-between; margin-bottom:12px; color:#888; font-family:Outfit; letter-spacing:1px;'>
            <span>REVENUE TARGET</span>
            <span style='color:#d4c5a8'>{int(progress*100)}%</span>
        </div>
        <div style='height:8px; background:rgba(255,255,255,0.05); border-radius:4px; overflow:hidden;'>
            <div style='width:{progress*100}%; height:100%; background:linear-gradient(90deg, #8c7b60, #d4c5a8); border-radius:4px;'></div>
        </div>
        <div style='text-align:right; margin-top:8px; color:#555; font-size:0.8rem;'>
            ₹{total_rev:,} / ₹{target_rev:,}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("PERFORMANCE MATRIX")
    
    cat_perf = df.groupby('category').apply(lambda x: pd.Series({'revenue': (x['sales']*x['price']).sum()})).reset_index().sort_values('revenue')
    cat_perf['category'] = cat_perf['category'].apply(format_name)
    
    fig = px.bar(cat_perf, x='revenue', y='category', orientation='h', 
                 color='revenue', color_continuous_scale=['#2a2d36', '#d4c5a8'], 
                 template='plotly_dark', text_auto='.2s')
    fig.update_layout(height=800, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False, font_family='Outfit')
    st.plotly_chart(fig, use_container_width=True) 


