"""
Utilitários para geração e cache de embeddings
"""
import pickle
import hashlib
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


class EmbeddingCache:
    """Cache de embeddings para evitar recalcular"""

    def __init__(self, cache_dir: Path, model_name: str):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.model_name = model_name

        # Criar hash do modelo para cache
        model_hash = hashlib.md5(model_name.encode()).hexdigest()[:8]
        self.cache_file = self.cache_dir / f"embeddings_{model_hash}.pkl"

        self.cache = self._load_cache()

    def _load_cache(self) -> Dict:
        """Carrega cache do disco"""
        if self.cache_file.exists():
            with open(self.cache_file, 'rb') as f:
                return pickle.load(f)
        return {}

    def _save_cache(self) -> None:
        """Salva cache no disco"""
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.cache, f)

    def get(self, text: str) -> Optional[np.ndarray]:
        """Busca embedding no cache"""
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return self.cache.get(text_hash)

    def set(self, text: str, embedding: np.ndarray) -> None:
        """Adiciona embedding ao cache"""
        text_hash = hashlib.md5(text.encode()).hexdigest()
        self.cache[text_hash] = embedding

    def save(self) -> None:
        """Persiste cache no disco"""
        self._save_cache()

    def clear(self) -> None:
        """Limpa cache"""
        self.cache = {}
        if self.cache_file.exists():
            self.cache_file.unlink()


class EmbeddingGenerator:
    """Gerador de embeddings com cache"""

    def __init__(self, model_name: str, cache_dir: Path, device: str = "cpu"):
        import torch

        self.model_name = model_name
        self.cache = EmbeddingCache(cache_dir, model_name)

        # Auto-detect and configure device
        if device == 'auto':
            if torch.cuda.is_available():
                self.device = 'cuda'
                print("✓ Auto-detectado CUDA GPU")
            elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
                self.device = 'mps'
                print("✓ Auto-detectado Apple Metal (MPS)")
            else:
                self.device = 'cpu'
                print("⚠ GPU não detectada, usando CPU")
        else:
            # Check device availability for explicit selections
            if device == 'cuda' and not torch.cuda.is_available():
                print("⚠ CUDA não disponível, usando CPU")
                self.device = 'cpu'
            elif device == 'mps':
                if not torch.backends.mps.is_available():
                    print("⚠ MPS não disponível (requer macOS 12.3+ e Apple Silicon)")
                    self.device = 'cpu'
                elif not torch.backends.mps.is_built():
                    print("⚠ MPS não compilado nesta instalação PyTorch, usando CPU")
                    self.device = 'cpu'
                else:
                    print("✓ Usando Apple Metal Performance Shaders (MPS)")
                    self.device = 'mps'
            else:
                self.device = device

        print(f"Carregando modelo de embeddings: {model_name}")
        self.model = SentenceTransformer(model_name, device=self.device)
        print(f"✓ Modelo carregado (device: {self.device})")

    def encode(self, texts: List[str], batch_size: int = 32,
               show_progress: bool = True) -> np.ndarray:
        """
        Gera embeddings para lista de textos (com cache)

        Args:
            texts: Lista de textos
            batch_size: Tamanho do batch para processamento
            show_progress: Mostrar barra de progresso

        Returns:
            Array numpy com embeddings
        """
        embeddings = []
        texts_to_encode = []
        indices_to_encode = []

        # Verificar cache
        for i, text in enumerate(texts):
            cached = self.cache.get(text)
            if cached is not None:
                embeddings.append(cached)
            else:
                texts_to_encode.append(text)
                indices_to_encode.append(i)
                embeddings.append(None)  # Placeholder

        # Gerar embeddings para textos não cacheados
        if texts_to_encode:
            desc = "Gerando embeddings" if show_progress else None
            new_embeddings = self.model.encode(
                texts_to_encode,
                batch_size=batch_size,
                show_progress_bar=show_progress,
                convert_to_numpy=True
            )

            # Adicionar ao cache e à lista
            for idx, text, emb in zip(indices_to_encode, texts_to_encode, new_embeddings):
                self.cache.set(text, emb)
                embeddings[idx] = emb

            # Salvar cache
            self.cache.save()

        return np.array(embeddings)

    def encode_single(self, text: str) -> np.ndarray:
        """Gera embedding para um único texto"""
        return self.encode([text], show_progress=False)[0]


def cosine_similarity(emb1: np.ndarray, emb2: np.ndarray) -> float:
    """Calcula similaridade cosine entre dois embeddings"""
    return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))


def similarity_matrix(embeddings: np.ndarray) -> np.ndarray:
    """
    Calcula matriz de similaridade para conjunto de embeddings

    Args:
        embeddings: Array (n_samples, embedding_dim)

    Returns:
        Matriz de similaridade (n_samples, n_samples)
    """
    # Normalizar embeddings
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    normalized = embeddings / norms

    # Calcular similaridades (produto matricial de embeddings normalizados)
    return np.dot(normalized, normalized.T)
