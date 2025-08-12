# Print Studios Games API

Bu basit Python Flask API, `scraped_date_printstudios.json` dosyasındaki oyun verilerini sunar.

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. API'yi çalıştırın:
```bash
python app.py
```

API varsayılan olarak `http://localhost:5000` adresinde çalışacaktır.

## API Endpoints

### 1. Tüm Oyunları Getir
```
GET /games
```

**Response:**
```json
{
  "success": true,
  "count": 23,
  "data": [...]
}
```

### 2. ID'ye Göre Oyun Getir
```
GET /games/{id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "gameId": 1,
    "name": "Holy Hand Grenade 2 (DD)",
    "subtitle": "The Bishop is Back!",
    "releaseDate": "Aug 27, 2025",
    "rtp": 96.01,
    "rtpWithBonusBuy": 96.51,
    "volatility": "5 out of 5",
    "maxWin": "30,000x",
    "features": {...},
    "demoLink": "..."
  }
}
```

### 3. Sağlık Kontrolü
```
GET /health
```

### 4. Ana Sayfa
```
GET /
```

## Örnek Kullanım

### Tüm oyunları listele:
```bash
curl http://localhost:5000/games
```

### ID 1 olan oyunu getir:
```bash
curl http://localhost:5000/games/1
```

## Veri Yapısı

Her oyun aşağıdaki alanları içerir:
- `gameId`: Oyun ID'si
- `name`: Oyun adı
- `subtitle`: Oyun alt başlığı
- `releaseDate`: Yayın tarihi
- `rtp`: RTP oranı
- `rtpWithBonusBuy`: Bonus satın alma ile RTP
- `volatility`: Volatilite seviyesi
- `maxWin`: Maksimum kazanç
- `features`: Oyun özellikleri
- `demoLink`: Demo oyun linki
