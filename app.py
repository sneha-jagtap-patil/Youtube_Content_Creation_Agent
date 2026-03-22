import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai 
from tavily import TavilyClient

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
