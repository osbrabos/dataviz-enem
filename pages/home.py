import streamlit as st
from pycaret.regression import *
import pandas as pd 

def check_input(lc, ch, cn, mt, red):
    try:
        scores = list(map(int, [lc, ch, cn, mt, red]))
        if all((0<=scores[0]<=45, 0<=scores[1]<=45, 0<=scores[2]<=45, 0<=scores[3]<=45, 0<=scores[4]<=1000)):
            return scores
        else:
            st.error('Um dos valores digitados não corresponde ao intervalo esperado. Verifique se os acertos estão entre 0 e 45 e a redação entre 0 e 1000.')
    except:
        st.error('Existe algum problema nos valores informados, verifique se existem apenas números nos campos de texto.')
    

def write():
    """Used to write the page in the app.py file"""
    st.title('Preditor de notas do ENEM')

    
    lc = st.text_input(label='Acertos em Linguagens e Códigos:', max_chars=2)
    ch = st.text_input(label='Acertos em Ciências Humanas:', max_chars=2)
    cn = st.text_input(label='Acertos em Ciências da Natureza:', max_chars=2)
    mt = st.text_input(label='Acertos Matemática:', max_chars=2)
    red = st.text_input(label='Nota de Redação:', max_chars=4)

    if st.button('Gerar predição!'):
        scores = check_input(lc, ch, cn, mt, red)
        if scores is not None:
            model_saved = load_model('enem_predictor')
            scores_df = pd.DataFrame([scores[:4]], columns =['ACERTOS_LC', 'ACERTOS_CH', 'ACERTOS_CN', 'ACERTOS_MT'])
            prediction = predict_model(model_saved, data=scores_df)
            prediction['REDAÇÃO']=scores[4]
            st.success(f"A média prevista para os dados recebidos é de: {(prediction[['Label', 'REDAÇÃO']].sum(axis=1)/5)[0]:.2f} pontos!")
    

        

    
    
    