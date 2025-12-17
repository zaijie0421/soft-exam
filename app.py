import streamlit as st
import os
import sys
import subprocess

# --- 🏴‍☠️ 绝杀技：运行时自动安装依赖 ---
# 这段代码会检查服务器有没有 google-generative-ai，没有就当场安装
try:
    import google.generative_ai as genai
except ImportError:
    st.toast("正在初始化 AI 引擎，请稍候...", icon="🔧")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generative-ai"])
    import google.generative_ai as genai

# --- 页面配置 ---
st.set_page_config(page_title="软考高项论文AI阅卷", page_icon="📝", layout="wide")

st.title("📝 软考高项论文 AI 阅卷老师")
st.info("💡 提示：这是一个 MVP 原型，旨在演示 AI 批改能力。")

# --- 侧边栏 ---
with st.sidebar:
    st.header("🔑 身份验证")
    api_key = st.text_input("请输入 Google API Key", type="password")
    st.markdown("[获取免费 Key](https://aistudio.google.com/app/apikey)")
    st.markdown("---")
    st.markdown("### 商业版功能预览")
    st.write("✅ 历年真题库")
    st.write("✅ 考点押题")
    st.write("✅ 1对1 私教")

# --- 主逻辑 ---
essay_input = st.text_area("在此粘贴您的论文范文 (2000字以内):", height=400)

if st.button("🚀 开始智能批改", type="primary"):
    if not api_key:
        st.error("❌ 请先在左侧输入 API Key")
    elif not essay_input:
        st.warning("⚠️ 请先粘贴论文内容")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            prompt = f"""
            你是一位严厉的软考高项（信息系统项目管理师）阅卷专家。
            请对以下论文进行评分（满分75分，45分及格）。
            
            请按以下格式输出：
            1. **预估分数**：X分
            2. **致命硬伤**：(列出3点)
            3. **修改建议**：(针对摘要、正文、结尾给出具体建议)
            
            论文内容：
            {essay_input}
            """
            
            with st.spinner("AI 阅卷老师正在逐字审读..."):
                response = model.generate_content(prompt)
                
            st.success("✅ 批改完成！")
            st.markdown("### 📊 阅卷报告")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"发生错误: {e}")
