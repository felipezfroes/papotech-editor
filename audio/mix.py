from pydub import AudioSegment
from pydub.effects import normalize


def criar_mix_referencia(
        mic1: AudioSegment,
        mic2: AudioSegment
):
    """
    Cria um áudio mono utilizado apenas para
    análise, transcrição e referência.
    """

    m1 = mic1.set_channels(1) - 6
    m2 = mic2.set_channels(1) - 6

    mix = m1.overlay(m2)

    mix = normalize(
        mix,
        headroom=1.5
    )

    return mix