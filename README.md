# Audiobook Splitter

Script Python para dividir audiobooks em arquivos de áudio de **10 minutos**, facilitando a organização e reprodução.

## Requisitos

- Python 3.10+
- FFmpeg e FFprobe instalados e disponíveis no PATH

### Instalar FFmpeg (Windows)

```powershell
winget install Gyan.FFmpeg
```

Verifique a instalação:

```powershell
ffmpeg -version
ffprobe -version
```

## Configuração

No arquivo `split_audio.py`, configure o caminho da pasta que contém seus audiobooks:

no meu caso, é assim: 

```python
BOOKS_DIR = Path(r"C:..\raul\livros")
```

Cada audiobook deve estar dentro de uma pasta correspondente à sua série.

## Como usar

Execute:

```bash
python split_audio.py
```

1. Selecione a série pelo número no menu.
2. Aguarde a divisão dos arquivos.

## Exemplo de saída

```text
mother of learning/
├── Arc 1 - Mother of Learning Arc 1.m4b
├── Arc 2 - Mother of Learning Arc 2.m4b
└── split/
    ├── Arc 1 - Mother of Learning Arc 1_001.m4b
    ├── Arc 1 - Mother of Learning Arc 1_002.m4b
    ├── Arc 1 - Mother of Learning Arc 1_003.m4b
    ├── ...
    └── Arc 2 - Mother of Learning Arc 2_001.m4b
```

## Funcionalidades

- Divisão em partes de aproximadamente 10 minutos.
- Suporte a `.m4b`, `.m4a` e `.mp3`.
- Recodificação para AAC 128 kbps.
- Numeração sequencial independente para cada arquivo.
- Último trecho pode ter menos de 10 minutos.
- Arquivos originais preservados.
- Arquivos já existentes são ignorados.
- Progresso exibido no terminal.

**Nota:** Os arquivos gerados são salvos na subpasta `split` da série selecionada. A recodificação pode causar perda de qualidade e os metadados e capítulos originais não são mantidos.