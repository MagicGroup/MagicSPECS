#!/usr/bin/env bash
#spec 中需删除的文档和po 列表

dir_base="
$RPM_BUILD_ROOT/usr/share/doc/HTML/
$RPM_BUILD_ROOT/usr/share/locale/
$RPM_BUILD_ROOT/usr/share/man/
$RPM_BUILD_ROOT/opt/trinity/share/doc/HTML/
$RPM_BUILD_ROOT/opt/trinity/share/doc/tde/HTML/
$RPM_BUILD_ROOT/opt/trinity/share/locale/
$RPM_BUILD_ROOT/opt/trinity/share/man/
"

for d in $dir_base;
do
if [[ -d $d ]];
then
# kde style documentation
find $d -type f -name '*.docbook' | grep -v "^$d\(en/\|zh_..\)" | \
        sed -e 's/\(.*\/share\/doc\/HTML\/[^/]*\/\).*/\1/' | sort -u | \
        xargs rm -rfv
# gettext translation
find $d -type f -name '*.mo' | grep -v "^$d\(en/\|zh_..\)" | \
        sed -e 's/\(.*\/share\/locale\/[^/]*\/\).*/\1/' | sort -u | \
        xargs rm -rfv
# man page translation
find $d -type f | grep -v "^$d\(en/\|zh_..\|man\)" | \
        sed -e 's/\(.*\/share\/man\/[^/]*\/\).*/\1/' | sort -u | \
        xargs rm -rfv
fi
done
