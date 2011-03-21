
# available groups, use groups=group1,group2,...
#
% for group in c.groups:
# ${group.name}
% endfor

#
# dump=machines will dump all machines

#
# pass format=dsh to write a dsh $CLUSTER file, all other options will be ignored
# pass format=bind to write a bind config format
# pass format=rbind to write a reverse bind config format
# pass format=xml to write an xml config format
# pass format=json to write a json config format
# group names with spaces will be replaced with -
