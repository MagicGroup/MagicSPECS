Name:           gnugo
Version:        3.8
Release:        5%{?dist}

Summary:        Text based go program
Summary(zh_CN.UTF-8): 基于文本的围棋程序

Group:          Amusements/Games
Group(zh_CN.UTF-8): 娱乐/游戏
License:        GPLv3+
URL:            http://www.gnu.org/software/gnugo/gnugo.html
Source0:        http://ftp.gnu.org/gnu/gnugo/gnugo-%{version}.tar.gz
Patch0:         gnugo-3.8-format-security.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ncurses-devel readline-devel
BuildRequires:  texinfo
Requires(post): info
Requires(preun): info

%description
This software is a free program that plays the game of Go. GNU Go has played
thousands of games on the NNGS Go server. GNU Go is now also playing regularly
on the Legend Go Server in Taiwan and the WING server in Japan.

%description -l zh_CN.UTF-8
这款软件是自由软件的围棋游戏程序。

%prep
rm -rf ${RPM_BUILD_ROOT}
%setup -q
%patch0 -p1
# convert docs to UTF-8
for f in AUTHORS THANKS; do
  iconv -f iso8859-1 -t utf-8 $f > $f.conv
  touch -r $f $f.conv
  mv $f.conv $f
done

%build
%configure --enable-color --with-readline
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install
rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :

%preun
if [ "$1" = 0 ]; then
   /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi

%files
%defattr(-,root,root,755)
%doc AUTHORS COPYING README THANKS doc/newlogo.jpg doc/oldlogo.jpg
%doc %{_mandir}/man6/*
%{_bindir}/*
%{_infodir}/gnugo.*

%changelog
* Sat Sep 19 2015 Liu Di <liudidi@gmail.com> - 3.8-5
- 为 Magic 3.0 重建

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 3.8-4
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 3.8-3
- 为 Magic 3.0 重建

* Wed Dec 07 2011 Liu Di <liudidi@gmail.com> - 3.8-2
- 为 Magic 3.0 重建

