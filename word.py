from wordcloud import WordCloud
 
string = 'Nowadays, machines like computers and mobile devices are developing towards having human-like behaviors and thoughts. However, they are unable to completely replace humans because of the high levels of uncertainty and vulnerability. It is expedient to combine humans and machines to complement disadvantages of each other. The previous computing methods are lack of a general definition and framework for combining humans and machines in a dynamic environment. This paper proposes a new concept on cooperation between humans and machines that can give more meaningful inspiration for future development of the filed; we call the proposed computing paradigm human–machine computing (HMC). HMC aims to provide a general framework for machines and humans working on a task interactively in an evolving environment, such that machines achieve optimized performance under human guidance during the computing procedure. In this paper, we describe HMC from six perspectives: definition, framework, challenges, technologies, comparisons, and case studies.'
wc = WordCloud(background_color='white',
               width=1000,
               height=800,
               collocations=True,
               ).generate(string)
wc.to_file('word.png') #保存图片