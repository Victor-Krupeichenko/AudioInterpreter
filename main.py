import os
import speech_recognition as sr
import multiprocessing
from googletrans import Translator
from file_converter import Mp3ToWavConverter
from transl_voice_model_conf import TranslationModelConfig
from playsound import playsound


class StartProgram(Mp3ToWavConverter):
    """
    Класс для запуска основного потока программы.
    """

    def __init__(self, path_mp3_file, file_lang='en', target_lang='ru', delete_file=True):
        """
        Инициализация класса StartProgram.
        :param path_mp3_file: Путь к mp3-файлу.
        :param file_lang: Язык файла.
        :param target_lang: Язык перевода.
        :param delete_file: Удалить файл с переводом по завершению работы
        """
        super().__init__(path_mp3_file)
        self.transl_model_config = TranslationModelConfig(output_file_name=self.wav_file)
        self.file_lang = file_lang
        self.target_lang = target_lang
        self.delete_file = delete_file
        self.recognizer = sr.Recognizer()
        self.translate = Translator()

    def start_playaudio_processing(self):
        """
        Запуск процесса воспроизведения аудиофайла и удаляет файл с переводом после воспроизведения
        """
        try:
            play_audio = multiprocessing.Process(target=playsound, args=(self.wav_file,))
            play_audio.start()
            play_audio.join()
            if play_audio.is_alive():
                play_audio.terminate()
            if self.delete_file:
                os.remove(self.wav_file)
                print(f'Файл {self.wav_file} был удален после воспроизведения')
        except Exception as e:
            print(f'Ошибка во время воспроизведения файла: {e}')

    def run(self):
        """
        Запуск основного потока программы.
        """
        try:
            with sr.AudioFile(self.wav_file) as source:
                audio = self.recognizer.record(source)
                print(f'{"-" * 32} Запущен процесс получения текста из аудиофайла')
                recognized_text = self.recognizer.recognize_google(audio, language=self.file_lang)
                print(f'{"-" * 32} Запущен процесс перевода текста')
                translated_text = self.translate.translate(text=recognized_text, dest=self.target_lang).text
                print(f'{"-" * 32} Запущен процесс сохранения переведенного текста в .wav файл')
                self.transl_model_config.save_translate_file(translated_text)
        except sr.UnknownValueError:
            print('Ошибка распознавания: не удалось распознать аудио')
        except sr.RequestError as e:
            print(f'Ошибка сервиса распознавания речи: {e}')
        except Exception as exc:
            print(f'Ошибка во время выполнения программы: {exc}')
        self.start_playaudio_processing()


if __name__ == '__main__':
    mp3_file = 'phrases.mp3'
    start_program = StartProgram(mp3_file)
    start_program.run()
