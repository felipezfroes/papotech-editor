import numpy as np

from pydub import AudioSegment
from scipy.signal import find_peaks

from config import (
    SYNC_SEARCH_MS,
    SYNC_MIN_DISTANCE_MS,
    SYNC_MAX_DISTANCE_MS,
    SYNC_REMOVE_AFTER_CLAP_MS,
)


def detectar_palmas(audio: AudioSegment):
    """
    Procura duas palmas fortes no início da gravação.
    Retorna os tempos das duas palmas em milissegundos.
    """

    trecho = audio[:SYNC_SEARCH_MS]

    # Para análise, não precisamos de estéreo.
    trecho = trecho.set_channels(1)

    samples = np.array(
        trecho.get_array_of_samples()
    ).astype(np.float64)

    if len(samples) == 0:
        raise RuntimeError("Áudio vazio.")

    max_amplitude = trecho.max_possible_amplitude

    samples /= max_amplitude

    sample_rate = trecho.frame_rate

    # Janela de aproximadamente 10 ms.
    window_ms = 10

    window_samples = max(
        1,
        int(sample_rate * window_ms / 1000)
    )

    quantidade = len(samples) // window_samples

    samples = samples[:quantidade * window_samples]

    blocos = samples.reshape(
        quantidade,
        window_samples
    )

    # Energia RMS de cada janela.
    rms = np.sqrt(
        np.mean(blocos ** 2, axis=1)
    )

    if len(rms) == 0:
        raise RuntimeError(
            "Não foi possível analisar o áudio."
        )

    maior_energia = np.max(rms)

    threshold = max(
        np.percentile(rms, 85),
        maior_energia * 0.20
    )

    distancia_minima_picos = max(
        1,
        int(150 / window_ms)
    )

    peaks, properties = find_peaks(
        rms,
        height=threshold,
        prominence=maior_energia * 0.08,
        distance=distancia_minima_picos
    )

    if len(peaks) < 2:
        raise RuntimeError(
            "Não foi possível detectar duas palmas."
        )

    candidatos = []

    for i in range(len(peaks)):

        for j in range(i + 1, len(peaks)):

            tempo1 = peaks[i] * window_ms
            tempo2 = peaks[j] * window_ms

            distancia = tempo2 - tempo1

            if (
                SYNC_MIN_DISTANCE_MS
                <= distancia
                <= SYNC_MAX_DISTANCE_MS
            ):
                energia1 = rms[peaks[i]]
                energia2 = rms[peaks[j]]

                score = energia1 + energia2

                candidatos.append(
                    (
                        score,
                        tempo1,
                        tempo2
                    )
                )

    if not candidatos:
        raise RuntimeError(
            "Nenhum par de palmas válido encontrado."
        )

    candidatos.sort(
        key=lambda item: item[0],
        reverse=True
    )

    _, palma1, palma2 = candidatos[0]

    return int(palma1), int(palma2)


def sincronizar(mic1: AudioSegment,
                mic2: AudioSegment):

    print("Detectando palmas do MIC 1...")

    palmas1 = detectar_palmas(mic1)

    print(
        f"MIC 1: "
        f"{palmas1[0]} ms / "
        f"{palmas1[1]} ms"
    )

    print("Detectando palmas do MIC 2...")

    palmas2 = detectar_palmas(mic2)

    print(
        f"MIC 2: "
        f"{palmas2[0]} ms / "
        f"{palmas2[1]} ms"
    )

    intervalo1 = palmas1[1] - palmas1[0]
    intervalo2 = palmas2[1] - palmas2[0]

    if abs(intervalo1 - intervalo2) > 150:

        raise RuntimeError(
            "As palmas detectadas nos dois "
            "microfones parecem diferentes."
        )

    centro1 = sum(palmas1) / 2
    centro2 = sum(palmas2) / 2

    offset = int(
        round(centro2 - centro1)
    )

    trim1 = 0
    trim2 = 0

    # Se a palma aparece mais tarde no arquivo 2,
    # ele possui mais áudio antes dela.
    if offset > 0:

        trim2 = offset
        mic2 = mic2[offset:]

    elif offset < 0:

        trim1 = abs(offset)
        mic1 = mic1[abs(offset):]

    # Tempos corrigidos das palmas.
    palma2_mic1 = palmas1[1] - trim1
    palma2_mic2 = palmas2[1] - trim2

    palma2_sincronizada = int(
        round(
            (
                palma2_mic1 +
                palma2_mic2
            ) / 2
        )
    )

    # Retira as palmas do áudio que irá para o podcast.
    inicio_programa = (
        palma2_sincronizada +
        SYNC_REMOVE_AFTER_CLAP_MS
    )

    mic1 = mic1[inicio_programa:]
    mic2 = mic2[inicio_programa:]

    # Os arquivos finais precisam possuir
    # exatamente o mesmo tamanho.
    tamanho = min(
        len(mic1),
        len(mic2)
    )

    mic1 = mic1[:tamanho]
    mic2 = mic2[:tamanho]

    dados = {
        "palmas_mic1": palmas1,
        "palmas_mic2": palmas2,
        "offset_ms": offset,
        "inicio_removido_ms": inicio_programa,
    }

    return mic1, mic2, dados