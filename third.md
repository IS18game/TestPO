<<<<<<< HEAD
Тест-кейс 1:

ID: 011

Название: Проверка правильности комиссии суммы перевода

Описание: Проверить, правильно ли вычисляется комиссия за перевод

Приоритет: Средний

Предусловия: Открыт интерфейс перевода на карту

Шаги:
1	Ввести корректный 16-значный номер                  Ожидаемый результат: Система принимает номер без ошибок
2	Ввести суммы перевода 680₽                          Ожидаемый результат: Система должна показать комиссиию 10% от суммы перевода

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Тест-кейс 2:

ID: 012

Название: Проверка правильности заполнения счета банка

Описание: Проверить, отобразится ли ввод суммы -30000 рублей на счете банка

Приоритет: Высокий

Предусловия: Открыт интерфейс банка

Шаги:

1	Ввести в URL значение -30000                        Ожидаемый результат: Система выдаст ошибку

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Тест-кейс 3:

ID: 013

Название: Проверка перевода евро

Описание: Проверить, правильность отображения перевода евро

Приоритет: Средний

Предусловия: Открыт интерфейс банка

Шаги:

1	Ввести корректный 16-значный номер                  Ожидаемый результат: Система принимает номер без ошибок
2	Ввести суммы перевода 200€                          Ожидаемый результат: Система должна показать комиссиию 10% от суммы перевода
3   Нажать "Перевести"                                  Ожидаемый результат: Система выдаст сообщение с корректным переводом

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Тест-кейс 4:

ID: 014

Название: Проверка введение банковской карты

Описание: Проверить, что при введении банковской карты с 15 и меньше числами, не появится вкладка с переводом

Приоритет: Средний

Предусловия: Открыт интерфейс банка

Шаги:

1	Ввести 15 либо меньше чисел банковской карты                Ожидаемый результат: Система не покажет введение суммы для перевода

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Тест-кейс 5:

ID: 015

Название: Проверка перевода нулевой суммы

Описание: Проверка, корректно ли система реагирует на попытку перевести нулевую сумму

Приоритет: Высокий

Предусловия: Открыт интерфейс перевода

Шаги:

1	Ввести корректный 16-значный номер                  Ожидаемый результат: Система принимает номер без ошибок
=======
Тест-кейс 1:

ID: 011

Название: Проверка правильности комиссии суммы перевода

Описание: Проверить, правильно ли вычисляется комиссия за перевод

Приоритет: Средний

Предусловия: Открыт интерфейс перевода на карту

Шаги:
1	Ввести корректный 16-значный номер                  Ожидаемый результат: Система принимает номер без ошибок
2	Ввести суммы перевода 680₽                          Ожидаемый результат: Система должна показать комиссиию 10% от суммы перевода

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Тест-кейс 2:

ID: 012

Название: Проверка правильности заполнения счета банка

Описание: Проверить, отобразится ли ввод суммы -30000 рублей на счете банка

Приоритет: Высокий

Предусловия: Открыт интерфейс банка

Шаги:

1	Ввести в URL значение -30000                        Ожидаемый результат: Система выдаст ошибку

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Тест-кейс 3:

ID: 013

Название: Проверка перевода евро

Описание: Проверить, правильность отображения перевода евро

Приоритет: Средний

Предусловия: Открыт интерфейс банка

Шаги:

1	Ввести корректный 16-значный номер                  Ожидаемый результат: Система принимает номер без ошибок
2	Ввести суммы перевода 200€                          Ожидаемый результат: Система должна показать комиссиию 10% от суммы перевода
3   Нажать "Перевести"                                  Ожидаемый результат: Система выдаст сообщение с корректным переводом

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Тест-кейс 4:

ID: 014

Название: Проверка введение банковской карты

Описание: Проверить, что при введении банковской карты с 15 и меньше числами, не появится вкладка с переводом

Приоритет: Средний

Предусловия: Открыт интерфейс банка

Шаги:

1	Ввести 15 либо меньше чисел банковской карты                Ожидаемый результат: Система не покажет введение суммы для перевода

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Тест-кейс 5:

ID: 015

Название: Проверка перевода нулевой суммы

Описание: Проверка, корректно ли система реагирует на попытку перевести нулевую сумму

Приоритет: Высокий

Предусловия: Открыт интерфейс перевода

Шаги:

1	Ввести корректный 16-значный номер                  Ожидаемый результат: Система принимает номер без ошибок
>>>>>>> 4427ae98e757cd8a0f94e6b45c56524806d3ad2a
2	Ввести суммы перевода 0                             Ожидаемый результат: Система должна сообщить об ошибке