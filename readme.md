# Проект по биоинформатика

Започнат на 10/12/2020

## Резултати
|геном|съвпадения|
|-|-|
|свински (Sus Scrofa) chr 1|900|
|свински (Sus Scrofa) chr 2|559|
|свински (Sus Scrofa) chr 3|553|
|пилешки (Gallus Gallus) chr 1|6
|агнешки (Ovis Aries) chr 1|12093
|конски (Equus caballus) chr 1|105 

## Задача
* Да се вземе геномен файл оттук: https://www.ncbi.nlm.nih.gov/genome/?term=swine
* Да се прочетат в някакъв удобен вид
* Да се видят поредиците от `SausageTest.fasta` колко често присъстват във всеки геномен файл

## Функции
1. **bio_main.py** - извиква всички останали функции, указва геномния файл и файла проба. Дава възможност за начало на търсенето.
2. **read_sausage.py** - отваря файла проба и вкарва в паметта всички секвенции от него.
   <br>Игнорира секвенции, съдържащи неуспешно прочетени бази (N).
3. **organize_sausage.py** - разделя получените секвенции от файла проба в 4 масива в паметта, според първата им база.
4. **split_genome.py** - разделя геномния файл на няколко части, броят им се задава от потребителя.
5. **compare_genome.py** - отваря геномен файл и сравнява намерена секвенция със секвенции от файла проба (SausageTest.fasta).
   <br>Запаметява данните от търсенето (съвпадения, позиция в геномния файл и т.н.) на всеки 2млн (по подразбиране) проверени прозореца.
   <br>При неочаквано прекъсване, търсенето може да продължи от последната запаметена позиция.
   <br>След приключване на търсенето, създава файл с резюме на получените резултати.
    

## Проблеми
1. **split_genome.py** - при делене на геномния файл на части, няколкото прозореца в края на всяка част се губят.
   <br>Тези загуби са практически пренебрежими, поради огромното количество прозорци в генома.
2. **compare_genome.py** - при четене на геномния файл и връщането на указателя назад из файла, е възможно да се стигне до неколкократно прочитане на един и същи прозорец.
   <br>Програмата прави проверка за повторение и така грешно полученият прозорец не се използва. Този проблем не влияе на крайните резултати от търсенето.
