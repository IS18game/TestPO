
### Локальный запуск

1. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

2. **Запустите веб-сервер:**
```bash
python -m http.server 8000
```

3. **Запустите тесты:**
```bash
pytest -v
```

### Запуск с подробным выводом
```bash
pytest -v -s