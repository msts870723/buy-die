import streamlit as st
import pandas as pd
import locale

# 숫자 포맷 설정 (한국 기준)
locale.setlocale(locale.LC_ALL, '')

def format_number(num):
    return locale.format_string("%d", num, grouping=True)

def parse_number(s):
    try:
        return int(s.replace(",", ""))
    except:
        return 0

# 데이터 정의
data = {
    '손절률(%)': list(range(3, 26)),
    '매수비중(%)': [
        100, 75, 60, 50, 43, 38, 33, 30, 27, 25,
        23, 21, 20, 19, 18, 17, 16, 15, 14, 14,
        13, 13, 12
    ]
}
df = pd.DataFrame(data)

st.title("💹 손절률 기반 매수 전략 시뮬레이터")

# 👇 사용자 입력값 (쉼표포맷)
col1, col2, col3 = st.columns(3)

with col1:
    총매수금액_input = st.text_input("총 매수금액 (₩)", value=format_number(1000000))
    총매수금액 = parse_number(총매수금액_input)

with col2:
    현재가_input = st.text_input("현재가", value=format_number(38025))
    현재가 = parse_number(현재가_input)

with col3:
    손절가_input = st.text_input("손절가", value=format_number(35050))
    손절가 = parse_number(손절가_input)

# 👉 손절률 계산
if 현재가 > 0 and 손절가 > 0 and 손절가 < 현재가:
    손절률 = round((현재가 - 손절가) / 현재가 * 100, 2)
    st.markdown(f"### 📉 손절률: **{손절률}%**")

    # 👉 매수금액 계산 및 콤마 추가
    df["매수금액"] = ((df["매수비중(%)"] / 100) * 총매수금액).round().astype(int)
    df["매수금액"] = df["매수금액"].apply(lambda x: f"{x:,}")

    # 👉 추천 전략 표시
    추천 = df[df["손절률(%)"] == round(손절률)]
    if not 추천.empty:
        st.success("💡 해당 손절률의 매수 전략")
        st.dataframe(추천)
    else:
        st.warning("😢 해당 손절률에 맞는 매수전략이 없습니다.")

    # 👉 전체 전략표 표시
    with st.expander("📋 전체 전략표 보기"):
        st.dataframe(df)
else:
    st.info("ℹ️ 현재가와 손절가를 올바르게 입력해주세요. (손절가는 현재가보다 작아야 합니다)")
