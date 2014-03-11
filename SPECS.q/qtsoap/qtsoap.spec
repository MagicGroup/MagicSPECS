Name:           qtsoap
Version:        2.7
Release:        4%{?dist}
Summary:        The Simple Object Access Protocol Qt-based client side library

Group:          System Environment/Libraries
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

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
Development files for %{name}.

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
