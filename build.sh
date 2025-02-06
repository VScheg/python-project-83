#!/usr/bin/env bash

set -e

curl -LsSf https://astral.sh/uv/install.sh | sh

if [ -f "$HOME/.local/bin/env" ]; then
    echo "🔹 Загружаем переменные окружения..."
    source "$HOME/.local/bin/env"
else
    echo "⚠️  Файл $HOME/.local/bin/env не найден!"
fi

export PATH="$HOME/.local/bin:$PATH"

make install

if ! command -v gunicorn &> /dev/null; then
    echo "⚠️  Gunicorn не найден! Пробуем установить..."
    uv pip install gunicorn
fi