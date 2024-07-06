from pydub import AudioSegment


class CheckFormat:
    """
    Класс-дескриптор проверяет формат переданного файла
    """

    def __set_name__(self, owner, name):
        """
        Автоматически привязывает имя атрибута к дескриптору
        :param owner: ссылка на класс в котором будет примениться дескриптор
        :param name: имя атрибута
        """
        self.name = f'_{name}'

    def __set__(self, instance, value):
        """
        Проверяет формат файла переданного в атрибут и присваивает его параметру в экземпляр класса
        :param instance: экземпляр класса
        :param value: значение атрибута
        """
        if value.endswith('.mp3'):
            setattr(instance, self.name, value)
        else:
            raise ValueError(f'файл {value}: должен быть в формате mp3')

    def __get__(self, instance, owner):
        """
        Возвращает значение атрибута из экземпляра класса
        :param instance: экземпляр класса
        :param owner: ссылка на класс в котором будет примениться дескриптор
        :return: значение атрибута
        """
        return getattr(instance, self.name)


class Mp3ToWavConverter:
    """
    Конвертирует mp3-файл в файл в формате wav
    """
    path_mp3_file = CheckFormat()

    def __init__(self, path_mp3_file):
        """
        :param path_mp3_file: Путь к mp3-файлу
        """
        self.path_mp3_file = path_mp3_file
        self.wav_file = 'default_name_file.wav'
        self.convert()

    def convert(self):
        """
        Конвертирует mp3-файл в wav-файл
        """
        try:
            audio = AudioSegment.from_mp3(self.path_mp3_file)
            audio.set_channels(1)
            audio.export(self.wav_file, format='wav')
        except Exception as exc:
            print(f'Ошибка конвертирования файла: {exc}')
        else:
            print(f'Файл {self.path_mp3_file} успешно конвертирован в {self.wav_file}')
