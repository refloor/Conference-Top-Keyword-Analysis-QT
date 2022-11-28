from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPalette, QBrush, QPixmap
from pandas import read_csv
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt 
import numpy as np
from wordcloud import WordCloud
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

    def handleCalc(self):
        year = self.ui.comboBox_1.currentText()
        conference = self.ui.comboBox_2.currentText()
        self.num_keyword = self.ui.lineEdit_8.text()
        drawgraph = DrawGraph(year,conference,self.banned,self.num_keyword)
        drawgraph.compute_word()
        drawgraph.frequent_graph()
        drawgraph.word_cloud_graph()
        
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
            self.ui.comboBox_1.addItems(years)
        if(conference_index == 1):
            years = {'2019','2021'}
            self.ui.comboBox_1.addItems(years)
        if(conference_index == 2):
            years = {'2020','2021','2022'}
            self.ui.comboBox_1.addItems(years)
        
    def graph_display(self):
        frequent = QPixmap('frequent.png')
        self.ui.label.setPixmap(frequent)
        wordcloud = QPixmap('wordcloud.png')
        self.ui.label_2.setPixmap(wordcloud)


class DrawGraph:

    def __init__(self,year,conference,banned,num_keyword):
        self.year = year
        self.conference = conference
        self.banned = banned
        self.num_keyword = num_keyword

    def compute_word(self):
        file_name = self.conference + '_' + self.year + '.csv'
        #读取标题
        df = read_csv('./data/'+file_name,usecols = ['Title'])
        #转换为list
        title = df.values.tolist()

        # self.banned = ['learning', 'network', 'neural', 'networks', 'deep', 'via', 'using', 'convolutional', 'single']
        
        self.keyword_list = []
        for i in range(len(title)):
            # print(i, "th paper's title : ", title[i])
            #将数组转换成string 再分割
            word_list = "".join(title[i]).split(" ")
            word_list = list(set(word_list))
            word_list_cleaned = [] 
            for word in word_list: 
                word = word.lower()
                if word not in stopwords.words('english') and word not in self.banned: #remove stopwords
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
        plt.savefig('frequent.png', transparent=False, bbox_inches='tight')

    def word_cloud_graph(self):
        # Show the word cloud forming by keywords
        
        wordcloud = WordCloud(max_font_size=64, max_words=160, 
                            width=1280, height=640,
                            background_color="black").generate(' '.join(self.keyword_list))
        plt.figure(figsize=(16, 8))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig('wordcloud.png', transparent=False, bbox_inches='tight')
        # plt.show()

# class WordList:
#     def __init__(self):
        
    


app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec()