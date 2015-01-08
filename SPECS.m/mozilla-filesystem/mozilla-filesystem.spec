Name:           mozilla-filesystem
Version:        1.9
Release:        4%{?dist}
Summary:        Mozilla filesytem layout
Summary(zh_CN.UTF-8): Mozilla 文件系统布局
Group:          Applications/Internet
Group(zh_CN.UTF-8):	应用程序/互联网
License:        MPL
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
This package provides some directories required by packages which use
Mozilla technologies such as NPAPI plugins or toolkit extensions.

%description -l zh_CN.UTF-8
这个包提供了使用 Mozilla 技术，比如 NPAPI 插件或工具包扩展需要的目录。

%prep

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/{lib,%{_lib}}/mozilla/{plugins,extensions}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/mozilla/extensions
mkdir -p $RPM_BUILD_ROOT/etc/skel/.mozilla/{plugins,extensions}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
/usr/lib*/mozilla
%{_datadir}/mozilla
/etc/skel/.mozilla

%changelog
* Mon Dec 01 2014 Liu Di <liudidi@gmail.com> - 1.9-4
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.9-3
- 为 Magic 3.0 重建

* Tue Jan 17 2012 Liu Di <liudidi@gmail.com> - 1.9-2
- 为 Magic 3.0 重建

