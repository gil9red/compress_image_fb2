#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

"""Скрипт сжимает картинки в файле fb2."""

import os
import base64
import io
from lxml import etree
from PIL import Image
from imagequant import quantize_pil_image as quantize_image # Исправленный импорт для Федоры
# В остльных случаях quantize_pil_image as не нужен Наверное

def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def compress_image_fb2(fb2_file_name, is_resize_image=True, is_convert_to_jpeg=False, use_percent=False, percent=False,
                       set_width=None, set_height=None):
    """Функция сжимает изображения в файле FB2 и сохраняет копию с сжатыми картинками в папке с скриптом,
    добавляя в начало имени файла строку "compress_".

    :param fb2_file_name: Путь к файлу fb2
    :param is_resize_image: Если True, менять размер изображения
    :param is_convert_to_jpeg: Конвертирование изображений в jpeg, который более легкий, чем png
    :param use_percent: Использовать процентное изменение размера
    :param percent: На сколько процентов изменить размер
    :param set_width: Установка ширины изображения (Используется если:
    is_resize_image == True and use_percent == False)
    :param set_height: Установка высоты изображения (Используется если:
    is_resize_image == True and use_percent == False)

    """

    total_image_size = 0
    compress_total_image_size = 0
    
    print(fb2_file_name + ':')

    fb2 = open(fb2_file_name, encoding='utf8')
    xml_fb2 = etree.XML(fb2.read().encode())

    binaries = xml_fb2.xpath("//*[local-name()='binary']")
    for i, binary in enumerate(binaries, 1):
        try:
            content_type = binary.attrib['content-type']
            short_content_type = content_type.split('/')[-1]

            im_id = binary.attrib['id']
            im_data = base64.b64decode(binary.text.encode())
            compress_im_data = im_data

            im = Image.open(io.BytesIO(im_data))
            count_bytes = len(im_data)
            total_image_size += count_bytes

            diff_dict = {
                'before': {
                    'short_content_type': short_content_type.upper(),
                    'count_bytes': sizeof_fmt(count_bytes),
                    'size': '{}x{}'.format(*im.size),
                },
                'after': {
                    'short_content_type': None,
                    'count_bytes': None,
                    'size': None,
                }
            }
            order_print_diff = ['short_content_type', 'count_bytes', 'size']

            # Сжатие изображения
            jpeg_buffer = io.BytesIO()
            if im.format.lower() in ('png'):
              quantized_im = quantize_image(im)  # Исправленное использование
              quantized_im.save(jpeg_buffer, format='png', optimize=True)
            else:
              im.save(jpeg_buffer, format=im.format, optimize=True, quality=75)
            compress_im_data = jpeg_buffer.getvalue()

            # Изменение размера изображения
            if is_resize_image:
                # Определяем большую сторону изображения
                max_size = 800  # Максимальный размер большей стороны
                width, height = im.size

                if max(width, height) > max_size:
                    # Вычисляем коэффициент масштабирования
                    if width > height:
                        new_width = max_size
                        new_height = int(height * (max_size / width))
                    else:
                        new_height = max_size
                        new_width = int(width * (max_size / height))

                   # Изменяем размер изображения
                    compress_im = Image.open(io.BytesIO(compress_im_data))
                    resized_im = compress_im.resize((new_width, new_height), Image.Resampling.LANCZOS)

                   # Сохраняем изменённое изображение
                    resize_buffer = io.BytesIO()
                    if im.format.lower() in ('png'):
                        quantized_im = quantize_image(resized_im) # Исправленное использование
                        quantized_im.save(resize_buffer, format='png', optimize=True)
                    else:
                        resized_im.save(resize_buffer, format=im.format, optimize=True, quality=75)
                    compress_im_data = resize_buffer.getvalue()

            compress_count_bytes = len(compress_im_data)
            compress_total_image_size += compress_count_bytes
            im = Image.open(io.BytesIO(compress_im_data))
            diff_dict['after']['short_content_type'] = im.format.upper()
            diff_dict['after']['count_bytes'] = sizeof_fmt(compress_count_bytes)
            diff_dict['after']['size'] = '{}x{}'.format(*im.size)
            diff_percent = ((count_bytes - compress_count_bytes) / count_bytes) * 100 if count_bytes else 0
            diff_str = f'{(round(diff_percent)) if use_percent else round(diff_percent)}'
            print(f'    {im_id}. Compress: {diff_str}%')
            if diff_str:
               for diff in order_print_diff:
                  if diff_dict['before'][diff] != diff_dict['after'][diff]:
                     print(f'        {diff_dict["before"][diff]} --> {diff_dict["after"][diff]}')
            binary.text = base64.b64encode(compress_im_data).decode()
        except FileNotFoundError:
            print(f"Ошибка: Файл изображения не найден: {fb2_file_name}")
        except Exception as e:
            print(f"Произошла ошибка при обработке файла: {fb2_file_name}: {e}")
        finally:
            try:
                im.close()
            except:
                pass

    fb2.close()
    compress_file_name = 'compress_' + os.path.basename(fb2_file_name)
    if compress_total_image_size < total_image_size:
      compress_file_path = os.path.join(os.path.dirname(fb2_file_name), compress_file_name) # Сохранение в директории с исходным файлом
      with open(compress_file_path, 'wb') as new_fb2:
        new_fb2.write(etree.tostring(xml_fb2, encoding='utf8', pretty_print=True, xml_declaration=True))
      print(f'    All images compression: {sizeof_fmt(total_image_size)} --> {sizeof_fmt(compress_total_image_size)} ')
      diff_percent = ((total_image_size - compress_total_image_size) / total_image_size) * 100 if total_image_size else 0
      print(f'    Diff size: {round(diff_percent)}%')
      print(f'    Файл сохранен: {compress_file_path}')
    else:
      compress_file_path = os.path.join(os.path.dirname(fb2_file_name), compress_file_name) # Сохранение в директории с исходным файлом
      with open(compress_file_path, 'wb') as new_fb2:
        new_fb2.write(etree.tostring(xml_fb2, encoding='utf8', pretty_print=True, xml_declaration=True))
      print('    Сжатие не дало результата, но файл сохранен!')
      print(f'    Файл сохранен: {compress_file_path}')
    return None

    fb2_file_size = os.path.getsize(fb2_file_name)
    print()
    print('FB2 file size =', sizeof_fmt(fb2_file_size))
    print('Total image size = {} ({:.0f}%)'.format(sizeof_fmt(total_image_size),
                                                   total_image_size / fb2_file_size * 100))

    if compress_total_image_size:
        # К имени файла fb2 добавим строку 'compress_'
        split_path = os.path.split(fb2_file_name)
        compress_fb2_file_name = os.path.join(split_path[0], 'compress_' + split_path[-1])

        # Save to XML file
        tree = etree.ElementTree(xml_fb2)
        tree.write(compress_fb2_file_name, xml_declaration=True, encoding='utf-8')

        print()
        print('Compressed fb2 file saved as {} ({})'.format(compress_fb2_file_name,
                                                            sizeof_fmt(os.path.getsize(compress_fb2_file_name))))
        print('Compress total image size = {}'.format(sizeof_fmt(compress_total_image_size)))
        print('Compress: {:.0f}%'.format(100 - (compress_total_image_size / total_image_size * 100)))
    else:
        print('Compress: 0%')

# TODO: замена в zip архиве

if __name__ == '__main__':
    import click

    @click.command(help='Функция сжимает изображения в файле FB2 и сохраняет копию с сжатыми '
                        'картинками в папке с скриптом, добавляя в начало имени файла строку "compress_".')
    @click.argument('fb2_file_name', type=click.Path(exists=True))
    @click.option('--is_resize_image', default=True, type=bool, help='Менять размер изображения')
    @click.option('--is_convert_to_jpeg', default=True, type=bool, help='Конвертирование изображений в jpeg, '
                                                                        'который более легкий, чем png')
    @click.option('--use_percent', default=True, type=bool, help='Использовать процентное изменение размера')
    @click.option('--percent', default=50, type=int, help='На сколько процентов изменить размер')
    @click.option('--set_width', type=int, help=' Установка ширины изображения (Используется если: --is_resize_'
                                                'image == True and --use_percent == False)')
    @click.option('--set_height', type=int, help='Установка высоты изображения (Используется если: --is_resize_'
                                                 'image == True and --use_percent == False)')
    def main(**kwargs):
        compress_image_fb2(**kwargs)

    main()

