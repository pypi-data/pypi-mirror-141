# -*- coding = utf-8 -*-
# @time: 2022/3/4 3:18 下午
# @Author: erazhan
# @File: main_qa.py

# ----------------------------------------------------------------------------------------------------------------------

# -*- coding = utf-8 -*-
# @time: 2022/3/1 1:37 下午
# @Author: erazhan
# @File: main_mitc.py

# ----------------------------------------------------------------------------------------------------------------------
import os
import copy

from transformers import BertTokenizer

from erazhan_utils import read_json_file

from erazhan_algorithms.QA import init_qa_model, train_qa,eval_qa,predict_on_batch_qa
from erazhan_algorithms.QA import get_qa_params_help,get_qa_parser,QA_DEFAULT_PARAM_DICT,QA_OTHER_PARAM_DICT
from erazhan_algorithms.QA import generate_qa_tokens

QA_DEFAULT_PARAM_DICT = {"gpu": 1,
                         "maxlen": 256,
                         "batch_size": 64,
                         "predict_batch_size": 4,
                         "learning_rate": 2e-5,
                         "warmup_proportion": 0.1,
                         "epochs": 10,
                         "save_steps": 500,
                         "print_steps": 20,
                         "disable": False}

QA_OTHER_PARAM_DICT = {"bert_model": "/home/zhanjiyuan/code/pretrained_model/chinese-roberta-wwm-ext",
                         "train_file": "./data/test_train_qa_v1.json",
                         "eval_file": "./data/test_eval_qa_v1.json",
                         "output_dir": "./model_qa_e10_doc",
                         "predict_dir": "./model_qa_e10_doc",
                         }

os.environ["CUDA_VISIBLE_DEVICES"] = "%d"%QA_DEFAULT_PARAM_DICT["gpu"]

def train_or_eval_from_eralgo(mode = "train"):

    param_dict = copy.deepcopy(QA_DEFAULT_PARAM_DICT)
    param_dict.update(QA_OTHER_PARAM_DICT)

    qa_args = get_qa_parser(param_dict)
    tokenizer = BertTokenizer.from_pretrained(qa_args.bert_model)

    train_data = read_json_file(param_dict["train_file"])
    eval_data = read_json_file(param_dict["eval_file"])

    # return
    if mode == "train":
        kwargs = {"args": qa_args,
                  "train_data": train_data,
                  "eval_data": eval_data,
                  "tokenizer": tokenizer}
        train_qa(**kwargs)
    elif mode == "eval":
        eval_kwargs = {"args": qa_args, "tokenizer": tokenizer}
        model = init_qa_model(qa_args, from_scratch = False)
        eval_qa(model,eval_data,**eval_kwargs)
        # eval_qa(model, text_list = eval_text, label_list = eval_intent_labels, **eval_kwargs)
    else:

        model = init_qa_model(qa_args, from_scratch=False)

        for_intent_list = ["询问身高","询问体重","询问过敏史","询问体温"]
        question = "孩子的身高体重是多少？"
        answer = "98斤"

        data_list = []
        for one_intent in for_intent_list:
            one_data = generate_qa_tokens(question=question, answer = answer,maxlen = qa_args.maxlen, question_intent = one_intent)
            data_list.append(one_data)

        eval_kwargs = {"args": qa_args, "tokenizer": tokenizer}
        start_target_list, end_target_list = predict_on_batch_qa(model, data_list, **eval_kwargs)

        for i,one_data in enumerate(data_list):
            tokens = one_data["tokens"]
            start_pos = start_target_list[i]
            end_pos = end_target_list[i]

            pred_entity = "".join(tokens[start_pos:end_pos+1])
            print("tokens:\n",tokens)
            print("pred_entity:\n",pred_entity, start_pos, end_pos)
            print("-"*50)

if __name__ == "__main__":

    get_qa_params_help()
    mode = "train"
    mode = "eval"
    mode = "test"
    train_or_eval_from_eralgo(mode = mode)

    pass

