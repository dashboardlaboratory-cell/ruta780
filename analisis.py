
def ticket(venta, trx):
    return venta / trx

if __name__ == "__main__":
    # Esto SOLO corre si ejecutas el archivo directamente:
    #   python analisis.py
    # No corre si alguien hace: import analisis
    print("ticket de prueba:", ticket(4200, 140))
