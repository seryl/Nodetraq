Start=
End=
Graph=${c.graph}
RCS=${h.quote("Describe your changes here before saving...", "")}
USERSAID=${h.quote("Save Graph", "")}
% for item in c.datasource:
DS=${item[0]}
% endfor
XTRAS=On
% for i, item in enumerate(c.datasource):
${item[0]}_Seq=${i+1}
${item[0]}_File=${h.quote("/var/lib/ganglia/rrds/index//", "")}${item[1]}
${item[0]}_DS=sum
${item[0]}_RRA=LAST
${item[0]}_CDEF=
${item[0]}_Type=LINE1
${item[0]}_Color=${c.colors[i % len(c.colors)]}
${item[0]}_Label=${item[2]}
${item[0]}_XTRAS=LAST
% if (i+1) % c.brmod == 0 and i != 0:
${item[0]}_BR=Y
% endif
% endfor
gTitle=${h.quote(c.title)}
gVLabel=
gBase=1024
gUExp=6
gWidth=500
gHeight=120
gYUp=
gYLow=
gYGrid=Auto
gAuto=No
gFormat=PNG
gRaw=
fn_FILTER=1_5
% for char, item, host in c.datasource:
db_FILES=${h.quote("/var/lib/ganglia/rrds/index/", "")}${item}
% endfor
db_FILTER=
db_RRAS=LAST
% for char, item, host in c.datasource:
${char}_Width=
% endfor
