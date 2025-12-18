"""
Configurações globais para os scripts de validação e refinamento
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Diretórios base
BASE_DIR = Path(__file__).parent.parent
THEMES_DIR = BASE_DIR.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"

# Arquivo principal da árvore temática
THEMES_FILE = THEMES_DIR / "themes_tree_enriched_full.yaml"

# Diretórios de dados
EMBEDDINGS_CACHE_DIR = DATA_DIR / "embeddings_cache"
ANNOTATIONS_DIR = DATA_DIR / "annotations"
CONFUSION_MATRICES_DIR = REPORTS_DIR / "04_confusion_matrices"

# Criar diretórios se não existirem
for directory in [DATA_DIR, REPORTS_DIR, NOTEBOOKS_DIR,
                  EMBEDDINGS_CACHE_DIR, ANNOTATIONS_DIR, CONFUSION_MATRICES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Configurações de Embeddings
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
)
EMBEDDING_BATCH_SIZE = int(os.getenv("EMBEDDING_BATCH_SIZE", "32"))
EMBEDDING_DEVICE = os.getenv("EMBEDDING_DEVICE", "auto")  # auto detecta cuda/mps/cpu

# Thresholds de Confiança
CONFIDENCE_THRESHOLD_L1 = float(os.getenv("CONFIDENCE_THRESHOLD_L1", "0.4"))
CONFIDENCE_THRESHOLD_L2 = float(os.getenv("CONFIDENCE_THRESHOLD_L2", "0.5"))
CONFIDENCE_THRESHOLD_L3 = float(os.getenv("CONFIDENCE_THRESHOLD_L3", "0.6"))

# Configurações de Dataset
TEST_DATASET_SIZE = int(os.getenv("TEST_DATASET_SIZE", "500"))
ANNOTATION_BATCH_SIZE = int(os.getenv("ANNOTATION_BATCH_SIZE", "50"))

# Typesense
TYPESENSE_HOST = os.getenv("TYPESENSE_HOST", "localhost")
TYPESENSE_PORT = int(os.getenv("TYPESENSE_PORT", "8108"))
TYPESENSE_API_KEY = os.getenv("TYPESENSE_API_KEY", "")
TYPESENSE_PROTOCOL = os.getenv("TYPESENSE_PROTOCOL", "http")
TYPESENSE_COLLECTION = os.getenv("TYPESENSE_COLLECTION", "news")

# Validação
MIN_KEYWORDS = int(os.getenv("MIN_KEYWORDS", "5"))
MAX_KEYWORDS = int(os.getenv("MAX_KEYWORDS", "20"))
MIN_DESCRIPTION_WORDS = int(os.getenv("MIN_DESCRIPTION_WORDS", "30"))
MAX_DESCRIPTION_WORDS = int(os.getenv("MAX_DESCRIPTION_WORDS", "200"))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.85"))

# Métricas de Sucesso
TARGET_ACCURACY_L1 = float(os.getenv("TARGET_ACCURACY_L1", "0.85"))
TARGET_ACCURACY_L2 = float(os.getenv("TARGET_ACCURACY_L2", "0.70"))
TARGET_ACCURACY_L3 = float(os.getenv("TARGET_ACCURACY_L3", "0.60"))
TARGET_HIERARCHICAL_ACCURACY = float(os.getenv("TARGET_HIERARCHICAL_ACCURACY", "0.55"))

# Multi-label
MAX_LABELS = int(os.getenv("MAX_LABELS", "3"))
SECONDARY_LABEL_THRESHOLD = float(os.getenv("SECONDARY_LABEL_THRESHOLD", "0.4"))

# Cores para output (opcional)
COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
}

def print_config():
    """Imprime configuração atual"""
    print(f"{COLORS['bold']}=== Configuração ==={COLORS['reset']}")
    print(f"Base dir: {BASE_DIR}")
    print(f"Themes file: {THEMES_FILE}")
    print(f"Embedding model: {EMBEDDING_MODEL}")
    print(f"Device: {EMBEDDING_DEVICE}")
    print(f"Test dataset size: {TEST_DATASET_SIZE}")
    print(f"Typesense: {TYPESENSE_PROTOCOL}://{TYPESENSE_HOST}:{TYPESENSE_PORT}")
    print()

if __name__ == "__main__":
    print_config()
