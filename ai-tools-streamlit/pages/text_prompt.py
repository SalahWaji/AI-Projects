# pages/text_prompt.py
import streamlit as st
from dotenv import load_dotenv
import openai
import os

def enhance_text_prompt(original_prompt, use_case, style, additional_details):
    system_message = """You are an expert prompt engineer specialized in crafting perfect text generation prompts.
    You must ALWAYS return the response in this exact format:

    ### ENHANCED PROMPT:
    [The optimized prompt with clear role, context, and requirements]

    ### EXPLANATION:
    [Brief explanation of the prompt structure and key elements]

    ### VARIATIONS:
    1. [First alternative version]
    2. [Second alternative version]
    3. [Third alternative version]

    Key elements to include:
    1. Role Definition: Clear AI role/expertise
    2. Context Setting: Background information
    3. Task Description: Clear objectives
    4. Output Format: Desired structure
    5. Examples (if relevant): Few-shot examples
    6. Constraints: Any limitations or requirements
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"""
                Original Prompt: {original_prompt}
                Use Case: {use_case}
                Style: {style}
                Additional Details: {additional_details}
                
                Create an optimized text generation prompt that follows best practices and clearly defines the role, context, and requirements.
                """}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def show_text_prompt():
    st.title("✍️ Text Prompt Engineer")
    st.markdown("""
    Transform your basic prompts into well-structured instructions for text-based AI models.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Design Your Text Prompt")
        
        # Original prompt input
        original_prompt = st.text_area(
            "Enter your basic prompt",
            height=100,
            placeholder="Example: Write a blog post about artificial intelligence"
        )
        
        # Use case selection
        use_case = st.selectbox(
            "Select Use Case",
            ["Content Writing", "Creative Writing", "Technical Writing", 
             "Academic Writing", "Business Writing", "Chat Response",
             "Analysis & Research", "Brainstorming", "Other"]
        )
        
        # Style selection
        style = st.selectbox(
            "Select Writing Style",
            ["Professional", "Conversational", "Academic", "Creative", 
             "Technical", "Persuasive", "Instructional", "Narrative"]
        )
        
        # Additional details
        additional_details = st.text_area(
            "Additional Requirements (optional)",
            height=100,
            placeholder="Specify tone, length, format, or any other specific requirements"
        )
        
        if st.button("Generate Enhanced Prompt", type="primary"):
            if original_prompt:
                with st.spinner('Crafting your perfect prompt...'):
                    enhanced_prompt = enhance_text_prompt(original_prompt, use_case, style, additional_details)
                    st.session_state.enhanced_prompt = enhanced_prompt
            else:
                st.warning("Please enter a prompt to enhance.")
    
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
    
    # Prompt engineering tips
    with st.expander("📚 Prompt Engineering Tips"):
        st.markdown("""
        ### Best Practices for Text Prompts
        
        1. **Clear Role Definition**
           - Define the AI's expertise
           - Set the context and background
        
        2. **Specific Instructions**
           - Be clear about the desired outcome
           - Specify format and structure
        
        3. **Examples When Needed**
           - Provide few-shot examples
           - Show input/output pairs
        
        4. **Constraints & Requirements**
           - Specify any limitations
           - Define what to include/exclude
        
        5. **Format Specification**
           - Detail the desired output structure
           - Include section requirements
        
        6. **Evaluation Criteria**
           - Define success metrics
           - Specify quality requirements
        """)
        
    # Examples section
    with st.expander("💡 Example Prompts"):
        st.markdown("""
        ### Content Writing Example
        ```
        As a professional content writer with expertise in technology, write a comprehensive blog post about artificial intelligence.
        Target audience: Technology enthusiasts with basic understanding.
        Length: 1000-1200 words
        Structure:
        - Introduction with hook
        - 3-4 main sections
        - Practical examples
        - Conclusion with call to action
        Tone: Informative but conversational
        ```
        
        ### Technical Writing Example
        ```
        As a senior technical documentation specialist, create a step-by-step guide for [process].
        Include:
        - Prerequisites
        - System requirements
        - Detailed steps
        - Troubleshooting section
        Format: Markdown
        Focus on clarity and accuracy
        ```
        """)
        