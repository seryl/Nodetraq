<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN">
<html xml:lang="en" lang="en">
<head>
    <title>${c.title}</title>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
    <meta content="en-us" http-equiv="Content-Language" />
    <link rel="stylesheet" type="text/css" href="/css/login.css">
    <script language="javascript" type="text/javascript" src="/js/jquery.min.js"></script>
    <script type="text/javascript" src="/js/nodetraq.js"></script>
</head>
<body>

    <div id="wrapper">
        <div id="wrapper2">
            <%include file='header.mako' />
            <div id="main">
            % if c.flash:
            <div id="flash" class="${c.flash_error}">${c.flash}</div>
            % else:
                <div id="flash" class="hidden"></div>
            % endif
                <div id="login">
                    ${next.body()}
                </div>
            </div>
            <%include file='footer.mako' />
        </div>
    </div>

</body>
</html>

