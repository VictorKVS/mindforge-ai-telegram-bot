# LLMRouter Future Work
Version: 2.1

---

## 1. Planned Enhancements

### 1.1 ML-based Model Selection
Использование:
- latency prediction  
- token cost optimisation  
- success-rate trending  

### 1.2 Distributed Cache (Redis)
Общий кэш для нескольких ботов.

### 1.3 Circuit Breaker
Отключение моделей при системном сбое.

### 1.4 Semantic Routing
Выбор модели по типу задачи:
- coding → DeepSeek/Qwen  
- RU text → GigaChat  
- offline → LLaMA  

---

## 2. KM-6 Integration

Будет добавлено:
- policy-based model election  
- data-class based restrictions  
- audit trails across providers  

---

## 3. Additional Monitoring

- Prometheus exporter  
- Grafana dashboard template  
- SIEM connectors (Wazuh/ELK)  

---

