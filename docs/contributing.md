# Правила разработки

## Окружение

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements-dev.txt
python manage.py migrate
pytest
```

## Ветки

- `main` — стабильная ветка, из неё собираются релизы.
- `feature/<кратко>` — новая функциональность, например `feature/spot-map`.
- `fix/<кратко>` — исправление ошибки.
- `docs/<кратко>` — только документация.

Изменения попадают в `main` через pull request после зелёного CI.

## Коммиты

Используем [Conventional Commits](https://www.conventionalcommits.org/ru/):

```
<тип>(<область>): <что сделано>
```

| Тип | Когда |
|---|---|
| `feat` | новая функциональность |
| `fix` | исправление ошибки |
| `docs` | документация |
| `test` | тесты |
| `refactor` | рефакторинг без изменения поведения |
| `chore` | зависимости, конфигурация, CI |

Примеры: `feat(spots): add map with Leaflet`, `fix(flights): lock predictions after T-0`.

## Перед pull request

- [ ] `pytest` проходит
- [ ] `python manage.py makemigrations --check` не находит новых миграций
- [ ] добавлены тесты на новую логику
- [ ] обновлён раздел `[Unreleased]` в `CHANGELOG.md`

## Версии и релизы

Версии по [SemVer](https://semver.org/lang/ru/) `MAJOR.MINOR.PATCH`:

- **MAJOR** — несовместимые изменения (например, ломающая миграция данных);
- **MINOR** — новая функциональность;
- **PATCH** — исправления.

Как выпустить релиз:

1. Перенести пункты из `[Unreleased]` в новый раздел `[X.Y.Z] - ГГГГ-ММ-ДД` в `CHANGELOG.md`.
2. Обновить `__version__` в `config/__init__.py`.
3. Сделать коммит `chore(release): vX.Y.Z` и создать тег:
   ```bash
   git tag -a vX.Y.Z -m "vX.Y.Z"
   git push origin main --tags
   ```
4. Создать GitHub Release по тегу с текстом из CHANGELOG.
