imovel = float(input("Insira o valor do imovel:\t"))
entrada = float(input("Insira o valor da entrada:\t"))


def calculoEntrada():
    global entrada
    if entrada == 0:
        entrada = imovel * 0.30
        return entrada
    else:
        return entrada


def calculoParcela():
    valor = imovel - entrada
    parcelas = int(input("Insira a quantidade de parcela:\t"))
    inicial = valor / parcelas
    tax = (inicial * 12) * 0.09
    price = (inicial + tax) * 1.466
    sac = (inicial + tax) * 1.85
    print("\nQuantidade de parcelas:\t", parcelas)
    return price, sac


def calculoDocumentacao():
    documentacao = imovel * 0.06
    return documentacao


a = calculoEntrada()
b = calculoParcela()
c = calculoDocumentacao()


print("Valor do imovel:\t", imovel)
print(f"Valor da entrada:\t {a:.2f}")
print(f"Valor das parcelas:(Price)\t {b[0]:.2f}")
print(f"Valor das parcelas:(SAC)\t {b[1]:.2f}")
print(
    f"Documentação:\t {c:.2f}",
)
