%define ver      0.8.4
%define rel      1%{?dist}
%define prefix   /usr

Summary: Recite Word Easily.
Summary(zh_CN.UTF-8): 轻轻松松背单词
Name: reciteword
Version: %ver
Release: %rel.1
License: GPL
Group: Applications/Productivity
Group(zh_CN.UTF-8): 应用程序/生产力
Source: reciteword-%{ver}.tar.bz2
Patch0: reciteword-%{ver}-gcc44.patch
BuildRoot: /var/tmp/%{name}-%{version}-root

URL: http://reciteword.sourceforge.net/

Requires: gtk2 >= 2.2
Requires: esound >= 0.2.28

%description
ReciteWord is a education software to help people to study English,recite words.

%description -l zh_CN.UTF-8
这是一个帮助人们学习英语单词的教育软件。

%prep
%setup
%patch0 -p1

%build
if [ ! -f configure ]; then
  CFLAGS="$MYCFLAGS" ./autogen.sh $MYARCH_FLAGS --prefix=%prefix
else
  CFLAGS="$MYCFLAGS" ./configure $MYARCH_FLAGS --prefix=%prefix
fi

make

%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT%{prefix} install

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)

%{prefix}/bin/reciteword
%{prefix}/share/reciteword
%{prefix}/share/locale/*/LC_MESSAGES/reciteword.mo
%{prefix}/share/applications/reciteword.desktop
%{prefix}/share/pixmaps/reciteword.png
%{prefix}/share/applications/rwdict.desktop
%{prefix}/share/pixmaps/rwdict.png

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.8.4-1.1
- 为 Magic 3.0 重建

