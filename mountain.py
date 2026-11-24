import io
import streamlit as st
f*rom huggingface_hub import InferenceClient
import config

st.set_page_config(page_title="Ai mountain scenery", page_icon="🌄", layout="centered")

OPTIONS = {
    "mountain-type": ["volcano","dome mountain","valley","black mountains" ],
    "weather": ["sunny","rainy","snowy","sunny mountains" ],
    "time of day": ["morning","noon","afternoon","night" ],
    "mood": ["happy","sad","neutral","angry" ],
    "art style": ["art deco","renaissence","expressionism"," minimalism" ],



}
client = InferenceClient(api_key=config.HF_API_KEY)
st.session_state.setdefault("generated_image", None)

st.title("ai mountain scenery generator")
st.write("create your own image with AI")
st.markdown("choose your image details, then click generate")
st.subheader("Create your landscape image")


mode=st.selectbox("choose your prompt mode", ["Use image builder", "write your own custom prompt"])

if mode == "Use image builder":
    values={k: st.slectbox(f"Choose{k}", v) for k, v in OPTIONS.items()}
    extra=st.text_input("Add one extra detail(optional)", placeholder="example: lake in middle")
    prompt = (
        f"A {values['mountain-type']}",
        f"while being {values['weather']}",
        f"at {values['time of day']}",
        f"with a {values['mood']} vibe",
        f"{values['art style']} expression"
    )
    final-prompt=f"{prompt}, {extra}" if extra else prompt
else:
    final_prompt=st.text_area(
        "write your own prompt",
        placeholder="example: A snowy mountain with polar bears ...",
        height=150
    ).strip()


with st.expander("see AI prompt"):
    st.write(final prompt or "Your prompt will be here")


if st.button("generate avatar"):
    if not config.HR.API.KEY:
        st.error("hugging face api key is missing")
    elif not final_prompt:
        st.warning("please enter a prompt first")
    else:
        with st.spinner("creating avatar"):
            try:
                st.session_state.generated_image=client.text_to_image(
                    prompt=final_prompt,
                    model=config.HF.IMAGE.MODEL,

                )
                st.success("your avatar is ready")
            except Exception as e:
                st.error(f"something went wrong {e}")

if st.session_state.generated_image:
    st.image(st.session_state.generated_image, caption="your AI avatar", use_continer_width=True )
    buffer=io.BytesIO()
    st.session_state.generated_image.save(buffer,format="PNG")
    st.download_button(
        "download avatar",
        data=buffer.getvalue(),
        file_name="ai_avatar.png",
        mime="image/png",
        
    )
