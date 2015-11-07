Summary: The skeleton package which defines a simple Magic Linux system.
Summary(zh_CN.UTF-8): 一个定义了简单 Magic Linux 系统的框架
Name: basesystem
Version: 30
Release: 4%{?dist}
License: public domain
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
Prereq: setup filesystem
BuildRoot: /var/tmp/basesystem-root
BuildArchitectures: noarch

%description
Basesystem defines the components of a basic Magic Linux system (for
example, the package installation order to use during bootstrapping).
Basesystem should be the first package installed on a system, and it
should never be removed.

%description -l zh_CN.UTF-8
Basesystem定义了基本Magic Linux系统中的组件，这个包应该是系统里第一个
安装的包，而且永远不要移除它

%prep

%build

%install

%clean

%files

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 30-4
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 30-2
- 为 Magic 3.0 重建

* Fri Oct 01 2006 Liu Di <liudidi@gmail.com> - 8.0-5mgc
- rebuild
