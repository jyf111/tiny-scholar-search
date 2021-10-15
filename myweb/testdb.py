from django.http import HttpResponse
from scholar.models import Author
 
# 数据库操作
def testdb(request):
    # 初始化
    response = ""
    response1 = ""
    
    
    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    list = Author.objects.all()
    # filter相当于SQL中的WHERE，可设置条件过滤结果
    # response2 = Author.objects.filter(id=1) 
    
    # # 获取单个对象
    # response3 = Author.objects.get(id=2) 

    return HttpResponse("<p>" + 'OK' + "</p>")