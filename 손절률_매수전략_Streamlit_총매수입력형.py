import streamlit as st
import pandas as pd
import locale

# 한국식 숫자 포맷 설정
locale.setlocale(locale.LC_ALL, '')

def format_number(num):
    try:
        return locale.format_string("%d", num, grouping=True)
    except:
        return num

def parse_number(s):
    try:
        return int(s.replace(",", "").strip())
    except:
        return 0

# 매수 전략 테이블 정의
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

# 🎯 입력 (왼쪽: 입력창, 오른쪽: 콤마 표시)
col1, col2 = st.columns(2)
with col1:
    총매수금액_raw = st.text_input("총 매수금액 (₩)", "1000000")
    총매수금액 = parse_number(총매수금액_raw)
with col2:
    st.markdown(f"🧾 포맷된 금액: **{format_number(총매수금액)}원**")

col3, col4 = st.columns(2)
with col3:
    현재가_raw = st.text_input("현재가", "38025")
    현재가 = parse_number(현재가_raw)
with col4:
    st.markdown(f"💰 현재가: **{format_number(현재가)}**")

col5, col6 = st.columns(2)
with col5:
    손절가_raw = st.text_input("손절가", "35050")
    손절가 = parse_number(손절가_raw)
with col6:
    st.markdown(f"🔻 손절가: **{format_number(손절가)}**")

# 📉 손절률 계산
if 현재가 > 0 and 손절가 > 0 and 손절가 < 현재가:
    손절률 = round((현재가 - 손절가) / 현재가 * 100, 2)
    st.markdown(f"### 📉 손절률: **{손절률}%**")

    # 💡 전략 계산
df["매수금액"] = ((df["매수비중(%)"] / 100) * 총매수금액).round().astype(int)
df["매수금액"] = df["매수금액"].apply(lambda x: format_number(x))  # 콤마 추가

추천 = df[df["손절률(%)"] == round(손절률)]
if not 추천.empty:
    st.success("💡 해당 손절률의 매수 전략")
    st.table(추천)  # ✅ st.dataframe → st.table
else:
    st.warning("😢 해당 손절률에 맞는 전략이 없습니다.")

with st.expander("📋 전체 전략표 보기"):
    st.table(df)  # ✅ 여기도 dataframe 말고 table
else:
    st.info("ℹ️ 현재가와 손절가를 정확히 입력해주세요 (손절가는 현재가보다 작아야 합니다).")
