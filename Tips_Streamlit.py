import streamlit as st
import pandas as pd
import koreanize_matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
# streamlit_card 모듈이 없어서 제거했습니다

# 데이터 파일 경로
DATA_PATH = "TIPS 운영사 정리.csv"

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
    </style>
    """, unsafe_allow_html=True)
    
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
    
    # 주요 지표 섹션 - 협회 회원사 데이터
    st.subheader("협회 회원사 데이터")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">운영 회원사 수</div>
            <div class="metric-value">{assoc_operators}개사</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">일반형 팁스</div>
            <div class="metric-value">{assoc_tips}개사</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">스케일업 팁스(투자)</div>
            <div class="metric-value">{assoc_scaleup_invest}개사</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">스케일업 팁스(R&D)</div>
            <div class="metric-value">{assoc_scaleup_rd}개사</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">프리팁스</div>
            <div class="metric-value">{assoc_pretips}개사</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">립스</div>
            <div class="metric-value">{assoc_lips}개사</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 주요 지표 섹션 - 전체 대비 협회 회원사 비율
    st.subheader("전체 대비 협회 회원사 비율")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">운영 회원사 수</div>
            <div class="metric-value">{association_ratio['운영사 수'][0]}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">일반형 팁스</div>
            <div class="metric-value">{association_ratio['일반형 팁스'][0]}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">스케일업 팁스(투자)</div>
            <div class="metric-value">{association_ratio['스케일업 팁스(투자)'][0]}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">스케일업 팁스(R&D)</div>
            <div class="metric-value">{association_ratio['스케일업 팁스(R&D)'][0]}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">프리팁스</div>
            <div class="metric-value">{association_ratio['프리팁스'][0]}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">립스</div>
            <div class="metric-value">{association_ratio['립스'][0]}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 시각화 섹션
    st.markdown("## 📈 데이터 시각화")
    
    # 차트 데이터 준비
    chart_cols = list(total_data.keys())[1:]  # '운영사 수' 제외
    chart_data = {
        '구분': [],
        '프로그램': [],
        '운영사 수': []
    }
    
    for col in chart_cols:
        chart_data['구분'].extend(['전체', '협회 회원사'])
        chart_data['프로그램'].extend([col, col])
        chart_data['운영사 수'].extend([total_data[col][0], association_data[col][0]])
    
    chart_df = pd.DataFrame(chart_data)
    
    # 프로그램별 운영사 현황 차트만 표시
    st.subheader("프로그램별 운영사 현황")
    fig = px.bar(
        chart_df, 
        x='프로그램', 
        y='운영사 수', 
        color='구분',
        barmode='group',
        color_discrete_map={'전체': '#FF9E44', '협회 회원사': '#4CAF50'},
        height=400
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.2)'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)
    
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

if __name__ == "__main__":
    main()


# streamlit run Tips_Streamlit.py
