import streamlit as st

# ---------------- Functions ----------------

def two_product_formula(F=None, C=None, T=None, f=None, c=None, t=None):
    knowns = {'F': F, 'C': C, 'T': T, 'f': f, 'c': c, 't': t}
    unknowns = [k for k, v in knowns.items() if v is None]

    if len(unknowns) != 2:
        return {"Error": "Please leave exactly two variables as None."}

    # Initialize results
    results = {"C": None, "T": None, "Recovery": None}

    # Example: C and T unknown
    if 'C' in unknowns and 'T' in unknowns and F is not None:
        if all(v is not None for v in [F, f, c, t]):
            C = (F * (f - t)) / (c - t)
            T = F - C
            results["C"] = round(C, 2)
            results["T"] = round(T, 2)
        else:
            return {"Error": "Not enough info to solve for C and T."}

    # Recovery
    if all(v is not None for v in [F, C, f, c]) and f != 0:
        recovery = 100 * (C * c) / (F * f)
        results["Recovery"] = round(recovery, 2)

    return results


def water_calculation(F=None, U=None, V=None, f=None, u=None, v=None, m=None):
    knowns = {'F': F, 'U': U, 'V': V, 'f': f, 'u': u, 'v': v}
    unknowns = [k for k, l in knowns.items() if l is None]

    if len(unknowns) != 2:
        return {"Error": "Please leave exactly two variables as None."}

    results = {"F": F, "U": U, "V": V}

    # 1) U and V
    if 'U' in unknowns and 'V' in unknowns and F is not None:
        if all(l is not None for l in [F, f, u, v]):
            U = (F * (f - v)) / (u - v)
            V = F - U
            results["U"] = round(U, 2)
            results["V"] = round(V, 2)

    # 2) F and U
    elif 'F' in unknowns and 'U' in unknowns and all(l is not None for l in [V, f, u, v]):
        F = V * (v - u) / (f - u)
        U = F - V
        results["F"] = round(F, 2)
        results["U"] = round(U, 2)

    # 3) F and V
    elif 'F' in unknowns and 'V' in unknowns and all(l is not None for l in [U, f, u, v]):
        F = U * (u - v) / (f - v)
        V = F - U
        results["F"] = round(F, 2)
        results["V"] = round(V, 2)

    else:
        return {"Error": "Combination not supported or insufficient data."}

    # Water calculations
    if all(val is not None for val in [F, V, U, f, u, v, m]):
        water_ball_mill_feed = round(V * (m / (100 - m)) + U * u, 1)
        water_cyclone_feed = round((V + U) * f, 1)
        water_requirement_cyclone = round(water_cyclone_feed - water_ball_mill_feed, 1)

        results["Water in Ball Mill Feed"] = f"{water_ball_mill_feed} m³/h"
        results["Water in Cyclone Feed"] = f"{water_cyclone_feed} m³/h"
        results["Water Requirement at Cyclone Feed"] = f"{water_requirement_cyclone} m³/h"
    else:
        results["Note"] = "Water calculation skipped due to missing values."

    return results


# ---------------- Streamlit App ----------------

st.set_page_config(page_title="Mineral Processing Tool", page_icon="⛏️", layout="wide")
st.title("Mineral Processing Tool")

st.sidebar.header("Instructions")
st.sidebar.write("This Mineral Processing Tool lets you perform **two-product** and **water balance** calculations. "
                 "Enter known values, mark exactly two variables as Unknown, and click Calculate.")

# --- Two Product Formula ---
st.header("⚖️ Two-Product Formula")

col1, col2, col3 = st.columns(3)
two_inputs = {}
two_unknowns = {}

with col1:
    two_inputs['F'] = st.text_input("Feed (F) [t/h]")
    two_inputs['C'] = st.text_input("Concentrate (C) [t/h]")
    two_inputs['T'] = st.text_input("Tailings (T) [t/h]")
with col2:
    two_inputs['f'] = st.text_input("Feed Grade (f) [%]")
    two_inputs['c'] = st.text_input("Concentrate Grade (c) [%]")
    two_inputs['t'] = st.text_input("Tailings Grade (t) [%]")
with col3:
    two_unknowns['F'] = st.checkbox("Unknown F")
    two_unknowns['C'] = st.checkbox("Unknown C")
    two_unknowns['T'] = st.checkbox("Unknown T")
    two_unknowns['f'] = st.checkbox("Unknown f")
    two_unknowns['c'] = st.checkbox("Unknown c")
    two_unknowns['t'] = st.checkbox("Unknown t")

if st.button("Calculate Two-Product"):
    inputs = {}
    unknown_count = 0
    for k in two_inputs:
        if two_unknowns[k]:
            inputs[k] = None
            unknown_count += 1
        else:
            try:
                inputs[k] = float(two_inputs[k]) if two_inputs[k] else None
            except:
                inputs[k] = None

    if unknown_count != 2:
        st.error("Please mark exactly two variables as Unknown.")
    else:
        result = two_product_formula(**inputs)

        if "Error" in result:
            st.error(result["Error"])
        else:
            col1, col2, col3 = st.columns(3)
            if result["C"] is not None:
                col1.metric("Concentrate (C)", f"{result['C']} t/h")
            if result["T"] is not None:
                col2.metric("Tailings (T)", f"{result['T']} t/h")
            if result["Recovery"] is not None:
                col3.metric("Recovery", f"{result['Recovery']} %")


# --- Water Calculation ---
st.header("💧 Water Balance")

col4, col5, col6 = st.columns(3)
water_inputs = {}
water_unknowns = {}

with col4:
    water_inputs['F'] = st.text_input("Feed (F) [t/h]", key="wF")
    water_inputs['U'] = st.text_input("Underflow (U) [t/h]", key="wU")
    water_inputs['V'] = st.text_input("Overflow (V) [t/h]", key="wV")
with col5:
    water_inputs['f'] = st.text_input("Feed Dilution Ratio (f) [ratio]", key="wf")
    water_inputs['u'] = st.text_input("Underflow Dilution Ratio (u) [ratio]", key="wu")
    water_inputs['v'] = st.text_input("Overflow Dilution Ratio (v) [ratio]", key="wv")
    water_inputs['m'] = st.text_input("Moisture Content (m) [%]", key="wm")
with col6:
    water_unknowns['F'] = st.checkbox("Unknown F", key="uF")
    water_unknowns['U'] = st.checkbox("Unknown U", key="uU")
    water_unknowns['V'] = st.checkbox("Unknown V", key="uV")
    water_unknowns['f'] = st.checkbox("Unknown f", key="uf")
    water_unknowns['u'] = st.checkbox("Unknown u", key="uu")
    water_unknowns['v'] = st.checkbox("Unknown v", key="uv")

if st.button("Calculate Water"):
    inputs = {}
    unknown_count = 0
    for k in ['F','U','V','f','u','v']:
        if water_unknowns[k]:
            inputs[k] = None
            unknown_count += 1
        else:
            try:
                inputs[k] = float(water_inputs[k]) if water_inputs[k] else None
            except:
                inputs[k] = None
    try:
        inputs['m'] = float(water_inputs['m']) if water_inputs['m'] else None
    except:
        inputs['m'] = None

    if unknown_count != 2:
        st.error("Please mark exactly two variables as Unknown.")
    else:
               else:
            # First row for F, U, V
            col1, col2, col3 = st.columns(3)
            if result.get("F") is not None:
                col1.metric("Feed (F)", f"{result['F']} t/h")
            if result.get("U") is not None:
                col2.metric("Underflow (U)", f"{result['U']} t/h")
            if result.get("V") is not None:
                col3.metric("Overflow (V)", f"{result['V']} t/h")

            # Second row for water balances
            col4, col5, col6 = st.columns(3)
            if result.get("Water in Ball Mill Feed") is not None:
                col4.metric("Water in Ball Mill Feed", result["Water in Ball Mill Feed"])
            if result.get("Water in Cyclone Feed") is not None:
                col5.metric("Water in Cyclone Feed", result["Water in Cyclone Feed"])
            if result.get("Water Requirement at Cyclone Feed") is not None:
                col6.metric("Water Requirement at Cyclone Feed", result["Water Requirement at Cyclone Feed"])

