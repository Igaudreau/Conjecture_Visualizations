import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Recamán's Sequence Visualizer", layout="centered")

st.title("Recamán's Sequence Visualizer")
st.markdown(
    "Recamán's sequence starts at 0. At step $n$, subtract $n$ if the result is positive and not already in the sequence; otherwise, add $n$."
)

n_terms = st.number_input(
    label="Enter number of terms:",
    min_value=2,
    max_value=1000,
    value=75,
    step=1
)

@st.cache_data
def generate_recaman(n):
    """Generates the first n terms of Recamán's sequence."""
    seq = [0]
    used = {0}
    for i in range(1, n):
        back = seq[-1] - i
        if back > 0 and back not in used:
            seq.append(back)
            used.add(back)
        else:
            forward = seq[-1] + i
            seq.append(forward)
            used.add(forward)
    return seq

terms = generate_recaman(n_terms)

fig, ax = plt.subplots(figsize=(15, 6))
colors = plt.cm.plasma(np.linspace(0, 1, max(len(terms) - 1, 1)))

for i in range(len(terms) - 1):
    x1, x2 = terms[i], terms[i+1]
    center = (x1 + x2) / 2.0
    radius = abs(x1 - x2) / 2.0
    
    # Alternate semicircles above and below the x-axis
    if i % 2 == 0:
        theta = np.linspace(0, np.pi, 200)
    else:
        theta = np.linspace(np.pi, 2 * np.pi, 200)
        
    x = center + radius * np.cos(theta)
    y = radius * np.sin(theta)
    
    ax.plot(x, y, color=colors[i], lw=1.5, alpha=0.8)

ax.axhline(0, color='gray', lw=0.8, linestyle='--')
ax.set_aspect('equal')
ax.set_title(f"Recamán's Sequence (First {n_terms} Terms)", fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel("Sequence Values", fontsize=12)
ax.get_yaxis().set_visible(False)

for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)

plt.tight_layout()

st.pyplot(fig)