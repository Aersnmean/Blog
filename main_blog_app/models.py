from django.db import models


# 用户类
class User(models.Model):
    # 用户账户（手机号）
    account = models.CharField(max_length=11, primary_key=True)
    # 用户名
    username = models.CharField(max_length=20)
    # 账户密码
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.account

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'


# 文章类
class Post(models.Model):
    # 文章标题
    title = models.CharField(max_length=70)
    # 文章正文
    body = models.TextField()
    # 创建时间
    created_time = models.DateTimeField(auto_now_add=True)
    # 修改时间
    modified_time = models.DateTimeField(auto_now=True)
    # 文章摘要
    excerpt = models.CharField(max_length=200, blank=True)
    # 阅读量
    views = models.PositiveIntegerField(default=0)
    # 文章作者
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # # 自定义 get_absolute_url 方法
    # # 记得从 django.urls 中导入 reverse 函数
    # def get_absolute_url(self):
    #     return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_time']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            # md = markdown.Markdown(extensions=[
            #     'markdown.extensions.extra',
            #     'markdown.extensions.codehilite',
            # ])
            # # 先将 Markdown 文本渲染成 HTML 文本
            # # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # # 从文本摘取前 54 个字符赋给 excerpt
            # self.excerpt = strip_tags(md.convert(self.body))[:54]
            self.excerpt = self.body[:50]

        # 将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)


# 评论
class Review(models.Model):
    # 评论内容
    text = models.TextField()
    # 评论文章
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # 评论用户
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 评论时间
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_time']

