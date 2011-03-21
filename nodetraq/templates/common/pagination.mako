
<%def name="generate_pagination(page, total_pages, page_count, item_count, link_append=None)" >
% if page > 1:
<a href="?page=${page-1}${link_append}">&laquo; Previous</a>
% endif
% if page > 3:
<a href="?page=1${link_append}">1</a>
% endif
% if page > 4:
...
% endif
<%
low_range = page-2 if page-2 > 1 else 1
high_range = page+3 if page+3 < total_pages+1 else total_pages+1
%>
% for i in xrange(low_range, high_range):
    % if i == page:
${page}
    % else:
<a href="?page=${i}${link_append}">${i}</a>
    % endif
% endfor
% if page <= total_pages - 4:
...
% endif
% if page <= total_pages - 3:
<a href="?page=${total_pages}${link_append}">${total_pages}</a>
% endif
% if page != total_pages:
<a href="?page=${page+1}${link_append}">Next &raquo;</a>
% endif
% if page == total_pages:
(${page_count or 1}-${item_count}/${item_count})
% else:
(${page_count or 1}-${page_count + 25}/${item_count})
% endif
</%def>

