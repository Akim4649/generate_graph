import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="CSV可視化アプリ", layout="wide")
st.title("📊 CSVヒートマップ／散布図アプリ")

# --- ファイルアップロード ---
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df = df.apply(pd.to_numeric, errors='ignore')
    st.subheader("データプレビュー.上位5個まで表示")
    st.dataframe(df.head(5))

    # --- 列選択 ---
    st.sidebar.header("表示設定")
    x_col = st.sidebar.selectbox("x軸の列を選択", df.columns)
    y_col = st.sidebar.selectbox("y軸の列を選択", df.columns)
    color_col = st.sidebar.selectbox("色（値）の列を選択", df.columns)

    # --- 散布図 or ヒートマップの判定 ---
    x_is_numeric = pd.api.types.is_numeric_dtype(df[x_col])
    y_is_numeric = pd.api.types.is_numeric_dtype(df[y_col])

    st.subheader("プロット結果")

    if x_is_numeric and y_is_numeric:
        # ---------- 散布図モード ----------
        fig, ax = plt.subplots(figsize=(8, 6))
        scatter = sns.scatterplot(
            data=df, x=x_col, y=y_col, hue=color_col,
            palette="viridis", s=100, edgecolor="black", ax=ax
        )
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        # 凡例をグラフの外に配置
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        # グラフタイトル非表示
        plt.title("")
        st.pyplot(fig)

    else:
        # ---------- ヒートマップモード ----------
        try:
            pivot_df = df.pivot(index=y_col, columns=x_col, values=color_col)
        except Exception as e:
            st.error(f"ピボットテーブル作成時にエラーが発生しました: {e}")
        else:
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(
                pivot_df,
                cmap="viridis",
                annot=True,
                fmt=".2f",
                annot_kws={"color": "black"},  # 🔹黒字指定
                cbar_kws={"shrink": 0.8, "pad": 0.02}  # カラーバーの位置調整
            )
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.title("")  # 🔹タイトル非表示
            st.pyplot(fig)
else:
    st.info("📂 左上またはここにCSVファイルをドラッグ＆ドロップしてください。")
