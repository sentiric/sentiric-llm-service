# 🧠 Sentiric LLM Service - Görev Listesi

Bu belge, `llm-service`'in geliştirme yol haritasını ve önceliklerini tanımlar.

---

### Faz 1: Tek Sağlayıcılı Ağ Geçidi (Mevcut Durum)

Bu faz, servisin tek bir LLM sağlayıcısı (Google Gemini) için güvenilir bir ağ geçidi olarak çalışmasını hedefler.

-   [x] **FastAPI Sunucusu:** `/generate` ve `/health` endpoint'leri.
-   [x] **Google Gemini Entegrasyonu:** Gelen prompt'ları Gemini API'sine gönderip yanıtı alma.
-   [x] **Yapılandırılmış Loglama:** Her istek için `trace_id` ile birlikte detaylı loglama.
-   [x] **Sağlam Hata Yönetimi:** API anahtarı eksikliği veya harici API hataları gibi durumları yönetme.

---

### Faz 2: Çoklu Sağlayıcı ve Adaptör Mimarisi (Sıradaki Öncelik)

Bu faz, servisi gerçek bir "Tak-Çıkar Lego Seti" haline getirmeyi hedefler.

-   [ ] **Görev ID: LLM-001 - Adaptör Deseni Refaktörü**
    -   **Açıklama:** Mevcut Gemini mantığını bir `GeminiAdapter` sınıfı içine taşı. Tüm adaptörlerin implemente edeceği bir `BaseLLMAdapter` soyut sınıfı oluştur.
    -   **Kabul Kriterleri:**
        -   [ ] `BaseLLMAdapter` oluşturulmalı.
        -   [ ] `GeminiAdapter`, bu base sınıftan türetilmeli.
        -   [ ] `.env` dosyasındaki `LLM_PROVIDER` değişkenine göre doğru adaptör dinamik olarak yüklenmeli.
        

-   [ ] **Görev ID: LLM-002 - OpenAI Adapter**
    -   **Açıklama:** OpenAI'nin GPT modellerini destekleyen bir `OpenAIAdapter` oluştur.
    -   **Durum:** ⬜ Planlandı.

-   [ ] **Görev ID: LLM-003 - Dinamik Adaptör Seçimi**
    -   **Açıklama:** `/generate` isteğine opsiyonel bir `provider` alanı ekleyerek, isteği yapan servisin hangi LLM'i kullanacağını seçebilmesini sağla.
    -   **Durum:** ⬜ Planlandı.

---

### Faz 3: Gelişmiş Özellikler

-   [ ] **Görev ID: LLM-004 - RAG Entegrasyonu**
    -   **Açıklama:** `/generate` isteğine bir `context_documents` alanı ekle. Eğer bu alan doluysa, bu dokümanları LLM prompt'una otomatik olarak ekleyerek RAG (Retrieval-Augmented Generation) akışını destekle.
    -   **Durum:** ⬜ Planlandı.