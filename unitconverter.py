import streamlit as st
import pandas as pd

# Conversion Functions


def convert_length(value, from_unit, to_unit):
    conversions = {
        "meters": 1.0,
        "kilometers": 1000.0,
        "centimeters": 0.01,
        "millimeters": 0.001,
        "inches": 0.0254,
        "feet": 0.3048,
        "yards": 0.9144,
        "miles": 1609.34,
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_weight(value, from_unit, to_unit):
    conversions = {
        "grams": 1.0,
        "kilograms": 1000.0,
        "milligrams": 0.001,
        "pounds": 453.592,
        "ounces": 28.3495,
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_temperature(value, from_unit, to_unit):
    if from_unit == "celsius":
        if to_unit == "fahrenheit": return (value * 9/5) + 32
        if to_unit == "kelvin": return value + 273.15
    elif from_unit == "fahrenheit":
        if to_unit == "celsius": return (value - 32) * 5/9
        if to_unit == "kelvin": return (value - 32) * 5/9 + 273.15
    elif from_unit == "kelvin":
        if to_unit == "celsius": return value - 273.15
        if to_unit == "fahrenheit": return (value - 273.15) * 9/5 + 32
    return value

def convert_speed(value, from_unit, to_unit):
    conversions = {
        "m/s": 1.0,
        "km/h": 0.277778,
        "mph": 0.44704,
        "knots": 0.514444
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_time(value, from_unit, to_unit):
    conversions = {
        "seconds": 1,
        "minutes": 60,
        "hours": 3600,
        "days": 86400
    }
    return value * conversions[from_unit] / conversions[to_unit]

def convert_data(value, from_unit, to_unit):
    conversions = {
        "bytes": 1,
        "kilobytes": 1024,
        "megabytes": 1024**2,
        "gigabytes": 1024**3,
        "terabytes": 1024**4
    }
    return value * conversions[from_unit] / conversions[to_unit]

# Title

st.set_page_config(
    page_title="Ultimate Unit Converter",
    page_icon="📐",
    layout="wide"
)

# Session State Initialization

if "history" not in st.session_state:
    st.session_state.history = []
    
if "favorites" not in st.session_state:
    st.session_state.favorites = []


# Unit Definitions

UNIT_CATEGORIES = {
    "Length": ["meters", "kilometers", "centimeters", "millimeters", 
              "inches", "feet", "yards", "miles"],
    "Weight": ["grams", "kilograms", "milligrams", "pounds", "ounces"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Speed": ["m/s", "km/h", "mph", "knots"],
    "Time": ["seconds", "minutes", "hours", "days"],
    "Data Storage": ["bytes", "kilobytes", "megabytes", "gigabytes", "terabytes"]
}


# Theme 

def set_theme(theme_name):
    if theme_name == "Dark":
     st.markdown(
            """
            <style>
                /* Background */
                .stApp {
                    background-color:rgb(39, 36, 36) !important; /* Bright grey */
                    color: black !important;
                }
                /* Widgets (boxes, buttons, etc.) */
                .stTextInput, .stNumberInput, .stSelectbox, .stButton>button {
                    background-color:rgb(130, 131, 131) !important; /* Dark grey */
                    color: black !important;
                    border-color:rgb(28, 24, 24) !important;
                }
                /* Labels and titles */
                .stMarkdown, .stHeader, .stTitle, .stSubheader, .stText {
                    color: back !important;
                }
                /* Sidebar */
                .css-1d391kg, .css-1d391kg>div {
                    background-color: #E0E0E0 !important; /* Light grey */
                    color: black !important;
                }
                /* Dataframes */
                .stDataFrame {
                    background-color: #D3D3D3 !important;
                    color: black !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
    elif theme_name == "Professional":
        st.markdown(
            """
            <style>
                /* Background */
                .stApp {
                    background-color: #ed9a5a !important; /* Bright grey */
                    color: black !important;
                }
                /* Widgets (boxes, buttons, etc.) */
                .stTextInput, .stNumberInput, .stSelectbox, .stButton>button {
                    background-color: #ed9a5a  !important; /* Dark grey */
                    color: black !important;
                    border-color: #A9A9A9 !important;
                }
                /* Labels and titles */
                .stMarkdown, .stHeader, .stTitle, .stSubheader, .stText {
                    color: black !important;
                }
                /* Sidebar */
                .css-1d391kg, .css-1d391kg>div {
                    background-color: #E0E0E0 !important; /* Light grey */
                    color: black !important;
                }
                /* Dataframes */
                .stDataFrame {
                    background-color: #D3D3D3 !important;
                    color: black !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:  # Light theme
        st.markdown(
            """
            <style>
                .stApp {
                    background-color: white;
                    color: black;
                }
            </style>
            """,
            unsafe_allow_html=True,)

# Main App Layout

def main():
    # Theme Selection
    with st.sidebar:
        st.header("Settings")
        theme = st.selectbox("Theme", ["Light", "Dark", "Professional"])
        set_theme(theme)
        
        # Favorites Management
        st.subheader("⭐NOTES & FAVOURIES")
        favorite_name = st.text_input("Save  notes, comments & conversions as favorite:")
        if st.button("Add"):
            if favorite_name:
                st.session_state.favorites.append({
                    "name": favorite_name,
                    "category": st.session_state.input_values["category"],
                    "from_unit": st.session_state.input_values["from_unit"],
                    "to_unit": st.session_state.input_values["to_unit"]
                })
        
        if st.session_state.favorites:
            st.write("Saved Favorites:")
            for fav in st.session_state.favorites:
                col1, col2 = st.columns([3,1])
                with col1:
                    st.write(f"📌 {fav['name']}")
                with col2:
                    if st.button(f"❌", key=f"del_{fav['name']}"):
                        st.session_state.favorites.remove(fav)

    # Initialize input values
    if "input_values" not in st.session_state:
        default_category = "Length"
        default_units = UNIT_CATEGORIES[default_category]
        st.session_state.input_values = {
            "value": 1.0,
            "from_unit": default_units[0],
            "to_unit": default_units[0],
            "category": default_category
        }

    # Main Interface
    st.title("🚀 Your Ultimate Unit Converter")
    st.markdown("---")
    
    # Category Selection
    category = st.selectbox(
        "Select Conversion Type",
        list(UNIT_CATEGORIES.keys()),
        key="category_select"
    )

    # Input Fields
    col1, col2 = st.columns(2)
    with col1:
        new_value = st.number_input(
            "Enter Value",
            min_value=0.0,
            value=st.session_state.input_values["value"],
            key="value_input"
        )
        try:
            from_index = UNIT_CATEGORIES[category].index(st.session_state.input_values["from_unit"])
        except ValueError:
            from_index = 0
        new_from_unit = st.selectbox(
            "From Unit",
            UNIT_CATEGORIES[category],
            index=from_index,
            key="from_unit_select"
        )

    with col2:
        try:
            to_index = UNIT_CATEGORIES[category].index(st.session_state.input_values["to_unit"])
        except ValueError:
            to_index = 0
        new_to_unit = st.selectbox(
            "To Unit",
            UNIT_CATEGORIES[category],
            index=to_index,
            key="to_unit_select"
        )

    # Conversion Logic
    inputs_changed = (
        new_value != st.session_state.input_values["value"] or
        new_from_unit != st.session_state.input_values["from_unit"] or
        new_to_unit != st.session_state.input_values["to_unit"] or
        category != st.session_state.input_values["category"]
    )

    if inputs_changed:
        # Handle category changes
        if category != st.session_state.input_values["category"]:
            new_from_unit = UNIT_CATEGORIES[category][0]
            new_to_unit = UNIT_CATEGORIES[category][0]

        st.session_state.input_values = {
            "value": new_value,
            "from_unit": new_from_unit,
            "to_unit": new_to_unit,
            "category": category
        }

        try:
            if category == "Length":
                result = convert_length(new_value, new_from_unit, new_to_unit)
            elif category == "Weight":
                result = convert_weight(new_value, new_from_unit, new_to_unit)
            elif category == "Temperature":
                result = convert_temperature(new_value, new_from_unit, new_to_unit)
            elif category == "Speed":
                result = convert_speed(new_value, new_from_unit, new_to_unit)
            elif category == "Time":
                result = convert_time(new_value, new_from_unit, new_to_unit)
            elif category == "Data Storage":
                result = convert_data(new_value, new_from_unit, new_to_unit)
            else:
                raise ValueError("Invalid category")

            st.success(f"✅ **{new_value:.2f} {new_from_unit} = {result:.4f} {new_to_unit}**")
            st.session_state.history.append(
                f"{new_value:.2f} {new_from_unit} → {result:.4f} {new_to_unit} ({category})"
            )

        except Exception as e:
            st.error(f"⚠️ Conversion error: {str(e)}")

    # History Section
    st.markdown("---")
    st.subheader("📜 Conversion History")
    
    if st.button("Clear History"):
        st.session_state.history = []
    
    if st.session_state.history:
        history_df = pd.DataFrame(reversed(st.session_state.history), columns=["Conversion"])
        st.dataframe(history_df, use_container_width=True)
        
        if st.button("Export History as CSV"):
            history_df.to_csv("conversion_history.csv", index=False)
            st.success("History exported successfully!")
    else:
        st.info("No conversion history yet.")

if __name__ == "__main__":
    main()


st.markdown("---")
st.write(f"--MADE BY ZAIN UL ABIDEEN--")   