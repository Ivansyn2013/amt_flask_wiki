До запуска нужно провести миграции\
```flas db upgrade```

Настройки находят в .env и объекте DbConfig подкючаются в app

**app.config.from_envvar(test_config)**
берет конфиги из env файла, но путь к нему нужно передать как переменную среды