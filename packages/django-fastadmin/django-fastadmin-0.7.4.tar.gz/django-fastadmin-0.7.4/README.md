# django-fastadmin

## 文档

- [中文文档]()
- [English Document]()

## 项目描述

为Django默认的后台管理界面提供丰富的扩展。

## 扩展列表

### UuidFieldSearchableAdmin

#### 基本功能

对于UUID字段，默认情况下，使用带中间分割线UUID字符串（如：59a5da60-35c3-4bd1-a873-c4666266b47e）作为查询条件是无法正确搜索到结果的。集成该插件，可以将搜索的带中间分割线UUID字符串转化成后台能识别的格式（如：59a5da6035c34bd1a873c4666266b47e），然后进行搜索。

#### 使用限制

- 会导致其它文本字段串的UUID字符不能正确被搜索，原因是：插件对输入的带中间分割符的UUID字符串进行了强制转化为不带中间分割符的UUID字符串，这样导致了转化后的字符串与文本字段中的UUID字符串不匹配。

#### 使用方法

在编写Admin类时，继承UuidFieldSearchableAdmin扩展即可。

```
from django.contrib import admin

from django_admin.admin import UuidFieldSearchableAdmin

from .models import M1

class M1Admin(UuidFieldSearchableAdmin, admin.ModelAdmin):
    list_display = [...]
    search_fields = [...]

admin.site.register(M1, M1Admin)
```

### InlineBooleanFieldsAllowOnlyOneCheckedMixin

#### 插件预览

#### 基本功能

#### 使用限制

#### 使用方法


