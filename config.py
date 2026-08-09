from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

ENTRADA_DIR = BASE_DIR / "entrada"
SAIDA_DIR = BASE_DIR / "saida"
ASSETS_DIR = BASE_DIR / "assets"


MIC1_PATH = ENTRADA_DIR / "mic1.wav"
MIC2_PATH = ENTRADA_DIR / "mic2.wav"

ABERTURA_PATH = ASSETS_DIR / "abertura.mp3"
ENCERRAMENTO_PATH = ASSETS_DIR / "encerramento.mp3"


# ============================================================
# SINCRONIZAÇÃO
# ============================================================

# Procurar as palmas apenas no início.
SYNC_SEARCH_MS = 20_000

# Distância permitida entre palma 1 e palma 2.
SYNC_MIN_DISTANCE_MS = 350
SYNC_MAX_DISTANCE_MS = 1_200

# Depois da segunda palma, descartamos este tempo.
SYNC_REMOVE_AFTER_CLAP_MS = 1_200


# ============================================================
# PAUSAS
# ============================================================

# Apenas pausas maiores que 2,5 segundos serão modificadas.
MIN_SILENCE_MS = 2_500

# None = calcula automaticamente com base no áudio.
SILENCE_THRESHOLD_DBFS = None


# ============================================================
# WHISPER
# ============================================================

WHISPER_MODEL = "small"
WHISPER_LANGUAGE = "pt"


# ============================================================
# PODCAST
# ============================================================

MIN_PODCAST_DURATION_MS = 60 * 60 * 1000