def ativar_modo_noturno(root, modo_noturno_ativo):
    if modo_noturno_ativo:
        root.configure(bg="white")
        for widget in root.winfo_children():
            widget.configure(bg="white")
    else:
        root.configure(bg="black")
        for widget in root.winfo_children():
            widget.configure(bg="black")

    return not modo_noturno_ativo