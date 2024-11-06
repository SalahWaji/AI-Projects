# app.py
import streamlit as st
from dotenv import load_dotenv
import openai
import os
from pages.image_prompt import show_image_prompt
from pages.text_prompt import show_text_prompt
from pages.linkedin_repurposer import show_linkedin_repurposer

# Load environment variables

if os.path.exists(".env"):
    load_dotenv()
    

openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()


def create_card(title, description, icon, features, button_key, color="#4A90E2"):
    card_html = f"""
    <div style='
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        height: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        &:hover {{
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }}
    '>
        <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
            <span style='
                background-color: {color}; 
                color: white;
                padding: 8px;
                border-radius: 8px;
                margin-right: 10px;
            '>{icon}</span>
            <h3 style='margin: 0; color: {color};'>{title}</h3>
        </div>
        <p style='color: #666; margin-bottom: 1rem;'>{description}</p>
        <ul style='color: #444; margin-bottom: 1rem;'>
    """
    
    for feature in features:
        card_html += f"<li style='margin-bottom: 0.5rem;'>• {feature}</li>"
    
    card_html += "</ul></div>"
    
    st.markdown(card_html, unsafe_allow_html=True)
    if st.button(f"Launch {title}", key=button_key, type="primary"):
        st.session_state.current_tool = button_key
        st.rerun()

def show_home():
    st.title("🚀 AI Tools Hub")
    st.markdown("### Transform Your Content with AI")
    
    # Create three columns for cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_card(
            "Image Prompt Engineer",
            "Create perfect prompts for AI image generation",
            "🎨",
            ["DALL-E Optimization", "Midjourney Format", "Stable Diffusion Style"],
            "image_prompt",
            "#FF6B6B"
        )
        
    with col2:
        create_card(
            "Text Prompt Engineer",
            "Craft effective prompts for text generation",
            "✍️",
            ["ChatGPT Mastery", "Role Definition", "Context Setting"],
            "text_prompt",
            "#4ECDC4"
        )
        
    with col3:
        create_card(
            "LinkedIn Repurposer",
            "Transform content into LinkedIn-ready posts",
            "💼",
            ["Professional Tone", "Engagement Hooks", "Call-to-Action"],
            "linkedin_repurposer",
            "#45B7D1"
        )

def main():
    st.set_page_config(
        page_title="AI Tools Hub",
        page_icon="🚀",
        layout="wide"
    )

    # Custom CSS for better styling
    st.markdown("""
        <style>
        .stButton button {
            width: 100%;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            margin-top: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'current_tool' not in st.session_state:
        st.session_state.current_tool = "home"

    # Sidebar navigation
    with st.sidebar:
        st.title("Navigation")
        if st.button("🏠 Home", type="secondary"):
            st.session_state.current_tool = "home"
            st.rerun()
        
        st.markdown("---")
        st.markdown("### Tools")
        if st.button("🎨 Image Prompts"):
            st.session_state.current_tool = "image_prompt"
            st.rerun()
        if st.button("✍️ Text Prompts"):
            st.session_state.current_tool = "text_prompt"
            st.rerun()
        if st.button("💼 LinkedIn Repurposer"):
            st.session_state.current_tool = "linkedin_repurposer"
            st.rerun()

    # Display current tool
    if st.session_state.current_tool == "home":
        show_home()
    elif st.session_state.current_tool == "image_prompt":
        show_image_prompt()
    elif st.session_state.current_tool == "text_prompt":
        show_text_prompt()
    elif st.session_state.current_tool == "linkedin_repurposer":
        show_linkedin_repurposer()

if __name__ == "__main__":
    main()