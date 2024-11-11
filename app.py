import streamlit as st

import modules.semec.data_manipulation_semec as semec
import modules.peixe_boi.data_manipulation_peixe_boi as peixe_boi
import modules.altaneira_ce.data_manipulation_altaneira as altaneira


def set_initial_state():
    st.session_state.current_page = 'home'

# Verificar se o estado atual existe, ses não, inicializar
if 'current_page' not in st.session_state:
    set_initial_state()

st.title('Bem-vindo ao Criador de Etiquetas')

if st.sidebar.button('Criação de Etiquetas - SEMEC'):
    st.session_state.current_page = 'SEMEC'

if st.sidebar.button('Criação de Etiquetas - PEIXE BOI'):
    st.session_state.current_page = 'PEIXE BOI'

if st.sidebar.button('Criação de Etiquetas - ALTANEIRA'):
   st.session_state.current_page = 'ALTANEIRA'

if st.session_state.current_page == 'SEMEC':
    semec.main()

if st.session_state.current_page == 'PEIXE BOI':
    peixe_boi.main()

if st.session_state.current_page == 'ALTANEIRA':
    altaneira.main()

elif st.session_state.current_page == 'home':
    st.write('Por favor, escolha uma opção ao lado para criar as etiquetas.')

# Espaços adicionais na barra lateral, para estética
for _ in range(10):
    st.sidebar.write("_____")