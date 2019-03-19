from django.db import models

class CeleryTaskResultExtensionModel(models.Model):
    '''
        扩展 celery task 执行结果表; 因为 celery 保存的 task 执行结果,相关内容不全,如 执行的worker,执行时间等;
        这里是持久化 flower api 的结果,比 celery 原生保存在数据库的内容更全
    '''
    uuid = models.CharField("任务 id",unique=True,max_length=50,help_text="自动生成的任务ID")
    name = models.CharField("任务名称",null=True, max_length=255, help_text="任务名称")
    state = models.CharField("任务执行状态",max_length=50, help_text="任务执行状态")
    received = models.CharField("接收任务时间",max_length=50,null=True,help_text="接收任务的时间")
    sent = models.CharField("暂不清楚",max_length=100,null=True,blank=True,help_text="暂时不清楚")
    started = models.CharField("任务开始执行时间",max_length=50,null=True,blank=True,help_text="任务开始执行时间")
    rejected = models.CharField("是否被拒绝执行",max_length=10,null=True,blank=True,help_text="是否被拒绝执行")
    succeeded = models.CharField("任务执行成功时间",max_length=50,null=True,blank=True,help_text="任务执行成功的时间")
    failed = models.CharField("任务执行失败时间",max_length=50,null=True,blank=True,help_text="任务执行失败的时间")
    retried = models.CharField("已经重试的次数",max_length=10,null=True,blank=True,help_text="已经重试的次数")
    revoked = models.CharField("任务是否被撤销",max_length=10,null=True,blank=True,help_text="任务是否被撤销")
    args = models.TextField("任务位置参数",null=True,blank=True,help_text="传给任务的位置参数")
    kwargs = models.TextField("任务关键字参数",null=True,blank=True,help_text="传给任务的关键字参数")
    eta = models.CharField("任务预期执行时间",max_length=50,null=True,blank=True,help_text="任务预期执行的时间")
    expires = models.CharField("任务过期时间",max_length=50,null=True,blank=True,help_text="任务过期时间")
    retries = models.CharField("任务重试次数",max_length=50,null=True,blank=True,help_text="任务重试次数")
    worker = models.CharField("执行任务的worker",max_length=100,null=True,blank=True,help_text="执行任务的worker")
    result = models.TextField("任务执行结果",null=True,blank=True,help_text="任务执行的结果")
    exception = models.TextField("异常信息",null=True,blank=True,help_text="任务执行时的异常信息")
    timestamp = models.CharField("未知时间",max_length=50,null=True,blank=True,help_text="暂不清楚是什么时间")
    runtime = models.CharField("任务运行时长",max_length=10,null=True,blank=True,help_text="任务执行的时长")
    traceback = models.TextField("任务执行时的异常信息追踪",blank=True, null=True, help_text="任务执行时的异常信息追踪")
    exchange = models.CharField("交换器名称",max_length=100,null=True,blank=True,help_text="任务使用的交换器名称")
    routing_key = models.CharField("路由键名称",max_length=100,null=True,blank=True,help_text="任务使用的路由键名称")
    clock = models.CharField("暂不清楚",max_length=50,null=True,blank=True,help_text="暂不清楚")
    client = models.CharField("暂不清楚",max_length=50,null=True,blank=True,help_text="暂不清楚")
    root = models.CharField("暂不清楚",max_length=50,null=True,blank=True,help_text="暂不清楚")
    root_id = models.CharField("暂不清楚", max_length=50, null=True, blank=True, help_text="暂不清楚")
    parent = models.CharField("暂不清楚", max_length=50, null=True, blank=True, help_text="暂不清楚")
    parent_id = models.CharField("暂不清楚", max_length=50, null=True, blank=True, help_text="暂不清楚")
    children = models.CharField("暂不清楚", max_length=100, null=True, blank=True, help_text="暂不清楚")
    create_time = models.DateTimeField("添加时间", auto_now_add=True, null=True, help_text="添加时间")

    def __str__(self):
        return self.uuid

    class Meta:
        verbose_name = "celery 任务执行结果表"
        db_table = "taskschedule_task_reuslt"