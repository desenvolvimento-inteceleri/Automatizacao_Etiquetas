import streamlit as st

from table_treatment_semec import main as verifica_main
import table_treatment_moju
import table_treatment_obidos


def set_initial_state():
    st.session_state.current_page = 'home'

# Verificar se o estado atual existe, se não, inicializar
if 'current_page' not in st.session_state:
    set_initial_state()

st.title('Bem-vindo ao Criador de Etiquetas')

if st.sidebar.button('Criação de Etiquetas - SEMEC'):
    st.session_state.current_page = 'main'

if st.sidebar.button('Criação de Etiquetas - MOJU'):
    st.session_state.current_page = 'MOJU'

if st.sidebar.button('Criação de Etiquetas - OBIDOS'):
    st.session_state.current_page = 'OBIDOS'

if st.session_state.current_page == 'main':
    verifica_main()

elif st.session_state.current_page == 'home':
    st.write('Por favor, escolha uma opção ao lado para criar as etiquetas.')

# Espaços adicionais na barra lateral, para estética
for _ in range(10):
    st.sidebar.write("_____")