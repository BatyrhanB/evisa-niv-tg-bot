import cv2
import numpy as np
import argparse
from mltu.inferenceModel import OnnxInferenceModel
from mltu.utils.text_utils import ctc_decoder, get_cer

class ImageToWordModel(OnnxInferenceModel):
    def __init__(self, char_list: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.char_list = char_list

    def predict(self, image: np.ndarray):
        image = cv2.resize(image, self.input_shape[:2][::-1])
        image_pred = np.expand_dims(image, axis=0).astype(np.float32)
        preds = self.model.run(None, {self.input_name: image_pred})[0]
        text = ctc_decoder(preds, self.char_list)[0]
        return text

def main():
    from mltu.configs import BaseModelConfigs
    parser = argparse.ArgumentParser(description="Captcha Breaker")
    parser.add_argument("image_path", type=str, help="Path to the input image")

    args = parser.parse_args()

    configs = BaseModelConfigs.load("Models/captcha_breaker/202402151032/configs.yaml")
    model = ImageToWordModel(model_path=configs.model_path, char_list=configs.vocab)

    image_path = args.image_path
    image = cv2.imread(image_path)

    prediction_text = model.predict(image)

    print(prediction_text)

if __name__ == "__main__":
    main()
