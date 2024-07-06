import os
import torch
import psutil


class TranslationModelConfig:
    """
    Конфигурация модели озвучки перевода.
    """

    def __init__(self, output_file_name, sample_rate=48000):
        """
        Инициализация конфигурации модели озвучки перевода.
        :param output_file_name: Имя файла в формате .wav в который сохранится озвученный текст.
        :param sample_rate: Частота дискретизации звучания.
        """
        self.sample_rate = sample_rate
        self.speaker = self.selected_speaker()
        self.output_file_name = output_file_name
        self.local_filename_model = 'model.pt'
        self.device = self.get_device()
        self.get_inf_about_processor()
        self.check_model_file()
        self.model = torch.package.PackageImporter(self.local_filename_model).load_pickle("tts_models", "model")
        self.model.to(self.device)

    def selected_speaker(self):
        """
        Выбор говорящего.
        """
        speakers_list = ['aidar', 'baya', 'kseniya', 'xenia', 'eugene', 'random']
        for num, speaker in enumerate(speakers_list, start=1):
            print(f'{num}. {speaker}')
        while True:
            try:
                speaker_num = int(input('Выберите голос перевода: '))
                if 1 <= speaker_num <= len(speakers_list):
                    print(f'выбран голос: {speakers_list[speaker_num - 1]}')
                    return speakers_list[speaker_num - 1]
                else:
                    print('Введен неверный номер говорящего.')
            except ValueError:
                print('Введено не число. Попробуйте снова.')

    def get_device(self):
        """
        Возвращает устройство для выполнения операций.
        """
        return torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    @staticmethod
    def get_inf_about_processor():
        """
        Получение информации о процессоре
        """
        num_threads = psutil.cpu_count(logical=True)
        torch.set_num_threads(num_threads)

    def check_model_file(self):
        """
        Проверка существования файла модели. Если нет, загрузка модели из интернета.
        """
        url_download_modal = 'https://models.silero.ai/models/tts/ru/v4_ru.pt'
        if not os.path.isfile(self.local_filename_model):
            torch.hub.download_url_to_file(url_download_modal, self.local_filename_model)

    def save_translate_file(self, translated_text):
        """
        Сохранение озвученного файла перевода.
        :param translated_text: Текст для перевода.
        :return Путь к файлу
        """
        self.model.save_wav(
            text=translated_text,
            speaker=self.speaker,
            sample_rate=self.sample_rate,
            audio_path=self.output_file_name
        )
