from PIL import Image, ImageDraw

def create_app_icon(output_path="icon.ico"):
    # Desenha em resolução alta 512x512 para máxima qualidade e nitidez
    w, h = 512, 512
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Fundo moderno arredondado (Azul Royal Vibrante com borda Cyan)
    margin = 32
    radius = 110
    draw.rounded_rectangle(
        [margin, margin, w - margin, h - margin],
        radius=radius,
        fill=(30, 58, 138, 255), # Azul profundo
        outline=(59, 130, 246, 255), # Borda Azul Brilhante
        width=16
    )

    # 2. Folha / Prancheta de Questões (Branco limpo)
    doc_x1, doc_y1 = 130, 95
    doc_x2, doc_y2 = 382, 417
    draw.rounded_rectangle(
        [doc_x1, doc_y1, doc_x2, doc_y2],
        radius=28,
        fill=(255, 255, 255, 255),
        outline=(226, 232, 240, 255),
        width=4
    )

    # 3. Título / Cabeçalho da Folha
    draw.rounded_rectangle(
        [160, 135, 300, 160],
        radius=8,
        fill=(30, 64, 175, 255)
    )

    # 4. Linhas de Alternativas (A, B, C) com indicador de Gabarito correto
    # Linha A
    draw.ellipse([160, 190, 185, 215], fill=(203, 213, 225, 255))
    draw.rounded_rectangle([200, 195, 350, 210], radius=6, fill=(203, 213, 225, 255))

    # Linha B (Gabarito Verde Correto)
    draw.ellipse([160, 240, 185, 265], fill=(16, 185, 129, 255)) # Verde esmeralda
    draw.rounded_rectangle([200, 245, 350, 260], radius=6, fill=(16, 185, 129, 255))

    # Linha C
    draw.ellipse([160, 290, 185, 315], fill=(203, 213, 225, 255))
    draw.rounded_rectangle([200, 295, 330, 310], radius=6, fill=(203, 213, 225, 255))

    # Linha D
    draw.ellipse([160, 340, 185, 365], fill=(203, 213, 225, 255))
    draw.rounded_rectangle([200, 345, 310, 360], radius=6, fill=(203, 213, 225, 255))

    # 5. Badge Dourado de Parser / Inteligência no canto
    badge_cx, badge_cy = 385, 385
    badge_r = 75
    draw.ellipse(
        [badge_cx - badge_r, badge_cy - badge_r, badge_cx + badge_r, badge_cy + badge_r],
        fill=(245, 158, 11, 255), # Dourado
        outline=(255, 255, 255, 255),
        width=10
    )

    # Raio no Badge
    lightning_points = [
        (385, 335),
        (360, 385),
        (380, 385),
        (370, 435),
        (410, 375),
        (390, 375)
    ]
    draw.polygon(lightning_points, fill=(255, 255, 255, 255))

    # Gera todos os tamanhos padrão do Windows com interpolação suave (Lanczos)
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    images = [img.resize(size, Image.Resampling.LANCZOS) for size in icon_sizes]

    images[0].save(output_path, format="ICO", sizes=icon_sizes)
    print(f"Icone gerado com sucesso: {output_path}")

if __name__ == "__main__":
    create_app_icon("icon.ico")
