import streamlit as st

# ---------------- Functions ----------------

def two_product_formula(F=None, C=None, T=None, f=None, c=None, t=None):
    knowns = {'F': F, 'C': C, 'T': T, 'f': f, 'c': c, 't': t}
    unknowns = [k for k, v in knowns.items() if v is None]

    if len(unknowns) != 2:
        return "Please leave exactly two variables as None."

    result = ""

    # 1)  C and T
    if 'C' in unknowns and 'T' in unknowns and F is not None:
        if all(v is not None for v in [F, f, c, t]):
            C = (F * (f - t)) / (c - t)
            T = F - C
            result += f"C = {round(C, 2)}\nT = {round(T, 2)}\n"
        else:
            return "Not enough info to solve for C and T."

    # 2)  F and C
    elif 'F' in unknowns and 'C' in unknowns and all(v is not None for v in [T, f, c, t]):
        F = T * (t - c) / (f - c)
        C = F - T
        result += f"F = {round(F, 2)}\nC = {round(C, 2)}\n"

    # 3) F and T
    elif 'F' in unknowns and 'T' in unknowns and all(v is not None for v in [C, f, c, t]):
        F = C * (c - t) / (f - t)
        T = F - C
        result += f"F = {round(F, 2)}\nT = {round(T, 2)}\n"

    # 4) C and f
    elif 'C' in unknowns and 'f' in unknowns and all(v is not None for v in [F, T, c, t]):
        C = F - T
        f = (C * c + T * t) / F
        result += f"C = {round(C, 2)}\nf = {round(f, 4)}\n"

    # 5)  F and f
    elif 'F' in unknowns and 'f' in unknowns and all(v is not None for v in [C, T, c, t]):
        F = C + T
        f = (C * c + T * t) / F
        result += f"F = {round(F, 2)}\nf = {round(f, 4)}\n"

    #6) f and t
    elif 'f' in unknowns and 't' in unknowns and all(v is not None for v in [F, C, T, c]):
        return "Cannot uniquely solve for f and t. Underdetermined system."

    else:
        return "Combination not supported or insufficient data."

    # Recovery
    if all(v is not None for v in [F, C, f, c]) and f != 0:
        recovery = 100 * (C * c) / (F * f)
        result += f"Recovery = {round(recovery, 2)}%"
    else:
        result += "Recovery cannot be calculated due to insufficient data."

    return result


def water_calculation(F=None, U=None, V=None, f=None, u=None, v=None, m=None):
    knowns = {'F': F, 'U': U, 'V': V, 'f': f, 'u': u, 'v': v}
    unknowns = [k for k, l in knowns.items() if l is None]

    if len(unknowns) != 2:
        return "Please leave exactly two variables as None."

    result = ""

    # 1)  U and V
    if 'U' in unknowns and 'V' in unknowns and F is not None:
        if all(l is not None for l in [F, f, u, v]):
            U = (F * (f - v)) / (u - v)
            V = F - U
            result += f"U = {round(U, 2)}\nV = {round(V, 2)}\n"

    # 2)  F and U
    elif 'F' in unknowns and 'U' in unknowns and all(l is not None for l in [V, f, u, v]):
        F = V * (v - u) / (f - u)
        U = F - V
        result += f"F = {round(F, 2)}\nU = {round(U, 2)}\n"

    # 3) F and V
    elif 'F' in unknowns and 'V' in unknowns and all(l is not None for l in [U, f, u, v]):
        F = U * (u - v) / (f - v)
        V = F - U
        result += f"F = {round(F, 2)}\nV = {round(V, 2)}\n"

    else:
        return "Combination not supported or insufficient data."

    # Water calculations
    if all(val is not None for val in [F, V, U, f, u, v, m]):
        water_ball_mill_feed = V * (m / (100 - m)) + U * u
        water_ball_mill_feed = round(water_ball_mill_feed, 1)

        total_solids_cyclone = V + U
        water_cyclone_feed = total_solids_cyclone * f
        water_cyclone_feed = round(water_cyclone_feed, 1)

        water_requirement_cyclone = round(water_cyclone_feed - water_ball_mill_feed, 1)

        result += (
            f"Water in Ball Mill Feed = {water_ball_mill_feed} m3/h\n"
            f"Water in Cyclone Feed = {water_cyclone_feed} m3/h\n"
            f"Water Requirement at Cyclone Feed = {water_requirement_cyclone} m3/h\n"
        )
    else:
        result += "Water calculation skipped due to missing values.\n"

    return result

# ---------------- Streamlit App ----------------

st.set_page_config(page_title="Mining Calculations", layout="wide")
st.title("Mineral Processing Tool")

st.sidebar.header("Instructions")
st.sidebar.write("This Mineral Processing Tool lets you perform two-product and water balance calculations. Enter known values, mark exactly two variables as Unknown, and click Calculate.")

# --- Two Product Formula ---
st.header("Two-Product Formula")

col1, col2, col3 = st.columns(3)
two_inputs = {}
two_unknowns = {}

with col1:
    two_inputs['F'] = st.text_input("Feed (F) [t/h]")
    two_inputs['C'] = st.text_input("Concentrate (C) [t/h]")
    two_inputs['T'] = st.text_input("Tailings (T) [t/h]")
with col2:
    two_inputs['f'] = st.text_input("Feed Grade (f) %")
    two_inputs['c'] = st.text_input("Concentrate Grade (c) %")
    two_inputs['t'] = st.text_input("Tailings Grade (t) %")
with col3:
    two_unknowns['F'] = st.checkbox("Unknown F [t/h]")
    two_unknowns['C'] = st.checkbox("Unknown C [t/h]")
    two_unknowns['T'] = st.checkbox("Unknown T [t/h]")
    two_unknowns['f'] = st.checkbox("Unknown f %")
    two_unknowns['c'] = st.checkbox("Unknown c %")
    two_unknowns['t'] = st.checkbox("Unknown t %")

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
        st.text(two_product_formula(**inputs))

# --- Water Calculation ---
st.header("Water Calculation")

col4, col5, col6 = st.columns(3)
water_inputs = {}
water_unknowns = {}

with col4:
    water_inputs['F'] = st.text_input("Feed (F)", key="wF")
    water_inputs['U'] = st.text_input("Underflow (U)", key="wU")
    water_inputs['V'] = st.text_input("Overflow (V)", key="wV")
with col5:
    water_inputs['f'] = st.text_input("Feed Dilution Ratio (f)", key="wf")
    water_inputs['u'] = st.text_input("Underflow Dilution Ratio (u)", key="wu")
    water_inputs['v'] = st.text_input("Overflow Dilution Ratio (v)", key="wv")
    water_inputs['m'] = st.text_input("Moisture Content (m)", key="wm")
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
        st.text(water_calculation(**inputs))
