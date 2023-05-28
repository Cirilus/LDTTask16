# Решения 16 трека ЛЦТ
Интерактивная платформа-сообщество для стажеров и участников молодежных карьерных проектов

## Features

- Интеграция с SSO (keycloak)
- Подключение S3 хранилище (minio)
- Управление доступом на основе ролей
- Конструктор тестов для вакансий
- Использование CI/CD

## Documentation
Мы реализовывали архитектуру цитадель, поскольку считаем, что она идеально подходит для данной задачи, так как данный сервис не предполагает большого количества RPS (запросов в секунду), но все равно могут быть какие-то узкие горлышки. Например, сервис аутентификации и данная архитектура позволяет быстро и легко разрабатывать приложения, но также не забывать о горизонтальном масштабировании

- Authentication - сервис аутентификации. Имеется 4 роли:
    - Mentor - наставник
    - Curator - куратор
    - Company - Кадры
    - Trainee - кандидаты и стажеры
- Company - основная бизнес-логика приложения, которая реализует взаимодействие между вакансией и пользователем
- Test - сервис, реализующий логику конструктора тестов
- Notifications - это микросервис на FastAPI, реализующий логику уведомлений

## Plans
- Интегрировать уведомления в чат-бота telegram
- Интегрироваться с различными сторонними базами данных для того, чтобы автоматизировать большую часть ручной работы. Например, получить доступ к базам данных университетов, для того чтобы получать подтверждение обучения пользователя в данном университете
- Расширение обрабатываемой и собираемой статистики.
- Разработка Telegram Web решения.
