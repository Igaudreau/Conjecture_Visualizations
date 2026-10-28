import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Collatz Coral", layout="centered", page_icon="🪸")

st.title("🪸 Collatz Conjecture Visualization")

st.subheader("Settings")
even_deg = st.slider('Rotate Even (deg)', 0, 90, 13)
odd_deg = st.slider('Rotate Odd (deg)', 0, 90, 8)
runs = st.number_input('Enter a integer from 1 to 3000', 1, 3000, 1)
def color_picker():
    return np.random.choice(['orangered', 'maroon', 'lightcoral', 'chocolate'])


@st.cache_data(show_spinner="Calculating sequences...")
def get_collatz_path(n, even_angle, odd_angle):
    seq = []
    curr = n
    while curr > 1:
        seq.append(curr)
        curr = curr // 2 if curr % 2 == 0 else 3 * curr + 1
    seq.append(1)
    seq.reverse() # start from 1 to build the tree outward
    
    # Vectorized Math
    seq_arr = np.array(seq)
    angles = np.where(seq_arr % 2 == 0, np.radians(even_angle), -np.radians(odd_angle))
    cumulative_angles = np.cumsum(angles)
    
    x = np.concatenate([[0], np.cumsum(np.cos(cumulative_angles))])
    y = np.concatenate([[0], np.cumsum(np.sin(cumulative_angles))])
    return x, y

fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
ax.set_facecolor('none')
fig.patch.set_facecolor('none')
ax.axis('off')

for i in range(1, runs + 1):
    x, y = get_collatz_path(i, even_deg, odd_deg)
    ax.plot(x, y, color=color_picker(), alpha=1, linewidth=0.5)


# buffer in RAM
buf = io.BytesIO()
fig.savefig(buf, format="png", transparent=True)
buf.seek(0)

st.pyplot(fig, clear_figure=True)

st.download_button(
    label="Download Image",
    data=buf,
    file_name=f"cc_{even_deg}_{odd_deg}_{runs}.png",
    mime="image/png"
)

