from rpa_login import login_glovo

if __name__ == "__main__":
    EMAIL = "hola@solucioning.net"
    PASSWORD = "Solucioning25+-."
    resultado = login_glovo(EMAIL, PASSWORD)
    print(f"[RPA] Resultado: {resultado}") 