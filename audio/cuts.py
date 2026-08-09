from pydub import AudioSegment
from pydub.silence import detect_silence

from config import (
    MIN_SILENCE_MS,
    SILENCE_THRESHOLD_DBFS,
)


def calcular_silence_threshold(
        audio: AudioSegment
):

    if SILENCE_THRESHOLD_DBFS is not None:
        return SILENCE_THRESHOLD_DBFS

    if audio.dBFS == float("-inf"):
        return -40

    # Heurística automática baseada
    # no volume médio da gravação.
    threshold = audio.dBFS - 18

    threshold = max(
        -50,
        min(-32, threshold)
    )

    return threshold


def pausa_que_deve_ficar(
        duracao_ms
):

    if duracao_ms < 4000:
        return 1200

    if duracao_ms < 7000:
        return 900

    return 800


def criar_mapa_de_cortes(
        referencia: AudioSegment
):

    threshold = calcular_silence_threshold(
        referencia
    )

    print(
        f"Threshold de silêncio: "
        f"{threshold:.1f} dBFS"
    )

    silencios = detect_silence(
        referencia,
        min_silence_len=MIN_SILENCE_MS,
        silence_thresh=threshold,
        seek_step=10
    )

    mapa = []

    total_removido = 0

    for inicio, fim in silencios:

        duracao = fim - inicio

        manter = pausa_que_deve_ficar(
            duracao
        )

        if duracao <= manter:
            continue

        # Em vez de apagar a pausa toda,
        # retiramos apenas seu centro.
        manter_inicio = manter // 2
        manter_fim = manter - manter_inicio

        cortar_inicio = (
            inicio +
            manter_inicio
        )

        cortar_fim = (
            fim -
            manter_fim
        )

        remover = (
            cortar_fim -
            cortar_inicio
        )

        if remover <= 0:
            continue

        mapa.append({
            "silencio_inicio": inicio,
            "silencio_fim": fim,

            "cortar_inicio": cortar_inicio,
            "cortar_fim": cortar_fim,

            "duracao_original": duracao,
            "pausa_final": manter,
            "removido": remover,
        })

        total_removido += remover

    return mapa, total_removido, threshold


def aplicar_mapa_de_cortes(
        audio: AudioSegment,
        mapa
):

    partes = []

    cursor = 0

    for corte in mapa:

        inicio = corte["cortar_inicio"]
        fim = corte["cortar_fim"]

        partes.append(
            audio[cursor:inicio]
        )

        cursor = fim

    partes.append(
        audio[cursor:]
    )

    resultado = audio[:0]

    for parte in partes:
        resultado += parte

    return resultado