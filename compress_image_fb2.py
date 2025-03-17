#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт сжимает картинки в файле FB2."""


import base64
import io
import traceback

from dataclasses import dataclass, field, fields
from functools import total_ordering
from pathlib import Path
from timeit import default_timer

from lxml import etree
from imagequant import quantize_pil_image

from PIL import Image, UnidentifiedImageError
from PIL.Image import Resampling


# NOTE: Подсказка по форматам и модам
"""
    JPEG поддерживает режимы:
        L (8-bit pixels, grayscale)
        RGB (3x8-bit pixels, true color)
        CMYK (4x8-bit pixels, color separation)

    А PNG поддерживает:
        1 (1-bit pixels, black and white, stored with one pixel per byte)
        L (8-bit pixels, grayscale)
        LA (L with alpha)
        I (32-bit signed integer pixels)
        P (8-bit pixels, mapped to any other mode using a color palette)
        RGB (3x8-bit pixels, true color)
        RGBA (4x8-bit pixels, true color with transparency mask)
"""


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/fec522a6d931b0e353ed9e1025fe0a1c2d7c4ae6/human_byte_size.py#L7-L14
def sizeof_fmt(num: int | float) -> str:
    for x in ["bytes", "KB", "MB", "GB"]:
        if num < 1024.0:
            return "%.1f %s" % (num, x)

        num /= 1024.0

    return "%.1f %s" % (num, "TB")


def img_to_buffer(img: Image, img_format: str) -> io.BytesIO:
    buffer = io.BytesIO()
    img.save(buffer, format=img_format)
    return buffer


def img_to_bytes(img: Image, img_format: str | None = None) -> bytes:
    if not img_format:
        img_format = img.format
    return img_to_buffer(img, img_format).getvalue()


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/c29ae90abffae049af041088192680f267d004e8/pil_pillow__examples/resize_width_or_height_with_keep_ratio/main.py#L12-L38
def _resize_img(
    img: Image,
    width: int,
    height: int,
    resample: Resampling | None = None,
) -> Image:
    img_resized = img.resize(size=(width, height), resample=resample)
    img_resized.format = img.format  # NOTE: resize reset format
    return img_resized


def resize_height_img(
    img: Image,
    height: int,
    resample: Resampling | None = None,
) -> Image:
    """Resize by height, keep ratio."""
    return _resize_img(img, img.width * height // img.height, height, resample)


def resize_width_img(
    img: Image,
    width: int,
    resample: Resampling | None = None,
) -> Image:
    """Resize by width, keep ratio."""
    return _resize_img(img, width, img.height * width // img.width, resample)


def resize_max_width_and_height_img(
    img: Image,
    max_width: int | None,
    max_height: int | None,
) -> Image:
    resample = Image.Resampling.LANCZOS

    img_resized = img

    if max_width and img_resized.size[0] > max_width:
        img_resized = resize_width_img(img_resized, width=max_width, resample=resample)

    if max_height and img_resized.size[1] > max_height:
        img_resized = resize_height_img(
            img_resized, height=max_height, resample=resample
        )

    return img_resized


def get_percent(
    value: int | float,
    max_value: int | float,
    from_100: bool = False,
) -> float:
    if value == 0:
        return 0

    result = (value / max_value) * 100
    if from_100:
        result = 100 - result
    return result


@total_ordering
@dataclass
class CompressImageResult:
    img_data: bytes
    error: Exception | None = None

    def is_ok(self) -> bool:
        return self.error is None

    def __eq__(self, other: "CompressImageResult") -> bool:
        return len(self.img_data) == len(other.img_data)

    def __lt__(self, other: "CompressImageResult") -> bool:
        return len(self.img_data) < len(other.img_data)


class StrategyCompressImage:
    def __init__(self, img_data: bytes):
        self.img_data = img_data
        self.img = Image.open(io.BytesIO(self.img_data))

    def do_process(self) -> bytes:
        raise NotImplementedError()

    def process(self) -> CompressImageResult:
        try:
            return CompressImageResult(img_data=self.do_process())
        except Exception as e:
            return CompressImageResult(img_data=self.img_data, error=e)

    @classmethod
    def get_strategies(
        cls,
        strategies: list[str] | None = None,
    ) -> list[type["StrategyCompressImage"]]:
        return [
            obj
            for obj in cls.__subclasses__()
            # NOTE: Для пустого списка не нужно фильтровать
            if not strategies or obj.__name__ in strategies
        ]

    @classmethod
    def get_strategy_names(cls) -> list[str]:
        return [obj.__name__ for obj in cls.get_strategies()]


class StrategyCompressImage1(StrategyCompressImage):
    """
    Стратегия конвертации в тот же формат. Может быть меньший размер за счет не сохранения
    метаинформации
    """

    def do_process(self) -> bytes:
        return img_to_bytes(self.img)


class StrategyCompressImage2(StrategyCompressImage):
    """
    Стратегия конвертации в PNG с поддержкой прозрачности и размером цвета в 1 байт.
    Если это будет JPEG c прозрачностью, то оно будет конвертировано в PNG
    """

    def do_process(self) -> bytes:
        new_img = self.img
        new_format = new_img.format

        # NOTE: Можно попробовать
        if new_format == "JPEG" and new_img.mode in ["RGB", "CMYK"]:
            new_format = "PNG"

            buffer = img_to_buffer(new_img, new_format)
            buffer.seek(0)
            new_img = Image.open(buffer)

        # NOTE: Fix "image has wrong mode"
        if new_img.mode == "LA":
            new_img = new_img.convert("P")

        new_img = quantize_pil_image(new_img)
        return img_to_bytes(new_img, new_format)


class StrategyCompressImage3(StrategyCompressImage):
    """
    Стратегия конвертации PNG без прозрачности в JPEG
    """

    def do_process(self) -> bytes:
        new_img = self.img

        # Для PNG без прозрачности
        if new_img.format != "PNG" or new_img.has_transparency_data:
            return self.img_data

        # NOTE: Fix "cannot write mode P as JPEG"
        if new_img.mode.upper() == "P":
            new_img = new_img.convert("RGB")

        # Конвертируем в JPG
        return img_to_bytes(new_img, "JPEG")


@dataclass
class ImageInfo:
    img: Image = field(repr=False)
    format: str = field(init=False)
    mode: str = field(init=False)
    data_size_bytes: int = field(repr=False)
    data_size_human: str = field(init=False)
    size: str = field(init=False)

    @classmethod
    def from_bytes(cls, data: bytes) -> "ImageInfo":
        return cls(
            img=Image.open(io.BytesIO(data)),
            data_size_bytes=len(data),
        )

    def __post_init__(self):
        self.data_size_human = sizeof_fmt(self.data_size_bytes)
        self.format = self.img.format
        self.mode = self.img.mode
        self.size = f"{self.img.size[0]}x{self.img.size[1]}"

    def suffix(self) -> str:
        if self.format == "JPEG":
            return "jpg"
        return self.format.lower()


def compress_image_fb2(
    fb2_file_name: Path,
    output_dir: Path | None = None,
    pattern_output_file_name: str = "{path.stem}_compress{path.suffix}",
    used_strategies: list[str] | None = None,
    max_width: int | None = None,
    max_height: int | None = None,
    is_extract_images: bool = False,
    is_log: bool = True,
    is_log_diff_equals: bool = True,
):
    """
    Функция сжимает изображения в файле FB2 и сохраняет копию с сжатыми картинками в папке с скриптом.

    :param fb2_file_name: Путь к файлу FB2
    :param output_dir: Папка для вывода сжатого файла
    :param pattern_output_file_name: Шаблон имени сжатого FB2
    :param used_strategies: Используемые стратегии сжатия картинок
    :param max_width: Максимальная ширина картинки
    :param max_height: Максимальная высота картинки
    :param is_extract_images: Вывод оригинальных и сжатых изображений в папку по имени файла
    :param is_log: Вывод информации по сжатию файла
    :param is_log_diff_equals: Вывод неизмененных полей картинки после сжатия

    """

    def log(*args, **kwargs):
        is_log and print(*args, **kwargs)

    start_time: float = default_timer()

    if not output_dir:
        output_dir: Path = fb2_file_name.parent

    output_dir.mkdir(parents=True, exist_ok=True)

    total_image_size: int = 0
    compress_total_image_size: int = 0

    log(f"{fb2_file_name}:")

    fb2_data: bytes = fb2_file_name.read_bytes()
    fb2_file_size: int = len(fb2_data)

    xml_fb2 = etree.fromstring(
        text=fb2_data,
        parser=etree.XMLParser(
            # Уменьшение размера XML
            # Замена \n\r на \n выполняется штатно перед парсингом:
            # https://www.w3.org/TR/REC-xml/#sec-line-ends
            remove_blank_text=True,
            remove_comments=True,
            ns_clean=True,
            huge_tree=True,
        ),
    )

    strategy_classes: list[
        type[StrategyCompressImage]
    ] = StrategyCompressImage.get_strategies(used_strategies)

    binaries: list = xml_fb2.xpath("//*[local-name()='binary']")
    for i, binary in enumerate(binaries, 1):
        img_id: str = binary.attrib["id"]
        try:
            binary_text = binary.text
            img_data: bytes = base64.b64decode(binary_text)

            try:
                original_info = ImageInfo.from_bytes(img_data)
            except UnidentifiedImageError:
                log(f"    {i}. {img_id}. - Невалидное изображение")
                continue

            compress_img_data: bytes = img_data
            original_img_data_size: int = len(compress_img_data)

            total_image_size += len(binary_text)

            name_by_strategy: dict[str, CompressImageResult] = {
                strategy_cls.__name__: strategy_cls(compress_img_data).process()
                for strategy_cls in strategy_classes
            }
            if name_by_strategy:
                max_result_name, max_result = min(
                    name_by_strategy.items(), key=lambda x: x[1]
                )
                if max_result.is_ok():
                    compress_img_data = max_result.img_data

            compress_info = ImageInfo.from_bytes(compress_img_data)

            if max_width or max_height:
                img_resized = resize_max_width_and_height_img(
                    img=compress_info.img,
                    max_width=max_width,
                    max_height=max_height,
                )

                compress_img_data = img_to_bytes(img_resized)
                compress_info = ImageInfo.from_bytes(compress_img_data)

            compress: float = get_percent(
                compress_info.data_size_bytes,
                original_info.data_size_bytes,
                from_100=True,
            )

            log(
                f"    {i}. {img_id}. Сжатие: {compress:.2f}%{'' if compress > 0 else ' - Пропущено'}"
            )

            # Меняем информация о формате и заменяем картинку
            if compress > 0:
                binary.attrib["content-type"] = f"image/{compress_info.format.lower()}"
                binary.text = base64.b64encode(compress_img_data).decode("utf-8")

            compress_total_image_size += len(binary.text)

            if name_by_strategy:
                log(f"        Использованные стратегии ({len(name_by_strategy)}):")
                for name, result in name_by_strategy.items():
                    compress_result: float = get_percent(
                        len(result.img_data),
                        original_img_data_size,
                        from_100=True,
                    )
                    log(
                        f"            {name}: {compress_result:.2f}%"
                        if result.is_ok()
                        else f"            {name}: Ошибка: {result.error}",
                    )

                max_compress: float = get_percent(
                    len(max_result.img_data),
                    original_img_data_size,
                    from_100=True,
                )
                log(f"            MAX ({max_result_name}): {max_compress:.2f}%")

            else:
                log("        Отсутствуют стратегии сжатия")

            for f in fields(original_info):
                if not f.repr:
                    continue

                before_value = getattr(original_info, f.name)
                after_value = getattr(compress_info, f.name)
                if before_value != after_value:
                    log(f"        {before_value} -> {after_value}")
                elif is_log_diff_equals:
                    log(f"        {before_value} = {after_value}")

            if is_extract_images:
                # Добавление имени файла FB2 к пути
                img_output_dir = output_dir / f"{fb2_file_name.name}-images"
                img_output_dir.mkdir(parents=True, exist_ok=True)

                # Если в binary@id окончание файла совпадает с действительным форматом,
                # то сохраняется как есть, иначе к значению binary@id добавлен формат
                file_name: str = (
                    img_id
                    if img_id.upper().endswith(original_info.suffix().upper())
                    else f"{img_id}.{original_info.suffix()}"
                )
                img_path_original: Path = img_output_dir / file_name
                log(f"        Сохранение оригинала в: {img_path_original.absolute()}")
                img_path_original.write_bytes(img_data)

                if compress > 0:
                    file_name: str = (
                        f"{img_path_original.stem}_compressed.{compress_info.suffix()}"
                    )
                    img_path_compressed: Path = img_output_dir / file_name
                    log(
                        f"        Сохранение сжатой в: {img_path_compressed.absolute()}"
                    )
                    img_path_compressed.write_bytes(compress_img_data)

            log()

        except Exception:
            log(f"Ошибка при обработке binary@id={img_id}")
            traceback.print_exc()

    log()
    log(f"Оригинальный размер FB2: {sizeof_fmt(fb2_file_size)}")
    log(
        f"Общий размер картинок: {sizeof_fmt(total_image_size)} "
        f"({get_percent(total_image_size, fb2_file_size):.2f}%)"
    )
    remain_size: int = fb2_file_size - total_image_size
    log(
        f"Остальное: {sizeof_fmt(remain_size)} "
        f"({get_percent(remain_size, fb2_file_size):.2f}%)"
    )

    # Получение байтов XML
    result_fb2_data: bytes = etree.tostring(
        xml_fb2,
        xml_declaration=True,
        encoding="utf-8",
    )
    result_fb2_data_size: int = len(result_fb2_data)

    if result_fb2_data_size < fb2_file_size:
        log()

        # Формирование имени файла fb2 из шаблона
        output_file_name: str = pattern_output_file_name.format(path=fb2_file_name)
        compress_fb2_file_name: Path = output_dir / output_file_name

        compress_fb2_file_name.write_bytes(result_fb2_data)

        percent_result_fb2: float = get_percent(
            result_fb2_data_size, fb2_file_size, from_100=True
        )
        log(
            f"FB2 с сжатием: {sizeof_fmt(result_fb2_data_size)} (сжатие {percent_result_fb2:.2f}%)"
        )
        log(
            f"Общий размер картинок: {sizeof_fmt(compress_total_image_size)} "
            f"({get_percent(compress_total_image_size, result_fb2_data_size):.2f}%, "
            f"сжатие {get_percent(compress_total_image_size, total_image_size, from_100=True):.2f}%)"
        )
        remain_compress_size: int = result_fb2_data_size - compress_total_image_size
        log(
            f"Остальное: {sizeof_fmt(remain_compress_size)} "
            f"({get_percent(remain_compress_size, result_fb2_data_size):.2f}%, "
            f"сжатие {get_percent(remain_compress_size, remain_size, from_100=True):.2f}%)"
        )

        log()
        log(f"Сжатый FB2 сохранен в: {compress_fb2_file_name.absolute()} ")
    else:
        log("Сжатие: 0%")

    log(f"\nЗавершено за {default_timer() - start_time:.3f} сек.")


if __name__ == "__main__":
    import click

    @click.command(
        help="""
        Функция сжимает изображения в файле FB2 и сохраняет копию с сжатыми картинками в папке с скриптом.
        """
    )
    @click.argument(
        "fb2_file_name",
        type=click.Path(exists=True, path_type=Path),
    )
    @click.option(
        "--output_dir",
        help="Папка для вывода сжатого файла. Если не указывать, то используется папка файла FB2",
        type=click.Path(path_type=Path),
    )
    @click.option(
        "--pattern_output_file_name",
        help="Шаблон имени сжатого FB2",
        type=str,
        default="{path.stem}_compress{path.suffix}",
        show_default=True,
    )
    @click.option(
        "--used_strategies",
        help="Используемые стратегии сжатия картинок",
        type=click.Choice(StrategyCompressImage.get_strategy_names()),
        multiple=True,
    )
    @click.option(
        "--max_width",
        help="Максимальная ширина картинки. Если больше, то будет уменьшена с сохранением пропорций",
        type=int,
    )
    @click.option(
        "--max_height",
        help="Максимальная высота картинки. Если больше, то будет уменьшена с сохранением пропорций",
        type=int,
    )
    @click.option(
        "--is_extract_images",
        help="Вывод оригинальных и сжатых изображений в папку по имени файла",
        type=bool,
        default=False,
        show_default=True,
    )
    @click.option(
        "--is_log",
        help="Вывод информации по сжатию файла",
        type=bool,
        default=True,
        show_default=True,
    )
    @click.option(
        "--is_log_diff_equals",
        help="Вывод неизмененных полей картинки после сжатия",
        type=bool,
        default=True,
        show_default=True,
    )
    def main(**kwargs):
        compress_image_fb2(**kwargs)

    main()
