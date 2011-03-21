<%inherit file="/common/base.mako" />
<%def name="head_tags()">
</%def>

<!--
<div id="split_content_right" class="box">
    This helper takes csv files and imports them as nodes.
</div>
-->

<div id="node_importcsv">
<h2>Import csv</h2>

${h.form(h.url(controller='nodes', action='upload_csv'), "post", multipart=True)}
File: ${h.file('uploaded_file')} <br /><br />
Description: <br />
${h.textarea('description', cols=40, rows=10)} <br /><br />
${h.submit('Submit', None)}
${h.end_form()}

</div>

<div class="break"></div>