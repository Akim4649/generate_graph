import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="CSV可視化アプリ", layout="wide")
st.title("📊 CSVヒートマップ／散布図アプリ")

# --- ファイルアップロード ---
uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df = df.apply(pd.to_numeric, errors='ignore')
    st.subheader("データプレビュー")
    st.dataframe(df.head())

    # --- グラフタイプ選択 ---
    st.sidebar.header("グラフの種類")
    plot_type = st.sidebar.radio(
        "表示タイプを選択",
        ("散布図", "マトリクス表（ヒートマップ）")
    )

    # --- 軸設定 ---
    st.sidebar.header("表示設定")
    x_col = st.sidebar.selectbox("x軸の列を選択", df.columns)
    y_col = st.sidebar.selectbox("y軸の列を選択", df.columns)
    color_col = st.sidebar.selectbox("色（値）の列を選択", df.columns)

    st.subheader("プロット結果")

    # ---------- 散布図 ----------
    if plot_type == "散布図":
        fig, ax = plt.subplots(figsize=(8, 6))

        x = df[x_col]
        y = df[y_col]
        c = df[color_col]

        scatter = ax.scatter(
            x=x,
            y=y,
            c=c,
            cmap="coolwarm",
            edgecolors="black",
            s=100
        )

        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title("")
        cbar = plt.colorbar(scatter, ax=ax, pad=0.02, shrink=0.8)
        cbar.set_label(color_col, rotation=270, labelpad=15)
        st.pyplot(fig)

    # ---------- ヒートマップ ----------
    else:
        try:
            pivot_df = df.pivot_table(
                index=y_col, columns=x_col, values=color_col, aggfunc="mean"
            )
        except Exception as e:
            st.error(f"ピボットテーブル作成時にエラーが発生しました: {e}")
        else:
            # --- 軸の要素選択 ---
            st.sidebar.header("表示要素の選択（ヒートマップ用）")

            all_y = pivot_df.index.tolist()
            all_x = pivot_df.columns.tolist()

            selected_y = st.sidebar.multiselect(
                "縦軸に表示する要素を選択（未選択なら全て）", all_y, default=all_y
            )
            selected_x = st.sidebar.multiselect(
                "横軸に表示する要素を選択（未選択なら全て）", all_x, default=all_x
            )

            # --- ユーザー選択に基づくフィルタ ---
            pivot_df = pivot_df.loc[selected_y, selected_x]

            # --- 縦軸反転 ---
            pivot_df = pivot_df.iloc[::-1]

            n_rows, n_cols = pivot_df.shape
            total_cells = n_rows * n_cols
            font_size = max(6, 16 - np.log10(total_cells + 1) * 2)
            center_val = np.nanmedian(pivot_df.values)

            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(
                pivot_df,
                cmap="coolwarm",
                center=center_val,
                annot=True,
                fmt=".2f",
                annot_kws={"color": "black", "size": font_size},
                cbar=True,
                cbar_kws={"shrink": 0.8, "pad": 0.02, "label": color_col}
            )
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.title("")
            st.pyplot(fig)

else:
    st.info("📂 左上またはここにCSVファイルをドラッグ＆ドロップしてください。")
