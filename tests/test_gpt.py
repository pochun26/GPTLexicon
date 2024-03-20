from fastapi.testclient import TestClient
import random
from app.main import app

client = TestClient(app)

word_list = ['apple', 'banana', 'cat', 'dog', 'elephant', 'flower', 'guitar', 'house', 'ice cream', 'jungle', 'kangaroo', 'lion', 'mountain', 'notebook', 'ocean', 'piano', 'queen', 'rabbit', 'sun', 'tree', 'umbrella', 'violin', 'watermelon', 'xylophone', 'yacht', 'zebra', 'airplane', 'ball', 'car', 'duck', 'elephant', 'fish', 'guitar', 'hat', 'island', 'jacket', 'kite', 'lion', 'monkey', 'nest', 'orange', 'pencil', 'quilt', 'rose', 'sunflower', 'table', 'umbrella', 'vase', 'water', 'xylophone', 'yoga', 'zebra',
             'ant', 'butterfly', 'candle', 'dragon', 'elephant', 'feather', 'guitar', 'horse', 'ice cream', 'jellyfish', 'kiwi', 'lion', 'monkey', 'nest', 'orange', 'penguin', 'queen', 'rabbit', 'snake', 'tiger', 'umbrella', 'violet', 'whale', 'xylophone', 'yogurt', 'zebra', 'acorn', 'butterfly', 'coconut', 'dolphin', 'elephant', 'feather', 'guitar', 'honey', 'igloo', 'jaguar', 'kiwi', 'lemon', 'moon', 'nest', 'octopus', 'panda', 'queen', 'rainbow', 'sun', 'tiger', 'umbrella', 'violet', 'whale', 'xylophone', 'yogurt', 'zebra']
test_retry = 1


def test_explain():
    for _ in range(test_retry):
        word = random.choice(word_list)
        response = client.get(f"/gpt/explain/all/{word}")
        assert response.status_code == 200
        assert response.json().get("meaning") is not None
        assert response.json().get("example") is not None
        assert response.json().get("synonyms") is not None
        assert response.json().get("antonyms") is not None


def test_meaning():
    for _ in range(test_retry):
        word = random.choice(word_list)
        response = client.get(f"/gpt/explain/{word}?method=meaning")
        assert response.status_code == 200
        anwser = response.json().get("answer")
        assert type(anwser) == str


def test_example():
    for _ in range(test_retry):
        word = random.choice(word_list)
        response = client.get(f"/gpt/explain/{word}?method=example")
        assert response.status_code == 200
        anwser = response.json().get("answer")
        assert type(anwser) == list


def test_synonyms():
    for _ in range(test_retry):
        word = random.choice(word_list)
        response = client.get(f"/gpt/explain/{word}?method=synonyms")
        assert response.status_code == 200
        anwser = response.json().get("answer")
        assert type(anwser) == list


def test_antonyms():
    for _ in range(test_retry):
        word = random.choice(word_list)
        response = client.get(f"/gpt/explain/{word}?method=antonyms")
        assert response.status_code == 200
        anwser = response.json().get("answer")
        assert type(anwser) == list
