import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO

st.title("Running Mean Filter")

uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Preview Data:")
    st.dataframe(df.head())

    columns = df.columns.tolist()
    x_col = st.selectbox("Pilih kolom sumbu X (Time):", columns)
    y_col = st.selectbox("Pilih kolom sumbu Y (Signal):", columns)

    srate = st.number_input("Sampling Rate (Hz)", min_value=100, max_value=5000, value=1000, step=100)
    k = st.number_input("Filter Window (k)", min_value=1, max_value=100, value=20, step=1)

    time = df[x_col].values
    signal = df[y_col].values
    n = len(signal)

    filtsig = np.zeros(n)
    for i in range(k, n-k):
        filtsig[i] = np.mean(signal[i-k:i+k+1])

    windowsize = 1000*(2*k+1) / srate

    df['Filtered_Signal'] = filtsig

    # Plot interaktif
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=signal, mode='lines', name='Original Signal'))
    fig.add_trace(go.Scatter(x=time, y=filtsig, mode='lines', name='Filtered Signal'))
    fig.update_layout(title=f'Running-mean Filter (window size = {windowsize:.2f} ms)',
                      xaxis_title=x_col,
                      yaxis_title=y_col)

    st.plotly_chart(fig)

    # Download CSV hasil
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    st.download_button(
        label="💾 Download hasil CSV",
        data=csv_buffer,
        file_name="filtered_signal.csv",
        mime="text/csv"
    )
else:
    st.info("Silakan upload file CSV berisi sinyal untuk mulai.")
