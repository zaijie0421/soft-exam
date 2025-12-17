import streamlit as st
import requests
import json

# --- 页面配置 ---
st.set_page_config(page_title="软考高项论文AI阅卷", page_icon="📝", layout="wide")

st.title("📝 软考高项论文 AI 阅卷老师")
st.caption("🚀 极速版 - 采用 REST API 直连技术")

# --- 侧边栏配置 ---
with st.sidebar:
    st.header("🔑 身份验证")
    api_key = st.text_input("请输入 Google API Key", type="password")
    st.markdown("[点击获取免费 Key](https://aistudio.google.com/app/apikey)")
    
    st.divider()
    st.info("💡 为什么用这个版本？\n因为 Streamlit 服务器有时候装不上 AI 插件，这个版本使用了更底层的 Web 通信技术，更加稳定！")

# --- 核心逻辑：直接发网络请求给 Google ---
def call_gemini_api(key, text):
    # 这是 Google Gemini 的直接访问地址
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro:generateContent?key={key}"
    headers = {'Content-Type': 'application/json'}
    
    # 构造像阅卷老师一样的提示词
    prompt_text = f"""
    你是一位严厉的软考高项（信息系统项目管理师）阅卷专家。
    请对以下论文进行评分（满分75分，45分及格）。
    
    输出要求：
    1. 给出预估分数。
    2. 列出3个扣分点（致命硬伤）。
    3. 给出分段修改建议。
    
    学生论文内容：
    {text}
    """
    
    data = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    
    # 发送请求
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error: {response.text}"

# --- 界面交互 ---
essay_input = st.text_area("请在此粘贴论文内容 (建议2000字以内):", height=400)

if st.button("🚀 开始阅卷", type="primary"):
    if not api_key:
        st.error("❌ 必须要填 API Key 才能用哦！")
    elif not essay_input:
        st.warning("⚠️ 没看到论文，请先粘贴内容！")
    else:
        with st.spinner("正在通过加密通道连接 Google 大脑..."):
            try:
                result = call_gemini_api(api_key, essay_input)
                st.success("✅ 批改完成！")
                st.markdown("### 📊 阅卷报告")
                st.divider()
                st.markdown(result)
            except Exception as e:
                st.error(f"网络请求出错: {e}")
