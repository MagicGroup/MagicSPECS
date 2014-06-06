Name: kio-locate
Summary: kio-locate is a KDE I/O Slave for the locate command.
Summary(zh_CN.UTF-8): kio-locate是一个KDE I/O Slave的定位命令
Version: 0.4.5
Release: 2%{?dist}
License: GPL
Group: Applications/Productivity
Group(zh_CN.UTF-8): 应用程序/生产力
Source: %{name}_%{version}.tar.gz
Patch:	kio-locate-tde.patch
BuildRoot: %{_tmppath}/build-root-%{name}
Packager: KanKer
Url: http://arminstraub.de

%description
kio-locate is a KDE I/O Slave for the locate command.
This means that you can use kio-locate by simply typing in konquerors address box. You can e.g. type "locate:index.html" to find all files that contain "index.html" in their name.
There's even more: You can use kio-locate in all KDE applications, that accept URLs.

%description -l zh_CN.UTF-8
kio-locate是一个KDE I/O Slave的定位命令.
这个意思就是你可以在konqueor地址栏里简单输入来使用kio-locate。比如你可以输入 "locate:index.html" 来查找所有包含 "index.html"
的文件。
而且，你可以在所有KDE程序中使用kio-locate，只要接受URL。

%prep
rm -rf $RPM_BUILD_ROOT 
mkdir $RPM_BUILD_ROOT

%setup -q -n %{name}-%{version}
%patch -p1

%build

tar xjf admin/scons-mini.tar.bz2
python scons configure extraincludes=/usr/include/tqt
python scons

%install
python scons install DESTDIR=$RPM_BUILD_ROOT

%clean

%files 

%defattr(-,root,root,0755)
/usr
%exclude /usr/*/debug*

%changelog
* Mon Oct 09 2006 Liu Di <liudidi@gmail.com> - 0.4.5-1mgc
- update 0.4.5
