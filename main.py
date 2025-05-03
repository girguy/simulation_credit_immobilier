import streamlit as st
import pandas as pd


st.set_page_config(layout="wide")


def calcul_frais(valeur_maison, travaux, option, taux_interet, duree, apport_personel):
    if option == "12.5%":
        frais_enregistrement = 0.125 * valeur_maison
    elif option == "3%":
        frais_enregistrement = 0.03 * valeur_maison
    elif option == "6%":
        frais_enregistrement = 0.06 * valeur_maison
    else:
        raise ValueError("Option invalide. Choisir '12.5%', '3%' ou '6%'.")

   # Total du crédit attribué
    total_apport_personnel = apport_personel * (valeur_maison + travaux)
    
    # Frais de crédit fixes
    frais_credit_fixes = 100 + 813 + 304.43 + 100 + 285
    
    # Honoraires
    honoraires = (0.00524 * valeur_maison) + 1059.47

    #TVA
    tva = (0.0011 * valeur_maison) + 474.96
    
    # Frais de crédit totaux
    frais_credit = frais_credit_fixes + honoraires + tva
    
    # Total des frais de notaire
    total_frais_notaire = frais_enregistrement + frais_credit

    credit_attribue = (1 - apport_personel) * (valeur_maison + travaux)
    
    # Fonds propres nécessaires
    fonds_propres = total_frais_notaire + total_apport_personnel

    # Mensualité
    mensualite = credit_attribue * (taux_interet / 12) / (1 - (1 + taux_interet / 12)**(-duree * 12))
    
    # Résultat sous forme de DataFrame
    df = pd.DataFrame({
        "Prix de la maison": [valeur_maison],
        "Option": [option],
        "Frais d'enregistrement": [frais_enregistrement],
        "Frais de crédit": [frais_credit],
        "Frais de notaire": [total_frais_notaire],
        "Travaux": [travaux],
        "Crédit attribué": [credit_attribue],
        "Apport personnel": [total_apport_personnel],
        "Fonds propres nécessaires": [fonds_propres],
        "Durée du crédit (années)": [duree],
        "Taux d'intérêt": [taux_interet],
        "Mensualité": [mensualite]
    })
    
    return df


def load_simulation_result():
    try:
        df = pd.read_csv("simulation_result.csv")
        print("Fichier chargé avec succès.")
        return df
    except FileNotFoundError:
        print("Le fichier 'simulation_result.csv' est introuvable.")
        return None

df_loaded = load_simulation_result()

# --- Streamlit UI ---
st.title("Simulateur de frais immobiliers")

valeur_maison = st.number_input("Prix de la maison (€)", min_value=0, step=1000)
travaux = st.number_input("Montant des travaux (€)", min_value=0, step=1000)
option = st.selectbox("Option des frais d'enregistrement", ["12.5%", "3%", "6%"])
taux_interet = st.number_input("Taux d'intérêt annuel (%)", min_value=0.0, max_value=10.0, step=0.1) / 100
duree = st.selectbox("Durée du crédit (années)", [5, 10, 15, 20, 25])
apport_personel = st.slider("Apport (0.0 = aucun, 1 = 100%)", min_value=0.0, max_value=1.0, step=0.01)

if st.button("Calculer"):
    df_result = calcul_frais(valeur_maison, travaux, option, taux_interet, duree, apport_personel)
    if isinstance(df_loaded, pd.DataFrame):
        df_loaded = pd.concat([df_loaded, df_result], ignore_index=True)
    else:
        df_loaded = df_result
    df_loaded.to_csv("simulation_result.csv", index=False)
    st.dataframe(df_loaded.style.format({
        col: "{:,.2f}" for col in df_loaded.select_dtypes(include="number").columns
    }))



