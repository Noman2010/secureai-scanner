import streamlit as st
import requests

st.set_page_config(page_title="SecureAI Scanner", layout="wide")

st.title("🛡️ SecureAI Scanner")
st.caption("AI-powered website security analysis")

target = st.text_input("🌐 Enter Website URL")

# Clean input
if target:
    target = target.replace("https://", "").replace("http://", "").strip("/")
    url = "https://" + target

scan_clicked = st.button("🚀 Start Scan")

if scan_clicked and target:

    with st.spinner("🔄 Scanning your website..."):

        score = 100
        messages = []
        issues = []

        try:
            response = requests.get(url, timeout=5)
            headers = response.headers

            # -------- HTTPS CHECK --------
            if url.startswith("https://"):
                messages.append(("✅ HTTPS Enabled", "good"))
            else:
                messages.append(("❌ HTTPS Not Enabled", "high"))
                issues.append("Your site is not using HTTPS.")
                score -= 40

            # -------- STATUS CHECK --------
            if response.status_code == 200:
                messages.append(("✅ Website is reachable", "good"))
            else:
                messages.append(("⚠️ Website returned unusual status", "medium"))
                score -= 10

            # -------- SECURITY HEADERS --------
            if "Strict-Transport-Security" not in headers:
                messages.append(("⚠️ Missing HSTS protection", "medium"))
                issues.append("HSTS header not found.")
                score -= 10

            if "Content-Security-Policy" not in headers:
                messages.append(("⚠️ Missing Content Security Policy", "medium"))
                issues.append("CSP header not set.")
                score -= 10

        except:
            messages.append(("❌ Website not reachable", "high"))
            issues.append("Could not connect to website.")
            score -= 50

    # -------- UI --------
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("🔒 Security Score")
        st.metric("Score", f"{score}/100")
        st.progress(score)

        if score > 80:
            st.success("🟢 Secure")
        elif score > 50:
            st.warning("🟡 Moderate Risk")
        else:
            st.error("🔴 High Risk")

    with col2:
        st.subheader("🔍 Scan Results")

        for msg, level in messages:
            if level == "good":
                st.success(msg)
            elif level == "medium":
                st.warning(msg)
            else:
                st.error(msg)

    # -------- AI EXPLANATION --------
    st.subheader("🤖 AI Explanation")

    if not issues:
        st.success("Your website is well secured.")
    else:
        for issue in issues:
            st.write("• " + issue)

    # -------- SUMMARY --------
    st.subheader("🧠 Summary")

    if score > 80:
        st.write("Your website is secure with minor improvements needed.")
    elif score > 50:
        st.write("Your website has some security risks.")
    else:
        st.write("Your website is vulnerable and needs urgent fixes.")

    st.success("✅ Scan Completed")