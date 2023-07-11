import unittest
import yaml
from backend.server import create_app
from pathlib import Path


data = None
base_path = Path(__file__).parent
file_path = (base_path / "../../yaml/04_summary_custom.yaml").resolve()
with open(file_path, mode="rt", encoding="utf-8") as file:
    data = yaml.safe_load(file)


class SummaryTestcase(unittest.TestCase):
    def setUp(self):
        self.app, self.sio = create_app(data)
        self.client = self.app.test_client()
        self.runner = self.app.test_cli_runner()
        self.app.test_cli_runner()

    def test_get_select_model_options(self):
        assert self.client.get('/get_model_checklist').status_code == 200

    def test_all_datasets(self):
        response = self.client.get('/datasets')
        assert all(key in response.json for key in [
                   "datasets_search", "datasets_summarization"])

    def test_file_upload(self):
        response = self.client.post('/datasets/files/upload', json={
            "file": "dosg.txt",
            "content": "The quick brown fox jumped over the lazy dog!"
        })

        assert response.status_code == 201

    def test_all_models(self):
        response = self.client.get('/models', json={})
        assert all(key in response.json for key in [
                   "models_search", "models_summarization"])

    def test_all_files(self):
        response = self.client.get('/datasets/files?dataset=User')
        assert all(key in response.json for key in ["files"])

    # def test_summary(self):
    #     response = self.client.get('/summary', json={
    #         "model": "Bart",
    #         "content": "There was once a sweet little maid who lived with her father and\nmother in a pretty little cottage at the edge of the village. At the\nfurther end of the wood was another pretty cottage and in it lived her\ngrandmother.\n\nEverybody loved this little girl, her grandmother perhaps loved her\nmost of all and gave her a great many pretty things. Once she gave her\na red cloak with a hood which she always wore, so people called her\nLittle Red Riding Hood.\n\nOne morning Little Red Riding Hood's mother said, \"Put on your things\nand go to see your grandmother. She has been ill; take along this\nbasket for her. I have put in it eggs, butter and cake, and other\ndainties.\"\n\nIt was a bright and sunny morning. Red Riding Hood was so happy that\nat first she wanted to dance through the wood. All around her grew\npretty wild flowers which she loved so well and she stopped to pick a\nbunch for her grandmother.\n\nLittle Red Riding Hood wandered from her path and was stooping to pick\na flower when from behind her a gruff voice said, \"Good morning,\nLittle Red Riding Hood.\" Little Red Riding Hood turned around and saw\na great big wolf, but Little Red Riding Hood did not know what a\nwicked beast the wolf was, so she was not afraid.\n\n\"What have you in that basket, Little Red Riding Hood?\"\n\n\"Eggs and butter and cake, Mr. Wolf.\"\n\n\"Where are you going with them, Little Red Riding Hood?\"\n\n\"I am going to my grandmother, who is ill, Mr. Wolf.\"\n\n\"Where does your grandmother live, Little Red Riding Hood?\"\n\n\"Along that path, past the wild rose bushes, then through the gate at\nthe end of the wood, Mr. Wolf.\"\n\nThen Mr. Wolf again said \"Good morning\" and set off, and Little Red\nRiding Hood again went in search of wild flowers.\n\nAt last he reached the porch covered with flowers and knocked at the\ndoor of the cottage.\n\n\"Who is there?\" called the grandmother.\n\n\"Little Red Riding Hood,\" said the wicked wolf.\n\n\"Press the latch, open the door, and walk in,\" said the grandmother.\n\nThe wolf pressed the latch, and walked in where the grandmother lay in\nbed. He made one jump at her, but she jumped out of bed into a closet.\nThen the wolf put on the cap which she had dropped and crept under the\nbedclothes.\n\nIn a short while Little Red Riding Hood knocked at the door, and\nwalked in, saying, \"Good morning, Grandmother, I have brought you\neggs, butter and cake, and here is a bunch of flowers I gathered in\nthe wood.\" As she came nearer the bed she said, \"What big ears you\nhave, Grandmother.\"\n\n\"All the better to hear you with, my dear.\"\n\n\"What big eyes you have, Grandmother.\"\n\n\"All the better to see you with, my dear.\"\n\n\"But, Grandmother, what a big nose you have.\"\n\n\"All the better to smell with, my dear.\"\n\n\"But, Grandmother, what a big mouth you have.\"\n\n\"All the better to eat you up with, my dear,\" he said as he sprang at\nLittle Red Riding Hood.\n\nJust at that moment Little Red Riding Hood's father was passing the\ncottage and heard her scream. He rushed in and with his axe chopped\noff Mr. Wolf's head.\n\nEverybody was happy that Little Red Riding Hood had escaped the wolf.\nThen Little Red Riding Hood's father carried her home and they lived\nhappily ever after."
    #     })
    #     self.assertTrue("result" in response.json)