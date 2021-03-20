import re

from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.filter
def prs_normalize(prs_list):
    res = '''
          <div class="data">
          {}
          </div>
          '''
    b = ''
    prs_list = prs_list.split('),')
    temp = []
    for i in prs_list:
        i = re.sub(r"[\[\]() ']", "", i)
        temp.append(i)

    for pr in temp:
        try:
            pr_url, com_count = pr.split(',')
        except ValueError:
            b = '<p>Missing</p>'
            return mark_safe(res.format(b))

        pr_view = pr_url.split('.com/')[1]
        b += '''
             <a href="{pr_url}">{pr_view}</a>
             <p>Number of comments: {com_count}</p>
             <hr>
             '''.format(pr_url=pr_url, pr_view=pr_view, com_count=com_count)
    return mark_safe(res.format(b))
