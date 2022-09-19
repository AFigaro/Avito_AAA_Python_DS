from collections import Counter
from string import punctuation

class CountVectorizer:

    """
    Реализация CountVectorizer
    """

    def fit_transform(self, X, preprocess=False):

        """
        Превращает список предложений в терм-документную матрицу.
        NB: Метод чувствителен к регистру и знакам препинания

        Параметры:
        __________
            X : list of str
                Список предложений

            preprocess : bool, default=False
                препроцессинг предложений 
                (приведение к нижнему регистру 
                и удаление пунктуации)
        """

        if preprocess: 
            X_preproc = []
            for sentence in X:
                X_preproc.append(
                    ''.join([letter.lower() for letter in sentence if letter not in punctuation])
                    )  # Для удаления пунктуации используется модуль punctuation

            X = X_preproc # Заменяем исходный корпус на предобработанный

        self.word_set = Counter(" ".join(X).split()).keys() # Тут использую Counter для того, чтобы хранить порядок слов в корпусе
        term_matrix = []
        for sentence in X:
            word_frequency = Counter(sentence.split()) # Тут храним частоты слов по одному предложению (документу)
            term_matrix.append(
                [word_frequency[word] if word in sentence.split() else 0 for word in self.word_set]
                )
        
        return term_matrix
    
    def get_feature_names(self):
        
        """
        Возвращает список терминов всего корпуса
        """

        return list(self.word_set)

if __name__ == '__main__':
    corpus = [
            'Crock Pot Pasta Never boil pasta again',
            'Pasta Pomodoro Fresh ingredients Parmesan to taste'
             ]
    vectorizer = CountVectorizer()
    count_matrix = vectorizer.fit_transform(corpus, preprocess=True)

    print(count_matrix)
    print(vectorizer.get_feature_names())
