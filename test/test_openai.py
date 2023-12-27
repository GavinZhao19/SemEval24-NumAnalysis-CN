import unittest
from os.path import join

from src.llm.openai_chatgpt import OpenAIGPT
from src.utils import TxtService
from utils import DATA_DIR


class TestChatGPT(unittest.TestCase):

    def test_gpt4_turbo(self):
        chatbot = OpenAIGPT(api_key=TxtService.read_lines(join(DATA_DIR, "openai-key.txt"))[-1],
                            model_name="gpt-4-1106-preview",
                            assistant_prompt=None,
                            temp=0.1,
                            max_tokens=100)

        response = chatbot.ask("What's the color of the sky?")

        print(response)
        
        # The color of the sky can vary depending on the time of day, weather conditions,
        # and the presence of particles or pollutants in the air. During a clear day,
        # the sky typically appears blue to the human eye. This is due to Rayleigh scattering,
        # where shorter blue wavelengths of sunlight are scattered in all directions by the gases
        # and particles in the Earth's atmosphere, making the blue light more visible.

    def test_gpt35_turbo(self):
        chatbot = OpenAIGPT(api_key=TxtService.read_lines(join(DATA_DIR, "openai-key.txt"))[-1],
                            model_name="gpt-3.5-turbo-1106",
                            assistant_prompt=None,
                            temp=0.1,
                            max_tokens=100)

        response = chatbot.ask("What's the color of the sky?")

        print(response)

        # The color of the sky can vary depending on the time of day and weather conditions.
        # During the day, the sky is typically blue, but it can also appear gray or white when overcast.
        # At sunrise and sunset, the sky often takes on shades of red, orange, pink, and purple.
        # At night, the sky appears dark, but can be illuminated by the moon and stars.


if __name__ == '__main__':
    unittest.main()
