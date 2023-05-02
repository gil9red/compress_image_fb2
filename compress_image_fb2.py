#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

"""Скрипт сжимает картинки в файле fb2."""

import os
import base64
import io

from lxml import etree
from PIL import Image


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def compress_image_fb2(fb2_file_name, is_resize_image=True, is_convert_to_jpeg=True, use_percent=True, percent=50,
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

            # Для fb2 доступно 2 формата: png и jpg. jpg в силу своей природы лучше сжат, поэтому
            # способом сжатия может конвертирование в jpg
            if is_convert_to_jpeg and im.format == 'PNG':
                # Конверируем в JPG
                jpeg_buffer = io.BytesIO()
                if im.mode in ('RGBA', 'LA', 'P', 'PA'):
                    background = Image.new('RGB', im.size, 'white')
                    background.paste(im, im.split()[-1])
                    im = background
                im.save(jpeg_buffer, format='jpeg')
                compress_im_data = jpeg_buffer.getvalue()

                # Меняем информация о формате и заменяем картинку
                content_type = 'image/jpeg'
                short_content_type = 'jpeg'

            if is_resize_image:
                if use_percent:
                    base_width, base_height = im.size
                    width = int(base_width - (base_width / 100) * percent)
                    height = int(base_height - (base_height / 100) * percent)
                else:
                    if set_width is None or set_height is None:
                        raise Exception('Ширина и высота изображений должна быть задана.')

                    width, height = set_width, set_height

                compress_im = Image.open(io.BytesIO(compress_im_data))
                resized_im = compress_im.resize((width, height), Image.Resampling.LANCZOS)

                resize_buffer = io.BytesIO()
                resized_im.save(resize_buffer, format=short_content_type)

                compress_im_data = resize_buffer.getvalue()

            compress_im = Image.open(io.BytesIO(compress_im_data))
            compress_count_bytes = len(compress_im_data)
            compress_total_image_size += compress_count_bytes

            diff_dict['after']['short_content_type'] = short_content_type.upper()
            diff_dict['after']['count_bytes'] = sizeof_fmt(compress_count_bytes)
            diff_dict['after']['size'] = '{}x{}'.format(*compress_im.size)

            # Меняем информация о формате и заменяем картинку
            binary.attrib['content-type'] = content_type
            binary.text = base64.b64encode(compress_im_data)

            compress = 100 - (compress_count_bytes / count_bytes * 100)
            print('    {0}. {1}. Compress: {2:.0f}%'.format(i, im_id, compress))
            for k in order_print_diff:
                v = diff_dict['after'][k]
                before_v = diff_dict['before'][k]
                if v is not None and before_v != v:
                    print('        {} --> {}'.format(before_v, v))

        except Exception:
            import traceback
            traceback.print_exc()

    fb2.close()

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
