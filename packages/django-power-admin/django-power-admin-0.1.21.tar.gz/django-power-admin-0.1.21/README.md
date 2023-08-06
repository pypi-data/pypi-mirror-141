# django-power-admin

Django提供了快捷的生成后台管理站点的能力。本应用旨在增强Django Admin的能力，提供丰富的Admin、Widget、ListFilter、Form等等界面扩展类，同时也为常用的数据管理模型提供完整的管理功能。

## 使用说明

1. 依赖`django-middleware-global-request`，请参考[django-middleware-global-request文档](https://pypi.org/project/django-middleware-global-request/)。
1. 依赖`django_static_fontawesome`，请参考[django_static_fontawesome文档](https://pypi.org/project/django-static-fontawesome/)
1. 推荐使用`django-app-requires`解决包依赖问题，请参考[django-app-requires文档](https://pypi.org/project/django-app-requires/)。

## 功能扩展清单

### Admin后台管理界面整体控制

| 主要功能 |
| -------- |
| `@todo` 定制化的登录界面 |
| `@todo` 登录框增加图形验证码 |
| `@todo` 登录后增加短信验证 |
| `@todo` 顶部导航 |
| `@todo` 左侧导航 |
| `@todo` 首页控制面板 |
| `@todo` 应用模块级控制面板 |
| `@todo` 用户中心子站 |
| `@todo` 中国风的组织架构管理和用户管理 |

### PowerAdmin核心功能

| 类名 | 主要功能 |
| ---- | -------- |
| ChangelistToolbar机制 | 提供列表页顶部按钮自定义功能 |
| ChangelistObjectToolbar机制 | 提供列表页行按钮自定义功能 |
| Extra View机制 | 提供添加额外视图函数的功能 |
| View Hook机制 | 提供pre_xxx_view，post_xxx_view的Hook机制，<br />方便用户在进入视图前执行准备或清除工作 |
| Extra Context机制 | 为视图渲染注入额外的模板context机制。<br />`ChangelistToolbar机制`就是通过本机制注入额外的按钮列表数据的。 |
| Read & Change机制 | 设置只读、编辑两个不同的入口。这样现符合用户的操作习惯。 |
| Simple Export机制 | 数据导出机制，<br />默认即可导出所有表字段，<br />同时支持EXCEL模板配置、表头控制、字段配置等等。 |


### Admin辅助函数
| 函数名 | 主要功能 |
| ---- | -------- |
| add_extra_css | 为当前页添加额外的css代码段 |
| add_extra_js | 为当前页添加额外的js代码段 |


### Widget扩展类

| 类名 | 主要功能 |
| ---- | -------- |
| Select2 | 将标准select下拉框转为select2样式下拉框 |
| SelectMultiple2 | 将标准select复选框转为select2样式下拉式复选框 |
| ConfigTable | 健值对配置项编辑控件，数据json序列化后保存在TextField中 |
| `@todo` PasswordResetableWidget | 密码重置字段（只重置，不显示）|

### Field扩展类

| 类名 | 主要功能 |
| ---- | -------- |
| MPTTModelChoiceField | MPTT数据模型中的Parent字段关联的表单字段，<br />使用Select2样式控件。<br />建议在MPTTAdminForm中使用 |
| ModelChoiceFieldWithLabelProperty | 标准ModelChoiceField的扩展，<br />支持使用自定义的标签函数 |

### Form扩展类

### ListFilter扩展类

### 数据模型


## 使用方法说明

### django_power_admin.admin.PowerAdmin排序支持

#### django_power_admin.admin.PowerAdmin排序支持效果预览图

![django_power_admin.admin.PowerAdmin排序支持效果预览图](https://github.com/zencore-dobetter/pypi-images/raw/main/django-power-admin/admin/django_power_admin_admin_sorting_preview.png)


#### django_power_admin.admin.PowerAdmin排序支持使用方法

*models.py*

```
class SortableAdminExmapleModel(models.Model):
    title = models.CharField(max_length=64, verbose_name="标题")
    display_order = models.IntegerField(null=True, blank=True, verbose_name="排序")

    class Meta:
        verbose_name = "排序演示"
        verbose_name_plural = "排序演示"
    
    def __str__(self):
        return str(self.pk)

```

*admin.py*

```
from django.contrib import admin

from django_power_admin.admin import PowerAdmin

from .models import SortableAdminExmapleModel


class SortableAdminExmapleModelAdmin(PowerAdmin):
    list_display = ["title"]
    ordering = ["display_order"]
    changelist_object_toolbar_buttons = [
        "django_power_admin_move_up",
        "django_power_admin_move_down",
        "read_button",
        "change_button",
        "delete_button",
    ]

admin.site.register(SortableAdminExmapleModel, SortableAdminExmapleModelAdmin)

```


### django_power_admin.widgets.ConfigTable

#### django_power_admin.widgets.ConfigTable效果预览图

![django_power_admin.widgets.ConfigTable效果预览图](https://github.com/zencore-dobetter/pypi-images/raw/main/django-power-admin/widgets/ConfigTable/django_power_admin_widgets_config_table_preview.png)

#### django_power_admin.widgets.ConfigTable使用方法

*models.py*

```
from django.db import models

class ConfigTableExampleModel(models.Model):
    config = models.TextField(null=True, blank=True, verbose_name="配置")
    
    class Meta:
        verbose_name = "配置表控件演示"
        verbose_name_plural = "配置表控件演示"

    def __str__(self):
        return str(self.pk)
```

*admin.py*

```
from django import forms
from django.contrib import admin

from django_power_admin.widgets import ConfigTable
from django_power_admin.admin import PowerAdmin

class ConfigTableExampleModelForm(forms.ModelForm):
    class Meta:
        widgets = {
            "config": ConfigTable(),
        }

class ConfigTableExampleModelAdmin(admin.ModelAdmin):
    form = ConfigTableExampleModelForm

admin.site.register(ConfigTableExampleModel, ConfigTableExampleModelAdmin)
```


## 版本记录

### v0.1.0 2021/07/11

- 项目启动。
- 框架搭建。

### v0.1.7 2021/12/23 （首次发布）

- PowerAdmin类基本完成。

### v0.1.10 2021/12/24

- get_extra_views更名为get_extra_view_urls，避免与其它方法名冲突。
- view_action更名为read_xxx。xxx_action更名为xxx_button。
- 在list_display中追加change_list_object_toolbar字段。

### v0.1.11 2021/12/25

- 增加get_power_admin_class，用于统一扩展所有PowerAdmin的子类。

### v0.1.12 2021/12/29

- 增加has_change_permission_real, has_delete_permission_real方法，解决read/change机制导致的原始权限判断丢失的情况。
- 增加get_messages方法， 用于获取站点当前的messages队列。

### v0.1.18 2021/12/30

- 修正get_changelist_object_row_classes_javascript方法在遇到其它错误时导致的异常行为。
- ChangelistObjectToolbarButton可以直接引用extra view（需要为extra view添加按钮额外属性，如：short_description、icon、classes等）。
- change_list_xxx更名为changelist_xxx（注意：可能引起新旧版本的不兼容，特别是子类配置的change_list_toolbar_buttons属性需要改名为changelist_toolbar_buttons）。
- 引入ChangelistToolbar机制，用于添加额外的列表页顶部按钮。

### v0.1.20 2022/01/09

- 添加简易数据分享机制的支持（simple share model）。
- 添加数据导出功能。

### v0.1.21 2022/03/06

- 添加适用于TextField使用的“键值对”控件。
- PowerAdmin中方法名加上django_power_admin_前缀，避免与其它扩展类冲突。
