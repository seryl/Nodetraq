<%def name="show_disks(disks)">
% for disk in disks:
<div class="display_disk" id="disk_${disk.id}">
  <div class="disk_data disk_type_${disk.type}">
    Serial: ${disk.serial_no}<br />
    Capacity: ${disk.capacity}<br />
  </div>
</div>
% endfor
</%def>
