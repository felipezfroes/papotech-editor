from pydub import AudioSegment

from config import (
    MIC1_PATH,
    MIC2_PATH,
    ABERTURA_PATH,
    ENCERRAMENTO_PATH,
    SAIDA_DIR,
    MIN_PODCAST_DURATION_MS,
)

from audio.sync import sincronizar
from audio.mix import criar_mix_referencia
from audio.cuts import (
    criar_mapa_de_cortes,
    aplicar_mapa_de_cortes,
)

from analysis.transcription import (
    transcrever,
)

from analysis.markers import (
    analisar_marcacoes,
)

from reports.report import (
    salvar_transcricao,
    salvar_srt,
    salvar_marcacoes,
    salvar_cortes,
)

from utils.timecode import (
    formatar_ms,
)


def carregar_asset(
        caminho
):

    if not caminho.exists():
        return None

    return AudioSegment.from_file(
        caminho
    )


def main():

    print()
    print("=" * 55)
    print("               PAPOTECH EDITOR")
    print("=" * 55)
    print()

    SAIDA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # ========================================================
    # CARREGAMENTO
    # ========================================================

    print("[1/8] Carregando os dois microfones...")

    if not MIC1_PATH.exists():
        raise FileNotFoundError(
            f"Não encontrei: {MIC1_PATH}"
        )

    if not MIC2_PATH.exists():
        raise FileNotFoundError(
            f"Não encontrei: {MIC2_PATH}"
        )

    mic1 = AudioSegment.from_file(
        MIC1_PATH
    )

    mic2 = AudioSegment.from_file(
        MIC2_PATH
    )

    print(
        "MIC 1:",
        formatar_ms(len(mic1))
    )

    print(
        "MIC 2:",
        formatar_ms(len(mic2))
    )

    # ========================================================
    # SINCRONIZAÇÃO
    # ========================================================

    print()
    print(
        "[2/8] Sincronizando pelas palmas..."
    )

    mic1, mic2, sync_info = sincronizar(
        mic1,
        mic2
    )

    print(
        "Offset encontrado:",
        sync_info["offset_ms"],
        "ms"
    )

    print(
        "Duração sincronizada:",
        formatar_ms(len(mic1))
    )

    # ========================================================
    # MIX PARA DETECTAR PAUSAS
    # ========================================================

    print()
    print(
        "[3/8] Criando mix de análise..."
    )

    referencia_original = (
        criar_mix_referencia(
            mic1,
            mic2
        )
    )

    # ========================================================
    # PAUSAS
    # ========================================================

    print()
    print(
        "[4/8] Detectando pausas longas..."
    )

    (
        mapa,
        tempo_removido,
        threshold
    ) = criar_mapa_de_cortes(
        referencia_original
    )

    print(
        "Pausas modificadas:",
        len(mapa)
    )

    print(
        "Tempo removido:",
        formatar_ms(
            tempo_removido
        )
    )

    print(
        "Aplicando os MESMOS cortes "
        "nos dois microfones..."
    )

    mic1_editado = aplicar_mapa_de_cortes(
        mic1,
        mapa
    )

    mic2_editado = aplicar_mapa_de_cortes(
        mic2,
        mapa
    )

    tamanho = min(
        len(mic1_editado),
        len(mic2_editado)
    )

    mic1_editado = mic1_editado[
        :tamanho
    ]

    mic2_editado = mic2_editado[
        :tamanho
    ]

    # ========================================================
    # EXPORTAÇÃO DOS WAVS
    # ========================================================

    print()
    print(
        "[5/8] Exportando WAVs para CapCut..."
    )

    mic1_path = (
        SAIDA_DIR /
        "01_MIC1_EDITADO.wav"
    )

    mic2_path = (
        SAIDA_DIR /
        "02_MIC2_EDITADO.wav"
    )

    mic1_editado.export(
        mic1_path,
        format="wav"
    )

    mic2_editado.export(
        mic2_path,
        format="wav"
    )

    # ========================================================
    # MIX FINAL DE REFERÊNCIA
    # ========================================================

    print()
    print(
        "[6/8] Criando mix de referência..."
    )

    referencia_final = (
        criar_mix_referencia(
            mic1_editado,
            mic2_editado
        )
    )

    referencia_path = (
        SAIDA_DIR /
        "03_MIX_REFERENCIA.mp3"
    )

    referencia_final.export(
        referencia_path,
        format="mp3",
        bitrate="192k"
    )

    # ========================================================
    # WHISPER
    # ========================================================

    print()
    print(
        "[7/8] Analisando fala com Whisper..."
    )

    resultado = transcrever(
        referencia_path
    )

    marcacoes = analisar_marcacoes(
        resultado
    )

    # ========================================================
    # ASSETS
    # ========================================================

    abertura = carregar_asset(
        ABERTURA_PATH
    )

    encerramento = carregar_asset(
        ENCERRAMENTO_PATH
    )

    abertura_ms = (
        len(abertura)
        if abertura
        else 0
    )

    encerramento_ms = (
        len(encerramento)
        if encerramento
        else 0
    )

    # ========================================================
    # RELATÓRIOS
    # ========================================================

    print()
    print(
        "[8/8] Criando relatórios..."
    )

    salvar_transcricao(
        resultado
    )

    salvar_srt(
        resultado
    )

    salvar_marcacoes(
        marcacoes,
        abertura_ms
    )

    salvar_cortes(
        mapa
    )

    # ========================================================
    # RESUMO
    # ========================================================

    duracao_audio = len(
        mic1_editado
    )

    duracao_capcut = (
        abertura_ms +
        duracao_audio +
        encerramento_ms
    )

    print()
    print("=" * 55)
    print(
        "             PROCESSAMENTO CONCLUÍDO"
    )
    print("=" * 55)

    print()

    print(
        "Duração após edição:",
        formatar_ms(
            duracao_audio
        )
    )

    print(
        "Abertura:",
        formatar_ms(
            abertura_ms
        )
    )

    print(
        "Encerramento:",
        formatar_ms(
            encerramento_ms
        )
    )

    print(
        "Duração prevista no CapCut:",
        formatar_ms(
            duracao_capcut
        )
    )

    print()

    if (
        duracao_capcut
        >= MIN_PODCAST_DURATION_MS
    ):

        print(
            "✅ Episódio acima de 1 hora."
        )

    else:

        faltando = (
            MIN_PODCAST_DURATION_MS
            -
            duracao_capcut
        )

        print(
            "⚠ Episódio abaixo de 1 hora."
        )

        print(
            "Faltam:",
            formatar_ms(
                faltando
            )
        )

    print()

    print(
        "Possíveis erros encontrados:",
        len(marcacoes)
    )

    print()

    print(
        "Arquivos disponíveis em:"
    )

    print(
        SAIDA_DIR
    )

    print()


if __name__ == "__main__":
    main()