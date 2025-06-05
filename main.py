import streamlit as st
import pandas as pd
import datetime
import io

# ---------- Dados iniciais ----------
credito = [
    "INSS Beto",
    "Salario Beto",
    "INSS Daia",
    "Reembolso desp",
    "outros",
]

if 'debito_list' not in st.session_state:
    st.session_state['debito_list'] = [
        "Condomínio Joinville", "Condomínio Floripa", "Celesc Joinville", "Celesc Floripa",
        "Gás Joinville", "Celular família", "Internet Floripa", "Unimed Gab", "Unimed Luc",
        "Unimed Beto e Daia", "Academia Beto", "Netflix e outros", "Supermercado", "Almoço",
        "Café e lanches", "Diarista Joinville", "Diarista Floripa", "Cabelereiro, manicure",
        "Cartao crédito Gabriel", "Cartão crédito Lucas", "Seguro Apto Joinville", "Seguro apto Floripa",
        "Combustível / Uber / Bla", "Seguro Pajero / Terios", "Seguro Corolla", "Licenciamento carros",
        "Manutenção carros", "Farmácia", "Tarifas", "Safira", "Vestuário / calçados", "Presentes",
        "Artigos para casa", "SFH", "Apto em construção", "Gab Formatura", "IPTU Floripa", "IPTU Joinville",
    ]

if 'tabela_credito' not in st.session_state:
    st.session_state['tabela_credito'] = pd.DataFrame(columns=['Crédito', 'Data', 'Valor'])

if 'tabela_debito' not in st.session_state:
    st.session_state['tabela_debito'] = pd.DataFrame(columns=['Débito', 'Data', 'Valor'])

# ---------- Data atual ----------
data = datetime.datetime.now().strftime("%Y-%m-%d")

# ---------- TABS ----------
tab1, tab2 = st.tabs(["💰 Créditos", "💸 Débitos"])

# ---------- ABA 1 - CRÉDITO ----------
with tab1:
    st.header("💰 Créditos")
    for opcao in credito:
        valor = st.number_input(f"Informe o valor para '{opcao}'", min_value=None, step=0.01, key=opcao)
        if valor > 0:
            if st.button(f"Adicionar crédito: {opcao}", key="btn_cred_" + opcao):
                novo_credito = pd.DataFrame({'Crédito': [opcao], 'Data': [data], 'Valor': [valor]})
                st.session_state['tabela_credito'] = pd.concat(
                    [st.session_state['tabela_credito'], novo_credito], ignore_index=True
                )

    st.subheader("📄 Tabela de Créditos")
    st.table(st.session_state['tabela_credito'])

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        st.session_state['tabela_credito'].to_excel(writer, index=False)
    output.seek(0)
    st.download_button(
        label="📥 Exportar Créditos para Excel",
        data=output,
        file_name=f"tabela_credito-{data}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ---------- ABA 2 - DÉBITO ----------
with tab2:
    st.header("💸 Débitos")

    opcoes_debito = st.multiselect("Selecione débitos", options=st.session_state['debito_list'])

    add_linha = st.text_input("Adicionar novo tipo de gasto (débito)")
    if add_linha:
        if add_linha not in st.session_state['debito_list']:
            st.session_state['debito_list'].append(add_linha)
            st.success(f"Gasto '{add_linha}' adicionado com sucesso.")
        else:
            st.info(f"Gasto '{add_linha}' já está na lista.")

    if opcoes_debito:
        for opcao in opcoes_debito:
            valor = st.number_input(
                f"Informe o valor para '{opcao}'", min_value=None, step=0.01, key=opcao + "_deb")
            if valor > 0:
                if st.button(f"Adicionar débito: {opcao}", key="btn_deb_" + opcao):
                    novo_debito = pd.DataFrame({'Débito': [opcao], 'Data': [data], 'Valor': [valor]})
                    st.session_state['tabela_debito'] = pd.concat(
                        [st.session_state['tabela_debito'], novo_debito], ignore_index=True
                    )

    st.subheader("📄 Tabela de Débitos")
    st.table(st.session_state['tabela_debito'])

    output_debito = io.BytesIO()
    with pd.ExcelWriter(output_debito, engine='openpyxl') as writer:
        st.session_state['tabela_debito'].to_excel(writer, index=False)
    output_debito.seek(0)
    st.download_button(
        label="📥 Exportar Débitos para Excel",
        data=output_debito,
        file_name=f"tabela_debito-{data}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ---------- Totais ----------
st.markdown("---")
total_credito = st.session_state['tabela_credito']['Valor'].sum()
total_debito = st.session_state['tabela_debito']['Valor'].sum()
saldo = total_credito - total_debito

st.markdown(f"### ✅ Total Crédito: R$ {total_credito:.2f}")
st.markdown(f"### ❌ Total Débito: R$ {total_debito:.2f}")
st.markdown(f"### 📊 Saldo (Sobra/Falta): R$ {saldo:.2f}")
