import streamlit as st 
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title="Data Sweeper", layout='wide')


st.markdown("""
<style>
    body {
        background-color: #f4f4f4;
        color: #222;
    }
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: transparent;
        color: #808080;
        font-weight: bold;
        border-radius: 8px;
        border: 2px solid #808080;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        color: #FF0000;
        border-color: #FF0000;
        background-color: transparent;
    }
    .stButton>button:active {
        color: #FF0000;
        background-color: rgba(255, 0, 0, 0.1);
        border-color: #FF0000;
    }
    .stDownloadButton>button {
        width: 100%;
        background-color: transparent;
        color: #808080;
        font-weight: bold;
        border-radius: 8px;
        border: 2px solid #808080;
        transition: all 0.3s ease;
    }
    .stDownloadButton>button:hover {
        color: #FF0000;
        border-color: #FF0000;
        background-color: transparent;
    }
    .stDownloadButton>button:active {
        color: #FF0000;
        background-color: rgba(255, 0, 0, 0.1);
        border-color: #FF0000;
    }
    .stTitle {
        font-size: 3rem;
        color: #1E3A5F;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stSubheader {
        color: #333;
        font-size: 1.4rem;
        font-weight: bold;
        margin-top: 1.5rem;
    }
    .description {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    /* Style for file uploader button */
    .stFileUploader > div > div > button {
        background-color: transparent;
        color: #808080;
        font-weight: bold;
        border-radius: 8px;
        border: 2px solid #808080;
        transition: all 0.3s ease;
    }
    .stFileUploader > div > div > button:hover {
        color: #FF0000;
        border-color: #FF0000;
        background-color: transparent;
    }
    .stFileUploader > div > div > button:active {
        color: #FFFFFF;
        background-color: #FF0000;
        border-color: #FF0000;
    }
</style>
""", unsafe_allow_html=True)


st.markdown("<h1 class='stTitle'>🧹 Data Sweeper</h1>", unsafe_allow_html=True)
st.markdown("<p class='description'>Effortlessly clean, transform, and visualize your data with just a few clicks!</p>", unsafe_allow_html=True)


uploaded_files = st.file_uploader("📂 Upload your CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else: 
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue        

        st.info(f"📄 **File Name:** {file.name}")
        st.info(f"📏 **File size:** {file.size/1024:.2f} KB")

        st.markdown("<h3 class='stSubheader'>👀 Data Preview</h3>", unsafe_allow_html=True)
        st.dataframe(df.head())
        
        st.markdown("<h3 class='stSubheader'>🧹 Data Cleaning</h3>", unsafe_allow_html=True)
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🔄 Remove Duplicates"):
                    original_count = len(df)
                    df.drop_duplicates(inplace=True)
                    new_count = len(df)
                    st.success(f"✅ Removed {original_count - new_count} duplicate rows.")

            with col2:
                if st.button(f"🔢 Fill Missing Values"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean()) 
                    st.success("✅ Missing values have been filled!")      

        st.markdown("<h3 class='stSubheader'>🎛️ Column Selection</h3>", unsafe_allow_html=True)
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        st.markdown("<h3 class='stSubheader'>📊 Data Visualization</h3>", unsafe_allow_html=True)
        if st.checkbox(f"Show Visualization for {file.name}"):
            numeric_cols = df.select_dtypes(include='number').columns
            if len(numeric_cols) >= 2:
                st.bar_chart(df[numeric_cols].iloc[:,:2])
            else:
                st.warning("⚠️ Not enough numeric columns for visualization.")    

        st.markdown("<h3 class='stSubheader'>🔄 File Conversion</h3>", unsafe_allow_html=True)
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"])
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, "_converted.csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, "_converted.xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)    

            st.download_button(
                label=f"⬇️ Download Converted {file.name}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

        st.markdown("---")

st.success("🎉 All files processed successfully!")
