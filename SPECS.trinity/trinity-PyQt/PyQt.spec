Distribution:	MagicLinux
Packager:  	Levin Du <zsdjw@21cn.com>

Name:      	PyQt
Version:   	3.18.1
Release:   	2%{?dist}
Provides:	PyQt
License: 	GNU/GPL
URL:		http://www.riverbankcomputing.co.uk/pyqt/
Group:     	Development/Libraries
Group(zh_CN.UTF-8):   开发/库
Source0: 	PyQt-x11-gpl-%{version}.tar.gz
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
Summary:   	PyQt is a set of Python bindings for the Qt toolkit.
Summary(zh_CN.UTF-8):	PyQt 是一组到 Qt 工具包的 Python 绑定
BuildRequires:	python, sip-devel >= 4.4.5, qt-devel
Requires:	python, sip >= 4.4.5

#%define pythonsitedir /usr/lib/python2.6/site-packages

%description
PyQt is a set of Python bindings for the Qt toolkit.

%description -l zh_CN.UTF-8
PyQt 是一组到 Qt 工具包的 Python 绑定.

%package devel
Summary: 	Files needed to build other bindings based on Qt
Summary(zh_CN.UTF-8): 建立基于 Qt 的其它绑定需要的文件
Requires: 	%{name} = %{version}-%{release}
Requires: 	sip-devel
Group: 		Development/Libraries
Group(zh_CN.UTF-8):   开发/库

%description devel
Files needed to build other bindings for C++ classes that inherit from any
of the Qt classes (e.g. KDE or your own).

%description devel -l zh_CN.UTF-8
建立其它继承自 Qt 类的 C++ 类(比如 KDE 或你自己的)的 Python 绑定需要的文件。

%package examples
Summary: 	Examples for PyQt
Summary(zh_CN.UTF-8): PyQt 的例子
Requires: 	%{name} = %{version}-%{release}
Group: 		Development/Libraries
Group(zh_CN.UTF-8):   开发/库


%description examples
Examples code demonstrating how to use the Python bindings for Qt.

%description examples -l zh_CN.UTF-8
演示如果使用 Qt 的 Python 绑定的例子代码。

%post
ldconfig

%postun
ldconfig

%prep
%setup -n PyQt-x11-gpl-%{version}

%build
QTDIR="" && . /etc/profile.d/qt3.sh

echo yes | python configure.py -y qt-mt -d %{python_sitearch} CXXFLAGS="%{optflags} -DANY=void" CFLAGS="%{optflags} -DANY=void"

# Makefiles are broken, workaround
make -C qt %{?_smp_mflags}
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
mv examples3 examples

%files
%defattr(-,root,root)
%{_bindir}/*
%python_sitearch

%files devel
%defattr(-,root,root)
%{_datadir}/sip/*
%doc doc/PyQt.html

%files examples
%defattr(-,root,root)
%doc examples/README examples/*.py
%doc examples/*.png examples/*.gif examples/*.bmp

%clean
%{__rm} -rf %{buildroot} %{_builddir}/%{buildsubdir}

%changelog
* Mon Jan 23 2012 Liu Di <liudidi@gmail.com> - 3.18.1-2
- 为 Magic 3.0 重建

* Sun Nov 18 2007 Ni Hui <shuizhuyuanluo@126.com> - 3.17-0.1mgc
- rebuild
- qt-mt

* Thu Jan 11 2007 Liu Di <liudidi@gmail.com> - 3.17-1mgc
- update to 3.17

* Tue Oct 10 2006 Liu Di <liudidi@gmail.com> - 3.16-1mgc
- update to 3.16

* Wed Sep 14 2005 Levin Du <zsdjw@21cn.com> 3.15-1mgc
- First build on MGC

* Wed Aug 31 2005 Christian Wasem <wasem@ccux-linux.de> 3.15-1
- Version Update to 3.15
* Sun Mar 06 2005 Christian Metzen <metzench@ccux-linux.de> 3.14.1-1
- Version Update to 3.14.1
* Sun Feb 20 2005 Christian Metzen <metzench@ccux-linux.de> 3.14-1
- Initial Release
