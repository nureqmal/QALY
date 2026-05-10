import streamlit as st
import anthropic

SYSTEM_PROMPT = """You are the AI marketing brain for Qaly, a Malaysian halal deodorant startup founded by PhD chemistry researchers at IIUM (International Islamic University Malaysia).

About Qaly:
- Products: Qaly Base (blank liquid deodorant, customer adds their own perfume), Syed (men's scented), Syeda (women's scented)
- Key ingredients: magnesium chloride, aloe vera, dipropylene glycol, potassium sorbate, water
- NO aluminium, NO paraben
- Founded by PhD/Master's students in halal chemistry
- Sells on campus (IIUM Gombak), Shopee (shopee.com.my/qaly.my), Instagram (@qaly.my)
- Target: Muslim millennials & Gen Z Malaysia, health-conscious, value local products

Brand voice: Confident, science-backed, relatable, authentic. Not corporate. Not preachy.
Brand USP: Only deodorant in Malaysia where you personalise the scent yourself (blank base concept).
Tagline: "Your scent. Our science."

Always write content that is specific to Qaly — not generic deodorant marketing.
For Instagram captions: include a hook line, body, call to action, and relevant hashtags.
Keep Malay/English mix natural when writing in Bahasa Malaysia."""

def call_claude(messages, api_key):
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=messages
    )
    return response.content[0].text

def show():
    st.title("✍️ AI Content Studio")
    st.caption("Generate captions, ideas, and copy — powered by Claude AI")
    st.divider()

    if "api_key" not in st.session_state:
        st.warning("⚠️ Add your Anthropic API key in Settings (sidebar) to use AI features.")
        st.stop()

    tab1, tab2, tab3 = st.tabs(["📸 Caption Generator", "💡 Content Ideas", "💬 Qaly AI Chat"])

    # ── Tab 1: Caption Generator ──────────────────────
    with tab1:
        st.subheader("Instagram caption generator")

        col1, col2 = st.columns(2)
        with col1:
            product = st.selectbox("Product", ["Qaly Base", "Syed", "Syeda", "All products / brand"])
            pillar = st.selectbox("Content pillar", [
                "Educate — ingredient science",
                "Personalise — blank base concept",
                "Local pride — Malaysian founders",
                "Social proof — testimonial style",
                "Promo — soft sell",
            ])
        with col2:
            language = st.selectbox("Language", ["English", "Bahasa Malaysia", "Mix (Manglish)"])
            tone = st.selectbox("Tone", ["Informative", "Casual & relatable", "Bold & confident", "Soft & warm"])

        extra = st.text_area("Any specific angle or info to include?", placeholder="e.g. mention it's perfect for gym days, or reference Ramadan season")

        if st.button("Generate caption ✨", use_container_width=True):
            prompt = f"""Write an Instagram caption for Qaly.

Product: {product}
Content pillar: {pillar}
Language: {language}
Tone: {tone}
Extra context: {extra if extra else 'None'}

Include: hook, body, call to action, and 10 relevant hashtags."""

            with st.spinner("Writing your caption..."):
                try:
                    result = call_claude([{"role": "user", "content": prompt}], st.session_state["api_key"])
                    st.session_state["last_caption"] = result
                except Exception as e:
                    st.error(f"API error: {e}")

        if "last_caption" in st.session_state:
            st.divider()
            st.subheader("Generated caption")
            st.text_area("Caption", st.session_state["last_caption"], height=350, key="caption_output")
            if st.button("📋 Copy to clipboard"):
                st.write("Select all text above and copy (Ctrl+A, Ctrl+C)")
            if st.button("🔄 Regenerate with different style"):
                del st.session_state["last_caption"]
                st.rerun()

    # ── Tab 2: Content Ideas ──────────────────────────
    with tab2:
        st.subheader("Weekly content idea generator")
        col1, col2 = st.columns(2)
        with col1:
            num_ideas = st.slider("Number of ideas", 3, 10, 7)
            focus = st.multiselect("Focus on", ["Reels", "Carousel", "Single post", "Story"], default=["Reels", "Carousel"])
        with col2:
            theme = st.text_input("Any theme this week?", placeholder="e.g. back to campus, Eid prep, gym season")

        if st.button("Generate content plan ✨", use_container_width=True):
            prompt = f"""Create {num_ideas} Instagram content ideas for Qaly this week.

Format types to include: {', '.join(focus) if focus else 'mixed'}
Theme/context: {theme if theme else 'general'}

For each idea, give:
1. Post type (Reel/Carousel/Single/Story)
2. Hook/title
3. What to show visually
4. Key message
5. Best time to post

Make them specific and actionable for a small team with limited budget."""

            with st.spinner("Generating ideas..."):
                try:
                    result = call_claude([{"role": "user", "content": prompt}], st.session_state["api_key"])
                    st.markdown(result)
                except Exception as e:
                    st.error(f"API error: {e}")

    # ── Tab 3: AI Chat ────────────────────────────────
    with tab3:
        st.subheader("Chat with Qaly AI")
        st.caption("Ask anything — marketing, strategy, copywriting, business advice")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Quick prompt from dashboard
        if "quick_prompt" in st.session_state:
            initial = st.session_state.pop("quick_prompt")
            st.session_state.chat_history.append({"role": "user", "content": initial})
            with st.spinner("Thinking..."):
                try:
                    reply = call_claude(st.session_state.chat_history, st.session_state["api_key"])
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"Error: {e}")

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("Ask Qaly AI anything...")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        reply = call_claude(st.session_state.chat_history, st.session_state["api_key"])
                        st.markdown(reply)
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    except Exception as e:
                        st.error(f"API error: {e}")

        if st.session_state.chat_history:
            if st.button("🗑️ Clear chat"):
                st.session_state.chat_history = []
                st.rerun()
