# Deploy Render (Chuẩn 100% – không cần set Root Directory)

## Cách 1 (khuyến nghị): Deploy bằng Blueprint `render.yaml`
1) Push repo lên GitHub.
2) Render → New → **Blueprint** → chọn repo.
3) Render tự đọc `render.yaml` và tạo service.

### Env bắt buộc
- OPENAI_API_KEY (secret)

### Tuỳ chọn
- PROFILE_MODE = SALES hoặc SOFT
- OPENAI_MODEL = gpt-4o-mini

## Cách 2: Tạo Web Service thủ công (nhưng vẫn từ repo root)
- Build command: `pip install -r app/backend/requirements.txt`
- Start command: `python app/backend/app.py`
- Env: OPENAI_API_KEY, PROFILE_MODE, OPENAI_MODEL

## Test
- /health
- / (UI demo chat)
