# coding: utf-8

'''
医疗NER识别主流程
'''
import os
import re
import ahocorasick
# from paddlenlp import Taskflow
import numpy as np
import json

'''
AC自动机识别
'''
class ACTree:
    def __init__(self):
        # 字典地址
        current_dir = os.path.dirname(__file__)
        self.sentence_path = os.path.join(current_dir, 'data/dict/sentence.txt')
        self.deny_path = os.path.join(current_dir, 'data/dict/deny.txt')
        self.food_path = os.path.join(current_dir, 'data/dict/food.txt')
        self.drug_path = os.path.join(current_dir, 'data/dict/drug.txt')
        self.check_path = os.path.join(current_dir, 'data/dict/check.txt')
        self.disease_path = os.path.join(current_dir, 'data/dict/disease.txt')
        self.symptom_path = os.path.join(current_dir, 'data/dict/symptom.txt')
        self.producer_path = os.path.join(current_dir, 'data/dict/producer.txt')
        self.department_path = os.path.join(current_dir, 'data/dict/department.txt')
        self.physical_examination_path = os.path.join(current_dir, 'data/dict/physical_examination.txt')
        # 加载特征词
        self.disease_wds = [i.strip() for i in open(self.disease_path) if i.strip()]
        self.department_wds = [i.strip() for i in open(self.department_path) if i.strip()]
        self.check_wds = [i.strip() for i in open(self.check_path) if i.strip()]
        self.drug_wds = [i.strip() for i in open(self.drug_path) if i.strip()]
        self.food_wds = [i.strip() for i in open(self.food_path) if i.strip()]
        self.producer_wds = [i.strip() for i in open(self.producer_path) if i.strip()]
        self.symptom_wds = [i.strip() for i in open(self.symptom_path) if i.strip()]
        self.physical_examination_wds = [i.strip() for i in open(self.physical_examination_path) if i.strip()]
        self.region_words = set(
            self.department_wds + self.disease_wds + self.check_wds + self.drug_wds + self.food_wds + self.producer_wds + self.symptom_wds + self.physical_examination_wds)
        self.deny_words = [i.strip() for i in open(self.deny_path) if i.strip()]
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()

    '''
    构造actree，加速过滤
    '''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''
    构造词对应的类型
    '''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.disease_wds:
                wd_dict[wd].append('disease')
            if wd in self.department_wds:
                wd_dict[wd].append('department')
            if wd in self.check_wds:
                wd_dict[wd].append('check')
            if wd in self.drug_wds:
                wd_dict[wd].append('drug')
            if wd in self.food_wds:
                wd_dict[wd].append('food')
            if wd in self.symptom_wds:
                wd_dict[wd].append('symptom')
            if wd in self.producer_wds:
                wd_dict[wd].append('producer')
            if wd in self.physical_examination_wds:
                wd_dict[wd].append('physical_examination')
        return wd_dict

    '''
    获取句子中的医疗实体
    '''
    def check_medical(self, sentence):
        entities = []
        for i in self.region_tree.iter(sentence):
            word = i[1][1]
            for match in re.finditer(word, sentence):
                element = {}
                start_idx = match.start()
                end_idx = match.end()
                type = self.wdtype_dict.get(word)[0]
                element["start_idx"] = start_idx
                element["end_idx"] = end_idx - 1
                element["type"] = type
                element["entity"] = word
                if element not in entities:
                    entities.append(element)
        return entities

# '''
# 解语识别
# '''
# class check_medical:
#     def __init__(self):
#         self.medical_type = ['药物类', '药物类_中药', '疾病损伤类']
#         self.medical2type = {'药物类': 'drug', '药物类_中药': 'drug', '疾病损伤类': 'symptom'}
#
#     def nptag(self, sentence):
#         nptag = Taskflow("knowledge_mining", model="nptag")
#         return nptag(sentence)
#
#     def wordtag(self, sentence):
#         wordtag = Taskflow("knowledge_mining", model="wordtag", linking=True)
#         return wordtag(sentence)
#
#     def filter(self, sentence):
#         entities = []
#         result = self.wordtag(sentence)[0]
#         for item in dict(result).get('items'):
#             wordtag_label = item.get('wordtag_label')
#             if wordtag_label in self.medical_type:
#                 word = item.get('item')
#                 type = self.medical2type.get(wordtag_label)
#                 for match in re.finditer(word, sentence):
#                     element = {}
#                     start_idx = match.start()
#                     end_idx = match.end()
#                     element["start_idx"] = start_idx
#                     element["end_idx"] = end_idx - 1
#                     element["type"] = type
#                     element["entity"] = word
#                     entities.append(element)
#         return entities



from bert4keras.backend import keras, K
from bert4keras.backend import multilabel_categorical_crossentropy
from bert4keras.layers import GlobalPointer
from bert4keras.models import build_transformer_model
from bert4keras.optimizers import Adam
from bert4keras.tokenizers import Tokenizer
from bert4keras.snippets import open, to_array
from keras.models import Model


# def load_data(filename):
#     """
#     加载数据
#     单条格式：[text, (start, end, label), (start, end, label), ...]，
#               意味着text[start:end + 1]是类型为label的实体。
#     """
#     D = []
#     for d in json.load(open(filename)):
#         D.append([d['text']])
#         for e in d['entities']:
#             start, end, label = e['start_idx'], e['end_idx'], e['type']
#             if start <= end:
#                 D[-1].append((start, end, label))
#             categories.add(label)
#     return D

categories = ['check', 'department', 'disease', 'drug', 'food',
              'physical_examination', 'producer', 'symptom']

# # 标注数据
# dev_output_split = './data/train/dev_split.json'
# valid_data = load_data(dev_output_split)
# categories = list(sorted(categories))
# print(categories)

'''
模型识别
'''
class medical_model:
    def __init__(self, config_path, checkpoint_path, dict_path, model_path):
        # current_dir = os.path.dirname(__file__)
        self.config_path = config_path
        self.checkpoint_path = checkpoint_path
        self.dict_path = dict_path
        # self.config_path = os.path.join(current_dir, 'model_package/chinese_bert/bert_config.json')
        # self.checkpoint_path = os.path.join(current_dir, 'model_package/chinese_bert/bert_model.ckpt')
        # self.dict_path = os.path.join(current_dir, 'model_package/chinese_bert/vocab.txt')
        self.learning_rate = 2e-5
        self.tokenizer = Tokenizer(self.dict_path, do_lower_case=True)

        os.environ['CUDA_VISIBLE_DEVICES'] = '2, 3'
        self.model = build_transformer_model(self.config_path, self.checkpoint_path)
        output = GlobalPointer(len(categories), 64)(self.model.output)

        self.model = Model(self.model.input, output)
        self.model.summary()

        self.model.compile(
            loss=self.global_pointer_crossentropy,
            optimizer=Adam(self.learning_rate),
            metrics=[self.global_pointer_f1_score]
        )
        self.model.load_weights(model_path)
        # self.model.load_weights(os.path.join(current_dir, 'model_result/best_model_cmeee_globalpointer.weights'))


    def recognize(self, text, threshold=0):
        tokens = self.tokenizer.tokenize(text, maxlen=512)
        mapping = self.tokenizer.rematch(text, tokens)
        token_ids = self.tokenizer.tokens_to_ids(tokens)
        segment_ids = [0] * len(token_ids)
        token_ids, segment_ids = to_array([token_ids], [segment_ids])
        scores = self.model.predict([token_ids, segment_ids])[0]
        scores[:, [0, -1]] -= np.inf
        scores[:, :, [0, -1]] -= np.inf
        entities = []
        for l, start, end in zip(*np.where(scores > threshold)):
            entities.append(
                (mapping[start][0], mapping[end][-1], categories[l])
            )
        return entities


    def global_pointer_crossentropy(self, y_true, y_pred):
        bh = K.prod(K.shape(y_pred)[:2])
        y_true = K.reshape(y_true, (bh, -1))
        y_pred = K.reshape(y_pred, (bh, -1))
        return K.mean(multilabel_categorical_crossentropy(y_true, y_pred))


    def global_pointer_f1_score(self, y_true, y_pred):
        y_pred = K.cast(K.greater(y_pred, 0), K.floatx())
        return 2 * K.sum(y_true * y_pred) / K.sum(y_true + y_pred)


    def predict(self, sentence):
        entities = self.recognize(sentence)
        result = []
        for e in entities:
            result.append({
                'start_idx': e[0],
                'end_idx': e[1],
                'type': e[2],
                'entity': sentence[e[0]: e[1]+1]
            })
        return result



actree = ACTree()

# cm = check_medical()

'''
区间合并：范围重合且类型一致，以大范围区间为准
'''
def result_filter(result_model, result_actree):
    for r in result_model:
        if r not in result_actree:
            result_actree.append(r)
    # for r in result_jieyu:
    #     if r not in result_actree:
    #         if actree.wdtype_dict.get(r.get('entity')) == r.get('type') or actree.wdtype_dict.get(r.get('entity')) is None:
    #             result_actree.append(r)
    return result_actree


def ner(sentence, config_path, checkpoint_path, dict_path, model_path):
    m = medical_model(config_path, checkpoint_path, dict_path, model_path)
    model_result = m.predict(sentence)
    ac_result = actree.check_medical(sentence)
    # jieyu_result = cm.filter(sentence)
    return result_filter(model_result, ac_result)


if __name__ == '__main__':
    sentence = '没有及时的盖被子，都会导致感冒的情况发生，下面我们一起了解下热感冒了吃什么好的快吧！风热感冒常伴有内火患者会出现咳嗽以及嗓子痒痛，在药物治疗的饿同时可以患者可以适当的吃冰糖雪梨茶，冰糖雪梨能够有效的去火，缓解患者因咽喉肿痛引起的咳嗽嗓子疼痛症状'
    current_dir = os.path.dirname(__file__)
    config_path = os.path.join(current_dir, 'model_package/chinese_bert/bert_config.json')
    checkpoint_path = os.path.join(current_dir, 'model_package/chinese_bert/bert_model.ckpt')
    dict_path = os.path.join(current_dir, 'model_package/chinese_bert/vocab.txt')
    model_path = os.path.join(current_dir, 'model_result/best_model_cmeee_globalpointer.weights')
    rs = ner(sentence, config_path, checkpoint_path, dict_path, model_path)
    print(rs)
    print(len(rs))
