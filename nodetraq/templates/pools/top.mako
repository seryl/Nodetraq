<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<script type="text/javascript" src="/js/pools.js"></script>
</%def>

<div>
  <label for="selected_pool">Pool:</label>
  <select id="selected_pool" onChange="change_pool();">
    <option value="default">default</option>
    <option value="facebook">facebook</option>
    <option value="ads">ads</option>
    <option value="myspace">myspace</option>
    <option value="casino">casino</option>
    <option value="dotd">dotd</option>
    <option value="oauth">oauth</option>
    <option value="toyland">toyland</option>
  </select>
</div>
<br />

<div id="pool_data">
  <table class="list">
    <thead>
      <tr>
        <th><a href="#">Flags</a></th>
        <th><a href="#">Hostname</a></th>
        <th><a href="#">Load average</th>
        <th><a href="#">Mem % free / Free / Total</th>
        <th><a href="#">Apache</th>
      </tr>
    </thead>
    <tbody>
    </tbody>
  </table>
</div>
