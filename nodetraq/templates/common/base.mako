<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN">
<html xml:lang="en" lang="en">
<head>
    <title>${c.title}</title>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
    <meta content="en-us" http-equiv="Content-Language" />
    <meta content="${c.selected_page}" name="selected_page" />
    <meta content="${c.subpage}" name="subpage" />
    <meta content="false" name="check_status" />
    <link rel="stylesheet" type="text/css" href="/css/base.css" />
    <script type="text/javascript" src="/js/jquery.min.js"></script>
    <script type="text/javascript" src="/js/jquery.shiftcheckbox.js"></script>
    <script type="text/javascript" src="/js/json2.js"></script>
    <script type="text/javascript" src="/js/mustache.js"></script>
    <script type="text/javascript" src="/js/nodetraq.js"></script>
    ${self.head_tags()}
</head>
<body>

    <div id="wrapper">
    <div id="wrapper2">
        <%include file="header.mako" />
        <div id="main">
            <div id="sidebar">
                % if c.selected_page:
                <%include file="/${c.selected_page}/sidebar.mako" />
                % endif
            </div>
            <div id="content">
                % if c.flash:
                <div id="flash" class="${c.flash_error}">${c.flash}</div>
                % else:
                <div id="flash" class="hidden"></div>
                % endif
                ${ next.body() }
            </div>
        </div>
        <%include file="footer.mako"/>
    </div>
    </div>

</body>
</html>

