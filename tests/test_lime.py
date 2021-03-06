# -*- coding: utf-8 -*-
from __future__ import absolute_import

from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.naive_bayes import MultinomialNB

from eli5.lime import get_local_pipeline_text
from eli5.sklearn import explain_prediction_sklearn
from eli5.formatters import format_as_text
from sklearn.pipeline import make_pipeline


def test_lime_explain_probabilistic(newsgroups_train):
    docs, y, target_names = newsgroups_train
    vec = HashingVectorizer(non_negative=True)
    clf = MultinomialNB()

    X = vec.fit_transform(docs)
    clf.fit(X, y)

    pipe = make_pipeline(vec, clf)
    doc = docs[0]

    clf_local, vec_local, metrics = get_local_pipeline_text(doc,
                                                            pipe.predict_proba,
                                                            n_samples=5000,
                                                            expand_factor=10)
    print(metrics)
    assert metrics['score'] > 0.7

    res = explain_prediction_sklearn(clf_local, doc, vec_local, top=10,
                                     target_names=target_names)
    expl = format_as_text(res)
    print(expl)
    assert 'file' in expl
