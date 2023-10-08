<details>
<summary>Служебный аккаунт для таблиц</summary>

1. Перейдите [Google Developers Console](https://console.developers.google.com/) и
создайте новый проект (или выберите существующий).

2. В поле "Search for APIs and Services", найдите "Google Drive API" и включите
   его.

3. В поле "Search for APIs and Services", найдите "Google Sheets API" и
   включите его.

4. Перейдите в "APIs & Services > Credentials" и выберите "Create credentials >
   Service account key".

5. Заполните форму и предоставьте роль редактора.

6. Нажмите "Manage service accounts" над Service Accounts.

7. Нажмите ⋮ рядом с недавно созданным служебным аккаунтом, выберите "Manage
   keys" и затем нажмите на "ADD KEY > Create new key".

8. Выберите тип ключа JSON и нажмите "Create".

9. Скопируйте адрес почты аккаунта из скачанного ключа(поле client mail) или из
   вкладки "Service Accounts"

10. В настройках таблицы перейдите в настройки доступа и предоставьте доступ
    аккаунту в качестве редактора

11. Положить скачанный файл в папку с проектом и переименовать его в service_account

</details>

<details>
<summary>Настройки проекта</summary>

Переименуйте файл sample.env в .env и заполните его своими данными

* SPREADSHEET_URL - Ссылка на таблицу(Настройки доступа > Копировать)
* WORKSHEET_NAME - Имя листа с которым будем работать
* DIGISELLER_API_KEY - API ключ, получение через кабинет Digi, присылают на WebMoney


</details>

<details>
<summary>Примеры использования</summary>

```python
table = GoogleSheetsAPI(CREDENTIALS_PATH, SPREADSHEET_URL, WORKSHEET_NAME)
data = [['data1', 'data2'], ['data3', 'data4']]
table.write_data(data)
```


</details>