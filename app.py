import streamlit as st
import google.generative_ai as genai

st.set_page_config(page_title="软考高项论文AI阅卷", page_icon="📝", layout="wide")

st.title("📝 软考高项论文 AI 阅卷老师")
st.markdown("### 这是一个免费的测试版工具")

# 让用户输入Key，这样你不需要配置复杂的后台
api_key = st.text_input("第一步：请输入 Google API Key (回车确认)", type="password")
st.markdown("[还没有Key? 点这里免费获取](https://aistudio.google.com/app/apikey)")

essay_input = st.text_area("第二步：请在此粘贴你的论文正文", height=400)

if st.button("🚀 开始阅卷", type="primary"):
    if not api_key:
        st.error("请先输入 API Key！")
    elif not essay_input:
        st.warning("请先粘贴论文内容！")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')
            prompt = f"你是一位严厉的软考高项阅卷专家。请对以下论文进行评分（满分75，及格45）。请指出致命硬伤，并给出修改建议。\n\n论文内容：\n{essay_input}"
            
            with st.spinner("阅卷老师正在读你的文章..."):
                response = model.generate_content(prompt)
                
            st.markdown("### 📊 阅卷报告")
            st.markdown(response.text)
            st.success("想要更详细的备考计划？请联系我们的产品经理！")
            
        except Exception as e:
            st.error(f"出错了，请检查Key是否正确。错误信息: {e}")
