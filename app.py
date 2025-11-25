import streamlit as st
import requests

API_BASE = "http://localhost:5000"
 # FastAPI Server URL

st.set_page_config(page_title="Finance MCP Dashboard", page_icon="💹", layout="wide")

st.title("💹 Finance MCP – Streamlit Dashboard")
st.write("Interact with your Finance MCP Server using this interface.")

st.markdown("---")

# ---------------------------
# 🏥 HEALTH CHECK
# ---------------------------
st.header("🔍 Server Health Check")
if st.button("Check Server Health"):
    try:
        response = requests.get(f"{API_BASE}/health").json()
        st.success("Server is Running")
        st.json(response)
    except:
        st.error("❌ Unable to connect to FastAPI server.")

st.markdown("---")

# ---------------------------
# 📈 STOCK PRICE SECTION
# ---------------------------
st.header("📈 Stock Price")

symbol = st.text_input("Enter Stock Symbol (Example: AAPL, TSLA)", "")

if st.button("Get Stock Price"):
    if symbol.strip() == "":
        st.warning("Enter a stock symbol.")
    else:
        try:
            payload = {"symbol": symbol}
            response = requests.post(f"{API_BASE}/stock_price", json=payload).json()

            if "error" in response:
                st.error(response["error"])
            else:
                st.success(f"Price fetched for {response['symbol']}")
                st.json(response)
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")

# ---------------------------
# 🪙 CRYPTO PRICE SECTION
# ---------------------------
st.header("🪙 Crypto Price")

crypto = st.text_input("Enter Crypto Symbol (BTC, ETH)", "")

if st.button("Get Crypto Price"):
    if crypto.strip() == "":
        st.warning("Enter a crypto symbol.")
    else:
        try:
            payload = {"symbol": crypto}
            response = requests.post(f"{API_BASE}/crypto_price", json=payload).json()
            st.json(response)
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")

# ---------------------------
# 📰 FINANCE NEWS SECTION
# ---------------------------
st.header("📰 Finance News")

query = st.text_input("Enter News Query (Example: stocks, crypto, market)", "finance")

# Load available sources from API
try:
    sources = requests.get(f"{API_BASE}/news_sources").json()
    source_options = [src["name"] for src in sources["available_sources"]]
except:
    source_options = ["all", "yahoo", "newsapi", "alphavantage"]

selected_source = st.selectbox("News Source", source_options)

if st.button("Get News"):
    try:
        payload = {"query": query, "source": selected_source}
        response = requests.post(f"{API_BASE}/finance_news", json=payload).json()

        # SAFE ACCESS
        articles = response.get("articles", [])
        count = response.get("articles_found", len(articles))

        st.success(f"Found {count} articles")

        for article in articles:
            st.subheader(article.get("title", "No title"))
            st.write(f"Source: **{article.get('source', 'N/A')}**")
            st.write(article.get("publishedAt", "Unknown date"))
            st.write(f"[Read More]({article.get('url', '#')})")
            st.markdown("---")

    except Exception as e:
        st.error(f"Error: {e}")

# ---------------------------
# 🤖 AI FINANCIAL ANALYSIS
# ---------------------------
st.header("🤖 AI Finance Analysis (GPT)")

prompt = st.text_area("Enter your question (Example: Analyze Tesla stock movement)")

if st.button("Get AI Analysis"):
    try:
        payload = {"prompt": prompt}
        response = requests.post(f"{API_BASE}/ai_analysis", json=payload).json()
        st.success("AI Response:")
        st.write(response["response"])
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")

st.info("🚀 Finance MCP Dashboard Connected to FastAPI Server")
