from django import forms

class QuantityForm(forms.Form):
    """
    QuantityForm 是一个表单类，用于处理数量输入。

    属性:
    - quantity: 一个整数字段，用于接收用户输入的数量。
                其配置包括一个自定义标签、最小值、最大值和一个自定义小部件来改善用户界面。
    """
    # 定义一个名为quantity的字段，它是一个整数字段，要求用户输入的值在1到9之间。
    # 使用一个自定义的HTML小部件来渲染这个字段，增加类名和占位符，以提高表单的可填写性。
    quantity = forms.IntegerField(label='',
        min_value=1, max_value=9, widget=forms.NumberInput(
            attrs={'class': 'form-control mt-1','placeholder': '数量'}
        )
    )
