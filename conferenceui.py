from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPalette, QBrush, QPixmap
from pandas import read_csv
# import nltk
# nltk.download('stopwords')
# from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt 
import numpy as np
# from wordcloud import WordCloud
class Stats:
    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('conference.ui')

        #tab1 的按钮连接
        self.ui.pushButton.clicked.connect(self.handleCalc)
        # self.ui.comboBox_1.currentIndexChanged.connect(self.selectionchange)
        #self.ui.label_1

        #tab2 显示提示词
        self.banned = ['learning', 'network', 'neural', 'networks', 'deep', 'via', 'using', 'convolutional', 'single']
        self.display_word()

        #tab2 add banned word
        self.ui.pushButton_3.clicked.connect(self.add_word)
        #tab2 del banned word
        self.ui.pushButton_5.clicked.connect(self.del_word)
        #tab3 展示词语数量
        self.ui.pushButton_6.clicked.connect(self.change_number)
        #tab3 提交表单
        self.ui.pushButton_2.clicked.connect(self.handleCalc)
        #二级下拉菜单 会议与年份对应
        self.ui.comboBox_2.currentIndexChanged.connect(self.conference_menu)

        #读取文件
        self.data = read_csv('./data/conference.csv')

    def handleCalc(self):
        year = self.ui.comboBox_1.currentText()
        conference = self.ui.comboBox_2.currentText()
        self.num_keyword = self.ui.lineEdit_8.text()
        drawgraph = DrawGraph(year,conference,self.banned,self.num_keyword,self.data)
        drawgraph.compute_word()
        drawgraph.frequent_graph()
        # drawgraph.word_cloud_graph()
        
        #更新图片展示
        self.ui.label.update()
        self.ui.label.repaint()
        self.ui.tabWidget.update()
        self.graph_display()
    
    def add_word(self):
        word_obj = self.ui.lineEdit_4.text()
        if(word_obj not in self.banned):
            self.banned.append(word_obj)
        self.display_word()

    def del_word(self):
        word_obj = self.ui.lineEdit_7.text()
        if(word_obj in self.banned):
            self.banned.remove(word_obj)
        self.display_word()

    def change_number(self):
        word_number = self.ui.lineEdit_8.text()
        self.num_keyword = word_number

    def display_word(self):
        self.ui.textBrowser.clear()
        for word in self.banned:
            self.ui.textBrowser.append(word)
        self.cursot = self.ui.textBrowser.textCursor()
        self.ui.textBrowser.moveCursor(self.cursot.End)
        QApplication.processEvents()
    
    def conference_menu(self):
        conference_index= self.ui.comboBox_2.currentIndex()
        self.ui.comboBox_1.clear()
        if(conference_index == 0):
            years = {'2013','2014','2015','2016','2017','2018','2019','2020','2021','2022'}
            #使用sorted使set按照顺序显示
            self.ui.comboBox_1.addItems(sorted(years))
        if(conference_index == 1):
            years = {'2013','2015','2017','2019','2021'}
            self.ui.comboBox_1.addItems(sorted(years))
        if(conference_index == 2):
            years = {'2020','2021','2022'}
            self.ui.comboBox_1.addItems(sorted(years))
        
    def graph_display(self):
        frequent = QPixmap('./data/frequent.png')
        self.ui.label.setPixmap(frequent)
        wordcloud = QPixmap('./data/wordcloud.png')
        self.ui.label_2.setPixmap(wordcloud)


class DrawGraph:

    def __init__(self,year,conference,banned,num_keyword,data):
        self.year = year
        self.conference = conference
        self.banned = banned
        self.num_keyword = num_keyword
        self.data = data

    def compute_word(self):
        rule = "Year == " + self.year + "& Conference == \"" + self.conference+ "\""
        #读取标题
        data_object = self.data.query(rule)
        title = data_object.iloc[:,0]
        
        #转换为list
        title = title.values.tolist()

        #from nltk.corpus import stopwords
        stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
        
        self.keyword_list = []
        for i in range(len(title)):
            # print(i, "th paper's title : ", title[i])
            #将数组转换成string 再分割
            word_list = "".join(title[i]).split(" ")
            word_list = list(set(word_list))
            word_list_cleaned = [] 
            for word in word_list: 
                word = word.lower()
                if word not in stopwords and word not in self.banned: #remove stopwords
                    word_list_cleaned.append(word)  
            for k in range(len(word_list_cleaned)):
                self.keyword_list.append(word_list_cleaned[k])

        self.keyword_counter = Counter(self.keyword_list)

        # Merge duplicates: CNNs and CNN
        duplicates = []
        for k in self.keyword_counter:
            if k+'s' in self.keyword_counter:
                duplicates.append(k)
        for k in duplicates:
            self.keyword_counter[k] += self.keyword_counter[k+'s']
            del self.keyword_counter[k+'s']

    def frequent_graph(self):
        # Show N most common keywords and their frequencies
        # self.num_keyword = 30 #FIXME
        self.num_keyword = int(self.num_keyword)
        keywords_counter_vis = self.keyword_counter.most_common(self.num_keyword)

        plt.rcdefaults()
        fig, ax = plt.subplots(figsize=(8, 18))

        key = [k[0] for k in keywords_counter_vis] 
        value = [k[1] for k in keywords_counter_vis] 
        y_pos = np.arange(len(key))
        ax.barh(y_pos, value, align='center', color='green', ecolor='black', log=True)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(key, rotation=0, fontsize=10)
        ax.invert_yaxis() 
        for i, v in enumerate(value):
            ax.text(v + 3, i + .25, str(v), color='black', fontsize=10)
        ax.set_xlabel('Frequency')
        ax.set_title('{} {} Submission Top {} Keywords'.format(self.conference.upper(), self.year, self.num_keyword))
        plt.savefig('./data/frequent.png', transparent=False, bbox_inches='tight')

    # def word_cloud_graph(self):
    #     # Show the word cloud forming by keywords
        
    #     wordcloud = WordCloud(max_font_size=64, max_words=160, 
    #                         width=1280, height=640,
    #                         background_color="black").generate(' '.join(self.keyword_list))
    #     plt.figure(figsize=(16, 8))
    #     plt.imshow(wordcloud, interpolation="bilinear")
    #     plt.axis("off")
    #     plt.savefig('./data/wordcloud.png', transparent=False, bbox_inches='tight')
    #     # plt.show()

# class WordList:
#     def __init__(self):
        
    


app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec()