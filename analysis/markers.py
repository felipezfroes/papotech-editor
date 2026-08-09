import re
import unicodedata


EXPRESSOES_CORRECAO = [
    "corta",
    "corta ai",
    "corta isso",
    "vou repetir",
    "deixa eu repetir",
    "deixa eu refazer",
    "desculpa",
    "nao pera",
    "pera ai",
    "quer dizer",
    "corrigindo",
]


def normalizar(texto):

    texto = texto.lower()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        char
        for char in texto
        if unicodedata.category(char) != "Mn"
    )

    texto = re.sub(
        r"[^\w\s]",
        " ",
        texto
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto.strip()


def encontrar_repeticao(palavras):

    # Palavra repetida:
    # "o protocolo protocolo TCP"

    for i in range(
        len(palavras) - 1
    ):

        if (
            len(palavras[i]) > 2
            and palavras[i]
            == palavras[i + 1]
        ):
            return True

    # Frases curtas repetidas:
    #
    # "isso acontece porque
    #  isso acontece porque"

    for tamanho in range(2, 5):

        for i in range(
            len(palavras) -
            tamanho * 2 + 1
        ):

            primeira = palavras[
                i:i + tamanho
            ]

            segunda = palavras[
                i + tamanho:
                i + tamanho * 2
            ]

            if primeira == segunda:
                return True

    return False


def analisar_marcacoes(
        resultado_whisper
):

    marcacoes = []

    for segmento in resultado_whisper[
        "segments"
    ]:

        texto_original = (
            segmento["text"].strip()
        )

        texto = normalizar(
            texto_original
        )

        palavras = texto.split()

        motivos = []

        for expressao in EXPRESSOES_CORRECAO:

            if expressao in texto:

                if expressao == "corta":
                    motivos.append(
                        "MARCADOR CORTA"
                    )

                else:
                    motivos.append(
                        f'Possível correção: '
                        f'"{expressao}"'
                    )

        if encontrar_repeticao(
            palavras
        ):
            motivos.append(
                "Possível repetição/gaguejo"
            )

        if motivos:

            inicio = max(
                0,
                segmento["start"] - 1.5
            )

            fim = (
                segmento["end"] +
                1.5
            )

            marcacoes.append({
                "inicio": inicio,
                "fim": fim,
                "texto": texto_original,
                "motivos": motivos,
            })

    return marcacoes