# pages/image_prompt.py
import streamlit as st
from dotenv import load_dotenv
import openai
import os

def enhance_prompt(original_prompt, ai_model, style, additional_details):
    system_message = """You are an expert prompt engineer specializing in image generation prompts for AI models. 
    You must ALWAYS return the response in this exact format:

    ### ENHANCED PROMPT:
    [The optimized prompt formatted specifically for the chosen AI model]

    ### EXPLANATION:
    [Brief explanation of the key elements and formatting choices]

    ### VARIATIONS:
    1. [First alternative version]
    2. [Second alternative version]
    3. [Third alternative version]

    For each model, strictly follow these formatting rules:

    DALL-E:
    - Format: [subject], [details], [style], [lighting], [technical parameters]
    - End with: high resolution, 4k, detailed
    - Example: "A majestic lion, mane flowing in wind, golden hour lighting, ultra realistic photography, 4k detail"

    Midjourney:
    - Format: [main subject] :: [detail 1] :: [detail 2] :: [parameters]
    - Always end with: --ar [ratio] --stylize [value] --quality [value]
    - Example: "majestic lion :: flowing mane :: golden hour lighting :: ultra realistic photography --ar 16:9 --stylize 100 --quality 2"

    Stable Diffusion:
    - Format: ([main subject]), [details], [quality tags], [negative prompt]
    - Always include: masterpiece, best quality, highly detailed
    - Always add negative prompt with --no
    - Example: "(majestic lion), flowing mane, golden hour lighting, masterpiece, best quality, highly detailed --no blur, noise, distortion"
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"""
                Original Prompt: {original_prompt}
                Target AI Model: {ai_model}
                Desired Style: {style}
                Additional Details: {additional_details}
                
                Create an optimized image generation prompt following the exact format requirements for {ai_model}.
                Incorporate the style '{style}' and maintain the core concept while enhancing detail and technical parameters.
                """}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def show_image_prompt():
    st.title("🎨 AI Image Prompt Engineer")
    st.markdown("""
    Transform your basic image ideas into powerful, detailed prompts optimized for AI image generation models.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Design Your Image Prompt")
        
        # Original prompt input
        original_prompt = st.text_area(
            "Describe your image idea",
            height=100,
            placeholder="Example: A magical forest at sunset with fireflies"
        )
        
        # AI Model selection
        ai_model = st.selectbox(
            "Choose AI Model",
            ["DALL-E", "Midjourney", "Stable Diffusion"]
        )
        
        # Style selection
        style = st.selectbox(
            "Select Art Style",
            ["Photorealistic", "Digital Art", "Oil Painting", "Watercolor", 
             "3D Render", "Anime", "Comic Book", "Abstract", "Minimalist"]
        )
        
        # Additional details
        additional_details = st.text_area(
            "Additional Details (optional)",
            height=100,
            placeholder="Specify lighting, perspective, mood, colors, or any other details"
        )
        
        if st.button("Generate Enhanced Prompt", type="primary"):
            if original_prompt:
                with st.spinner('Crafting your perfect prompt...'):
                    enhanced_prompt = enhance_prompt(original_prompt, ai_model, style, additional_details)
                    st.session_state.enhanced_prompt = enhanced_prompt
            else:
                st.warning("Please enter an image description.")
    
    with col2:
        st.markdown("### Enhanced Prompt")
        if 'enhanced_prompt' in st.session_state:
            # Split the response into sections
            sections = st.session_state.enhanced_prompt.split('###')
            
            for section in sections:
                if section.strip():
                    # Get section title and content
                    parts = section.strip().split('\n', 1)
                    if len(parts) == 2:
                        title, content = parts
                        st.subheader(title)
                        
                        # Display the main prompt in a copyable code block
                        if "ENHANCED PROMPT" in title:
                            st.code(content.strip(), language="markdown")
                            if st.button("📋 Copy Enhanced Prompt"):
                                try:
                                    st.code(content.strip())
                                    st.success("Click the copy button in the code block above!")
                                except:
                                    st.error("Couldn't create copy button, please copy manually")
                        else:
                            st.markdown(content)
    
    # Model-specific tips
    with st.expander("📚 Model-Specific Tips"):
        st.markdown("""
        ### DALL-E Prompt Tips
        - Be descriptive and specific
        - Mention style, lighting, and perspective
        - Use clear, natural language
        
        ### Midjourney Prompt Tips
        - Use :: to separate concepts
        - Add style modifiers (--stylize, --quality)
        - Specify aspect ratios (--ar 16:9)
        
        ### Stable Diffusion Prompt Tips
        - Use () for emphasis
        - Use [] for strong emphasis
        - Include quality tags (masterpiece, best quality)
        - Add negative prompts with the --no parameter
        """)
        
    # Examples section
    with st.expander("💡 Example Prompts"):
        st.markdown("""
        ### DALL-E Example
        ```
        A magical forest at sunset, golden light filtering through ancient trees, fireflies creating a ethereal atmosphere, photorealistic style, volumetric lighting, 4K resolution
        ```
        
        ### Midjourney Example
        ```
        magical forest at sunset :: ancient trees with twisted branches :: swirling fireflies :: golden hour lighting --ar 16:9 --stylize 1000 --quality 2
        ```
        
        ### Stable Diffusion Example
        ```
        (magical forest at sunset), [ancient twisted trees], floating fireflies, (volumetric golden lighting), masterpiece, best quality, highly detailed --negative low quality, blurry, dark
        ```
        """)