import streamlit as st
import pandas as pd
import koreanize_matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
# streamlit_card 모듈이 없어서 제거했습니다

# 데이터 파일 경로
DATA_PATH = "TIPS 운영사 정리.csv"
INVESTMENT_DATA_PATH = "accelerator_data_2024.csv"

# Streamlit 앱 구성
def main():
    st.set_page_config(layout="wide")
    
    # 헤더 섹션 스타일링
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem;
        border-bottom: 2px solid #3B82F6;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    .metric-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
    }
    .metric-ratio {
        font-size: 0.9rem;
        color: #4B5563;
    }
    .highlight-card {
        background-color: #e6f7ff;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        margin-bottom: 20px;
        border-left: 5px solid #1890ff;
    }
    .highlight-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #0050b3;
        margin-bottom: 8px;
    }
    .highlight-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1890ff;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 페이지 선택 사이드바
    st.sidebar.markdown("## 페이지 선택")
    page = st.sidebar.radio("이동할 페이지를 선택하세요:", ["투자 데이터 분석", "TIPS 운영사 데이터 대시보드"])
    
    if page == "TIPS 운영사 데이터 대시보드":
        show_main_dashboard()
    elif page == "투자 데이터 분석":
        show_investment_dashboard()

def show_main_dashboard():
    st.markdown('<div class="main-header">TIPS 운영사 데이터 대시보드</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">전체 운영사 및 초기투자액셀러레이터협회 회원사 데이터를 비교 분석합니다.</div>', unsafe_allow_html=True)

    # 데이터 로드
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
    st.markdown("## 📊 주요 지표")
    
    # 주요 지표 섹션 - 전체 데이터
    st.subheader("전체 데이터")
    
    # 전체 데이터 좌우 분할
    left_col, right_col = st.columns(2)
    
    # 좌측 - 숫자 데이터
    with left_col:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">운영사 수</div>
                <div class="metric-value">{total_operators}개사</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">일반형 팁스</div>
                <div class="metric-value">{total_tips}개사</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">스케일업 팁스(투자)</div>
                <div class="metric-value">{total_scaleup_invest}개사</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">스케일업 팁스(R&D)</div>
                <div class="metric-value">{total_scaleup_rd}개사</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">프리팁스</div>
                <div class="metric-value">{total_pretips}개사</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">립스</div>
                <div class="metric-value">{total_lips}개사</div>
            </div>
            """, unsafe_allow_html=True)
    
    # 우측 - 원그래프
    with right_col:
        # 원그래프 데이터 준비
        pie_labels = ["일반형 팁스", "스케일업 팁스(투자)", "스케일업 팁스(R&D)", "프리팁스", "립스"]
        pie_values = [total_tips, total_scaleup_invest, total_scaleup_rd, total_pretips, total_lips]
        
        # 원그래프 생성
        fig = px.pie(
            names=pie_labels,
            values=pie_values,
            title="전체 운영사 프로그램 비중",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            margin=dict(t=50, b=50, l=20, r=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 주요 지표 섹션 - 협회 회원사 데이터 (비율 포함)
    st.subheader("협회 회원사 데이터")
    
    # 협회 회원사 데이터 좌우 분할
    left_col, right_col = st.columns(2)
    
    # 좌측 - 숫자 데이터
    with left_col:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">운영 회원사 수</div>
                <div class="metric-value">{assoc_operators}개사 <span class="metric-ratio">({association_ratio['운영사 수'][0]}%)</span></div>
            </div>
            <div class="metric-card">
                <div class="metric-title">일반형 팁스</div>
                <div class="metric-value">{assoc_tips}개사 <span class="metric-ratio">({association_ratio['일반형 팁스'][0]}%)</span></div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">스케일업 팁스(투자)</div>
                <div class="metric-value">{assoc_scaleup_invest}개사 <span class="metric-ratio">({association_ratio['스케일업 팁스(투자)'][0]}%)</span></div>
            </div>
            <div class="metric-card">
                <div class="metric-title">스케일업 팁스(R&D)</div>
                <div class="metric-value">{assoc_scaleup_rd}개사 <span class="metric-ratio">({association_ratio['스케일업 팁스(R&D)'][0]}%)</span></div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">프리팁스</div>
                <div class="metric-value">{assoc_pretips}개사 <span class="metric-ratio">({association_ratio['프리팁스'][0]}%)</span></div>
            </div>
            <div class="metric-card">
                <div class="metric-title">립스</div>
                <div class="metric-value">{assoc_lips}개사 <span class="metric-ratio">({association_ratio['립스'][0]}%)</span></div>
            </div>
            """, unsafe_allow_html=True)
    
    # 우측 - 원그래프
    with right_col:
        # 원그래프 데이터 준비
        assoc_pie_labels = ["일반형 팁스", "스케일업 팁스(투자)", "스케일업 팁스(R&D)", "프리팁스", "립스"]
        assoc_pie_values = [assoc_tips, assoc_scaleup_invest, assoc_scaleup_rd, assoc_pretips, assoc_lips]
        
        # 원그래프 생성
        assoc_fig = px.pie(
            names=assoc_pie_labels,
            values=assoc_pie_values,
            title="협회 회원사 프로그램 비중",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.4
        )
        assoc_fig.update_traces(textposition='inside', textinfo='percent+label')
        assoc_fig.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            margin=dict(t=50, b=50, l=20, r=20)
        )
        
        st.plotly_chart(assoc_fig, use_container_width=True)
    
    # 시각화 섹션
    st.markdown("## 📈 데이터 시각화")
    
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
    
    # Altair를 사용한 프로그램별 운영사 현황 차트
    st.subheader("프로그램별 운영사 현황")
    
    # Altair 차트 생성
    chart = alt.Chart(chart_df).mark_bar().encode(
        x=alt.X('프로그램:N', title='프로그램', sort=None),  # sort=None으로 설정하여 카테고리 순서 유지
        y=alt.Y('운영사 수:Q', title='운영사 수'),
        color=alt.Color('구분:N', scale=alt.Scale(
            domain=['전체', '협회 회원사'],
            range=['#FF9E44', '#4CAF50']
        )),
        column='구분:N'
    ).properties(
        width=300,
        height=300
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    )
    
    # 그룹화된 막대 차트 (grouped bar chart)
    grouped_chart = alt.Chart(chart_df).mark_bar().encode(
        x=alt.X('프로그램:N', title='프로그램', sort=None),  # sort=None으로 설정하여 카테고리 순서 유지
        y=alt.Y('운영사 수:Q', title='운영사 수'),
        color=alt.Color('구분:N', scale=alt.Scale(
            domain=['전체', '협회 회원사'],
            range=['#FF9E44', '#4CAF50']
        )),
        xOffset='구분:N'  # 이것이 그룹화를 만듭니다
    ).properties(
        width=600,
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_legend(
        orient='top',
        titleFontSize=14,
        labelFontSize=12
    )
    
    st.altair_chart(grouped_chart, use_container_width=True)
    
    # 상세 데이터 테이블 (접을 수 있는 섹션)
    with st.expander("📋 상세 데이터 테이블"):
        tab1, tab2, tab3 = st.tabs(["전체 데이터", "협회 회원사", "전체 대비 비율(%)"])
        
        with tab1:
            st.dataframe(df_total.style.set_properties(**{
                'background-color': '#FFEB99',
                'color': 'black',
                'text-align': 'center'
            }), use_container_width=True)
        
        with tab2:
            st.dataframe(df_association.style.set_properties(**{
                'background-color': '#C6E2A6',
                'color': 'black',
                'text-align': 'center'
            }), use_container_width=True)
        
        with tab3:
            st.dataframe(df_ratio.style.format("{:.1f}").set_properties(**{
                'background-color': '#D1E0FF',
                'color': 'black',
                'text-align': 'center'
            }), use_container_width=True)

def show_investment_dashboard():
    st.markdown("## 💰 투자 데이터 분석")
    st.write("이 페이지에서는 투자 데이터를 분석하고 시각화합니다.")

    # 데이터 로드
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
    st.markdown("### 📊 투자 데이터 요약")
    
    # 전체 투자 데이터 하이라이트 (강조 표시)
    st.markdown(f"""
    <div class="highlight-card">
        <div class="highlight-title">전체 투자 금액</div>
        <div class="highlight-value">{total_investment:,.0f}억원</div>
        <div class="metric-title">전체 투자 기업 수</div>
        <div class="metric-value">{total_companies:,}개사</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 연도별 투자 데이터 카드
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">2024년 투자 금액</div>
            <div class="metric-value">{investment_2024:,.0f}억원</div>
            <div class="metric-ratio">투자 기업 수: {companies_2024:,}개사</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">2023년 투자 금액</div>
            <div class="metric-value">{investment_2023:,.0f}억원</div>
            <div class="metric-ratio">투자 기업 수: {companies_2023:,}개사</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">2022년 투자 금액</div>
            <div class="metric-value">{investment_2022:,.0f}억원</div>
            <div class="metric-ratio">투자 기업 수: {companies_2022:,}개사</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">2021년 투자 금액</div>
            <div class="metric-value">{investment_2021:,.0f}억원</div>
            <div class="metric-ratio">투자 기업 수: {companies_2021:,}개사</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">2020년 투자 금액</div>
            <div class="metric-value">{investment_2020:,.0f}억원</div>
            <div class="metric-ratio">투자 기업 수: {companies_2020:,}개사</div>
        </div>
        """, unsafe_allow_html=True)

    # 연도별 투자 금액 변화 시각화 (선 그래프)
    st.subheader("📈 연도별 투자 금액 변화")

    # 데이터 준비
    investment_trend = df[["회사명", "2020 투자 금액(억)", "2021 투자 금액(억)", 
                            "2022 투자 금액(억)", "2023 투자 금액(억)", "2024 투자 금액(억)"]]
    
    investment_trend = investment_trend.melt(id_vars=["회사명"], 
                                             var_name="연도", 
                                             value_name="투자 금액(억)")
    investment_trend["연도"] = investment_trend["연도"].str.extract(r'(\d+)').astype(int)

    # 회사 선택 위젯 추가
    companies = sorted(df["회사명"].unique())
    selected_company = st.selectbox("회사를 선택하세요:", companies)
    
    # 선택된 회사의 데이터만 필터링
    filtered_data = investment_trend[investment_trend["회사명"] == selected_company]
    
    # 선택된 회사의 연도별 투자 금액 변화 그래프
    fig = px.line(filtered_data, x="연도", y="투자 금액(억)", 
                  title=f"{selected_company}의 연도별 투자 금액 변화", 
                  markers=True)
    
    fig.update_layout(
        xaxis_title="연도",
        yaxis_title="투자 금액(억원)",
        xaxis=dict(tickmode='linear'),
        yaxis=dict(gridcolor='lightgray'),
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # 운용사별 전체 투자 금액 비교 (막대 그래프)
    st.subheader("🏢 운용사별 전체 투자 금액 비교")

    top_investors = df.sort_values("전체 투자 금액(억)", ascending=False).head(15)
    fig = px.bar(top_investors, x="회사명", y="전체 투자 금액(억)", 
                 title="상위 15개 운용사 전체 투자 금액", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    # 투자 기업 수 대비 투자 금액 비율 (산점도)
    st.subheader("📊 투자 기업 수 대비 투자 금액 비율")

    fig = px.scatter(df, x="전체 투자 기업 수", y="전체 투자 금액(억)", 
                     size="전체 투자 금액(억)", color="회사명",
                     title="투자 기업 수 대비 투자 금액 산점도")
    st.plotly_chart(fig, use_container_width=True)

    # 데이터 테이블 표시
    st.subheader("📋 원본 데이터 보기")
    st.dataframe(df)

if __name__ == "__main__":
    main()



