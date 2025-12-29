import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="අතථ්‍ය රසායනාගාරය", layout="wide")

st.title("⚛️ පරමාණුක ව්‍යුහය සහ ඉලෙක්ට්‍රෝන චලනය")
st.write("මුලද්‍රව්‍යයක් තෝරා එහි ඉලෙක්ට්‍රෝන කක්ෂගත වන අයුරු නිරීක්ෂණය කරන්න.")

# මුලද්‍රව්‍ය දත්ත (ප්‍රධාන කිහිපයක් මෙහි ඇත, ඔබට අවශ්‍ය නම් තවත් එක් කළ හැක)
elements = {
    "Hydrogen": {"Z": 1, "config": [1]},
    "Helium": {"Z": 2, "config": [2]},
    "Lithium": {"Z": 3, "config": [2, 1]},
    "Beryllium": {"Z": 4, "config": [2, 2]},
    "Boron": {"Z": 5, "config": [2, 3]},
    "Carbon": {"Z": 6, "config": [2, 4]},
    "Nitrogen": {"Z": 7, "config": [2, 5]},
    "Oxygen": {"Z": 8, "config": [2, 6]},
    "Neon": {"Z": 10, "config": [2, 8]},
    "Sodium": {"Z": 11, "config": [2, 8, 1]},
    "Magnesium": {"Z": 12, "config": [2, 8, 2]},
    "Aluminum": {"Z": 13, "config": [2, 8, 3]},
}

selected_el = st.selectbox("මුලද්‍රව්‍යය තෝරන්න:", list(elements.keys()))
data = elements[selected_el]

st.subheader(f"{selected_el} පරමාණුවේ ආකෘතිය (Atomic Number: {data['Z']})")

def create_atom_plot(config):
    fig = go.Figure()

    # න්‍යෂ්ටිය (Nucleus)
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers',
                             marker=dict(size=20, color='red'), name='Nucleus'))

    # කක්ෂ සහ ඉලෙක්ට්‍රෝන ඇඳීම
    for i, e_count in enumerate(config):
        radius = (i + 1) * 2  # කක්ෂයේ අරය
        
        # කක්ෂය (Orbit line)
        theta = np.linspace(0, 2*np.pi, 100)
        fig.add_trace(go.Scatter(x=radius*np.cos(theta), y=radius*np.sin(theta),
                                 mode='lines', line=dict(color='gray', dash='dash'), 
                                 showlegend=False))

        # ඉලෙක්ට්‍රෝන (Electrons)
        e_angles = np.linspace(0, 2*np.pi, e_count, endpoint=False)
        fig.add_trace(go.Scatter(
            x=radius*np.cos(e_angles),
            y=radius*np.sin(e_angles),
            mode='markers',
            marker=dict(size=10, color='blue'),
            name=f"Shell {i+1} ({e_count}e)"
        ))

    fig.update_layout(
        xaxis=dict(range=[-10, 10], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-10, 10], showgrid=False, zeroline=False, visible=False),
        width=600, height=600,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

st.plotly_chart(create_atom_plot(data['config']))

# ඉලෙක්ට්‍රෝනික වින්‍යාසය පෙන්වීම
st.info(f"ඉලෙක්ට්‍රෝනික වින්‍යාසය: {', '.join(map(str, data['config']))}")
