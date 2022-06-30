from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
import numpy as np
import lexvec
import words
import json
from past_games import load_historic

LEXVEC_MODEL_PATH = 'models/lexvec.commoncrawl.ngramsubwords.300d.W.pos.bin'
LEXVEC_MODEL = lexvec.Model(LEXVEC_MODEL_PATH)
FREQS = words.load_freqs()
WORDS = words.load_words()

historic_raw = load_historic()
valid = []
invalid = []
limit = 1000
for i, h in enumerate(historic_raw.values()):
    if i > limit:
        break
    valid += h['valid']
    invalid += h['invalid']

# balance valid and invalid (should I remove this step?)
# valid = valid[:len(invalid)]
# invalid = invalid[:len(valid)]

print(len(valid), len(invalid))

words = valid + invalid


def embed_word(w: str):
    lexical_embedding = LEXVEC_MODEL.word_rep(w)
    freq = 0
    if w in FREQS:
        freq = FREQS[w] / 1000000
    return np.append(lexical_embedding, freq)


print('Embedding words...')
embeddings = [embed_word(w) for w in words]
features = np.array(embeddings)
labels = np.concatenate(
    [np.ones([len(valid)]), np.zeros([len(invalid)])])

print(np.shape(features))
print(np.shape(labels))

# Split our data
print('Splitting data...')
train, test, train_labels, test_labels = train_test_split(features,
                                                          labels,
                                                          test_size=0.1,
                                                          random_state=42)

# scale data to have more well behaved mean and variance
scaler = preprocessing.StandardScaler().fit(train)
train = scaler.transform(train)
test = scaler.transform(test)  # is this right?

# Initialize our classifier
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(32), max_iter=800, random_state=1)

# Train our classifier
model = clf.fit(train, train_labels)

# Evaluate accuracies
print('Train Accuracy:', accuracy_score(train_labels, clf.predict(train)))
print('Test Accuracy:', accuracy_score(test_labels, clf.predict(test)))

model.predict_proba(test)


def validity(words: list[str]):
    embeddings = [embed_word(w) for w in words]
    return model.predict_proba(embeddings)[:, 1]


validities = {w: v for w, v in zip(WORDS, validity(WORDS))}
with open('data/word_validities.json', mode='w') as f:
    json.dump(validities, f)
