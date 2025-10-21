import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="CSV Heatmap Viewer", layout="wide")

st.title("📊 CSVヒートマップ作成アプリ")

# --- ファイルアップロード ---
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

if uploaded_file is not None:
    # CSV読み込み
    df = pd.read_csv(uploaded_file)
    st.subheader("データプレビュー")
    st.dataframe(df.head())

    # --- 列選択 ---
    st.sidebar.header("ヒートマップ設定")
    x_col = st.sidebar.selectbox("x軸の列を選択", df.columns)
    y_col = st.sidebar.selectbox("y軸の列を選択", df.columns)
    color_col = st.sidebar.selectbox("色（値）の列を選択", df.columns)

    # --- ピボットテーブル作成 ---
    try:
        pivot_df = df.pivot(index=y_col, columns=x_col, values=color_col)
    except Exception as e:
        st.error(f"ピボットテーブル作成時にエラーが発生しました: {e}")
    else:
        # --- ヒートマップ描画 ---
        st.subheader("ヒートマップ")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(pivot_df, cmap="viridis", annot=True, fmt=".2f")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        st.pyplot(fig)
else:
    st.info("📂 左上またはここにCSVファイルをドラッグ＆ドロップしてください。")

