from pathlib import Path

import torch
import whisper

from config import (
    WHISPER_MODEL,
    WHISPER_LANGUAGE,
)


def transcrever(
        caminho_audio: Path
):

    print(
        f"Carregando Whisper "
        f"({WHISPER_MODEL})..."
    )

    model = whisper.load_model(
        WHISPER_MODEL
    )

    usar_fp16 = torch.cuda.is_available()

    print("Transcrevendo podcast...")

    resultado = model.transcribe(
        str(caminho_audio),
        language=WHISPER_LANGUAGE,
        fp16=usar_fp16,
        verbose=False,
        word_timestamps=True
    )

    return resultado