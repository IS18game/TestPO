<<<<<<< HEAD
Тест-кейс 1:

ID: 016

Название: Проверка правильности пересчета комиссии после смены номера карты

Описание: Проверить, правильно ли система обновляет комиссию при изменении номера карты

Приоритет: Высокий

Предусловия: Открыт интерфейс перевода на карту

Шаги:	Ожидаемый результат
1	Ввести номер карты 2222222222222222                 Ожидаемый результат:	Поле ввода суммы активируется
2	Ввести сумму 2000₽	                                Ожидаемый результат Комиссия отображается как 200₽
3	Изменить номер карты на другой корректный номер	    Ожидаемый результат: Комиссия должна автоматически обновиться (100₽)
4	Проверить сумму комиссии после смены номера	        Ожидаемый результат: Комиссия корректно пересчитывается
----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Тест-кейс 2:

ID: 017

Название: Проверка ошибки "Недостаточно средств" при наличии достаточного баланса

Описание: Проверить, корректно ли система рассчитывает доступные средства при переводе после учета резерва.

Приоритет: Высокий

Предусловия:

Баланс: 30,000₽

Резерв: 20,001₽

Доступная сумма для перевода: 9,999₽

Шаги	Ожидаемый результат
1	Открыть интерфейс ввода банковской карты	Ожидаемый результат: Ожидается корректное отображение текущего интерфейса
2   Ввести корректный 16-значный номер          Ожидаемый результат: Система принимает номер без ошибок
3	Ввести суммы 9,099₽                         Ожидаемый результат: Система принимает ввод

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Тест-кейс 3:

ID: 018

Название: Проверка баланса счета за счет перевода

Описание: Проверка ввода числа не стандартного формата

Приоритет: Средний

Предусловия: На счету 30000р


Шаги:
1	Открыть интерфейс перевода средств	Ожидаемый результат: Ожидается корректное отображение текущего интерфейса
2	Ввести сумму перевода 000012435р	Ожидаемый результат: Успевшный подсчет комиссии и кнопка отправки перевода

-------------------------------------------------------------------------------------------------------------------------------------------------------

Тест-кейс 4:

ID: 019

Название: Проверка отображения уведомления о переводе

Описание: Проверка отображения уведомления о переводе на наличие ошибок в уведомлении

Приоритет: Средний

Предусловия: Перевод 7000₽ с карты 5555555577777777

Шаги:
1	Открыть интерфейс перевода средств	                    Ожидаемый результат: Ожидается корректное отображение текущего интерфейса
2	Ввести номер карты 5555555577777777 и сумму 7000₽	    Ожидаемый результат: Комиссия рассчитывается корректно
3	Нажать "Перевести"	                                    Ожидаемый результат: Операция проходит успешно
4	Проверить уведомление на наличии ошибок в уведомлении   Ожидаемый результат: Перевод 7000₽ на карту 5555555577777777 принят банком!

------------------------------------------------------------------------------------------------------------------------------------------------------------

Тест-кейс 5:

ID: 020

Название: Проверка введение банковской карты

Описание: Проверить, что при введении банковской карты с 13 и меньше числами, не появится вкладка с переводом

Приоритет: Средний

Предусловия: Открыт интерфейс банка

Шаги:

=======
Тест-кейс 1:

ID: 016

Название: Проверка правильности пересчета комиссии после смены номера карты

Описание: Проверить, правильно ли система обновляет комиссию при изменении номера карты

Приоритет: Высокий

Предусловия: Открыт интерфейс перевода на карту

Шаги:	Ожидаемый результат
1	Ввести номер карты 2222222222222222                 Ожидаемый результат:	Поле ввода суммы активируется
2	Ввести сумму 2000₽	                                Ожидаемый результат Комиссия отображается как 200₽
3	Изменить номер карты на другой корректный номер	    Ожидаемый результат: Комиссия должна автоматически обновиться (100₽)
4	Проверить сумму комиссии после смены номера	        Ожидаемый результат: Комиссия корректно пересчитывается
----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Тест-кейс 2:

ID: 017

Название: Проверка ошибки "Недостаточно средств" при наличии достаточного баланса

Описание: Проверить, корректно ли система рассчитывает доступные средства при переводе после учета резерва.

Приоритет: Высокий

Предусловия:

Баланс: 30,000₽

Резерв: 20,001₽

Доступная сумма для перевода: 9,999₽

Шаги	Ожидаемый результат
1	Открыть интерфейс ввода банковской карты	Ожидаемый результат: Ожидается корректное отображение текущего интерфейса
2   Ввести корректный 16-значный номер          Ожидаемый результат: Система принимает номер без ошибок
3	Ввести суммы 9,099₽                         Ожидаемый результат: Система принимает ввод

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Тест-кейс 3:

ID: 018

Название: Проверка баланса счета за счет перевода

Описание: Проверка ввода числа не стандартного формата

Приоритет: Средний

Предусловия: На счету 30000р


Шаги:
1	Открыть интерфейс перевода средств	Ожидаемый результат: Ожидается корректное отображение текущего интерфейса
2	Ввести сумму перевода 000012435р	Ожидаемый результат: Успевшный подсчет комиссии и кнопка отправки перевода

-------------------------------------------------------------------------------------------------------------------------------------------------------

Тест-кейс 4:

ID: 019

Название: Проверка отображения уведомления о переводе

Описание: Проверка отображения уведомления о переводе на наличие ошибок в уведомлении

Приоритет: Средний

Предусловия: Перевод 7000₽ с карты 5555555577777777

Шаги:
1	Открыть интерфейс перевода средств	                    Ожидаемый результат: Ожидается корректное отображение текущего интерфейса
2	Ввести номер карты 5555555577777777 и сумму 7000₽	    Ожидаемый результат: Комиссия рассчитывается корректно
3	Нажать "Перевести"	                                    Ожидаемый результат: Операция проходит успешно
4	Проверить уведомление на наличии ошибок в уведомлении   Ожидаемый результат: Перевод 7000₽ на карту 5555555577777777 принят банком!

------------------------------------------------------------------------------------------------------------------------------------------------------------

Тест-кейс 5:

ID: 020

Название: Проверка введение банковской карты

Описание: Проверить, что при введении банковской карты с 13 и меньше числами, не появится вкладка с переводом

Приоритет: Средний

Предусловия: Открыт интерфейс банка

Шаги:

>>>>>>> 4427ae98e757cd8a0f94e6b45c56524806d3ad2a
1	Ввести 13 либо меньше чисел банковской карты                Ожидаемый результат: Система не покажет введение суммы для перевода