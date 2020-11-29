import streamlit as st
from pycaret.regression import *
import pandas as pd 

def check_input(scores):
    try:
        for keys in scores.keys(): 
            scores[keys] = int(scores[keys])
        if all((0<=scores['ACERTOS_LC']<=45, 0<=scores['ACERTOS_CH']<=45, 0<=scores['ACERTOS_CN']<=45, 0<=scores['ACERTOS_MT']<=45, 0<=scores['REDACAO']<=1000)):
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
        user_input = {'ACERTOS_LC': lc, 'ACERTOS_CH': ch, 'ACERTOS_CN': cn, 'ACERTOS_MT': mt, 'REDACAO':red}
        validated_inputs = check_input(user_input)
        if validated_inputs is not None:
            model_saved = load_model('model/enem_predictor')
            scores_df = pd.DataFrame(pd.DataFrame([list(validated_inputs.values())], columns=list(validated_inputs.keys()))).drop(columns='REDACAO')
            prediction = predict_model(model_saved, data=scores_df)
            prediction['REDACAO']=validated_inputs['REDACAO']
            st.success(f"A média prevista para os dados recebidos é de: {(prediction[['Label', 'REDACAO']].sum(axis=1)/5)[0]:.2f} pontos!")
    