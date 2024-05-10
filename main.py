from answer import Answer
from word import Word

if __name__ == '__main__':
    word = Word()
    answer = Answer()

    n = int(input("输入单词个数"))
    for i in range(n):
        word.routine()

    word_dic = word.get_dic()

    m = int(input("输入测试个数"))
    for k in range(m):
        answer.routine(word_dic)

    answer.show_result()
