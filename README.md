# Jenkins - MLflow Demo

Bu depo, Jenkins uzerinden MLflow kullanarak basit bir makine ogrenmesi deneyinin otomatik olarak nasil calistirilacagini gosterir. Pipeline, scikit-learn ile LogisticRegression modelini egitir ve sonuclari dosya tabanli bir MLflow tracking sunucusuna yazar.

## Bilesenler
- `train.py`: Iris veri seti uzerinde modeli egitir, metrikleri ve artefaktlari (`mlruns/`, `artifacts/`) MLflow'a loglar.
- `requirements.txt`: Gerekli Python paketlerini listeler.
- `Jenkinsfile`: Jenkins deklaratif pipeline tanimi.

## Jenkins Pipeline Akisi
1. `python:3.11-slim` Docker imajini root kullanicisi ile calistirir.
2. Bagimliliklari `pip install -r requirements.txt` ile yukler.
3. `train.py` dosyasini calistirarak MLflow run baslatir (`mlflow.set_tracking_uri("file:./mlruns")`).
4. Olusan `mlruns/` ve `artifacts/` klasorlerini build artefakti olarak arsivler.

## Lokalde Calistirma
```bash
python -m venv .venv
source .venv/bin/activate  # Windows'ta `.venv\Scripts\activate`
pip install -r requirements.txt
python train.py
```

Komutlar tamamlandiginda, MLflow calistirma detaylarini `mlruns/` altinda bulabilirsiniz. Modeller ve ek raporlar `artifacts/` klasorunde yer alir.
