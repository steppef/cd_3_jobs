Build и Push в Docker Hub
```
python3 build.py --rollback-commit=<commit> --django-service
python3 build.py --rollback-commit=<commit> --vision-service
python3 build.py --rollback-commit=<commit> --verme-service
```


Deploy
```
# Заполнить credentials.json
python3 deploy.py
```

Rollback
```
# Вначале откатить накатанную миграцию, если она есть: python3 rollback_migration.py
python3 rollback.py
```

Rollback Migration
```
python3 rollback_migration --rollback-migration-app-name=<app_name> rollback-migration-number-before=<number>
```
