import streamlit as st
import pandas as pd
import locale

# 한국식 천 단위 콤마 적용
locale.setlocale(locale.LC_ALL, '')

def format_number(num):
    return locale.format_string("%d", num, grouping=True)

def parse_number(s):
    try:
        return int(s.replace(",", "").strip())
    except:
        return 0

# 매수전략 데이터
data = {
    '손절률(%)': list(range(3, 26)),
    '매수비중(%)': [
        100, 75, 60, 50, 43, 38, 33, 30, 27, 25,
        23, 21, 20, 19, 18, 17, 16, 15, 14, 14,
        13, 13, 12
    ]
}
df = pd.DataFrame(data)

st.title("💹 매도를 잘하자")

# 👇 입력값을 문자열로 받되 콤마 표기 유지
col1, col2, col3 = st.columns(3)

with col1:
    총매수금액_raw = st.text_input("총 매수금액 (₩)", format_number(1000000))
    총매수금액 = parse_number(총매수금액_raw)

with col2:
    현재가_raw = st.text_input("현재가", format_number(38025))
    현재가 = parse_number(현재가_raw)

with col3:
    손절가_raw = st.text_input("손절가", format_number(35050))
    손절가 = parse_number(손절가_raw)

# 👉 손절률 계산
if 현재가 > 0 and 손절가 > 0 and 손절가 < 현재가:
    손절률 = round((현재가 - 손절가) / 현재가 * 100, 2)
    st.markdown(f"### 📉 손절률: **{손절률}%**")

    # 👉 매수금액 계산 후 콤마포맷
    df["매수금액"] = ((df["매수비중(%)"] / 100) * 총매수금액).round().astype(int)
    df["매수금액"] = df["매수금액"].apply(lambda x: f"{x:,}")

    # 👉 손절률에 해당하는 전략 추출
    추천 = df[df["손절률(%)"] == round(손절률)]
    if not 추천.empty:
        st.success("💡 해당 손절률의 매수 전략")
        st.dataframe(추천)
    else:
        st.warning("😢 해당 손절률에 맞는 전략이 없습니다.")

    with st.expander("📋 전체 전략표 보기"):
        st.dataframe(df)
else:
    st.info("ℹ️ 현재가와 손절가를 정확히 입력해주세요 (손절가는 현재가보다 작아야 합니다).")
