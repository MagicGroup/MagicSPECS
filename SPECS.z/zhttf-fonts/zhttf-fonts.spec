Summary: Default Fonts for Magic Linux
Summary(zh_CN.UTF-8): Magic Linux的默认字体
Name:          zhttf-fonts
Version:       2.5
Release:       5%{?dist}
License:       CopyRight
Group:         User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source:        zhttf-fonts.tar.gz
Requires: fontconfig, freetype, fileutils
BuildArch: noarch
#Requires: xorg-x11-font-utils
%description
Default Fonts for Magic Linux

%description -l zh_CN.UTF-8
Magic Linux的默认字体。

%prep
%setup -q -n %{name}

%build


%install
rm -rf $RPM_BUILD_ROOT/*
mkdir -p $RPM_BUILD_ROOT/usr/share/fonts/ttf/zh_CN
mkdir -p $RPM_BUILD_ROOT/usr/share/fonts/pcf/zh_CN
cp -r ttf/* $RPM_BUILD_ROOT/usr/share/fonts/ttf/zh_CN
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/zhttf-fonts
tar xvf DejaVu.tar.gz -C $RPM_BUILD_ROOT/usr/share/doc/zhttf-fonts
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/fonts/ttf/zh_CN
%{_docdir}/zhttf-fonts/DejaVu

%post
if [ -x /usr/bin/fc-cache ]; then 
    /usr/bin/fc-cache /usr/share/fonts/wqy-microhei || : 
fi

%postun
if [ -x /usr/bin/fc-cache ]; then 
    /usr/bin/fc-cache /usr/share/fonts/wqy-microhei || : 
fi

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 2.5-5
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2.5-3
- 为 Magic 3.0 重建

* Mon Nov 11 2010 haulm <haulm@126.com> - 2.5-1mgc
- update wqy-bitmapsong

* Sun Feb 03 2008 Liu Di <liudidi@gmail.com> - 2.1-2mgc
- remove uming fonts

* Tue Nov 06 2007 Liu Di <liudidi@gmail.com> - 2.1-1mgc
- update wqy to 0.9.9

* Thu Jan 11 2007 Liu Di <liudidi@gmail.com> - 2.0-8mgc
- update wqy to 0.8.0rc1

* Mon Jul 3 2006 kde <jack@linux.net.cn> -2.0-6mgc
- fix postun scripts
- fix script magic-fontalias-fix.sh and move it from /usr/bin to /usr/sbin
- remove "Requires: xorg-x11-font-utils" for coming xorg 7.x

* Fri Jun 2 2006 KanKer <kanker@163.com> -2.0-5mgc
- update Dejavu uming and wenquanyi
- update post and postun scripts
* Sun Mar 19 2006 KanKer <kanker@163.com>
- update Dejavu uming and wenquanyi
* Thu Jan 17 2006 KanKer <kanker@163.com>
- update Dejavu to 2.2
* Mon Dec 12 2005 KanKer <kanker@163.com>
- add uming.ttf and remove fireflysung.ttf
* Wed Nov 30 2005 KanKer <kanker@163.com>
- remove simsun and tahoma fonts
* Sun Oct 30 2005 KanKer <kanker@163.com>
- add a script magic-fontalias-fix.sh
* Wed Aug 10 2005 KanKer <kanker@163.com>
- update WenQuanYi to 0.6
* Wed Jul 27 2005 KanKer <kanker@163.com>
- remove /usr/share/fonts/ttf/zh_CN/fonts.dir fonts.scale
* Mon Jun 27 2005 KanKer <kanker@163.com>
- add WenQuanYi bitmapfont.
* Fri Jun 3 2005 KanKer <kanker@163.com>
- add fireflysung.ttf
* Thu Aug 26 2004 jackey
- Add new fonts 
- Relocate the fonts
* Fri Sep 12 2003 cjacker
- remove post script
- add font link to it
* Mon Jul 14 2003 cjacker
- first build for Magic Linux 1.2
