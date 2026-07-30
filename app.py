import pandas as pd
import streamlit as st
from snownlp import SnowNLP
import plotly.express as px

# 页面基础设置
st.set_page_config(page_title="社交舆论情感分析平台", layout="wide")
st.title("社交媒体舆论情感分析平台")
st.subheader("软件工程×传媒交叉实践项目 | 模拟网络评论舆情研判")

# 直接内置测试评论，不再依赖csv文件
test_data = {
    "评论": [
        "节目舞台效果太棒了，期待后续更新！",
        "宣传节奏有点拖沓，观感一般。",
        "嘉宾互动自然，整体非常治愈。",
        "剪辑很乱，看得一头雾水，有点失望。",
        "画面质感高级，文案很有感染力。",
        "中规中矩，没有特别亮眼的地方。",
        "强烈推荐，内容立意很有价值！",
        "节奏太慢，容易让人失去耐心。",
        "选题新颖，很有现实意义。",
        "无功无过，可以闲暇时候看看。"
    ]
}
df = pd.DataFrame(test_data)

# 情感分析函数
def get_sentiment(text):
    s = SnowNLP(str(text))
    score = s.sentiments
    if score > 0.6:
        return "正面", score
    elif score < 0.4:
        return "负面", score
    else:
        return "中性", score

# 批量计算情感结果
df[["情感倾向", "情感分数"]] = df["评论"].apply(lambda x: pd.Series(get_sentiment(x)))
st.info(f"共载入 {len(df)} 条用户评论数据")

# 侧边筛选栏
st.sidebar.header("筛选条件")
select_type = st.sidebar.multiselect("选择情感倾向", df["情感倾向"].unique(), df["情感倾向"].unique())
filter_df = df[df["情感倾向"].isin(select_type)]

# 展示统计图表
col1, col2 = st.columns(2)
with col1:
    count_fig = px.histogram(filter_df, x="情感倾向", title="评论情感数量分布")
    st.plotly_chart(count_fig, use_container_width=True)
with col2:
    score_fig = px.histogram(filter_df, x="情感分数", title="情感分数分布区间")
    st.plotly_chart(score_fig, use_container_width=True)

# 展示原始数据表格
st.subheader("评论明细数据")
st.dataframe(filter_df, use_container_width=True)