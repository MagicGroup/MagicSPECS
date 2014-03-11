Name:kdmtheme
Summary:kde theme manager
Summary(zh_CN.UTF-8): kdm 主题管理器
Version:1.1.2
Release:5%{?dist}
Group:Applications/System 
Group(zh_CN.UTF-8): 应用程序/系统
License : GPL 
Source0: %{name}-%{version}.tar.bz2
Source1: %{name}-zh_CN.po
Patch1:	kdmtheme-tde.patch
BuildRoot:%{_tmppath}/%{name}-%{version}-%{release}-root 
 
URL  :  http://apps.kde.org  
Packager  : Tingxx <tingxx@21cn.com> 
 
%description 
 the kdm of kde 3.4 can use the theme,the kdmtheme can manage the themes of kdm.

%description -l zh_CN.UTF-8
kde 3.4以上可以kdm可以使用主题，kdmtheme可以管理kdm的主题。
 
%prep 
 
%setup  -q -n %{name}-%{version} 
%patch1 -p1
chmod 777 admin/*

%build  #开始构建包 
make -f admin/Makefile.common
%configure --disable-debug
make
msgfmt %{SOURCE1} -o %{name}-zh_CN.mo

%install  
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install 
mkdir -p $RPM_BUILD_ROOT/usr/share/locale/zh_CN/LC_MESSAGES
install -m 644 %{name}-zh_CN.mo $RPM_BUILD_ROOT/usr/share/locale/zh_CN/LC_MESSAGES/%{name}.mo

magic_rpm_clean.sh
%clean
 rm -rf $RPM_BUILD_ROOT
 rm -rf $RPM_BUILD_DIR/%{name}-%{version} 
 
%files  
%defattr  (-,root,root)
%{_prefix}
%exclude %{_prefix}/*/debug*

%changelog
* Mon Oct 09 2006 Liu Di <liudidi@gmail.com> - 1.1.2-1mgc
- update to 1.1.2

* Thu Mar 21 2006 KanKer <kanker@163.com>
- fix kdmtheme.desktop bug

* Sun Feb 5 2006 KanKer <kanker@163.com>
- update 1.0.1

* Fri Dec 30 2005 KanKer <kanker@163.com>
- update 0.9.2

* Fri Oct 28 2005 KanKer <kanker@163.com>
- update 0.9.1
 
* Wed Mar 30 2005 tingxx <tingxx@21cn.com> 
- init the spec file.
 
