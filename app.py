import streamlit as st 
import os 
from dotenv import load_dotenv 
from google import genai
from tavily import TavilyClient 

load_dotenv() 

# Configure APIs
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Select the model
MODEL_INFO = "gemini-flash-latest"
MODEL_SCRIPT = "gemini-flash-latest" 

st.set_page_config(
    page_title="StoryForge Agent",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ------------------- FUNCTIONS -------------------

def get_realtime_info(query):
    try:
        resp = tavily_client.search(
            query=query,
            max_results=3,
            topic="general"
        )

        if resp and resp.get("results"):
            summaries = []
            for r in resp["results"]:
                title = r.get("title", "")
                snippet = r.get("snippet", "")
                url = r.get("url", "")
                summaries.append(f"**{title}**\n\n{snippet}\n\n🔗 {url}")
            source_info = "\n\n---\n\n".join(summaries)
        else:
            source_info = f"No recent updates found on '{query}'."
    except Exception as e:
        st.error(f"❌ Error fetching info: {e}")
        return None

    prompt = f"""
Using the following real-time information, write an engaging and concise summary (around 200 words) for: {query}

{source_info}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_INFO,
            contents=prompt
        )
        return response.text.strip() if response.text else source_info
    except Exception as e:
        st.error(f"❌ Error generating summary: {e}")
        return source_info


def generate_video_script(info_text):
    prompt = f"""
Turn this into a short engaging video script (100–120 words) with a hook and CTA:

{info_text}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_SCRIPT,
            contents=prompt
        )
        return response.text.strip() if response.text else "⚠️ Could not generate video script."
    except Exception as e:
        st.error(f"❌ Error generating video script: {e}")
        return None


def main():
    st.title("🌐 StoryForge Agent")

    query = st.text_input("🔎 Enter your topic:")

    if query:
        with st.spinner("Fetching info..."):
            info_result = get_realtime_info(query)

        if info_result:
            st.subheader("📚 Summary")
            st.write(info_result)

            if st.button("Generate Script"):
                script = generate_video_script(info_result)

                if script:
                    st.subheader("🎥 Script")
                    st.write(script)


if __name__ == "__main__":
    main()