#!/usr/bin/env bash
set -e

echo "🔹 Устанавливаем uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh

echo "🔹 Добавляем $HOME/.local/bin в PATH..."
export PATH="$HOME/.local/bin:$PATH"

echo "🔹 Проверяем путь к gunicorn..."
which gunicorn || echo "⚠️ gunicorn не найден в PATH"

echo "🔹 Устанавливаем зависимости..."
make install

echo "✅ Сборка завершена!"