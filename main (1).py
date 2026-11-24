
import streamlit as st
from PIL import Image
from groq import Groq
import config


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="AI Visionary",
    page_icon="🕵️",
    layout="centered"
)


# ---------------- REPORT STYLES ----------------

STYLES = {
    "Normal": (
        "Look at this image carefully and write a clear, detailed report. "
        "Describe the scene, objects, and what seems to be happening."
    ),

    "Funny": (
        "Look at this image carefully and write a funny image report. "
        "Mention objects, details, and make the report playful and humorous, "
        "but still describe the image correctly."
    ),

    "Detective": (
        "Look at this image like a detective. "
        "Write an investigation-style report with clues, observations, "
        "and smart deductions. Clearly separate observations from guesses."
    ),

    "Dramatic": (
        "Look at this image and describe it in a dramatic, cinematic way. "
        "Make the report vivid, exciting, and expressive."
    ),

    "Story Mode": (
        "Look at this image and write a short story-like scene description. "
        "Describe the setting, objects, and mood creatively."
    ),
}


# ---------------- GROQ CLIENT ----------------

def get_groq_client():
    if not config.GROQ_API_KEY:
        raise ValueError(
            "Groq API key is missing. Add GROQ_API_KEY to your .env file."
        )

    return Groq(api_key=config.GROQ_API_KEY)


# ---------------- IMAGE ANALYSIS ----------------

def analyze_image(uploaded_file, style):

    client = get_groq_client()

    image_bytes = uploaded_file.getvalue()

    import base64

    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model=config.GROQ_VISION_MODEL,

        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": STYLES.get(style, STYLES["Normal"])
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": (
                                f"data:{uploaded_file.type};base64,"
                                f"{encoded_image}"
                            )
                        }
                    }
                ]
            }
        ],

        temperature=0.8,
        max_completion_tokens=700
    )

    return response.choices[0].message.content


# ---------------- APPLICATION UI ----------------

st.title("🕵️ The AI Visionary")

st.write(
    "Upload an image and let artificial intelligence "
    "create an interesting report about it!"
)

st.markdown(
    """
    Choose an image, select your preferred report style,
    and click **Analyze Image**.

    The AI will examine the image and generate a report.
    """
)

st.divider()


# ---------------- IMAGE UPLOAD ----------------

uploaded_file = st.file_uploader(
    "📸 Upload an image",
    type=["png", "jpg", "jpeg", "webp"],
    help="Supported formats: PNG, JPG, JPEG, WEBP"
)


# ---------------- REPORT STYLE ----------------

report_style = st.selectbox(
    "🎨 Choose your report style",
    list(STYLES.keys())
)


# ---------------- IMAGE PREVIEW ----------------

if uploaded_file:

    try:
        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )

    except Exception:
        st.error("Invalid image file. Please upload another image.")


st.divider()


# ---------------- ANALYZE BUTTON ----------------

if st.button("🔍 Analyze Image", type="primary", use_container_width=True):

    if not config.GROQ_API_KEY:

        st.error(
            "Groq API key is missing. "
            "Please add it to your .env file."
        )

    elif not uploaded_file:

        st.warning("Please upload an image first.")

    else:

        try:
            with st.spinner("🧠 AI is studying your image..."):

                report = analyze_image(
                    uploaded_file,
                    report_style
                )

            st.success("Report generated successfully!")

            st.subheader("📝 AI Report")

            st.markdown(report)

        except Exception as error:

            st.error("Something went wrong!")

            st.exception(error)


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "🕵️ AI Visionary | Powered by Python, Streamlit & Groq AI"
)
