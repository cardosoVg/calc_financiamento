def obter_entrada(valor_imovel, entrada_informada):
    if entrada_informada == 0:
        return valor_imovel * 0.30
    return entrada_informada


def calcular_financiamento(valor_imovel, entrada_real):
    valor_financiar = valor_imovel - entrada_real

    # Inputs do usuário
    prazo = int(input("Prazo (meses):\t\t\t"))
    taxa_anual = float(input("Taxa de juros anual (%):\t\t")) / 100

    # Taxas extras comuns em bancos
    taxa_adm = 25.0
    seguro_mensal = valor_imovel * 0.00015

    # Conversão para taxa mensal real
    taxa_mensal = (1 + taxa_anual) ** (1 / 12) - 1

    # --- Cálculo PRICE ---
    p_price_base = (
        valor_financiar
        * (taxa_mensal * (1 + taxa_mensal) ** prazo)
        / ((1 + taxa_mensal) ** prazo - 1)
    )
    parcela_price_total = p_price_base + taxa_adm + seguro_mensal
    total_pago_price = (parcela_price_total * prazo) + entrada_real

    # --- Cálculo SAC ---
    amortizacao = valor_financiar / prazo
    juros_inicial = valor_financiar * taxa_mensal
    parcela_sac_inicial = amortizacao + juros_inicial + taxa_adm + seguro_mensal

    juros_final = amortizacao * taxa_mensal
    parcela_sac_final = amortizacao + juros_final + taxa_adm + seguro_mensal

    total_pago_sac = (
        (parcela_sac_inicial + parcela_sac_final) / 2 * prazo
    ) + entrada_real

    return {
        "price": parcela_price_total,
        "sac_ini": parcela_sac_inicial,
        "sac_fim": parcela_sac_final,
        "total_price": total_pago_price,
        "total_sac": total_pago_sac,
        "prazo": prazo,
        "taxa_anual": taxa_anual,  # Retornando a taxa para usar no ponto de virada
    }


def calcular_ponto_virada(valor_imovel, entrada_real, prazo, taxa_anual, parcela_price):
    valor_financiar = valor_imovel - entrada_real
    taxa_mensal = (1 + taxa_anual) ** (1 / 12) - 1
    amortizacao_sac = valor_financiar / prazo

    taxa_adm = 25.0
    seguro_mensal = valor_imovel * 0.00015

    for mes in range(1, prazo + 1):
        saldo_devedor_atual = valor_financiar - (amortizacao_sac * (mes - 1))
        juros_mes = saldo_devedor_atual * taxa_mensal
        parcela_sac_atual = amortizacao_sac + juros_mes + taxa_adm + seguro_mensal

        if parcela_sac_atual <= parcela_price:
            return mes, parcela_sac_atual

    return None, None


# --- Execução e Exibição ---
imovel = float(input("Valor do imóvel:\t\t\t"))
entrada_usr = float(input("Entrada (0 para 30%):\t\t"))

# 1. Definimos a entrada final primeiro
entrada_final = obter_entrada(imovel, entrada_usr)

# 2. Calculamos o financiamento
res = calcular_financiamento(imovel, entrada_final)

# 3. Calculamos o ponto de virada usando os dados do dicionário 'res'
mes_vitoria, valor_vitoria = calcular_ponto_virada(
    imovel, entrada_final, res["prazo"], res["taxa_anual"], res["price"]
)

# --- Output Formatado ---
print("\n" + "=" * 40)
print(f"RESUMO DO FINANCIAMENTO ({res['prazo']} meses)")
print("=" * 40)
print(f"TABELA PRICE (Fixa):    R$ {res['price']:,.2f}")
print(f"TABELA SAC (Inicial):   R$ {res['sac_ini']:,.2f}")
print(f"TABELA SAC (Final):     R$ {res['sac_fim']:,.2f}")
print("-" * 40)
print(f"TOTAL PAGO (PRICE):     R$ {res['total_price']:,.2f}")
print(f"TOTAL PAGO (SAC):       R$ {res['total_sac']:,.2f}")
print(f"ECONOMIA NO SAC:        R$ {res['total_price'] - res['total_sac']:,.2f}")
print("=" * 40)

if mes_vitoria:
    # No lugar do print antigo, use este formato para garantir:
    print(f"\n\U0001f4a1 PONTO DE VIRADA:")  # Usando o código do emoji de lâmpada
    print(f"No mês {mes_vitoria}, a parcela do SAC (R$ {valor_vitoria:,.2f})")
    print(
        f"fica menor que a da PRICE. Isso é {(mes_vitoria/12):.1f} anos após o início."
    )
