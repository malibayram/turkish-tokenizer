# Turkish Tokenizer

[![PyPI version](https://badge.fury.io/py/turkish-tokenizer.svg)](https://badge.fury.io/py/turkish-tokenizer)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Dilbilim kurallarını temel alarak, çok dilli metinleri işlemek ve anlam bütünlüğünü korumak için gelişmiş bir tokenizer altyapısı.

## Kurulum

### PyPI üzerinden kurulum (Önerilen)

```bash
pip install turkish-tokenizer
```

### Geliştirme için kurulum

```bash
git clone https://github.com/malibayram/turkish-tokenizer.git
cd turkish-tokenizer
pip install -e .
```

## Hızlı Başlangıç

### Temel Tokenizer Kullanımı

```python
from turkish_tokenizer import TurkishTokenizer

# Tokenizer'ı başlat
tokenizer = TurkishTokenizer()

# Metin tokenizasyonu
text = "Merhaba dünya! Nasılsınız?"
tokens = tokenizer.encode(text)
print("Token IDs:", tokens)

# Token'ları metne geri çevir
decoded_text = tokenizer.decode(tokens)
print("Decoded:", decoded_text)
```

### Hugging Face Uyumlu Tokenizer

```python
from turkish_tokenizer import HFTurkishTokenizer

# Hugging Face uyumlu tokenizer'ı başlat
tokenizer = HFTurkishTokenizer()

# Model girişi için hazırla
model_inputs = tokenizer(
    "Bu cümle model girişi için hazırlanacak.",
    add_special_tokens=True,
    padding=True,
    truncation=True,
    max_length=512,
    return_tensors="pt"
)

print(model_inputs)
# Output: {'input_ids': tensor([[...]]), 'attention_mask': tensor([[...]])}
```

**Hugging Face entegrasyonu hakkında daha fazla bilgi için [README_HF.md](README_HF.md) dosyasına bakın.**

### Gelişmiş Tokenizasyon

```python
from turkish_tokenizer import TurkishTokenizer

# Tokenizer'ı başlat
tokenizer = TurkishTokenizer()

# Tokenları string olarak al
text = "Kitapları masa üzerinde bıraktım."
tokens = tokenizer.tokenize(text)
print("Tokens:", tokens)

# Token tiplerini öğren
token_details, _ = tokenizer.tokenize_text(text)
for token in token_details:
    print(f"Token: '{token['token']}', ID: {token['id']}, Type: {token['type']}")
```

## İlk Versiyon

- [x] Kelime köklerinin ses olayına uğramış olan hallerinin ses olayına uğramamış olan halleri ile aynı id ile temsil edilmesi
- [x] İlkHarfBüyük tokeni oluşturulması ve tüm tokenlerin ilk harfinin küçük harfe çevrilmesi
- [x] Çoğul tokeni oluşturulması ve ler - lar eklerinin silinmesi
- [x] Tamamen aynı olan ama sesleri farklı olan eklerin özel tokenler ile temsil edilmesi
- [x] Boşluk, satır sonu ve tab karakterlerinin özel tokenler ile temsil edilmesi

## Gelecek Özellikler

- [ ] Çok dilli destek
- [ ] Performans optimizasyonları
- [ ] Daha kapsamlı test senaryoları
- [ ] Web API desteği
- [ ] Docker entegrasyonu

## GitHub Actions Setup

This project uses GitHub Actions for automated testing and publishing to PyPI. To set up automated publishing:

### 1. Add PyPI API Token to GitHub Secrets

1. Go to your GitHub repository settings
2. Navigate to "Secrets and variables" → "Actions"
3. Add the following secrets:
   - `PYPI_API_TOKEN`: Your PyPI API token (starts with `pypi-`)
   - `TEST_PYPI_API_TOKEN`: Your TestPyPI API token (optional)

### 2. Publishing Workflow

The project will automatically publish to PyPI when:

- A new version tag is pushed (e.g., `v0.2.1`)
- The workflow is manually triggered from GitHub Actions

### 3. Testing Workflow

Tests run automatically on:

- Every push to `main` or `develop` branches
- Every pull request to `main` branch

---

## Projenin Amacı ve Kapsamı

Bu projenin amacı, metin analizi ve doğal dil işleme (NLP) süreçlerinde kullanılabilecek, dilbilgisel yapıları ve anlam bütünlüğünü dikkate alan bir tokenizer geliştirmektir. Proje, Türkçe dilbilgisi kurallarını referans alarak başlamış olsa da, evrensel dil kuralları doğrultusunda çok dilli bir yapıya sahip olacak şekilde genişletilecektir.

## Temel Özellikler

- Dilbilim kurallarına dayalı tokenizasyon
- Morfolojik analiz desteği
- Çok dilli destek altyapısı
- Genişletilebilir mimari
- Yüksek performanslı işleme
- Özel karakter ve boşluk işleme desteği

## Dosya Yapısı

Tokenizer üç temel sözlük dosyası kullanır:

- `kokler.json`: Kök kelimeler ve özel tokenler (0-20000 arası ID'ler)
- `ekler.json`: Ekler (20000-20256 arası ID'ler)
- `bpe_tokenler.json`: BPE token'ları

### Özel Tokenler

```json
{
  "<uppercase>": 0, // Büyük harf işareti
  "<unknown>": 1, // Bilinmeyen token
  " ": 2, // Boşluk karakteri
  "\n": 3, // Satır sonu
  "\t": 4, // Tab karakteri
  "<pad>": 5, // Padding token
  "<eos>": 6 // End of sequence token
}
```

## Kullanım

### Python Implementasyonu

```python
from turkish_tokenizer import TurkishTokenizer

tokenizer = TurkishTokenizer()

text = "Kitabı ve defterleri getirn,\nYouTube\t"
result = tokenizer.tokenize(text)
print(result)
```

## Geliştirme ve Katkıda Bulunma

### Geliştirme Ortamı Kurulumu

1. Repository'yi klonlayın:

```bash
git clone <repository-url>
cd tokenizer
```

2. Python ortamını hazırlayın:

```bash
python -m venv venv
source venv/bin/activate  # Unix/macOS
# veya
.\venv\Scripts\activate  # Windows
```

### Geliştirme Süreci

1. Yeni bir branch oluşturun:

```bash
git checkout -b feature/yeni-ozellik
```

2. Testleri çalıştırın:

```bash
# Python testleri
python -m pytest tests/

# Rust testleri
cargo test
```

3. Kod stilini kontrol edin:

```bash
# Python
flake8 .
black .
```

4. Değişikliklerinizi commit edin:

```bash
git add .
git commit -m "feat: yeni özellik eklendi"
```

### Pull Request Süreci

1. Branch'inizi push edin:

```bash
git push origin feature/yeni-ozellik
```

2. GitHub üzerinden pull request açın
3. Code review sürecini takip edin
4. Gerekli düzeltmeleri yapın
5. PR'ınız onaylandığında main branch'e merge edilecektir

### Geliştirme Gereksinimleri

#### Python

- Python 3.8+
- pytest
- black
- flake8

## Lisans

MIT

---

**Not:** Proje aktif geliştirme aşamasındadır.
