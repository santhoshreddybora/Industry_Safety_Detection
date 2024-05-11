import sys,os
from Industry_Safety_Detection.pipeline.training_pipeline import TrainPipeline
from Industry_Safety_Detection.exception import isdException
from Industry_Safety_Detection.utils.main_utils import decodeImage, encodeImageIntoBase64
from flask import Flask, request, jsonify, render_template,Response
from flask_cors import CORS, cross_origin



app = Flask(__name__)
CORS(app)


class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"



@app.route("/train")
def trainRoute():
    obj = TrainPipeline()
    obj.run_pipeline()
    return jsonify({"success"})
    


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/predict", methods=['POST','GET'])
@cross_origin()
def predictRoute():
    try:
        image = request.json['image']
        decodeImage(image, clApp.filename)

       
        os.system("cd yolov7-1/ && python detect.py --weights best.pt  --source ../data/inputImage.jpg")

        opencodedbase64 = encodeImageIntoBase64("yolov7-1/runs/detect/exp/inputImage.jpg")
        result = {"image": opencodedbase64.decode('utf-8')}
        os.system("rm -rf yolov7-1/runs")

    except ValueError as val:
        print(val)
        return Response("Value not found inside  json data")
    except KeyError:
        return Response("Key value error incorrect key passed")
    except Exception as e:
        print(e)
        result = "Invalid input"

    return jsonify(result)


if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host="0.0.0.0", port=8080)
    