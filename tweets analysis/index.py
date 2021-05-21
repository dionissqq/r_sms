from data_extractor import get_tweets_by_user
from preprocessing import preprocess_tweet
import tensorflow as tf
import tensorflow_hub as hub 
from consts import themes
import numpy as np

module_url = "https://tfhub.dev/google/tf2-preview/gnews-swivel-20dim/1"

hub_layer=hub.KerasLayer(module_url, input_shape=[], output_shape=[20], dtype=tf.string, trainable=False)

model = tf.keras.models.Sequential([
    hub_layer,
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(20)                                    
])

model.compile(optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy'])

model.load_weights('../model/my_h5_model.h5')

while True:
    print('enter username')
    username = input()

    tweets = []
    json_res = get_tweets_by_user(username)
    if 'data' in json_res.keys():
        for el in json_res['data']: 
            tweets.append(preprocess_tweet(el['text']))
        
        predicts = np.zeros(20)
        for el in tweets:
            # print(el)
            el_predicts = model.predict([el])
            predicts += np.squeeze(el_predicts)
            # category = themes[np.argmax(predicts)]
            # print(category)
            # number_of_recs[category] = number_of_recs.get('category', 0) + 1
        category = themes[np.argmax(predicts)]
        print('results : ', category)  
    else:
        print('no_records')
