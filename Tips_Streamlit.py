import streamlit as st
import pandas as pd
import koreanize_matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

# 데이터 파일 경로
DATA_PATH = "TIPS 운영사 정리.csv"
INVESTMENT_DATA_PATH = "accelerator_data_2024.csv"

# Streamlit 앱 구성
def main():
    st.set_page_config(layout="wide")
    
    # Font Awesome 추가
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">', unsafe_allow_html=True)
    
    # 헤더 섹션 스타일링 - 향상된 디자인
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 1.5rem 0;
        border-bottom: 2px solid #3B82F6;
        background: linear-gradient(to right, #f8fafc, #dbeafe, #f8fafc);
        border-radius: 8px;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1E3A8A;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #dbeafe;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        text-align: center;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease;
        border-top: 4px solid #3B82F6;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.08);
    }
    
    .metric-title {
        font-size: 0.95rem;
        font-weight: 500;
        color: #1E3A8A;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .metric-ratio {
        font-size: 0.85rem;
        color: #4B5563;
        background-color: #dbeafe;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        display: inline-block;
    }
    
    .highlight-card {
        background: linear-gradient(135deg, #ffffff, #e3f2fd);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 6px 12px rgba(37, 99, 235, 0.1);
        margin-bottom: 1.5rem;
        border-left: 6px solid #2196f3;
        position: relative;
        overflow: hidden;
    }
    
    .highlight-card::before {
        content: "";
        position: absolute;
        top: -50px;
        right: -50px;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background-color: rgba(37, 99, 235, 0.1);
        z-index: 0;
    }
    
    .highlight-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #0050b3;
        margin-bottom: 0.8rem;
        position: relative;
        z-index: 1;
    }
    
    .highlight-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E88E5;
        position: relative;
        z-index: 1;
    }
    
    /* 애니메이션 효과 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.6s ease-out forwards;
    }
    
    .delay-1 { animation-delay: 0.1s; }
    .delay-2 { animation-delay: 0.2s; }
    .delay-3 { animation-delay: 0.3s; }
    
    /* 차트 컨테이너 스타일링 */
    .chart-container {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
    }
    
    /* 데이터 테이블 스타일링 개선 */
    .dataframe {
        font-size: 0.9rem !important;
    }
    
    .dataframe th {
        background-color: #f1f5f9 !important;
        color: #1E3A8A !important;
        font-weight: 600 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        border-radius: 4px 4px 0 0;
        padding: 0 1rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        border-bottom: 2px solid #3B82F6;
    }
    
    /* 선택 위젯 스타일링 */
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 페이지 선택 사이드바
    st.sidebar.markdown("## 페이지 선택")
    page = st.sidebar.radio("이동할 페이지를 선택하세요:", ["액셀러레이터 투자 데이터", "TIPS 운영사 데이터"])
    
    if page == "TIPS 운영사 데이터":
        show_main_dashboard()
    elif page == "액셀러레이터 투자 데이터":
        show_investment_dashboard()

# 메트릭 카드 컴포넌트 함수 추가
def metric_card(title, value, ratio=None, icon=None):
    icon_html = f'<i class="{icon}"></i> ' if icon else ''
    ratio_html = f'<div class="metric-ratio">{ratio}</div>' if ratio else ''
    
    return f"""
    <div class="metric-card">
        <div class="metric-title">{icon_html}{title}</div>
        <div class="metric-value">{value}</div>
        {ratio_html}
    </div>
    """

def show_main_dashboard():
    st.markdown('<div class="main-header animate-fade-in">TIPS 운영사 데이터 대시보드</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header animate-fade-in delay-1">전체 운영사 및 초기투자액셀러레이터협회 회원사 데이터를 비교 분석합니다.</div>', unsafe_allow_html=True)

    # 데이터 로드
    with st.spinner("데이터를 분석 중입니다..."):
        @st.cache_data
        def load_data():
            return pd.read_csv(DATA_PATH, encoding="utf-8")

        data = load_data()

    # 데이터 전처리
    # 운영기관 칼럼의 실제 데이터 수를 세어 전체 운영사 수 계산
    total_operators = data["운영기관"].dropna().count()  # 전체 운영사 수 (B칼럼, 헤더 제외)
    total_tips = data["일반형 팁스"].eq("O").sum()  # 일반형 팁스 운영사 수
    total_scaleup_invest = data["스케일업 팁스(투자)"].eq("O").sum()  # 스케일업 팁스(투자) 운영사 수
    total_scaleup_rd = data["스케일업 팁스(R&D)"].eq("O").sum()  # 스케일업 팁스(R&D) 운영사 수
    total_pretips = data["프리팁스"].eq("O").sum()  # 프리팁스 운영사 수
    total_lips = data["립스"].eq("O").sum()  # 립스 운영사 수

    # 협회 회원사 데이터 필터링
    association_df = data[data["협회 회원사 여부"] == "O"]
    assoc_operators = len(association_df)  # 협회 회원사 수
    assoc_tips = association_df["일반형 팁스"].eq("O").sum()
    assoc_scaleup_invest = association_df["스케일업 팁스(투자)"].eq("O").sum()
    assoc_scaleup_rd = association_df["스케일업 팁스(R&D)"].eq("O").sum()
    assoc_pretips = association_df["프리팁스"].eq("O").sum()
    assoc_lips = association_df["립스"].eq("O").sum()

    # 전체 데이터 및 협회 회원사 데이터 정리
    total_data = {
        "운영사 수": [total_operators],
        "일반형 팁스": [total_tips],
        "스케일업 팁스(투자)": [total_scaleup_invest],
        "스케일업 팁스(R&D)": [total_scaleup_rd],
        "프리팁스": [total_pretips],
        "립스": [total_lips]
    }

    association_data = {
        "운영사 수": [assoc_operators],
        "일반형 팁스": [assoc_tips],
        "스케일업 팁스(투자)": [assoc_scaleup_invest],
        "스케일업 팁스(R&D)": [assoc_scaleup_rd],
        "프리팁스": [assoc_pretips],
        "립스": [assoc_lips]
    }

    # 협회 회원사 비율 계산 (소수점 첫째자리까지만 표시)
    association_ratio = {
        key: [round((association_data[key][0] / total_data[key][0]) * 100, 1) if total_data[key][0] != 0 else 0]
        for key in total_data
    }

    # DataFrame 변환
    df_total = pd.DataFrame(total_data, index=["전체 데이터"])
    df_association = pd.DataFrame(association_data, index=["협회 회원사"])
    df_ratio = pd.DataFrame(association_ratio, index=["전체 대비 비율(%)"])
    
    # 주요 지표 카드 표시
    st.markdown('<div class="section-header animate-fade-in delay-2"><i class="fas fa-chart-bar"></i> 주요 지표</div>', unsafe_allow_html=True)
    
    # 주요 지표 섹션 - 전체 데이터
    st.subheader("전체 데이터")
    
    # 전체 데이터 좌우 분할
    left_col, right_col = st.columns(2)
    
    # 좌측 - 숫자 데이터 (개선된 카드 디자인)
    with left_col:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(metric_card(
                "운영사 수", 
                f"{total_operators}개사", 
                icon="fas fa-building"
            ), unsafe_allow_html=True)
            
            st.markdown(metric_card(
                "일반형 팁스", 
                f"{total_tips}개사", 
                icon="fas fa-check-circle"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(metric_card(
                "스케일업 팁스(투자)", 
                f"{total_scaleup_invest}개사", 
                icon="fas fa-chart-line"
            ), unsafe_allow_html=True)
            
            st.markdown(metric_card(
                "스케일업 팁스(R&D)", 
                f"{total_scaleup_rd}개사", 
                icon="fas fa-flask"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(metric_card(
                "프리팁스", 
                f"{total_pretips}개사", 
                icon="fas fa-seedling"
            ), unsafe_allow_html=True)
            
            st.markdown(metric_card(
                "립스", 
                f"{total_lips}개사", 
                icon="fas fa-lightbulb"
            ), unsafe_allow_html=True)
    
    # 우측 - 원그래프 (개선된 스타일)
    with right_col:
        # 원그래프 데이터 준비
        pie_labels = ["일반형 팁스", "스케일업 팁스(투자)", "스케일업 팁스(R&D)", "프리팁스", "립스"]
        pie_values = [total_tips, total_scaleup_invest, total_scaleup_rd, total_pretips, total_lips]
        
        # 개선된 컬러 팔레트와 디자인
        fig = px.pie(
            names=pie_labels,
            values=pie_values,
            title="전체 운영사 프로그램 비중",
            color_discrete_sequence=px.colors.qualitative.Bold,
            hole=0.4
        )
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>%{value}개사<br>%{percent}<extra></extra>'
        )
        fig.update_layout(
            font=dict(family="Noto Sans KR, sans-serif"),
            title_font_size=18,
            title_font_color="#1E3A8A",
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=-0.2, 
                xanchor="center", 
                x=0.5,
                font=dict(size=12)
            ),
            margin=dict(t=60, b=60, l=20, r=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 주요 지표 섹션 - 협회 회원사 데이터 (비율 포함)
    st.subheader("협회 회원사 데이터")
    
    # 협회 회원사 데이터 좌우 분할
    left_col, right_col = st.columns(2)
    
    # 좌측 - 숫자 데이터 (개선된 카드 디자인)
    with left_col:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(metric_card(
                "운영 회원사 수", 
                f"{assoc_operators}개사", 
                f"{association_ratio['운영사 수'][0]}%",
                icon="fas fa-building"
            ), unsafe_allow_html=True)
            
            st.markdown(metric_card(
                "일반형 팁스", 
                f"{assoc_tips}개사", 
                f"{association_ratio['일반형 팁스'][0]}%",
                icon="fas fa-check-circle"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(metric_card(
                "스케일업 팁스(투자)", 
                f"{assoc_scaleup_invest}개사", 
                f"{association_ratio['스케일업 팁스(투자)'][0]}%",
                icon="fas fa-chart-line"
            ), unsafe_allow_html=True)
            
            st.markdown(metric_card(
                "스케일업 팁스(R&D)", 
                f"{assoc_scaleup_rd}개사", 
                f"{association_ratio['스케일업 팁스(R&D)'][0]}%",
                icon="fas fa-flask"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(metric_card(
                "프리팁스", 
                f"{assoc_pretips}개사", 
                f"{association_ratio['프리팁스'][0]}%",
                icon="fas fa-seedling"
            ), unsafe_allow_html=True)
            
            st.markdown(metric_card(
                "립스", 
                f"{assoc_lips}개사", 
                f"{association_ratio['립스'][0]}%",
                icon="fas fa-lightbulb"
            ), unsafe_allow_html=True)
    
    # 우측 - 원그래프 (개선된 스타일)
    with right_col:
        # 원그래프 데이터 준비
        assoc_pie_labels = ["일반형 팁스", "스케일업 팁스(투자)", "스케일업 팁스(R&D)", "프리팁스", "립스"]
        assoc_pie_values = [assoc_tips, assoc_scaleup_invest, assoc_scaleup_rd, assoc_pretips, assoc_lips]
        
        # 개선된 컬러 팔레트와 디자인
        assoc_fig = px.pie(
            names=assoc_pie_labels,
            values=assoc_pie_values,
            title="협회 회원사 프로그램 비중",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.4
        )
        assoc_fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>%{value}개사<br>%{percent}<extra></extra>'
        )
        assoc_fig.update_layout(
            font=dict(family="Noto Sans KR, sans-serif"),
            title_font_size=18,
            title_font_color="#1E3A8A",
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=-0.2, 
                xanchor="center", 
                x=0.5,
                font=dict(size=12)
            ),
            margin=dict(t=60, b=60, l=20, r=20)
        )
        
        st.plotly_chart(assoc_fig, use_container_width=True)
    
    # 시각화 섹션
    st.markdown('<div class="section-header animate-fade-in delay-3"><i class="fas fa-chart-area"></i> 데이터 시각화</div>', unsafe_allow_html=True)
    
    # 차트 데이터 준비 - 순서 지정
    program_order = ["일반형 팁스", "스케일업 팁스(투자)", "스케일업 팁스(R&D)", "프리팁스", "립스"]
    chart_data = {
        '구분': [],
        '프로그램': [],
        '운영사 수': []
    }
    
    for program in program_order:
        chart_data['구분'].extend(['전체', '협회 회원사'])
        chart_data['프로그램'].extend([program, program])
        chart_data['운영사 수'].extend([total_data[program][0], association_data[program][0]])
    
    chart_df = pd.DataFrame(chart_data)
    
    # 프로그램 순서 지정을 위한 카테고리 타입 설정
    chart_df['프로그램'] = pd.Categorical(
        chart_df['프로그램'], 
        categories=program_order, 
        ordered=True
    )
    
    # 그래프 컨테이너 추가
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("프로그램별 운영사 현황")
    
    # 그룹화된 막대 차트 (개선된 디자인)
    grouped_chart = alt.Chart(chart_df).mark_bar().encode(
        x=alt.X('프로그램:N', title='프로그램', sort=None, axis=alt.Axis(labelAngle=0, labelFontSize=12)),
        y=alt.Y('운영사 수:Q', title='운영사 수'),
        color=alt.Color('구분:N', scale=alt.Scale(
            domain=['전체', '협회 회원사'],
            range=['#3B82F6', '#10B981']
        ), legend=alt.Legend(title="구분")),
        xOffset='구분:N',
        tooltip=[
            alt.Tooltip('프로그램:N', title='프로그램'),
            alt.Tooltip('구분:N', title='구분'),
            alt.Tooltip('운영사 수:Q', title='운영사 수')
        ]
    ).properties(
        width=600,
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14,
        grid=False
    ).configure_legend(
        orient='top',
        titleFontSize=14,
        labelFontSize=12
    ).configure_view(
        strokeWidth=0
    )
    
    st.altair_chart(grouped_chart, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 상세 데이터 테이블 (접을 수 있는 섹션)
    with st.expander("📋 상세 데이터 테이블", expanded=False):
        tab1, tab2, tab3 = st.tabs(["전체 데이터", "협회 회원사", "전체 대비 비율(%)"])
        
        with tab1:
            st.markdown('<div class="data-table">', unsafe_allow_html=True)
            st.dataframe(df_total.style.set_properties(**{
                'background-color': '#EFF6FF',
                'color': 'black',
                'text-align': 'center',
                'font-weight': '500',
                'border': '1px solid #DBEAFE',
                'border-radius': '4px'
            }).format(precision=0), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="data-table">', unsafe_allow_html=True)
            st.dataframe(df_association.style.set_properties(**{
                'background-color': '#ECFDF5',
                'color': 'black',
                'text-align': 'center',
                'font-weight': '500',
                'border': '1px solid #D1FAE5',
                'border-radius': '4px'
            }).format(precision=0), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="data-table">', unsafe_allow_html=True)
            st.dataframe(df_ratio.style.format("{:.1f}%").set_properties(**{
                'background-color': '#F0F9FF',
                'color': 'black',
                'text-align': 'center',
                'font-weight': '500',
                'border': '1px solid #BAE6FD',
                'border-radius': '4px'
            }), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

def show_investment_dashboard():
    st.markdown('<div class="main-header animate-fade-in">액셀러레이터 투자 데이터 대시보드</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header animate-fade-in delay-1">이 페이지에서는 액셀러레이터 투자 데이터를 분석하고 시각화합니다.</div>', unsafe_allow_html=True)

    # 데이터 로드
    with st.spinner("데이터를 분석 중입니다..."):
        @st.cache_data
        def load_data():
            return pd.read_csv(INVESTMENT_DATA_PATH)

        df = load_data()
    
    # 투자 데이터 요약 계산
    total_investment = df["전체 투자 금액(억)"].sum()  # L열 합계
    total_companies = df["전체 투자 기업 수"].sum()  # M열 합계
    
    investment_2020 = df["2020 투자 금액(억)"].sum()  # J열 합계
    companies_2020 = df["2020 투자 기업 수"].sum()  # K열 합계
    
    investment_2021 = df["2021 투자 금액(억)"].sum()  # H열 합계
    companies_2021 = df["2021 투자 기업 수"].sum()  # I열 합계
    
    investment_2022 = df["2022 투자 금액(억)"].sum()  # F열 합계
    companies_2022 = df["2022 투자 기업 수"].sum()  # G열 합계
    
    investment_2023 = df["2023 투자 금액(억)"].sum()  # D열 합계
    companies_2023 = df["2023 투자 기업 수"].sum()  # E열 합계
    
    investment_2024 = df["2024 투자 금액(억)"].sum()  # B열 합계
    companies_2024 = df["2024 투자 기업 수"].sum()  # C열 합계
    
    # 전체 투자 데이터 하이라이트 카드
    st.markdown('<div class="section-header animate-fade-in delay-2"><i class="fas fa-money-bill-wave"></i> 투자 데이터 요약</div>', unsafe_allow_html=True)
    
    # 전체 투자 데이터 하이라이트 (강조 표시) - 좌우 분할
    left_col, right_col = st.columns(2)
    
    # 좌측 - 전체 투자 금액 표시
    with left_col:
        st.markdown(f"""
        <div class="highlight-card">
            <div class="highlight-title"><i class="fas fa-money-bill-wave"></i> 전체 투자 금액</div>
            <div class="highlight-value">{total_investment:,.0f}억원</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 우측 - 전체 투자 기업 수 표시
    with right_col:
        st.markdown(f"""
        <div class="highlight-card">
            <div class="highlight-title"><i class="fas fa-building"></i> 전체 투자 기업 수</div>
            <div class="highlight-value">{total_companies:,}개사</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 연도별 투자 데이터 카드
    st.markdown('<div class="section-header animate-fade-in delay-3"><i class="fas fa-calendar-alt"></i> 연도별 투자 추이</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(metric_card(
            "2024년 투자 금액", 
            f"{investment_2024:,.0f}억원",
            f"투자 기업 수: {companies_2024:,}개사",
            icon="fas fa-chart-line"
        ), unsafe_allow_html=True)

        st.markdown(metric_card(
            "2023년 투자 금액", 
            f"{investment_2023:,.0f}억원",
            f"투자 기업 수: {companies_2023:,}개사",
            icon="fas fa-chart-bar"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(metric_card(
            "2022년 투자 금액", 
            f"{investment_2022:,.0f}억원",
            f"투자 기업 수: {companies_2022:,}개사",
            icon="fas fa-chart-line"
        ), unsafe_allow_html=True)
        
        st.markdown(metric_card(
            "2021년 투자 금액", 
            f"{investment_2021:,.0f}억원",
            f"투자 기업 수: {companies_2021:,}개사",
            icon="fas fa-chart-bar"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(metric_card(
            "2020년 투자 금액", 
            f"{investment_2020:,.0f}억원",
            f"투자 기업 수: {companies_2020:,}개사",
            icon="fas fa-chart-bar"
        ), unsafe_allow_html=True)
    
    # 차트 컨테이너 시작
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    # 전체 연도별 투자 금액 및 기업 수 변화 시각화
    st.subheader("📈 전체 연도별 투자 흐름")
    
    # 전체 연도별 데이터 준비
    years = [2020, 2021, 2022, 2023, 2024]
    investment_by_year = [investment_2020, investment_2021, investment_2022, investment_2023, investment_2024]
    companies_by_year = [companies_2020, companies_2021, companies_2022, companies_2023, companies_2024]
    
    # 전체 연도별 투자 금액 및 기업 수 변화 그래프 (막대 + 선)
    fig = go.Figure()
    
    # 투자 금액 막대 그래프 추가
    fig.add_trace(go.Bar(
        x=years,
        y=investment_by_year,
        name="투자 금액(억원)",
        marker_color='#3B82F6',
        hovertemplate='%{x}년<br>투자 금액: %{y:,.0f}억원<extra></extra>'
    ))
    
    # 투자 기업 수 선 그래프 추가 (보조 y축)
    fig.add_trace(go.Scatter(
        x=years,
        y=companies_by_year,
        name="투자 기업 수",
        marker=dict(size=10),
        line=dict(width=3, color='#10B981'),
        yaxis="y2",
        hovertemplate='%{x}년<br>투자 기업 수: %{y:,}개사<extra></extra>'
    ))
    
    # 레이아웃 설정
    fig.update_layout(
        title={
            'text': "전체 연도별 투자 금액 및 투자 기업 수 변화",
            'font': {'size': 18, 'color': '#1E3A8A', 'family': 'Noto Sans KR, sans-serif'}
        },
        xaxis=dict(
            title="연도",
            tickmode='linear',
            tickfont=dict(size=12),
            title_font=dict(size=14)
        ),
        yaxis=dict(
            title="투자 금액(억원)",
            title_font=dict(size=14, color='#3B82F6'),
            tickfont=dict(size=12, color='#3B82F6'),
            gridcolor='#EFF6FF'
        ),
        yaxis2=dict(
            title="투자 기업 수",
            title_font=dict(size=14, color='#10B981'),
            tickfont=dict(size=12, color='#10B981'),
            anchor="x",
            overlaying="y",
            side="right",
            gridcolor='#EFF6FF'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        plot_bgcolor='white',
        hovermode="x unified",
        margin=dict(t=80, b=60, l=60, r=60)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 연도별 투자 금액 변화 시각화 (차트 컨테이너 사용)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📊 회사별 연도별 투자 데이터")

    # 필터 섹션 추가
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # 데이터 준비
        investment_trend = df[["회사명", "2020 투자 금액(억)", "2021 투자 금액(억)", 
                                "2022 투자 금액(억)", "2023 투자 금액(억)", "2024 투자 금액(억)"]]
        
        companies_trend = df[["회사명", "2020 투자 기업 수", "2021 투자 기업 수", 
                            "2022 투자 기업 수", "2023 투자 기업 수", "2024 투자 기업 수"]]
        
        investment_trend = investment_trend.melt(id_vars=["회사명"], 
                                                var_name="연도", 
                                                value_name="투자 금액(억)")
        
        companies_trend = companies_trend.melt(id_vars=["회사명"], 
                                            var_name="연도", 
                                            value_name="투자 기업 수")
        
        investment_trend["연도"] = investment_trend["연도"].str.extract(r'(\d+)').astype(int)
        companies_trend["연도"] = companies_trend["연도"].str.extract(r'(\d+)').astype(int)

        # 회사 선택 위젯 개선
        companies = sorted(df["회사명"].unique())
        selected_company = st.selectbox(
            "회사를 선택하세요:", 
            companies,
            help="데이터를 확인할 회사를 선택하세요"
        )
    
    # 선택된 회사의 데이터만 필터링
    filtered_investment = investment_trend[investment_trend["회사명"] == selected_company]
    filtered_companies = companies_trend[companies_trend["회사명"] == selected_company]
    
    # 선택된 회사의 연도별 투자 금액 및 기업 수 변화 그래프 (막대 + 선)
    fig = go.Figure()
    
    # 투자 금액 막대 그래프 추가
    fig.add_trace(go.Bar(
        x=filtered_investment["연도"],
        y=filtered_investment["투자 금액(억)"],
        name="투자 금액(억원)",
        marker_color='#3B82F6',
        hovertemplate='%{x}년<br>투자 금액: %{y:,.0f}억원<extra></extra>'
    ))
    
    # 투자 기업 수 선 그래프 추가 (보조 y축)
    fig.add_trace(go.Scatter(
        x=filtered_companies["연도"],
        y=filtered_companies["투자 기업 수"],
        name="투자 기업 수",
        marker=dict(size=10),
        line=dict(width=3, color='#10B981'),
        yaxis="y2",
        hovertemplate='%{x}년<br>투자 기업 수: %{y:,}개사<extra></extra>'
    ))
    
    # 레이아웃 설정 - 더 나은 시각적 디자인
    fig.update_layout(
        title={
            'text': f"{selected_company}의 연도별 투자 금액 및 기업 수 변화",
            'font': {'size': 18, 'color': '#1E3A8A', 'family': 'Noto Sans KR, sans-serif'},
            'y': 0.95
        },
        xaxis=dict(
            title="연도",
            tickmode='linear',
            tickfont=dict(size=12),
            title_font=dict(size=14)
        ),
        yaxis=dict(
            title="투자 금액(억원)",
            title_font=dict(size=14, color='#3B82F6'),
            tickfont=dict(size=12, color='#3B82F6'),
            gridcolor='#EFF6FF'
        ),
        yaxis2=dict(
            title="투자 기업 수",
            title_font=dict(size=14, color='#10B981'),
            tickfont=dict(size=12, color='#10B981'),
            anchor="x",
            overlaying="y",
            side="right",
            gridcolor='#EFF6FF'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        ),
        plot_bgcolor='white',
        hovermode="x unified",
        margin=dict(t=80, b=60, l=60, r=60)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 운용사별 전체 투자 금액 비교 (막대 그래프)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🏢 운용사별 전체 투자 금액 비교")

    # 상위 15개 운용사 데이터
    top_investors = df.sort_values("전체 투자 금액(억)", ascending=False).head(15)
    
    # 개선된 막대 그래프
    fig = px.bar(
        top_investors, 
        x="회사명", 
        y="전체 투자 금액(억)", 
        title="상위 15개 운용사 전체 투자 금액",
        text_auto=True,
        color="전체 투자 금액(억)",
        color_continuous_scale=px.colors.sequential.Blues,
        labels={"회사명": "운용사", "전체 투자 금액(억)": "투자 금액(억원)"}
    )
    
    fig.update_traces(
        texttemplate='%{y:,.0f}억원',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>투자 금액: %{y:,.0f}억원<extra></extra>',
        marker=dict(line=dict(width=1, color='white'))
    )
    
    fig.update_layout(
        font=dict(family="Noto Sans KR, sans-serif"),
        title_font=dict(size=18, color="#1E3A8A"),
        xaxis=dict(
            title="운용사",
            tickangle=-45,
            tickfont=dict(size=11),
            title_font=dict(size=14)
        ),
        yaxis=dict(
            title="투자 금액(억원)",
            tickfont=dict(size=12),
            title_font=dict(size=14),
            gridcolor='#EFF6FF'
        ),
        plot_bgcolor='white',
        margin=dict(t=60, b=80, l=60, r=40),
        coloraxis_showscale=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 투자 기업 수 대비 투자 금액 비율 (산점도)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📊 투자 기업 수 대비 투자 금액 비율")

    # 개선된 산점도
    fig = px.scatter(
        df, 
        x="전체 투자 기업 수", 
        y="전체 투자 금액(억)", 
        size="전체 투자 금액(억)", 
        color="회사명",
        title="투자 기업 수 대비 투자 금액 산점도",
        labels={"전체 투자 기업 수": "투자 기업 수", "전체 투자 금액(억)": "투자 금액(억원)"},
        hover_data=["회사명", "전체 투자 금액(억)", "전체 투자 기업 수"]
    )
    
    fig.update_traces(
        marker=dict(
            line=dict(width=1, color='white'),
            opacity=0.8,
            sizeref=0.1,
            sizemin=5
        ),
        hovertemplate='<b>%{customdata[0]}</b><br>투자 금액: %{y:,.0f}억원<br>투자 기업 수: %{x}개사<extra></extra>'
    )
    
    fig.update_layout(
        font=dict(family="Noto Sans KR, sans-serif"),
        title_font=dict(size=18, color="#1E3A8A"),
        xaxis=dict(
            title="투자 기업 수(개사)",
            tickfont=dict(size=12),
            title_font=dict(size=14),
            gridcolor='#EFF6FF'
        ),
        yaxis=dict(
            title="투자 금액(억원)",
            tickfont=dict(size=12),
            title_font=dict(size=14),
            gridcolor='#EFF6FF'
        ),
        plot_bgcolor='white',
        margin=dict(t=60, b=60, l=60, r=40),
        legend_title="회사명",
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.3,
            xanchor='center',
            x=0.5,
            font=dict(size=10)
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 데이터 테이블 표시
    with st.expander("📋 원본 데이터 보기", expanded=False):
        st.markdown('<div class="section-header">데이터 테이블</div>', unsafe_allow_html=True)
        
        # 검색 필터 추가
        search_term = st.text_input("회사명으로 검색:", "")
        
        if search_term:
            filtered_df = df[df["회사명"].str.contains(search_term, case=False)]
        else:
            filtered_df = df
        
        # 개선된 데이터 테이블 스타일링
        st.markdown('<div class="data-table">', unsafe_allow_html=True)
        st.dataframe(
            filtered_df.style.background_gradient(
                cmap='Blues', 
                subset=['전체 투자 금액(억)']
            ).background_gradient(
                cmap='Greens', 
                subset=['전체 투자 기업 수']
            ).format({
                "전체 투자 금액(억)": "{:,.0f}",
                "2020 투자 금액(억)": "{:,.0f}",
                "2021 투자 금액(억)": "{:,.0f}",
                "2022 투자 금액(억)": "{:,.0f}",
                "2023 투자 금액(억)": "{:,.0f}",
                "2024 투자 금액(억)": "{:,.0f}"
            }),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 데이터 새로고침 버튼
    if st.button("🔄 데이터 새로고침", key="refresh_button"):
        st.cache_data.clear()
        st.success("데이터를 새로고침하였습니다!")
        st.experimental_rerun()

if __name__ == "__main__":
    main()
