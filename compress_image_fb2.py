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


if __name__ == '__main__':
    fb2_file_name = 'mknr_1.fb2'

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

            im = Image.open(io.BytesIO(im_data))
            count_bytes = len(im_data)
            total_image_size += count_bytes
            print('    {}. {}: {} format={} size={}'.format(i, im_id, sizeof_fmt(count_bytes),
                                                            im.format, im.size), end='')

            # Для fb2 доступно 2 формата: png и jpg. jpg в силу своей природы лучше сжат, поэтому
            # способом сжатия может конвертирование в jpg
            if im.format == 'PNG':
                # Конверируем в JPG
                jpeg_buffer = io.BytesIO()
                im.save(jpeg_buffer, format='jpeg')
                jpg_im_data = jpeg_buffer.getvalue()

                jpg_count_bytes = len(jpg_im_data)
                compress_total_image_size += jpg_count_bytes

                # TODO: замена в zip архиве
                # TODO: сделать как модуль (класс/функция) и консоль
                # TODO: можно еще уменьшать размер картинок -- для экрана телефона картинки размером для
                # дисплея компа не нужны
                # # Открываем как Image объект
                # im = Image.open(jpeg_buffer)
                # print(' --> {} format={} size={}. Compress: {:.0f}%'.format(
                #     sizeof_fmt(jpg_count_bytes), im.format,
                #     im.size, 100 - (jpg_count_bytes / count_bytes * 100)), end='')
                #
                # TODO: im.size не изменился -- только формат поменяли
                # TODO: наверное, лучше вывести сравнение картинок в двух столбцах, типа:
                # 6. MKnR_v01_13.png: Compress: 77%
                #     793.7KiB          --> 182.4KiB
                #     format=PNG        --> format=JPEG
                #     size=(1199, 1762) --> size=(1199, 1762)
                print(' --> {} format=JPEG size={}. Compress: {:.0f}%'.format(
                    sizeof_fmt(jpg_count_bytes), im.size, 100 - (jpg_count_bytes / count_bytes * 100)), end='')

                # Меняем информация о формате и заменяем картинку
                binary.attrib['content-type'] = 'image/jpeg'
                binary.text = base64.b64encode(jpg_im_data)

            print()

        except Exception as e:
            import traceback
            traceback.print_exc()

    fb2.close()

    fb2_file_size = os.path.getsize(fb2_file_name)
    print()
    print('FB2 file size =', sizeof_fmt(fb2_file_size))
    print('Total image size = {} ({:.0f}%)'.format(sizeof_fmt(total_image_size),
                                                   total_image_size / fb2_file_size * 100))

    if compress_total_image_size:
        compress_fb2_file_name = 'compress_' + fb2_file_name

        # Save to XML file
        tree = etree.ElementTree(xml_fb2)
        tree.write(compress_fb2_file_name, xml_declaration=True, encoding='utf-8')

        print()
        print('Compressed fb2 file saved as {} ({})'.format(compress_fb2_file_name,
                                                            sizeof_fmt(os.path.getsize('compress_' + fb2_file_name))))
        print('Compress total image size = {}'.format(sizeof_fmt(compress_total_image_size)))
        print('Compress: {:.0f}%'.format(100 - (compress_total_image_size / total_image_size * 100)))
    else:
        print('Compress: 0%')
