Name: lrcShow-X
Summary: lrcShow-X script
Summary(zh_CN.UTF-8): lrcShow-X 动态歌词显示脚本
Version:	 2.1.1
Release: 5%{?dist}
License:	 GPL
Group: Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Url: http://www.sanfanling.cn/
Source0: http://kde-apps.org/CONTENT/content-files/103055-lrcShow-X_2_1_1.tar.bz2
Source1: lrcShow-X.desktop


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# PyQt >= 3.17.3 编译参数为 qt-mt
Requires: PyQt4 
Requires: dbus-python

%description
lrcShow-X script.

%description -l zh_CN.UTF-8
lrcShow-X 动态歌词显示脚本。

%prep
%setup -q -n %{name}

# we do not need chardet
#rm -rf chardet

# clean other languages
pushd locale
rm -rf da es hr id it ms ru uk
popd

pushd locale/zh_CN/LC_MESSAGES
rm -f lrcShow-X.po
popd

pushd locale/en_US/LC_MESSAGES
rm -f lrcShow-X.po
popd

pushd locale/zh_TW/LC_MESSAGES
rm -f lrcShow-X.po
popd

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/apps/%{name}

cp -rf * %{buildroot}%{_datadir}/apps/%{name}

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/bash
cd  %{_datadir}/apps/%{name}
./%{name}.py
EOF
chmod 755 %{buildroot}%{_bindir}/%{name}

# install desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop
# install app icon
mkdir -p %{buildroot}%{_datadir}/pixmaps
cp %{buildroot}%{_datadir}/apps/%{name}/icon/lrcShow-X.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(-, root, root)
%{_bindir}/%{name}
%{_datadir}/apps/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 2.1.1-5
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 2.1.1-4
- 为 Magic 3.0 重建

* Thu Jul 03 2014 Liu Di <liudidi@gmail.com> - 2.1.1-3
- 为 Magic 3.0 重建

* Thu Jul 03 2014 Liu Di <liudidi@gmail.com> - 2.1.1-2
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.0.0-3
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Liu Di <liudidi@gmail.com> - 2.0.0-2
- 为 Magic 3.0 重建

* Sun Sep 7 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.9.0-0.1mgc
- 更新至 0.9.0
- 戊子  八月初八  [白露]

* Mon Jun 30 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.8.0-0.1mgc
- 更新至 0.8.0
- 戊子  五月廿七

* Sun Jun 29 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.7.2-0.1mgc
- 更新至 0.7.2
- 戊子  五月廿六

* Thu Jan 24 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.6.0-0.1mgc
- 更新至 0.6.0

* Sun Jan 13 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.5.1-0.1mgc
- 更新至 0.5.1

* Sun Jan 06 2008 Ni Hui <shuizhuyuanluo@126.com> - 0.5.0-0.1mgc
- 更新至 0.5.0
- 移除路径补丁，使用脚本替换

* Sun Dec 23 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.4.2-0.1mgc
- 更新至 0.4.2

* Tue Dec 18 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.4.0-0.1mgc
- 更新至 0.4.0

* Wed Dec 12 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.3.1-0.1mgc
- 升级至 0.3.2

* Mon Dec 10 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.3.1-0.1mgc
- 升级至 0.3.1

* Sun Dec 09 2007 Ni Hui <shuizhuyuanluo@126.com> - 0.3.0-0.1mgc
- init rpm package
