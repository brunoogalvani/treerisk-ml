## Formatação do Dataset

O script `scripts/format_dataset.py` padroniza as imagens coletadas para
uso no treinamento. Ele converte todas as imagens para um formato único,
renomeia sequencialmente e remove duplicatas.

### Uso

O script solicita interativamente os diretórios de entrada e saída via `input()`.
Se você apenas pressionar Enter, ele usará por padrão `dataset/raw` como entrada
e `dataset/processed` como saída.

```bash
pip install Pillow

python scripts/format_dataset.py
```