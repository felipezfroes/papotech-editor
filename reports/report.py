import csv

from config import SAIDA_DIR
from utils.timecode import (
    formatar_ms,
    formatar_segundos,
    formatar_srt,
)


def salvar_transcricao(
        resultado
):

    caminho = (
        SAIDA_DIR /
        "04_transcricao.txt"
    )

    with open(
        caminho,
        "w",
        encoding="utf-8"
    ) as arquivo:

        for segmento in resultado[
            "segments"
        ]:

            tempo = formatar_segundos(
                segmento["start"]
            )

            texto = (
                segmento["text"].strip()
            )

            arquivo.write(
                f"[{tempo}] {texto}\n"
            )


def salvar_srt(
        resultado
):

    caminho = (
        SAIDA_DIR /
        "05_transcricao.srt"
    )

    with open(
        caminho,
        "w",
        encoding="utf-8"
    ) as arquivo:

        for indice, segmento in enumerate(
            resultado["segments"],
            start=1
        ):

            inicio = formatar_srt(
                segmento["start"]
            )

            fim = formatar_srt(
                segmento["end"]
            )

            texto = (
                segmento["text"].strip()
            )

            arquivo.write(
                f"{indice}\n"
            )

            arquivo.write(
                f"{inicio} --> {fim}\n"
            )

            arquivo.write(
                f"{texto}\n\n"
            )


def salvar_marcacoes(
        marcacoes,
        abertura_ms
):

    txt_path = (
        SAIDA_DIR /
        "06_marcacoes.txt"
    )

    csv_path = (
        SAIDA_DIR /
        "07_marcacoes.csv"
    )

    with open(
        txt_path,
        "w",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(
            "PAPOTECH - MARCAÇÕES PARA CAPCUT\n"
        )

        arquivo.write(
            "=" * 50
        )

        arquivo.write("\n\n")

        for numero, item in enumerate(
            marcacoes,
            start=1
        ):

            inicio_audio_ms = (
                item["inicio"] *
                1000
            )

            fim_audio_ms = (
                item["fim"] *
                1000
            )

            inicio_capcut = (
                inicio_audio_ms +
                abertura_ms
            )

            fim_capcut = (
                fim_audio_ms +
                abertura_ms
            )

            arquivo.write(
                f"MARCAÇÃO {numero}\n"
            )

            arquivo.write(
                f"CAPCUT: "
                f"{formatar_ms(inicio_capcut)}"
                f" → "
                f"{formatar_ms(fim_capcut)}\n"
            )

            arquivo.write(
                f"ÁUDIO: "
                f"{formatar_ms(inicio_audio_ms)}"
                f" → "
                f"{formatar_ms(fim_audio_ms)}\n"
            )

            arquivo.write(
                "MOTIVO: "
                + ", ".join(
                    item["motivos"]
                )
                + "\n"
            )

            arquivo.write(
                f'TEXTO: "{item["texto"]}"\n'
            )

            arquivo.write(
                "-" * 50
            )

            arquivo.write("\n")

    with open(
        csv_path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:

        writer = csv.writer(
            arquivo,
            delimiter=";"
        )

        writer.writerow([
            "Inicio CapCut",
            "Fim CapCut",
            "Motivo",
            "Texto",
        ])

        for item in marcacoes:

            inicio = (
                item["inicio"] *
                1000 +
                abertura_ms
            )

            fim = (
                item["fim"] *
                1000 +
                abertura_ms
            )

            writer.writerow([
                formatar_ms(inicio),
                formatar_ms(fim),
                " / ".join(
                    item["motivos"]
                ),
                item["texto"],
            ])


def salvar_cortes(
        mapa
):

    caminho = (
        SAIDA_DIR /
        "08_cortes_pausas.csv"
    )

    with open(
        caminho,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:

        writer = csv.writer(
            arquivo,
            delimiter=";"
        )

        writer.writerow([
            "Inicio",
            "Fim",
            "Pausa original",
            "Pausa final",
            "Tempo removido",
        ])

        for item in mapa:

            writer.writerow([
                formatar_ms(
                    item["silencio_inicio"]
                ),

                formatar_ms(
                    item["silencio_fim"]
                ),

                item["duracao_original"]
                / 1000,

                item["pausa_final"]
                / 1000,

                item["removido"]
                / 1000,
            ])