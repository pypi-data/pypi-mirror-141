#!/usr/bin/env python
# coding: utf-8

from Huatuo import huatuo

'''
NER model used for medical 
'''
def diagnosis(sentence, config_path, checkpoint_path, dict_path, model_path):
    return huatuo.ner(sentence, config_path, checkpoint_path, dict_path, model_path)