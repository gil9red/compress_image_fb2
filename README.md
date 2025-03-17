# compress_image_fb2
Скрипт для сжатия изображений в файле FB2.

## Аргументы

``` commandline
> python compress_image_fb2.py --help 
Usage: compress_image_fb2.py [OPTIONS] FB2_FILE_NAME

  Функция сжимает изображения в файле FB2 и сохраняет копию с сжатыми
  картинками в папке с скриптом.

Options:
  --output_dir PATH               Папка для вывода сжатого файла. Если не
                                  указывать, то используется папка файла FB2
  --pattern_output_file_name TEXT
                                  Шаблон имени сжатого FB2  [default:
                                  {path.stem}_compress{path.suffix}]
  --used_strategies [StrategyCompressImage1|StrategyCompressImage2|StrategyCompressImage3]
                                  Используемые стратегии сжатия картинок
  --max_width INTEGER             Максимальная ширина картинки. Если больше,
                                  то будет уменьшена с сохранением пропорций
  --max_height INTEGER            Максимальная высота картинки. Если больше,
                                  то будет уменьшена с сохранением пропорций
  --is_extract_images BOOLEAN     Вывод оригинальных и сжатых изображений в
                                  папку по имени файла  [default: False]
  --is_log BOOLEAN                Вывод информации по сжатию файла  [default:
                                  True]
  --is_log_diff_equals BOOLEAN    Вывод неизмененных полей картинки после
                                  сжатия  [default: True]
  --help                          Show this message and exit.
```

## Без опций
``` commandline
> python compress_image_fb2.py examples/mknr_1.fb2 
examples\mknr_1.fb2:
    1. MKnR_v01_a.png. Сжатие: 86.92%
        Использованные стратегии (3):
            StrategyCompressImage1: -2.06%
            StrategyCompressImage2: 63.47%
            StrategyCompressImage3: 86.92%
            MAX (StrategyCompressImage3): 86.92%
        PNG -> JPEG
        RGB = RGB
        1.0 MB -> 134.8 KB
        693x1024 = 693x1024

    2. MKnR_v01_09.png. Сжатие: 68.85%
        Использованные стратегии (3):
            StrategyCompressImage1: -2.43%
            StrategyCompressImage2: -23.12%
            StrategyCompressImage3: 68.85%
            MAX (StrategyCompressImage3): 68.85%
        PNG -> JPEG
        L = L
        622.6 KB -> 194.0 KB
        1187x1754 = 1187x1754

    3. MKnR_v01_10.png. Сжатие: 76.81%
        Использованные стратегии (3):
            StrategyCompressImage1: -3.42%
            StrategyCompressImage2: -34.50%
            StrategyCompressImage3: 76.81%
            MAX (StrategyCompressImage3): 76.81%
        PNG -> JPEG
        L = L
        665.4 KB -> 154.3 KB
        1173x1759 = 1173x1759

    4. MKnR_v01_11.png. Сжатие: 77.82%
        Использованные стратегии (3):
            StrategyCompressImage1: -3.20%
            StrategyCompressImage2: -32.87%
            StrategyCompressImage3: 77.82%
            MAX (StrategyCompressImage3): 77.82%
        PNG -> JPEG
        L = L
        706.2 KB -> 156.7 KB
        1178x1754 = 1178x1754

    5. MKnR_v01_12.png. Сжатие: 84.26%
        Использованные стратегии (3):
            StrategyCompressImage1: -4.52%
            StrategyCompressImage2: -37.56%
            StrategyCompressImage3: 84.26%
            MAX (StrategyCompressImage3): 84.26%
        PNG -> JPEG
        L = L
        824.9 KB -> 129.8 KB
        1172x1747 = 1172x1747

    6. MKnR_v01_13.png. Сжатие: 77.02%
        Использованные стратегии (3):
            StrategyCompressImage1: -3.50%
            StrategyCompressImage2: -35.73%
            StrategyCompressImage3: 77.02%
            MAX (StrategyCompressImage3): 77.02%
        PNG -> JPEG
        L = L
        793.7 KB -> 182.4 KB
        1199x1762 = 1199x1762

    7. MKnR_v01_14.png. Сжатие: 72.08%
        Использованные стратегии (3):
            StrategyCompressImage1: -2.72%
            StrategyCompressImage2: -26.23%
            StrategyCompressImage3: 72.08%
            MAX (StrategyCompressImage3): 72.08%
        PNG -> JPEG
        L = L
        737.3 KB -> 205.8 KB
        1175x1767 = 1175x1767

    8. MKnR_v01_15.png. Сжатие: 70.82%
        Использованные стратегии (3):
            StrategyCompressImage1: -2.77%
            StrategyCompressImage2: -26.57%
            StrategyCompressImage3: 70.82%
            MAX (StrategyCompressImage3): 70.82%
        PNG -> JPEG
        L = L
        591.4 KB -> 172.6 KB
        1195x1766 = 1195x1766

    9. MKnR_v01_16.png. Сжатие: 74.57%
        Использованные стратегии (3):
            StrategyCompressImage1: -2.96%
            StrategyCompressImage2: -22.24%
            StrategyCompressImage3: 74.57%
            MAX (StrategyCompressImage3): 74.57%
        PNG -> JPEG
        L = L
        824.8 KB -> 209.8 KB
        1195x1766 = 1195x1766

    10. MKnR_v01_17.png. Сжатие: 80.46%
        Использованные стратегии (3):
            StrategyCompressImage1: -6.78%
            StrategyCompressImage2: -29.34%
            StrategyCompressImage3: 80.46%
            MAX (StrategyCompressImage3): 80.46%
        PNG -> JPEG
        L = L
        624.4 KB -> 122.0 KB
        1166x1759 = 1166x1759

    11. MKnR_v01_18.png. Сжатие: 79.65%
        Использованные стратегии (3):
            StrategyCompressImage1: -2.48%
            StrategyCompressImage2: -41.96%
            StrategyCompressImage3: 79.65%
            MAX (StrategyCompressImage3): 79.65%
        PNG -> JPEG
        L = L
        770.2 KB -> 156.7 KB
        1172x1763 = 1172x1763


Оригинальный размер FB2: 11.2 MB
Общий размер картинок: 10.7 MB (94.94%)
Остальное: 582.1 KB (5.06%)

FB2 с сжатием: 2.9 MB (сжатие 74.07%)
Общий размер картинок: 2.4 MB (81.30%, сжатие 77.80%)
Остальное: 557.8 KB (18.70%, сжатие 4.17%)

Сжатый FB2 сохранен в: C:\Users\ipetrash\PycharmProjects\compress image fb2\examples\mknr_1_compress.fb2 

Завершено за 8.012 сек.
```

## Изменение папки выгрузки
``` commandline
> python compress_image_fb2.py --output_dir="C:/Users/ipetrash/PycharmProjects/compress image fb2/output/2025-03-17" examples/mknr_1.fb2 
examples\mknr_1.fb2:
    1. MKnR_v01_a.png. Сжатие: 86.92%
        Использованные стратегии (3):
            StrategyCompressImage1: -2.06%
            StrategyCompressImage2: 63.47%
            StrategyCompressImage3: 86.92%
            MAX (StrategyCompressImage3): 86.92%
        PNG -> JPEG
        RGB = RGB
        1.0 MB -> 134.8 KB
        693x1024 = 693x1024
    
    ...
    
    11. MKnR_v01_18.png. Сжатие: 79.65%
        Использованные стратегии (3):
            StrategyCompressImage1: -2.48%
            StrategyCompressImage2: -41.96%
            StrategyCompressImage3: 79.65%
            MAX (StrategyCompressImage3): 79.65%
        PNG -> JPEG
        L = L
        770.2 KB -> 156.7 KB
        1172x1763 = 1172x1763


Оригинальный размер FB2: 11.2 MB
Общий размер картинок: 10.7 MB (94.94%)
Остальное: 582.1 KB (5.06%)

FB2 с сжатием: 2.9 MB (сжатие 74.07%)
Общий размер картинок: 2.4 MB (81.30%, сжатие 77.80%)
Остальное: 557.8 KB (18.70%, сжатие 4.17%)

Сжатый FB2 сохранен в: C:\Users\ipetrash\PycharmProjects\compress image fb2\output\2025-03-17\mknr_1_compress.fb2 

Завершено за 8.216 сек.
```

## Выгрузка картинок
``` commandline
> python compress_image_fb2.py --is_extract_images=true examples/mknr_1.fb2 
examples\mknr_1.fb2:
    1. MKnR_v01_a.png. Сжатие: 86.92%
        Использованные стратегии (3):
            StrategyCompressImage1: -2.06%
            StrategyCompressImage2: 63.47%
            StrategyCompressImage3: 86.92%
            MAX (StrategyCompressImage3): 86.92%
        PNG -> JPEG
        RGB = RGB
        1.0 MB -> 134.8 KB
        693x1024 = 693x1024
        Сохранение оригинала в: C:\Users\ipetrash\PycharmProjects\compress image fb2\examples\mknr_1.fb2-images\MKnR_v01_a.png
        Сохранение сжатой в: C:\Users\ipetrash\PycharmProjects\compress image fb2\examples\mknr_1.fb2-images\MKnR_v01_a_compressed.jpg
    
    ...
    
    11. MKnR_v01_18.png. Сжатие: 79.65%
        Использованные стратегии (3):
            StrategyCompressImage1: -2.48%
            StrategyCompressImage2: -41.96%
            StrategyCompressImage3: 79.65%
            MAX (StrategyCompressImage3): 79.65%
        PNG -> JPEG
        L = L
        770.2 KB -> 156.7 KB
        1172x1763 = 1172x1763
        Сохранение оригинала в: C:\Users\ipetrash\PycharmProjects\compress image fb2\examples\mknr_1.fb2-images\MKnR_v01_18.png
        Сохранение сжатой в: C:\Users\ipetrash\PycharmProjects\compress image fb2\examples\mknr_1.fb2-images\MKnR_v01_18_compressed.jpg


Оригинальный размер FB2: 11.2 MB
Общий размер картинок: 10.7 MB (94.94%)
Остальное: 582.1 KB (5.06%)

FB2 с сжатием: 2.9 MB (сжатие 74.07%)
Общий размер картинок: 2.4 MB (81.30%, сжатие 77.80%)
Остальное: 557.8 KB (18.70%, сжатие 4.17%)

Сжатый FB2 сохранен в: C:\Users\ipetrash\PycharmProjects\compress image fb2\examples\mknr_1_compress.fb2 

Завершено за 8.201 сек.
```

### Изменение папки выгрузки
``` commandline
> python compress_image_fb2.py --is_extract_images=true "--output_dir=C:/Users/ipetrash/PycharmProjects/compress image fb2/output/2025-03-17" examples/mknr_1.fb2 
examples\mknr_1.fb2:
    1. MKnR_v01_a.png. Сжатие: 86.92%
        Использованные стратегии (3):
            StrategyCompressImage1: -2.06%
            StrategyCompressImage2: 63.47%
            StrategyCompressImage3: 86.92%
            MAX (StrategyCompressImage3): 86.92%
        PNG -> JPEG
        RGB = RGB
        1.0 MB -> 134.8 KB
        693x1024 = 693x1024
        Сохранение оригинала в: C:\Users\ipetrash\PycharmProjects\compress image fb2\output\2025-03-17\mknr_1.fb2-images\MKnR_v01_a.png
        Сохранение сжатой в: C:\Users\ipetrash\PycharmProjects\compress image fb2\output\2025-03-17\mknr_1.fb2-images\MKnR_v01_a_compressed.jpg
    
    ...
    
    11. MKnR_v01_18.png. Сжатие: 79.65%
        Использованные стратегии (3):
            StrategyCompressImage1: -2.48%
            StrategyCompressImage2: -41.96%
            StrategyCompressImage3: 79.65%
            MAX (StrategyCompressImage3): 79.65%
        PNG -> JPEG
        L = L
        770.2 KB -> 156.7 KB
        1172x1763 = 1172x1763
        Сохранение оригинала в: C:\Users\ipetrash\PycharmProjects\compress image fb2\output\2025-03-17\mknr_1.fb2-images\MKnR_v01_18.png
        Сохранение сжатой в: C:\Users\ipetrash\PycharmProjects\compress image fb2\output\2025-03-17\mknr_1.fb2-images\MKnR_v01_18_compressed.jpg


Оригинальный размер FB2: 11.2 MB
Общий размер картинок: 10.7 MB (94.94%)
Остальное: 582.1 KB (5.06%)

FB2 с сжатием: 2.9 MB (сжатие 74.07%)
Общий размер картинок: 2.4 MB (81.30%, сжатие 77.80%)
Остальное: 557.8 KB (18.70%, сжатие 4.17%)

Сжатый FB2 сохранен в: C:\Users\ipetrash\PycharmProjects\compress image fb2\output\2025-03-17\mknr_1_compress.fb2 

Завершено за 8.117 сек.
```

## Изменение размера картинок
### Максимальная ширина
``` commandline
> python compress_image_fb2.py --max_width=600 examples/mknr_1.fb2 
examples\mknr_1.fb2:
    1. MKnR_v01_a.png. Сжатие: 89.72%
        Использованные стратегии (3):
            StrategyCompressImage1: -2.06%
            StrategyCompressImage2: 63.47%
            StrategyCompressImage3: 86.92%
            MAX (StrategyCompressImage3): 86.92%
        PNG -> JPEG
        RGB = RGB
        1.0 MB -> 105.9 KB
        693x1024 -> 600x886
    
    ...
    
    11. MKnR_v01_18.png. Сжатие: 91.75%
        Использованные стратегии (3):
            StrategyCompressImage1: -2.48%
            StrategyCompressImage2: -41.96%
            StrategyCompressImage3: 79.65%
            MAX (StrategyCompressImage3): 79.65%
        PNG -> JPEG
        L = L
        770.2 KB -> 63.5 KB
        1172x1763 -> 600x902


Оригинальный размер FB2: 11.2 MB
Общий размер картинок: 10.7 MB (94.94%)
Остальное: 582.1 KB (5.06%)

FB2 с сжатием: 1.6 MB (сжатие 86.07%)
Общий размер картинок: 1.0 MB (65.19%, сжатие 90.43%)
Остальное: 557.8 KB (34.81%, сжатие 4.17%)

Сжатый FB2 сохранен в: C:\Users\ipetrash\PycharmProjects\compress image fb2\examples\mknr_1_compress.fb2 

Завершено за 8.341 сек.
```

### Максимальная высота
``` commandline
> python compress_image_fb2.py --max_height=600 examples/mknr_1.fb2 
examples\mknr_1.fb2:
    1. MKnR_v01_a.png. Сжатие: 94.50%
        Использованные стратегии (3):
            StrategyCompressImage1: -2.06%
            StrategyCompressImage2: 63.47%
            StrategyCompressImage3: 86.92%
            MAX (StrategyCompressImage3): 86.92%
        PNG -> JPEG
        RGB = RGB
        1.0 MB -> 56.7 KB
        693x1024 -> 406x600
    
    ...

    11. MKnR_v01_18.png. Сжатие: 95.33%
        Использованные стратегии (3):
            StrategyCompressImage1: -2.48%
            StrategyCompressImage2: -41.96%
            StrategyCompressImage3: 79.65%
            MAX (StrategyCompressImage3): 79.65%
        PNG -> JPEG
        L = L
        770.2 KB -> 36.0 KB
        1172x1763 -> 398x600


Оригинальный размер FB2: 11.2 MB
Общий размер картинок: 10.7 MB (94.94%)
Остальное: 582.1 KB (5.06%)

FB2 с сжатием: 1.1 MB (сжатие 90.05%)
Общий размер картинок: 586.9 KB (51.27%, сжатие 94.63%)
Остальное: 557.8 KB (48.73%, сжатие 4.17%)

Сжатый FB2 сохранен в: C:\Users\ipetrash\PycharmProjects\compress image fb2\examples\mknr_1_compress.fb2 

Завершено за 8.024 сек.
```

## Изменение используемых стратегий сжатия картинок
### Одна стратегия
``` commandline
> python compress_image_fb2.py --used_strategies=StrategyCompressImage2 examples/mknr_1.fb2 
examples\mknr_1.fb2:
    1. MKnR_v01_a.png. Сжатие: 63.47%
        Использованные стратегии (1):
            StrategyCompressImage2: 63.47%
            MAX (StrategyCompressImage2): 63.47%
        PNG = PNG
        RGB -> P
        1.0 MB -> 376.3 KB
        693x1024 = 693x1024
    
    ...
    
    11. MKnR_v01_18.png. Сжатие: -41.96% - Пропущено
        Использованные стратегии (1):
            StrategyCompressImage2: -41.96%
            MAX (StrategyCompressImage2): -41.96%
        PNG = PNG
        L -> P
        770.2 KB -> 1.1 MB
        1172x1763 = 1172x1763


Оригинальный размер FB2: 11.2 MB
Общий размер картинок: 10.7 MB (94.94%)
Остальное: 582.1 KB (5.06%)

FB2 с сжатием: 10.4 MB (сжатие 7.79%)
Общий размер картинок: 9.8 MB (94.74%, сжатие 7.98%)
Остальное: 557.8 KB (5.26%, сжатие 4.17%)

Сжатый FB2 сохранен в: C:\Users\ipetrash\PycharmProjects\compress image fb2\examples\mknr_1_compress.fb2 

Завершено за 7.120 сек.
```

### Несколько стратегий
``` commandline
> python compress_image_fb2.py --used_strategies=StrategyCompressImage1 --used_strategies=StrategyCompressImage3 examples/mknr_1.fb2 
examples\mknr_1.fb2:
    1. MKnR_v01_a.png. Сжатие: 86.92%
        Использованные стратегии (2):
            StrategyCompressImage1: -2.06%
            StrategyCompressImage3: 86.92%
            MAX (StrategyCompressImage3): 86.92%
        PNG -> JPEG
        RGB = RGB
        1.0 MB -> 134.8 KB
        693x1024 = 693x1024
    
    ...

    11. MKnR_v01_18.png. Сжатие: 79.65%
        Использованные стратегии (2):
            StrategyCompressImage1: -2.48%
            StrategyCompressImage3: 79.65%
            MAX (StrategyCompressImage3): 79.65%
        PNG -> JPEG
        L = L
        770.2 KB -> 156.7 KB
        1172x1763 = 1172x1763


Оригинальный размер FB2: 11.2 MB
Общий размер картинок: 10.7 MB (94.94%)
Остальное: 582.1 KB (5.06%)

FB2 с сжатием: 2.9 MB (сжатие 74.07%)
Общий размер картинок: 2.4 MB (81.30%, сжатие 77.80%)
Остальное: 557.8 KB (18.70%, сжатие 4.17%)

Сжатый FB2 сохранен в: C:\Users\ipetrash\PycharmProjects\compress image fb2\examples\mknr_1_compress.fb2 

Завершено за 1.060 сек.
```
