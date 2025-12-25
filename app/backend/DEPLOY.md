# Deploy nhanh (MVP)

## 1) Chạy local
```bash
cd app/backend
cp .env.example .env
# điền OPENAI_API_KEY
pip install -r requirements.txt
python app.py
```
Mở: http://localhost:8080

## 2) Đổi chế độ SOFT/SALES
Sửa `.env`:
- `PROFILE_MODE=SOFT` hoặc `PROFILE_MODE=SALES`

## 3) Thay dữ liệu doanh nghiệp
Thay file trong `data_kit/data/`:
- 01_PRODUCTS.csv
- 02_COMBOS.csv
- 03_FAQ.csv
- 04_ROUTING.csv
- 05_META.json
- 10_ALIAS_TAGS.json

## 4) Deploy Render (gợi ý)
- Build command: `pip install -r requirements.txt`
- Start command: `python app.py`
- Env vars: OPENAI_API_KEY, OPENAI_MODEL, PROFILE_MODE, DATA_DIR=../data_kit/data


## Render (từ repo root)
- Build: `pip install -r app/backend/requirements.txt`
- Start: `python app/backend/app.py`
