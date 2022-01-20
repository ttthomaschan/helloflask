from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
import torchvision.models as models
import torchvision.transforms as T
import torch
import torch.nn.functional as F
from PIL import Image
import io
import settings

app = Flask(__name__)
app.config.from_object(settings)
model = None
use_gpu = True

def load_model():
    global model
    model = models.resnet50(pretrained=True)
    model.eval()
    if use_gpu:
        model.cuda()

def prepare_image(image, target_size):
    if image.mode != 'RGB':
        image = image.convert("RGB")

    image = T.Resize(target_size)(image)
    image = T.ToTensor()(image)

    image = T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])(image)
    image = image[None]
    if use_gpu:
        image = image.cuda()
    return image

with open('imagenet_class.txt', 'r') as f:
    idx2label = eval(f.read())

@app.route('/', methods=['GET','POST'])
def predict():
    data = {"success": False}
    if request.method == 'GET':
        return render_template('home.html')
    if request.method == 'POST':
        if request.files.get("image"):
            image = request.files["image"].read()
            image = Image.open(io.BytesIO(image))
            image = prepare_image(image, target_size=(224, 224))
            preds = F.softmax(model(image), dim=1)
            results = torch.topk(preds.cpu().data, k=3, dim=1)
            results = (results[0].cpu().numpy(), results[1].cpu().numpy())
            label_name = idx2label[int(results[1][0][0])]
            data['predictions'] = label_name
            data['success'] = True
        if request.files.get("image_url"):
            data['url'] = request.files["image_url"].read()
    return jsonify(data)


# @app.route('/', methods=['GET', 'POST'])
# def home():
#     return render_template('home.html')
#
# @app.route('/signin', methods=['GET'])
# def signin_form():
#     return render_template('form.html')
#
# @app.route('/signin', methods=['POST'])
# def signin():
#     # 需要从request对象读取表单内容
#     if request.form['username'] == 'admin' and request.form['password'] == 'password':
#         a = 3
#         b = a*2
#         te = a*b
#         print(te)
#         return '<h3>Hello, admin!</h3>'
#     return '<h3>Bad username or password.</h3>'

##########################################
if __name__ == '__main__':

    # load_model()
    # image_path = "./dog.JPEG"
    # image = Image.open(image_path, "r")
    # image = prepare_image(image, target_size=(224, 224))
    # preds = F.softmax(model(image), dim=1)
    # results = torch.topk(preds.cpu().data, k=3, dim=1)
    # print(results)
    #
    # # 返回结果用的
    # with open('imagenet_class.txt', 'r') as f:
    #     idx2label = eval(f.read())
    #
    # label_name = idx2label[int(results[1][0][0])]
    # print(label_name)

    print("Loading PyTorch model and Flask starting server ...")
    print("Please wait until server has fully started")
    #先加载模型
    load_model()
    #再开启服务
    app.run(host="192.168.30.41", port=8080)