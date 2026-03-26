import argparse
import sys
import hashlib
from pathlib import Path

##Verificar se o pillow está instalado

try:
    from PIL import Image
except ImportError:
    print("Pillow não encontrado. Instale com: pip install Pillow")
    sys.exit(1)

## extensoes suportadas

SUPPORTED_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp",
}


def pegar_imagens(input_dir):
    """
    busca imagens suportadas no diretorio
    
    """

    images = []

    for file in sorted(input_dir.rglob("*")):
        if file.suffix.lower() in SUPPORTED_EXTENSIONS:
            images.append(file)
    return images
    


def verificar_hash(filepath):
    """
    Calcula o hash md5 do arquivo para verificar duplicidade

    """
    hasher = hashlib.md5()
    with open(filepath, "rb") as f: 
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()



def processar_imagens(input_dir, output_dir, prefix, fmt):
    """
    Converte em um formato padrao, renomeia e remove imagens duplicadas
    """
    images = pegar_imagens(input_dir)
    print(f"\nEncontradas: {len(images)}imagens")

    if not images:
        print("Nenhuma imagem encontrada")
        return
    
    if not images:
        print("Nenhuma imagem encontrada")
        return
    
#Cria pasta de saida se n tiver

    output_dir.mkdir(parents=True, exist_ok=True)

    seen_hashes = {}
    counter = 0
    duplicates = 0
    errors = 0
    

    for img_path in images:
        try:
            #verifica duplicata
            h = verificar_hash(img_path)
            if h in seen_hashes:
                print(f"Duplicata ignorada: {img_path.name}")
                duplicates += 1
                continue
            seen_hashes[h] = img_path

            with Image.open(img_path) as img:
                if img.mode != "RGB":
                    img = img.convert("RGB")


                #define novo nome
                counter += 1
                extension = ".jpg" if fmt == "jpg" else ".png"
                novo_nome = f"{prefix}_{counter:04d}{extension}"


                #salva o imagem
                save_args = {"quality": 95, "optimize": True} if fmt =="jpg" else {"optimize": True}
                img.save(output_dir /novo_nome, **save_args)

        except Exception as e:
            print(f"Erro em {img_path.name}: {e}")
            erros += 1



    print(f"\nResultado:")
    print(f"  Processadas: {counter}")
    print(f"  Duplicatas ignoradas: {duplicates}")
    print(f"  Erros: {errors}")



if __name__ == "__main__":
    print("=" * 50)
    print("TreeRisk - Formatador de imagens")
    print("=" * 50)


    #pasta aonde pega as imagens
    input_str = input("\nPasta de entrada (padrão: dataset/raw): ").strip()
    input_dir = Path(input_str) if input_str else Path ("dataset/raw")

    if not input_dir.exists():
        print(f"ERRO: Pasta '{input_dir}'não encontrada")
        sys.exit(1)


        #pasta aonde sai as imagens

    output_str = input("Pasta de saida (padrão: dataset/processed): ").strip()
    output_dir = Path(output_str) if output_str else Path("dataset/processed")


        #prefixo das imagens
    prefix = input("Prefixo dos arquivos (padrão: tree): ").strip()
    if not prefix:
        prefix = "tree"

        #formato

    fmt = input("Formato de saída [jpg/png] (padrão: jpg): ").strip().lower()
    if fmt not in ("jpg", "png"):
        fmt = "jpg"


        #confirmacAO de configuracao

    print(f"\nConfiguraçao: ")
    print(f"Entrada: {input_dir}")
    print(f"Saida {output_dir}")
    print(f"Prefixo {prefix}")
    print(f"Formato {fmt}")


    confirma = input("\nContinuar? [s/n]: ").strip().lower()
    if confirma != "s":
        print("Cancelado")
        sys.exit(0)

    processar_imagens(input_dir, output_dir, prefix, fmt)