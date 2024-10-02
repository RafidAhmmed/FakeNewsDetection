from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from ml import CustomScraper as CS, SimilarityFinder as SF
from django.urls import reverse
from django.utils.http import urlencode

import torch
import torch.nn as nn
from transformers import AutoModel, BertTokenizerFast
import numpy as np


class HomeView(View):
    def get(self, request):
        return render(request, 'home/home.html')
    
    def post(self, request):
        if request.user.is_authenticated:
            form_type = request.POST.get('form_type')
            if form_type == 'check_news':
                query = request.POST.get('query')
                analysis_type = request.POST.get('analysis_type')
                if analysis_type == '1':
                    bert = AutoModel.from_pretrained('bert-base-uncased')
                    tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
                    class BERT_Arch(nn.Module):
                        def __init__(self, bert):
                            super(BERT_Arch, self).__init__()
                            self.bert = bert
                            self.dropout = nn.Dropout(0.1)            # dropout layer
                            self.relu =  nn.ReLU()                    # relu activation function
                            self.fc1 = nn.Linear(768,512)             # dense layer 1
                            self.fc2 = nn.Linear(512,2)               # dense layer 2 (Output layer)
                            self.softmax = nn.LogSoftmax(dim=1)       # softmax activation function
                        
                        def forward(self, sent_id, mask):           # define the forward pass
                            cls_hs = self.bert(sent_id, attention_mask=mask)['pooler_output']
                                                                        # pass the inputs to the model
                            x = self.fc1(cls_hs)
                            x = self.relu(x)
                            x = self.dropout(x)
                            x = self.fc2(x)                           # output layer
                            x = self.softmax(x)                       # apply softmax activation
                            return x
                    
                    # Load BERT model and tokenizer via HuggingFace Transformers

                    model = BERT_Arch(bert)
                    path = 'ml/trained_model.pt'
                    model.load_state_dict(torch.load(path), strict=False)
                    # testing on unseen data
                    unseen_news_text = [query]

                    # tokenize and encode sequences in the test set
                    MAX_LENGHT = 15
                    tokens_unseen = tokenizer.batch_encode_plus(
                        unseen_news_text,
                        max_length = MAX_LENGHT,
                        pad_to_max_length=True,
                        truncation=True
                    )

                    unseen_seq = torch.tensor(tokens_unseen['input_ids'])
                    unseen_mask = torch.tensor(tokens_unseen['attention_mask'])

                    with torch.no_grad():
                        preds = model(unseen_seq, unseen_mask)
                        preds = preds.detach().cpu().numpy()

                    preds = np.argmax(preds, axis = 1)
                    if preds[0] == 1:
                        context = {"content": "According to the training data, The Mentioned news is probably a Fake News"}
                        return render(request, 'home/show.html', context)
                    else:
                        context = {"content": "According to the training data, The Mentioned news is probably a Real News"}
                        return render(request, 'home/show.html', context)
                    
                elif analysis_type == '2':
                    customScraper = CS.CustomScraper(query)
                    customScraper.getNews()
                    similarityFinder = SF.SimilarityFinder(query)
                    similarityFinder.findSimilarity()
                    output = open('ml/final_output.txt', 'r', encoding='utf-8').read()
                    return render(request,'home/show.html',context={'content':output})
            elif form_type == 'print_report':
                # implement print feature
                return HttpResponse("Print feature is not implemented yet!")
        login_url = reverse('login') + '?' + urlencode({'next': request.path})
        return redirect(login_url)

class Profile(View):
    def get(self, request):
        pass
