
import math
import shutil
import subprocess
import sys
from pathlib import Path

# Configurações
BOOKS_DIR = Path(
    r"C:\Users\raul\OneDrive\Ambiente de Trabalho\raul\livros"
)
SEGMENT_SECONDS = 10 * 60
EXTENSIONS = {".m4b", ".m4a", ".mp3"}


def check_ffmpeg():
    """Verifica se FFmpeg e FFprobe estão instalados."""
    for program in ("ffmpeg", "ffprobe"):
        if not shutil.which(program):
            print(f"\nERRO: {program} não encontrado no PATH.")
            print("Instale com: winget install Gyan.FFmpeg")
            sys.exit(1)


def select_book():
    """Mostra um menu para selecionar a série."""
    if not BOOKS_DIR.is_dir():
        sys.exit(f"Pasta não encontrada: {BOOKS_DIR}")

    folders = sorted(
        [p for p in BOOKS_DIR.iterdir() if p.is_dir()],
        key=lambda p: p.name.lower()
    )

    if not folders:
        sys.exit("Nenhuma série encontrada.")

    print("\n=== SELECIONE UMA SÉRIE ===\n")

    for index, folder in enumerate(folders, start=1):
        count = sum(
            1 for f in folder.iterdir()
            if f.is_file() and f.suffix.lower() in EXTENSIONS
        )
        print(f"{index}. {folder.name} ({count} arquivos)")

    while True:
        choice = input("\nNúmero da série (0 para sair): ").strip()

        if choice == "0":
            sys.exit(0)

        if choice.isdigit() and 1 <= int(choice) <= len(folders):
            return folders[int(choice) - 1]

        print("Opção inválida.")


def get_duration(file_path):
    """Retorna a duração do áudio em segundos."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(file_path)
        ],
        capture_output=True,
        text=True,
        check=True
    )
    return float(result.stdout.strip())


def format_time(seconds):
    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def split_file(file_path, output_dir):
    """Divide um audiobook em partes de até 10 minutos."""
    duration = get_duration(file_path)
    total_parts = math.ceil(duration / SEGMENT_SECONDS)

    print(f"\nLivro: {file_path.name}")
    print(f"Duração: {format_time(duration)}")
    print(f"Total de partes: {total_parts}")

    for index in range(total_parts):
        start = index * SEGMENT_SECONDS
        remaining = duration - start
        segment_duration = min(SEGMENT_SECONDS, remaining)

        output_file = output_dir / (
            f"{file_path.stem}_{index + 1:03d}{file_path.suffix.lower()}"
        )

        if output_file.exists():
            print(f"  [{index + 1}/{total_parts}] Já existe, pulando")
            continue

        print(
            f"  [{index + 1}/{total_parts}] "
            f"{format_time(start)} -> "
            f"{format_time(start + segment_duration)}",
            flush=True
        )

        temp_file = output_file.with_name(
            f"{output_file.stem}.partial{output_file.suffix}"
        )

        if temp_file.exists():
            temp_file.unlink()

        command = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel", "error",
            "-nostdin",
            "-y",
            "-ss", str(start),
            "-i", str(file_path),
            "-t", str(segment_duration),
            "-map", "0:a:0",
            "-vn",
            "-c:a", "aac",
            "-b:a", "128k",
            "-ar", "44100",
            "-ac", "2",
            "-map_metadata", "-1",
            "-map_chapters", "-1",
            str(temp_file)
        ]

        try:
            subprocess.run(command, check=True)
            temp_file.replace(output_file)
        except subprocess.CalledProcessError:
            if temp_file.exists():
                temp_file.unlink()
            print(f"  ERRO ao processar: {output_file.name}")
            raise

    print(f"Concluído: {file_path.name}")


def main():
    check_ffmpeg()

    selected_folder = select_book()

    audio_files = sorted(
        [
            p for p in selected_folder.iterdir()
            if p.is_file() and p.suffix.lower() in EXTENSIONS
        ],
        key=lambda p: p.name.lower()
    )

    if not audio_files:
        print("\nNenhum arquivo de áudio encontrado.")
        return

    output_dir = selected_folder / "split"
    output_dir.mkdir(exist_ok=True)

    print(f"\nSérie selecionada: {selected_folder.name}")
    print(f"Arquivos encontrados: {len(audio_files)}")
    print(f"Destino: {output_dir}")

    for index, audio_file in enumerate(audio_files, start=1):
        print(f"\n=== ARQUIVO {index}/{len(audio_files)} ===")
        try:
            split_file(audio_file, output_dir)
        except (subprocess.CalledProcessError, ValueError, OSError) as error:
            print(f"Falha em {audio_file.name}: {error}")
            print("Continuando com o próximo arquivo.")

    print("\n=== PROCESSAMENTO FINALIZADO ===")
    print(f"Arquivos disponíveis em: {output_dir}")


if __name__ == "__main__":
    main()
