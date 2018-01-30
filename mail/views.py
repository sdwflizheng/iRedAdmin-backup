from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
#from django.db import IntegrityError
from django.db.utils import IntegrityError
from .models import Domain,MailBox,Forwardings,UserQuota,Alias
from mylib.iredutils import generate_password_hash,generate_maildir_path

from mylib.utils import get_logger, str_to_datetime

logger = get_logger("view")

class DomainListView(LoginRequiredMixin,TemplateView):
    """
    显示
    """
    template_name = 'mail/domain.html'

    def get_context_data(self, **kwargs):
        context = {
            # 'app': 'Assets',
            # 'action': 'Asset list',
        }
        kwargs.update(context)
        return super(DomainListView, self).get_context_data(**kwargs)

class DomainAddView(LoginRequiredMixin,TemplateView):
    """
    添加
    """
    template_name = 'mail/domainadd.html'
    model = Domain

    #显示添加模板
    def get_context_data(self, **kwargs):

        context = {
            # 'action': 'Asset list',
        }
        kwargs.update(context)
        return super(DomainAddView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        domain = request.POST.get("domain")

        if domain == "":
            data={"code":0,"msg":"邮件域不能为空"}
            return JsonResponse(data)
        try:
            ormdata = self.model.objects.create(domain=domain)

            ormdata.save()
            data={"code":1,"msg":msg}
        except IntegrityError as e:
            #得到异常消息
            msg=str(e.__cause__)
            logger.error(e.__cause__)
            data={"code":0,"msg":msg}

        return JsonResponse(data)

class DomainEditView(LoginRequiredMixin,TemplateView):
    """
    编辑
    """
    template_name = 'mail/domainedit.html'
    model = Domain

    def get(self, request, *args, **kwargs):
        """
        得到提交的ids
        """
        self.id = request.GET.get('id')
        #根据id得到数据
        self.domain = self.model.objects.get(id=self.id)

        return super(DomainEditView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            'id': self.id,
            'domain': self.domain
        }
        kwargs.update(context)
        return super(DomainEditView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        _id = request.POST.get('id')
        domain = request.POST.get("domain")

        if domain == "":
            data={"code":0,"msg":"邮件域不能为空"}
            return JsonResponse(data)

        msg=""

        try:
            ormdata = self.model.objects.get(id=_id)
            ormdata.domain=domain

            ormdata.save()
            data={"code":1,"msg":msg}
        except IntegrityError as e:
            #得到异常消息
            msg=str(e.__cause__)
            #msg = "游戏名已经存在"
            logger.error(e.__cause__)
            data={"code":0,"msg":msg}

        return JsonResponse(data)

class DomainDelView(LoginRequiredMixin,TemplateView):
    """
    删除
    """
    model = Domain

    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        #得到批量或者单个要删除的id
        domain = request.POST.get("domain")

        msg="操作成功"

        num = MailBox.objects.filter(domain=domain).count()

        if num != 0:
            msg = "关联用户存在，禁止删除"
            data={"code":0,"msg":msg}
        else:
            self.model.objects.filter(domain=domain).delete()
            data={"code":1,"msg":msg}

        return JsonResponse(data)

class UserListView(LoginRequiredMixin,TemplateView):
    """
    显示
    """
    template_name = 'mail/user.html'

    def get_context_data(self, **kwargs):
        context = {
            # 'app': 'Assets',
            # 'action': 'Asset list',
        }
        kwargs.update(context)
        return super(UserListView, self).get_context_data(**kwargs)

class UserAddView(LoginRequiredMixin,TemplateView):
    """
    添加
    """
    template_name = 'mail/useradd.html'
    model = MailBox

    #显示添加模板
    def get_context_data(self, **kwargs):
        
        domain = Domain.objects.all()
        html_domain = []

        for i in domain:
            html_domain.append('<option value="%s">%s</option>' % (i.domain,i.domain))

        context = {
            'html_domain': html_domain,
        }
        kwargs.update(context)
        return super(UserAddView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        username = request.POST.get("username")
        domain = request.POST.get("domain")
        password = request.POST.get("row[password]")
        pwdAgain = request.POST.get("row[pwdAgain]")
        name = request.POST.get("name")
        quota = request.POST.get("quota")

        if username == "":
            data={"code":0,"msg":"用户名不能为空"}
            return JsonResponse(data)

        if password != pwdAgain:
            data={"code":0,"msg":"两次密码不一致"}
            return JsonResponse(data)
        #默认1G空间
        if quota == "":
            quota = 1024

        #没有填写显示名称
        if name == "" or name == None:
            name = username

        username=username + '@' + domain
        date1970 = str_to_datetime('1970-01-01 01:01:01')
        expired = str_to_datetime('9999-12-31 00:00:00')
        
        msg = ''
        try:
            ormdata = self.model.objects.create(username=username,
                                                name = name,
                                                password = generate_password_hash(password),
                                                maildir = generate_maildir_path(username),
                                                language = 'zh_CN',
                                                quota = quota,
                                                passwordlastchange = date1970,
                                                modified = date1970,
                                                expired = expired,
                                                local_part = username,
                                                domain=domain
            )

            ormdata.save()

            forward_ormdata = Forwardings.objects.create(address=username,
                                                        forwarding=username,
                                                        domain = domain,
                                                        is_forwarding=1,
                                                        dest_domain=domain
            )
            forward_ormdata.save()
            data={"code":1,"msg":msg}
        except IntegrityError as e:
            #得到异常消息
            msg=str(e.__cause__)
            logger.error(e.__cause__)
            data={"code":0,"msg":msg}

        return JsonResponse(data)

class UserEditView(LoginRequiredMixin,TemplateView):
    """
    编辑
    """
    template_name = 'mail/useredit.html'
    model = MailBox

    def get(self, request, *args, **kwargs):
        """
        得到提交的ids
        """
        username = request.GET.get('username')
        #根据id得到数据
        self.user = self.model.objects.filter(username=username).values('username','name','quota')[0]

        return super(UserEditView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            'user': self.user
        }
        kwargs.update(context)
        return super(UserEditView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        username = request.POST.get('username')
        name = request.POST.get("name")
        quota = request.POST.get("quota")

        if username == "":
            data={"code":0,"msg":"显示名称不能为空"}
            return JsonResponse(data)

        #默认1G空间
        if quota == "":
            quota = 1024

        msg=""

        try:
            self.model.objects.filter(username=username).update(name=name,quota=quota)

            data={"code":1,"msg":msg}
        except IntegrityError as e:
            #得到异常消息
            msg=str(e.__cause__)
            #msg = "游戏名已经存在"
            logger.error(e.__cause__)
            data={"code":0,"msg":msg}

        return JsonResponse(data)

class UserDelView(LoginRequiredMixin,TemplateView):
    """
    删除
    """
    model = MailBox

    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        #得到批量或者单个要删除的id
        username = request.POST.get("username")

        msg="操作成功"

        self.model.objects.filter(username=username).delete()
        Forwardings.objects.filter(address=username).delete()
        data={"code":1,"msg":msg}

        return JsonResponse(data)

class MakeStatusView(LoginRequiredMixin,TemplateView):
    """
    更改状态
    """

    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        active = request.POST.get("status")
        username = request.POST.get("username")
        op_type = request.POST.get("type")
        domain = request.POST.get("domain")

        msg=""

        if op_type == 'user':
            MailBox.objects.filter(username=username).update(active=active)
            Forwardings.objects.filter(address=username).update(active=active)
        elif op_type == 'domain':
            Domain.objects.filter(domain=domain).update(active=active)
        else:
            data={"code":0,"msg":'未知操作类型'}
            return JsonResponse(data)

        data={"code":1,"msg":msg}
        return JsonResponse(data)

class MakePasswordView(LoginRequiredMixin,TemplateView):
    """
    密码重置
    """
    template_name = 'mail/userpassword.html'
    model = MailBox

    def get(self, request, *args, **kwargs):
        """
        得到提交的ids
        """
        self.username = request.GET.get('username')

        return super(MakePasswordView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):

        context = {
            'username': self.username
        }
        kwargs.update(context)
        return super(MakePasswordView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        username = request.POST.get("username")
        password = request.POST.get("row[password]")
        pwdAgain = request.POST.get("row[pwdAgain]")

        if password != pwdAgain:
            data={"code":0,"msg":"两次密码不一致"}
            return JsonResponse(data)

        msg=""

        MailBox.objects.filter(username=username).update(password=generate_password_hash(password))

        data={"code":1,"msg":msg}
        return JsonResponse(data)


class GroupListView(LoginRequiredMixin,TemplateView):
    """
    显示
    """
    template_name = 'mail/group.html'

    def get_context_data(self, **kwargs):
        context = {
            # 'app': 'Assets',
            # 'action': 'Asset list',
        }
        kwargs.update(context)
        return super(GroupListView, self).get_context_data(**kwargs)

class GroupAddView(LoginRequiredMixin,TemplateView):
    """
    添加
    """
    template_name = 'mail/groupadd.html'
    model = Alias

    #显示添加模板
    def get_context_data(self, **kwargs):
        
        domain = Domain.objects.all()
        html_domain = []

        for i in domain:
            html_domain.append('<option value="%s">%s</option>' % (i.domain,i.domain))

        context = {
            'html_domain':html_domain
        }
        kwargs.update(context)
        return super(GroupAddView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        address = request.POST.get("address")
        domain = request.POST.get("domain")
        name = request.POST.get("name")
        users = request.POST.getlist("users")

        if address == "":
            data={"code":0,"msg":"用户名不能为空"}
            return JsonResponse(data)

        if users=="":
            data={"code":0,"msg":"成员不能为空"}
            return JsonResponse(data)

        #没有填写显示名称
        if name == "" or name == None:
            name = username

        username=address + '@' + domain
        
        msg = ''
        try:
            ormdata = self.model.objects.create(address=username,
                                                name = name,
                                                domain=domain
            )

            ormdata.save()

            forward_ormdata = Forwardings.objects.create(address=username,
                                                        forwarding=",".join(users),
                                                        domain = domain,
                                                        is_forwarding=0,
                                                        dest_domain=domain,
                                                        is_list=1
            )
            forward_ormdata.save()
            data={"code":1,"msg":msg}
        except IntegrityError as e:
            #得到异常消息
            msg=str(e.__cause__)
            logger.error(e.__cause__)
            data={"code":0,"msg":msg}

        return JsonResponse(data)

class GroupEditView(LoginRequiredMixin,TemplateView):
    """
    编辑
    """
    template_name = 'mail/groupedit.html'
    model = Alias

    def get(self, request, *args, **kwargs):
        """
        得到提交的ids
        """
        self.address = request.GET.get('address')
        #根据id得到数据
        self.alias = self.model.objects.filter(address=self.address).values('address','name')[0]

        return super(GroupEditView, self).get(request, *args, **kwargs)

    #显示编辑模板
    def get_context_data(self, **kwargs):
        
        users = Forwardings.objects.filter(address=self.address,is_list=1).values('address','forwarding')[0]
        html_users = []
        for i in users['forwarding'].split(','):
            html_users.append('<option value="%s" selected="selected">%s</option>' % (i,i))

        context = {
            'alias': self.alias,
            'html_users':html_users
        }
        kwargs.update(context)
        return super(GroupEditView, self).get_context_data(**kwargs)

    #数据提交接收方法
    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        address = request.POST.get("address")
        name = request.POST.get("name")
        users = request.POST.getlist("users")

        if address == "":
            data={"code":0,"msg":"用户名不能为空"}
            return JsonResponse(data)

        if users=="":
            data={"code":0,"msg":"成员不能为空"}
            return JsonResponse(data)

        #没有填写显示名称
        if name == "" or name == None:
            name = username

        msg = ''
        try:
            self.model.objects.filter(address=address).update(name=name)

            Forwardings.objects.filter(address=address).update(forwarding=",".join(users))

            data={"code":1,"msg":msg}
        except IntegrityError as e:
            #得到异常消息
            msg=str(e.__cause__)
            #msg = "游戏名已经存在"
            logger.error(e.__cause__)
            data={"code":0,"msg":msg}

        return JsonResponse(data)

class GroupDelView(LoginRequiredMixin,TemplateView):
    """
    删除
    """
    model = Alias

    def post(self, request, *args, **kwargs):
        """
        数据提交
        """
        #得到批量或者单个要删除的id
        address = request.POST.get("address")

        msg="操作成功"

        self.model.objects.filter(address=address).delete()
        Forwardings.objects.filter(address=address,is_list=1).delete()
        data={"code":1,"msg":msg}

        return JsonResponse(data)