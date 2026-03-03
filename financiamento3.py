import tkinter as tk
from tkinter import messagebox


def calcular():
    try:
        v_imovel = float(entry_imovel.get())
        v_entrada = float(entry_entrada.get())
        v_prazo = int(entry_prazo.get())
        v_taxa_anual = float(entry_taxa.get()) / 100

        if v_entrada == 0:
            v_entrada = v_imovel * 0.30

        valor_financiar = v_imovel - v_entrada
        taxa_mensal = (1 + v_taxa_anual) ** (1 / 12) - 1
        taxa_adm = 25.0
        seguro_mensal = v_imovel * 0.00015

        # --- Cálculos Price e SAC ---
        p_price_base = (
            valor_financiar
            * (taxa_mensal * (1 + taxa_mensal) ** v_prazo)
            / ((1 + taxa_mensal) ** v_prazo - 1)
        )
        price_total = p_price_base + taxa_adm + seguro_mensal
        total_price = (price_total * v_prazo) + v_entrada

        amort_sac = valor_financiar / v_prazo
        sac_ini = amort_sac + (valor_financiar * taxa_mensal) + taxa_adm + seguro_mensal
        sac_fim = amort_sac + (amort_sac * taxa_mensal) + taxa_adm + seguro_mensal
        total_sac = ((sac_ini + sac_fim) / 2 * v_prazo) + v_entrada

        # --- Lógica do Ponto de Virada ---
        mes_vitoria = "N/A"
        for mes in range(1, v_prazo + 1):
            saldo_devedor = valor_financiar - (amort_sac * (mes - 1))
            parc_sac_atual = (
                amort_sac + (saldo_devedor * taxa_mensal) + taxa_adm + seguro_mensal
            )
            if parc_sac_atual <= price_total:
                mes_vitoria = f"{mes} ({mes/12:.1f} anos)"
                break

        # Atualizando a Interface
        label_res_price.config(text=f"PRICE (Fixo): R$ {price_total:,.2f}")
        label_res_sac.config(text=f"SAC (Inicial): R$ {sac_ini:,.2f}")
        label_res_total_price.config(text=f"Total PRICE: R$ {total_price:,.2f}")
        label_res_total_sac.config(text=f"Total SAC: R$ {total_sac:,.2f}")
        label_economia.config(
            text=f"Economia no SAC: R$ {total_price - total_sac:,.2f}"
        )
        label_virada.config(text=f"Ponto de Virada: Mês {mes_vitoria}")

    except ValueError:
        messagebox.showerror("Erro", "Insira valores numéricos válidos.")


# --- Configuração da Janela (Dark Mode) ---
app = tk.Tk()
app.title("Simulador Imobiliário")
app.geometry("400x600")
app.configure(bg="#1e1e2e")  # Cor baseada no tema Catppuccin (comum em Hyprland)

style = {"bg": "#1e1e2e", "fg": "#cdd6f4", "font": ("Arial", 10)}

tk.Label(
    app,
    text="Simulador de Financiamento",
    font=("Arial", 14, "bold"),
    bg="#1e1e2e",
    fg="#89b4fa",
).pack(pady=15)

# Campos
fields = [
    ("Valor do Imóvel:", "entry_imovel"),
    ("Entrada (0 = 30%):", "entry_entrada"),
    ("Prazo (Meses):", "entry_prazo"),
    ("Taxa Anual (%):", "entry_taxa"),
]

entries = {}
for text, name in fields:
    tk.Label(app, text=text, **style).pack()
    ent = tk.Entry(
        app, bg="#313244", fg="white", insertbackground="white", borderwidth=0
    )
    ent.pack(pady=5, ipady=2)
    entries[name] = ent

entry_imovel, entry_entrada, entry_prazo, entry_taxa = entries.values()

tk.Button(
    app,
    text="CALCULAR",
    command=calcular,
    bg="#a6e3a1",
    fg="#11111b",
    font=("Arial", 10, "bold"),
    borderwidth=0,
).pack(pady=20, ipadx=20)

# Resultados
label_res_price = tk.Label(app, text="PRICE (Fixo): R$ 0,00", **style)
label_res_price.pack()
label_res_sac = tk.Label(app, text="SAC (Inicial): R$ 0,00", **style)
label_res_sac.pack()
tk.Label(app, text="-" * 40, **style).pack()
label_res_total_price = tk.Label(app, text="Total PRICE: R$ 0,00", **style)
label_res_total_price.pack()
label_res_total_sac = tk.Label(app, text="Total SAC: R$ 0,00", **style)
label_res_total_sac.pack()

label_economia = tk.Label(
    app,
    text="Economia no SAC: R$ 0,00",
    bg="#1e1e2e",
    fg="#a6e3a1",
    font=("Arial", 10, "bold"),
)
label_economia.pack(pady=10)

label_virada = tk.Label(
    app,
    text="Ponto de Virada: ---",
    bg="#1e1e2e",
    fg="#fab387",
    font=("Arial", 10, "italic"),
)
label_virada.pack()

app.mainloop()
