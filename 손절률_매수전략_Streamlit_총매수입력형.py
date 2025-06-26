import streamlit as st
import pandas as pd

# 기본값
기본_총매수금액 = 1000000

# 데이터 정의 (비중만 입력해두고 금액은 총매수금액 기반으로 계산)
data = {
    '손절률(%)': list(range(3, 26)),
    '매수비중(%)': [
        100, 75, 60, 50, 43, 38, 33, 30, 27, 25,
        23, 21, 20, 19, 18, 17, 16, 15, 14, 14,
        13, 13, 12
    ]
}
df = pd.DataFrame(data)

# UI
st.title("📊 손절률 기반 매수 전략 시뮬레이터")

# 입력 받기
col1, col2, col3 = st.columns(3)
with col1:
    총매수금액 = st.number_input("총 매수금액 (₩)", value=기본_총매수금액, step=100000, format="%d")
with col2:
    현재가 = st.number_input("현재가", value=38025, step=100, format="%d")
with col3:
    손절가 = st.number_input("손절가", value=35050, step=100, format="%d")

# 손절률 계산
if 현재가 > 0 and 손절가 > 0 and 손절가 < 현재가:
    손절률 = round((현재가 - 손절가) / 현재가 * 100, 2)
    st.markdown(f"### 📉 손절률: **{손절률}%**")

    # 매수금액 계산
    df["매수금액"] = (df["매수비중(%)"] / 100 * 총매수금액).round().astype(int)
    df["매수금액"] = df["매수금액"].apply(lambda x: f"{x:,}")

    # 해당 손절률 행 추출
    추천 = df[df["손절률(%)"] == round(손절률)]
    if not 추천.empty:
        st.success("💡 해당 손절률의 매수 전략")
        st.dataframe(추천)
    else:
        st.warning("해당 손절률에 맞는 매수전략이 없습니다.")

    # 전체 표도 출력
    with st.expander("📋 전체 전략표 보기"):
        st.dataframe(df)
else:
    st.info("ℹ️ 현재가와 손절가를 올바르게 입력해주세요 (손절가는 현재가보다 작아야 합니다).")
