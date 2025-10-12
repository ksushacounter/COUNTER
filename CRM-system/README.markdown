# CRM-System

## Описание проекта

Эта CRM-система предназначена для управления информацией о продавцах и их транзакциях. Система позволяет создавать, читать, обновлять и удалять данные о продавцах и транзакциях, а также предоставляет функции аналитики для обработки данных. Проект реализован на языке Java с использованием фреймворка Spring Boot. База данных — PostgreSQL (с возможностью использования H2 для тестирования). 

Система придерживается принципов сохранения историчности данных: вместо физического удаления сущностей они помечаются как удаленные с указанием даты удаления.

## Архитектура проекта

Проект структурирован в соответствии с принципами ООП и разделения ответственности:
- **controllers**: Обработка HTTP-запросов и взаимодействие с сервисами.
- **services**: Бизнес-логика приложения.
- **repositories**: Взаимодействие с базой данных через Spring Data JPA.
- **entities**: Описание моделей данных (Seller, Transaction).
- **dto**: Объекты передачи данных (например, Period для аналитики).
- **exception**: Кастомные исключения и централизованная обработка ошибок.

Используются паттерны проектирования, такие как Repository и Service Layer, для обеспечения модульности и поддерживаемости кода.

## Функциональность

### Сущности
- **Продавец (Seller)**:
  - ID (автоинкремент).
  - Имя (строка, не пустая).
  - Контактные данные (строка, не пустая).
  - Дата регистрации (LocalDateTime, в прошлом или настоящем).
- **Транзакция (Transaction)**:
  - ID (автоинкремент).
  - Ссылка на продавца (внешний ключ).
  - Сумма (десятичное число, положительное).
  - Тип оплаты (CASH, CARD, TRANSFER).
  - Дата транзакции (LocalDateTime, в прошлом или настоящем).

### REST API
- **Продавцы**:
  - Получить список всех активных продавцов: `GET /api/sellers`
  - Получить информацию о продавце по ID: `GET /api/sellers/{id}`
  - Создать нового продавца: `POST /api/sellers`
  - Обновить информацию о продавце: `PUT /api/sellers/{id}`
  - Удалить продавца (логическое удаление): `DELETE /api/sellers/{id}`
- **Транзакции**:
  - Получить список всех активных транзакций: `GET /api/transactions`
  - Получить информацию о транзакции по ID: `GET /api/transactions/{id}`
  - Создать новую транзакцию: `POST /api/transactions`
  - Получить все транзакции продавца: `GET /api/transactions/seller/{sellerId}`
- **Аналитика**:
  - Получить самого продуктивного продавца за период (по сумме транзакций): `GET /api/transactions/most-productive?start={start}&end={end}`
  - Получить список продавцов с суммой транзакций меньше указанной за период: `GET /api/transactions/less-than-amount?amount={amount}&start={start}&end={end}`
  - Получить наилучший период для продавца (максимальное количество транзакций): `GET /api/transactions/best-period?sellerId={sellerId}`

### Обработка ошибок
- Централизованная обработка ошибок с возвратом HTTP-кодов и сообщений (например, 404 для не найденных сущностей, 400 для валидационных ошибок).

## Необходимые зависимости

Проект использует Gradle для управления зависимостями. Основные зависимости (из `build.gradle`):
- `org.springframework.boot:spring-boot-starter-web`
- `org.springframework.boot:spring-boot-starter-data-jpa`
- `org.springframework.boot:spring-boot-starter-validation`
- `org.postgresql:postgresql:42.7.3`
- `com.h2database:h2:2.3.230` (runtime only, для тестирования)
- `org.springframework.boot:spring-boot-starter-test` (для тестирования)
- `org.springframework.boot:spring-boot-devtools`

### Требования
- Java 23
- PostgreSQL (локально или в Docker)
- Gradle

## Установка и настройка окружения

1. **Установка Java**:
   - Установите Java 23: `sudo apt install openjdk-23-jdk` (Linux) или используйте SDKMAN (`sdk install java 23-open`).
2. **Установка PostgreSQL**:
   - Установите PostgreSQL: `sudo apt install postgresql postgresql-contrib` (Linux).
   - Создайте базу данных:
     ```bash
     psql -U postgres -c "CREATE DATABASE crm_system;"
     ```
   - Убедитесь, что пользователь `postgres` имеет пароль `ksusha` (или измените в `application.properties`).
3. **Установка Gradle**:
   - Используйте Gradle Wrapper (`./gradlew`) или установите Gradle: `sdk install gradle`.
4. **Настройка IDE**:
   - Импортируйте проект в IntelliJ IDEA или VS Code, указав Gradle как сборщик.
   - Убедитесь, что JDK 23 настроен в IDE.

### Настройка базы данных
Настройте файл `src/main/resources/application.properties`:
```
spring.datasource.url=jdbc:postgresql://localhost:5432/crm_system
spring.datasource.username=postgres
spring.datasource.password=ksusha
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
```
Для тестирования с H2 (in-memory):
```
spring.datasource.url=jdbc:h2:mem:testdb
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.hibernate.ddl-auto=create-drop
```

### PostgreSQL в Docker
Для запуска PostgreSQL в Docker:
```bash
docker run -d --name postgres-crm -p 5432:5432 -e POSTGRES_DB=crm_system -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=ksusha postgres:latest
```

## Сборка и запуск

### Сборка
В корне проекта выполните:
```bash
./gradlew build
```
Создастся JAR-файл в `build/libs`.

### Запуск
Запустите приложение:
```bash
./gradlew bootRun
```
Или через IDE, запустив `CrmSystemApplication`. Приложение доступно на `http://localhost:8080`.

## Тестирование

Проект включает юнит- и интеграционные тесты, покрывающие минимум 50% критической логики. Используются JUnit и Spring Boot Test, с H2 для in-memory базы данных.

### Запуск тестов
```bash
./gradlew test
```
Отчеты доступны в `build/reports/tests/test`.

### Покрытие тестами
- **SellerService**: Тесты создания, получения, обновления, удаления продавцов и обработки исключений.
- **TransactionService**: Проверяются создание транзакций, аналитические методы и обработка ошибок.
- **Контроллеры**: Тестируются REST API с помощью `@WebMvcTest`.
- **Репозитории**: Проверяются запросы к базе данных с `@DataJpaTest`.
- Для анализа покрытия используйте JaCoCo:
  ```bash
  ./gradlew test jacocoTestReport
  ```
  Отчет о покрытии: `build/reports/jacoco/test/html/index.html`.

### Пример теста
Тест для `SellerService`:
```java
@Test
void testCreateNewSeller() {
    Seller seller = new Seller("Иван Иванов", "ivan@example.com", LocalDateTime.now());
    when(sellerRepository.save(any(Seller.class))).thenReturn(seller);
    Seller created = sellerService.createNewSeller(seller);
    assertEquals("Иван Иванов", created.getName());
    assertFalse(created.isDeleted());
}
```

### Тестирование API
Используйте Postman или `curl` для проверки API. Тесты покрывают:
- Корректность HTTP-ответов (200, 404, 400).
- Валидацию данных.
- Обработку ошибок.

## Примеры использования API

Базовый URL: `http://localhost:8080/api`. Даты в формате ISO (`yyyy-MM-dd'T'HH:mm:ss`).

### Продавцы
- **Получить всех продавцов**:
  ```bash
  curl -X GET http://localhost:8080/api/sellers
  ```
  **Пример ответа**:
  ```json
  [
    {
      "id": 1,
      "name": "Иван Иванов",
      "contactInfo": "ivan@example.com",
      "registrationDate": "2023-01-01T10:00:00",
      "deleted": false
    }
  ]
  ```

- **Создать продавца**:
  ```bash
  curl -X POST http://localhost:8080/api/sellers \
  -H "Content-Type: application/json" \
  -d '{"name": "Иван Иванов", "contactInfo": "ivan@example.com", "registrationDate": "2023-01-01T10:00:00"}'
  ```

### Транзакции
- **Создать транзакцию**:
  ```bash
  curl -X POST http://localhost:8080/api/transactions \
  -H "Content-Type: application/json" \
  -d '{"seller": {"id": 1}, "amount": 100.0, "paymentType": "CASH", "transactionDate": "2023-02-01T12:00:00"}'
  ```
  **Пример ответа**:
  ```json
  {
    "id": 1,
    "seller": {"id": 1},
    "amount": 100.0,
    "paymentType": "CASH",
    "transactionDate": "2023-02-01T12:00:00",
    "deleted": false
  }
  ```

### Аналитика
- **Самый продуктивный продавец**:
  ```bash
  curl -X GET "http://localhost:8080/api/transactions/most-productive?start=2023-01-01T00:00:00&end=2023-12-31T23:59:59"
  ```
  **Пример ответа**:
  ```json
  {
    "id": 1,
    "name": "Иван Иванов",
    "contactInfo": "ivan@example.com",
    "registrationDate": "2023-01-01T10:00:00",
    "deleted": false
  }
  ```

## Ограничения и известные проблемы
- Алгоритм `findBestPeriod` имеет сложность O(n²) и может быть медленным для больших объемов транзакций.
- Отсутствует кэширование для аналитических запросов, что может повлиять на производительность.

## Контрибьютинг
1. Форкните репозиторий.
2. Создайте ветку для изменений: `git checkout -b feature/описание`.
3. Следуйте стилю кода (CamelCase, понятные имена).
4. Добавьте тесты для новых функций.
5. Отправьте pull request с описанием изменений.

## Лицензия
Проект распространяется под лицензией MIT (или укажите другую, если требуется).

## Контакты
Для вопросов или сообщений об ошибках: [email@example.com](mailto:email@example.com) или создайте issue в репозитории.