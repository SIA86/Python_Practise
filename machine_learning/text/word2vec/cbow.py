import tensorflow as tf
import numpy as np
import string
from scipy.spatial.distance import cosine
print(tf.__version__)


class Word2Vec:
    def __init__(self, vocab_size, embedding_dim=16, optimizer='sgd', epochs=10000):
        self.vocab_size=vocab_size
        self.embedding_dim=embedding_dim
        self.epochs=epochs
        if optimizer=='adam':
            self.optimizer = tf.optimizers.Adam()
        else:
            self.optimizer = tf.optimizers.SGD(learning_rate=0.1)

    def train(self, x_train=None, y_train=None):
        self.W1 = tf.Variable(tf.random.normal([self.vocab_size, self.embedding_dim]))
        self.b1 = tf.Variable(tf.random.normal([self.embedding_dim])) #bias
        self.W2 = tf.Variable(tf.random.normal([self.embedding_dim, self.vocab_size]))
        self.b2 = tf.Variable(tf.random.normal([self.vocab_size]))
        for _ in range(self.epochs):
            with tf.GradientTape() as t:
                hidden_layer = tf.add(tf.matmul(x_train,self.W1),self.b1)
                output_layer = tf.nn.softmax(tf.add( tf.matmul(hidden_layer, self.W2), self.b2))
                cross_entropy_loss = tf.reduce_mean(-tf.math.reduce_sum(y_train * tf.math.log(output_layer), axis=[1]))
            grads = t.gradient(cross_entropy_loss, [self.W1, self.b1, self.W2, self.b2])
            self.optimizer.apply_gradients(zip(grads,[self.W1, self.b1, self.W2, self.b2]))
            if(_ % 1000 == 0):
                print(cross_entropy_loss)
    
    
    def vectorized(self, word_idx):
        return (self.W1+self.b1)[word_idx]


corpus_raw = """ He was not studying medicine. He had himself, in reply to a question, confirmed Stamford’s opinion upon that point. Neither did he appear to have pursued any course of reading which might
fit him for a degree in science or any other recognized portal which would give him an entrance into the learned world. Yet his zeal for certain studies was remarkable, and within eccentric limits his knowledge was so extraordinarily ample
and minute that his observations have fairly astounded me"""

corpus_raw = corpus_raw.lower()
# raw sentences is a list of sentences.
raw_sentences = corpus_raw.split('.')
sentences = []
for sentence in raw_sentences:
    sentences.append(sentence.translate(str.maketrans(dict.fromkeys(string.punctuation))).split())

data = []
WINDOW_SIZE = 2
for sentence in sentences:
    for word_index, word in enumerate(sentence):
        for nb_word in sentence[max(word_index - WINDOW_SIZE, 0) : min(word_index + WINDOW_SIZE, len(sentence)) + 1] :
            if nb_word != word:
                data.append([word, nb_word])
words = []
for word in corpus_raw.translate(str.maketrans(dict.fromkeys(string.punctuation))).split():
    words.append(word)
words = set(words) # so that all duplicate words are removed
word2int = {}
int2word = {}
vocab_size = len(words) # gives the total number of unique words
for i,word in enumerate(words):
    word2int[word] = i
    int2word[i] = word


def to_one_hot(data_point_index, vocab_size):
    temp = np.zeros(vocab_size)
    temp[data_point_index] = 1
    return temp

x_train = [] # input word
y_train = [] # output word
for data_word in data:
    x_train.append(to_one_hot(word2int[ data_word[0] ], vocab_size))
    y_train.append(to_one_hot(word2int[ data_word[1] ], vocab_size))
# convert them to numpy arrays
x_train = np.asarray(x_train, dtype='float32')
y_train = np.asarray(y_train, dtype='float32')

w2v = Word2Vec(vocab_size=vocab_size, optimizer='adam', epochs=10000)
w2v.train(x_train, y_train)


def distance(w1, w2):
    return cosine(w1, w2)


def closest_words(word):
    distances = {
        w: distance(w2v.vectorized(word2int[word]), w2v.vectorized(word2int[w]))
        for w in (word2int)
    }
    return sorted(distances, key=lambda w: distances[w])[:10]


def closest_word(embedding):
    return closest_words(embedding)[0]