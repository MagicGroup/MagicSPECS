Name:           qtsoap
Version:        2.7
Release:        6%{?dist}
Summary:        The Simple Object Access Protocol Qt-based client side library
Summary(zh_CN.UTF-8): 基于 Qt 的简单对象访问协议库

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2 with exceptions or GPLv3
URL:            http://qt.nokia.com/products/appdev/add-on-products/catalog/4/Utilities/qtsoap/
Source0:        http://get.qt.nokia.com/qt/solutions/lgpl/qtsoap-%{version}_1-opensource.tar.gz
Patch0:         qtsoap-2.7_1-opensource-install-pub-headers.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  qt4-devel

%description
The SOAP (Simple Object Access Protocol) library uses the XML standard
for describing how to exchange messages. Its primary usage is to invoke web
services and get responses from Qt-based applications.

%description -l zh_CN.UTF-8
基于 Qt 的简单对象访问协议库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description    devel
Development files for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n qtsoap-%{version}_1-opensource

# headers are not installed for shared library
%patch0 -p1 -b .install-pub-headers

sed -i 's:$$DESTDIR:%{qt4_libdir}:g' buildlib/buildlib.pro

%build
# we want shared library
echo "SOLUTIONS_LIBRARY = yes" > config.pri

echo "QTSOAP_LIBNAME = \$\$qtLibraryTarget(qtsoap)" >> common.pri
echo "VERSION=%{version}" >> common.pri

qmake-qt4 PREFIX=%{qt4_prefix}
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make INSTALL_ROOT=%{buildroot} install
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README.TXT LGPL_EXCEPTION.txt LICENSE.GPL3 LICENSE.LGPL
%{_qt4_libdir}/libqtsoap.so.*

%files devel
%defattr(-,root,root,-)
%doc LGPL_EXCEPTION.txt LICENSE.GPL3 LICENSE.LGPL
%{_qt4_libdir}/libqtsoap.so
%{_qt4_headerdir}/QtSoap/

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.7-6
- 为 Magic 3.0 重建

* Fri Sep 11 2015 Liu Di <liudidi@gmail.com> - 2.7-5
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.7-4
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 14 2011 Jaroslav Reznik <jreznik@redhat.com> - 2.7-2
- libqtsoap library name

* Thu May 19 2011 Jaroslav Reznik <jreznik@redhat.com> - 2.7-1
- fix version

* Tue Oct 26 2010 Jaroslav Reznik <jreznik@redhat.com> - 1.7-1
- Initial spec file
