#!/usr/bin/python
#-- coding:utf8 --
from flask import request, Flask, jsonify
from flask import render_template
from json import dumps
#导入库
from model.model import *
import torch,warnings,argparse

warnings.filterwarnings("ignore")

#选择哪个模型 ，是否使用gpu
# parser = argparse.ArgumentParser()
# parser.add_argument('--model', help='The path of your model file.', required=True, type=str)
# parser.add_argument('--device', help='Your program running environment, "cpu" or "cuda"', type=str, default='cpu')
# args = parser.parse_args()
# print(args)
#主程序，打印log，同时对话
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html", s="dd")
    # return 'Hello World!'

@app.route('/json', methods=['POST'])
def resjson():
    postdata = request.form['my']
    print('Loading the model...')
    # chatBot = ChatBot(args.model, device=torch.device(args.device))
    chatBot = ChatBot("model.pkl", device="cpu")
    print('Finished...')

    allRandomChoose, showInfo = True, False
    # 在控制端显示的词语
    print("问："+postdata)
    while True:
        inputSeq = postdata
        if inputSeq == '_crazy_on_':
            allRandomChoose = True
            print('小可爱: ', '成功开启疯狂模式...')
        elif inputSeq == '_crazy_off_':
            allRandomChoose = False
            print('小可爱: ', '成功关闭疯狂模式...')
        elif inputSeq == '_showInfo_on_':
            showInfo = True
            print('小可爱: ', '成功开启日志打印...')
        elif inputSeq == '_showInfo_off_':
            showInfo = False
            print('小可爱: ', '成功关闭日志打印...')
        else:
            outputSeq = chatBot.predictByBeamSearch(inputSeq, isRandomChoose=True, allRandomChoose=allRandomChoose,
                                                    showInfo=showInfo)
            print('小可爱: ', outputSeq)
        print()
        t = {
        'a': outputSeq
        }
        return dumps(t)


if __name__ == '__main__':
    app.run()
