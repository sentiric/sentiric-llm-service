# 🧠 Sentiric LLM Service

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)

**Sentiric LLM Service**, Sentiric platformunun merkezi **Büyük Dil Modeli (LLM) Ağ Geçidi (Gateway)** olarak görev yapar. `sentiric-agent-service` gibi çekirdek orkestrasyon servislerini, belirli LLM sağlayıcılarının (Google Gemini, OpenAI, vb.) karmaşıklığından ve bağımlılıklarından soyutlar.

Bu servis, "Adaptör Mimarisi" felsefemizin somut bir uygulamasıdır. Ana platform, "metin üret" gibi soyut bir komut verir; bu servisin görevi ise bu komutu, yapılandırılmış olan herhangi bir LLM sağlayıcısının anlayacağı dile çevirmek ve yanıtı geri iletmektir.

## 🎯 Temel Sorumluluklar

*   **Tek Birleşik Arayüz:** Farklı LLM sağlayıcıları için tek ve tutarlı bir HTTP/REST arayüzü (`/generate`) sunar.
*   **Bağımlılık İzolasyonu:** `google-generativeai` gibi potansiyel olarak çakışan veya ağır Python bağımlılıklarını, ana platformun geri kalanından tamamen izole eder.
*   **Sağlayıcı Esnekliği:** `.env` dosyasındaki basit bir değişiklikle, platformun kullandığı LLM'i (örn: Gemini'dan OpenAI'ye) kod değişikliği yapmadan değiştirmeyi sağlar.
*   **Gözlemlenebilirlik:** Gelen her istek için `trace_id` takibi yapar ve yapılandırılmış loglar üretir.

## 🛠️ Teknoloji Yığını

*   **Dil:** Python
*   **Web Çerçevesi:** FastAPI
*   **Bağımlılık Yönetimi:** Poetry
*   **AI Kütüphanesi:** `google-generativeai`

## 🔌 API Etkileşimleri

*   **Gelen (Sunucu):**
    *   `sentiric-agent-service` (REST/JSON): `/generate` endpoint'ine metin üretme istekleri alır.
*   **Giden (İstemci):**
    *   Google Gemini API (veya yapılandırılmış diğer LLM sağlayıcıları).

## 🚀 Yerel Geliştirme

1.  **Bağımlılıkları Yükleyin:**
2.  **Ortam Değişkenlerini Ayarlayın:** `.env.example` dosyasını `.env` olarak kopyalayın ve gerekli değişkenleri doldurun.
3.  **Servisi Çalıştırın:**

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen projenin ana [Sentiric Governance](https://github.com/sentiric/sentiric-governance) reposundaki kodlama standartlarına ve katkıda bulunma rehberine göz atın.

---
## 🏛️ Anayasal Konum

Bu servis, [Sentiric Anayasası'nın (v11.0)](https://github.com/sentiric/sentiric-governance/blob/main/docs/blueprint/Architecture-Overview.md) **Zeka & Orkestrasyon Katmanı**'nda yer alan merkezi bir bileşendir.