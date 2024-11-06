# pages/linkedin_repurposer.py
import streamlit as st
import openai

def enhance_for_linkedin(content, content_type, tone, goal):
    system_message = """You are an expert LinkedIn content strategist. Transform the provided content into an engaging LinkedIn post that follows these key principles:

    1. Format Requirements:
    - Use line breaks for readability
    - Include relevant emojis
    - Max 3-4 hashtags at the end
    - Include a clear call-to-action
    
    2. Structure:
    - Hook in first 2 lines
    - Short paragraphs (2-3 lines each)
    - Bullet points for key takeaways
    - Engaging question or CTA at the end

    3. LinkedIn Best Practices:
    - Professional yet conversational tone
    - Value-focused content
    - Storytelling elements
    - Actionable insights
    
    Return the response in this format:
    ### ENHANCED POST:
    [The LinkedIn-optimized post]

    ### HASHTAG SUGGESTIONS:
    [3-4 relevant hashtags]

    ### ENGAGEMENT TIPS:
    [2-3 tips for maximizing engagement]
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"""
                Original Content: {content}
                Content Type: {content_type}
                Desired Tone: {tone}
                Post Goal: {goal}
                
                Transform this content into an engaging LinkedIn post that achieves the specified goal.
                """}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def show_linkedin_repurposer():
    st.title("💼 LinkedIn Content Repurposer")
    st.markdown("""
    Transform your content into engaging LinkedIn posts that drive engagement and achieve your professional goals.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Your Content")
        
        content = st.text_area(
            "Original Content",
            height=200,
            placeholder="Paste your content here..."
        )
        
        content_type = st.selectbox(
            "Content Type",
            ["Article Summary", "Personal Achievement", "Company Update", 
             "Industry Insights", "Professional Tips", "Event Announcement"]
        )
        
        tone = st.select_slider(
            "Content Tone",
            options=["Highly Professional", "Professional & Friendly", 
                    "Conversational", "Inspirational", "Thought Leadership"]
        )
        
        goal = st.selectbox(
            "Post Goal",
            ["Drive Engagement", "Share Knowledge", "Generate Leads",
             "Build Authority", "Network Building", "Event Promotion"]
        )
        
        if st.button("Transform for LinkedIn", type="primary"):
            if content:
                with st.spinner('Optimizing your content for LinkedIn...'):
                    enhanced_content = enhance_for_linkedin(content, content_type, tone, goal)
                    st.session_state.enhanced_content = enhanced_content
            else:
                st.warning("Please enter some content to transform.")
    
    with col2:
        st.markdown("### LinkedIn-Optimized Version")
        if 'enhanced_content' in st.session_state:
            sections = st.session_state.enhanced_content.split('###')
            for section in sections:
                if section.strip():
                    parts = section.strip().split('\n', 1)
                    if len(parts) == 2:
                        title, content = parts
                        st.subheader(title.strip())
                        st.markdown(content.strip())
                        
                        if "ENHANCED POST" in title:
                            st.text_area("Copy your post", content.strip(), height=300)
    
    # LinkedIn best practices
    with st.expander("📚 LinkedIn Post Best Practices"):
        st.markdown("""
        ### Key Elements of High-Performing LinkedIn Posts
        
        1. **Strong Hook (First 2-3 Lines)**
           - Start with a question, statistic, or bold statement
           - Make readers want to click "see more"
        
        2. **Visual Structure**
           - Use line breaks for readability
           - Include emojis strategically
           - Utilize bullet points for key takeaways
        
        3. **Engagement Elements**
           - Ask questions
           - Include a clear call-to-action
           - Tag relevant connections when appropriate
        
        4. **Hashtag Strategy**
           - Use 3-4 relevant hashtags
           - Mix broad and niche hashtags
           - Place hashtags at the end of the post
        """)