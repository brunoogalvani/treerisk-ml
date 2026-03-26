## Formatação do Dataset

O script `scripts/format_dataset.py` padroniza as imagens coletadas para
uso no treinamento. Ele converte todas as imagens para um formato único,
renomeia sequencialmente e remove duplicatas.

### Uso
```bash
pip install Pillow

python scripts/format_dataset.py -i data/raw -o data/processed
```