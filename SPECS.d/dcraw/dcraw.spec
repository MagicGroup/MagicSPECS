Summary: Tool for decoding raw image data from digital cameras
Summary(zh_CN.UTF-8): 从数码相机中解码 raw 图像数据的工具
Name: dcraw
Version: 9.20
Release: 1%{?dist}
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
License: GPLv2+
URL: http://cybercom.net/~dcoffin/dcraw
Source0: http://cybercom.net/~dcoffin/dcraw/archive/dcraw-%{version}.tar.gz
BuildRequires: gettext
BuildRequires: libjpeg-devel
BuildRequires: lcms-devel
BuildRequires: jasper-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%__id_u -n)

%description
This package contains dcraw, a command line tool to decode raw image data
downloaded from digital cameras.

%description -l zh_CN.UTF-8
这个包提供了 dcraw，一个从数码相机中解码 raw 图像数据的命令行工具。

%prep
%setup -q -n dcraw

%build
gcc %optflags -lm -ljpeg -llcms -ljasper -DLOCALEDIR="\"%{_datadir}/locale\"" -o dcraw dcraw.c
# build language catalogs
for catsrc in dcraw_*.po; do
    lang="${catsrc%.po}"
    lang="${lang#dcraw_}"
    msgfmt -o "dcraw_${lang}.mo" "$catsrc"
done

%install
rm -rf %buildroot
install -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 dcraw %{buildroot}%{_bindir}

# install language catalogs
for catalog in dcraw_*.mo; do
    lang="${catalog%.mo}"
    lang="${lang#dcraw_}"
    install -d -m 0755 "%{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES"
    install -m 0644 "$catalog" "%{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES/dcraw.mo"
done

install -d -m 0755 %{buildroot}%{_bindir} %{buildroot}%{_mandir}/man1
install -m 0644 dcraw.1 %{buildroot}%{_mandir}/man1/dcraw.1
# localized manpages
rm -f %{name}-man-files
touch %{name}-man-files
for manpage in dcraw_*.1; do
    lang="${manpage%.1}"
    lang="${lang#dcraw_}"
    install -d -m 0755 "%{buildroot}%{_mandir}/${lang}/man1"
    install -m 0644 "${manpage}" "%{buildroot}%{_mandir}/${lang}/man1/dcraw.1"
    echo "%%lang($lang) %%{_mandir}/${lang}/man1/*" >> %{name}-man-files
done

%find_lang %{name}

%clean
rm -rf %buildroot

%files -f %{name}.lang -f %{name}-man-files
%defattr(-, root, root)
%{_bindir}/dcraw
%{_mandir}/man1/*

%changelog
* Wed Mar 19 2014 Liu Di <liudidi@gmail.com> - 9.20-1
- 更新到 9.20

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 9.11-2
- 为 Magic 3.0 重建


