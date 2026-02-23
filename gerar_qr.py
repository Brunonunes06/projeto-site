import qrcode
import os
import socket


def get_local_ip():
    """Tenta detectar o IP da rede local (192.168.x.x ou 10.x.x.x)"""
    try:
        # Cria um socket temporário para ver por qual interface ele sairia
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Não precisa conectar de verdade
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        # Fallback para o método antigo se falhar
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)


def generate_login_qr(url):
    static_folder = os.path.join(os.getcwd(), "static")
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    qr_path = os.path.join(static_folder, "login_qr.png")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(qr_path)

    print("-" * 30)
    print("QR CODE GERADO!")
    print(f"URL: {url}")
    print(f"Salvo em: {qr_path}")
    print("-" * 30)
    print("ATENÇÃO: Para o celular acessar, ele deve estar no mesmo Wi-Fi.")


if __name__ == "__main__":
    # Voltando para o IP da rede Wi-Fi local (Opção B)
    local_ip = get_local_ip()
    base_url = f"http://{local_ip}:8080/"
    generate_login_qr(base_url)
