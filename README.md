# 🧠 Sentiric LLM Service

**Açıklama:** Bu servis, Sentiric platformunun merkezi **Büyük Dil Modeli (LLM) Ağ Geçidi (Gateway)** olarak görev yapar. `sentiric-agent-service` gibi çekirdek orkestrasyon servislerini, belirli LLM sağlayıcılarının (Google Gemini, OpenAI, vb.) karmaşıklığından ve bağımlılıklarından soyutlar.

Bu servis, "Adaptör Mimarisi" felsefemizin somut bir uygulamasıdır. Ana platform, "metin üret" gibi soyut bir komut verir; bu servisin görevi ise bu komutu, yapılandırılmış olan herhangi bir LLM sağlayıcısının anlayacağı dile çevirmek ve yanıtı geri iletmektir.

## 🎯 Temel Sorumluluklar

*   **Tek Birleşik Arayüz:** Farklı LLM sağlayıcıları için tek ve tutarlı bir HTTP/REST arayüzü (`/generate`) sunar.
*   **Bağımlılık İzolasyonu:** `google-generativeai` gibi potansiyel olarak çakışan veya ağır Python bağımlılıklarını, ana platformun geri kalanından tamamen izole eder. Bu, platformun genel kararlılığını korur.
*   **Sağlayıcı Esnekliği:** `.env` dosyasındaki basit bir değişiklikle, platformun kullandığı LLM'i (örn: Gemini'dan OpenAI'ye) kod değişikliği yapmadan değiştirmeyi sağlar.
*   **Geleceğe Hazırlık:** Gelecekte açık kaynaklı ve yerel olarak çalıştırılan (örn: Llama 3) modeller için bir entegrasyon noktası görevi görür.

## 🛠️ Teknoloji Yığını

*   **Dil:** Python
*   **Web Çerçevesi:** FastAPI
*   **Sunucu:** Uvicorn
*   **Bağımlılık Yönetimi:** Poetry

## 🔌 API Etkileşimleri

*   **Gelen (Provider For):** `sentiric-agent-service`'ten (ve potansiyel olarak diğer iç servislerden) `/generate` endpoint'ine HTTP POST istekleri alır.
*   **Giden (Client Of):** Yapılandırılmış olan harici LLM sağlayıcısının (örn: Google Gemini API) API'sine istekler gönderir.

### API Kontratı

**Endpoint:** `POST /generate`

**İstek Gövdesi (`Request Body`):**
```json
{
  "prompt": "Bir müşteri hizmetleri temsilcisi olarak 'Merhaba' de.",
  "conversation_history": [
    {"role": "user", "text": "Selam"},
    {"role": "assistant", "text": "Merhaba, size nasıl yardımcı olabilirim?"}
  ],
  "provider": "gemini" // Opsiyonel: Gelecekte birden fazla sağlayıcıyı desteklemek için
}
```

**Başarılı Yanıt (`Response 200 OK`):**
```json
{
  "text": "Merhaba! Sentiric'e hoş geldiniz, size bugün nasıl yardımcı olabilirim?"
}
```

## 🚀 Yerel Geliştirme (Local Development)

1.  **Repo'yu Klonlayın:**
    ```bash
    git clone https://github.com/sentiric/sentiric-llm-service.git
    cd sentiric-llm-service
    ```
2.  **Poetry'yi Kurun:** (Eğer kurulu değilse)
    ```bash
    pip install poetry
    ```
3.  **Bağımlılıkları Kurun:**
    ```bash
    poetry install
    ```
4.  **Ortam Değişkenlerini Ayarlayın:**
    `.env.example` dosyasını `.env` olarak kopyalayın ve `GOOGLE_API_KEY`'inizi girin.
    ```bash
    cp .env.example .env
    nano .env
    ```
5.  **Servisi Başlatın:**
    ```bash
    poetry run uvicorn main:app --reload
    ```
    Servis artık `http://localhost:8000` adresinde çalışıyor olacaktır.

## 🐳 Docker ile Çalıştırma

Bu servis, `sentiric-infrastructure` reposundaki merkezi `docker-compose.yml` dosyası aracılığıyla platformun bir parçası olarak çalıştırılmak üzere tasarlanmıştır.

Servisi tek başına test etmek için:
```bash
# .env dosyanızın hazır olduğundan emin olun
docker compose -f docker-compose.service.yml up --build
```

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen projenin ana [Sentiric Governance](https://github.com/sentiric/sentiric-governance) reposundaki kodlama standartlarına ve katkıda bulunma rehberine göz atın.
