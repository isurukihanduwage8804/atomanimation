import streamlit as st
import plotly.graph_objects as go
import numpy as np
import requests

st.set_page_config(page_title="118 Elements Lab", layout="wide")

# මුලද්‍රව්‍ය 118 ම අඩංගු දත්ත ලබාගැනීම
@st.cache_data
def load_element_data():
    url = "https://raw.githubusercontent.com/Bowserinator/Periodic-Table-JSON/master/PeriodicTableJSON.json"
    response = requests.get(url)
    return response.json()['elements']

try:
    elements_data = load_element_data()
    
    st.title("⚛️ පරමාණුක ව්‍යුහය: මුලද්‍රව්‍ය 118 ම මෙතැනින්")
    
    # මුලද්‍රව්‍ය තේරීමේ ලැයිස්තුව
    el_names = [el['name'] for el in elements_data]
    selected_name = st.selectbox("මුලද්‍රව්‍යයක් තෝරන්න (Select an Element):", el_names)
    
    # තෝරාගත් මුලද්‍රව්‍යයේ දත්ත වෙන් කරගැනීම
    el_info = next(el for el in elements_data if el['name'] == selected_name)
    shells = el_info['shells'] # ඉලෙක්ට්‍රෝන වින්යාසය (උදා: [2, 8, 1])

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f"{selected_name} ({el_info['symbol']}) - පරමාණුක ආකෘතිය")
        
        fig = go.Figure()
        # න්‍යෂ්ටිය
        fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', 
                                 marker=dict(size=25, color='red'), name='Nucleus'))

        # සෑම කක්ෂයක් සඳහාම ඉලෙක්ට්‍රෝන ඇඳීම
        for i, e_count in enumerate(shells):
            radius = (i + 1) * 2
            # කක්ෂයේ රේඛාව
            theta = np.linspace(0, 2*np.pi, 100)
            fig.add_trace(go.Scatter(x=radius*np.cos(theta), y=radius*np.sin(theta),
                                     mode='lines', line=dict(color='lightgray', width=1), 
                                     showlegend=False))

            # ඉලෙක්ට්‍රෝන පිහිටීම (Animation එකක් වගේ පෙනීමට කෝණය මාරු කළ හැක)
            e_angles = np.linspace(0, 2*np.pi, e_count, endpoint=False)
            fig.add_trace(go.Scatter(
                x=radius*np.cos(e_angles),
                y=radius*np.sin(e_angles),
                mode='markers',
                marker=dict(size=10, color='blue', line=dict(width=1, color='white')),
                name=f"Shell {i+1}: {e_count}e"
            ))

        fig.update_layout(
            width=700, height=700,
            xaxis=dict(visible=False), yaxis=dict(visible=False),
            plot_bgcolor='white',
            showlegend=True
        )
        st.plotly_chart(fig)

    with col2:
        st.write("### විස්තර තොරතුරු")
        st.write(f"**පරමාණුක ක්‍රමාංකය:** {el_info['number']}")
        st.write(f"**සංකේතය:** {el_info['symbol']}")
        st.write(f"**පරමාණුක ස්කන්ධය:** {el_info['atomic_mass']}")
        st.write(f"**ප්‍රවර්ගය:** {el_info['category']}")
        st.info(f"**ඉලෙක්ට්‍රෝන වින්‍යාසය:** {shells}")
        st.write(f"**සාරාංශය:** {el_info['summary'][:200]}...")

except Exception as e:
    st.error(f"දත්ත ලබාගැනීමේදී දෝෂයක් සිදු විය: {e}")

st.divider()
st.caption("දත්ත සැපයීම: Periodic Table JSON Data")
