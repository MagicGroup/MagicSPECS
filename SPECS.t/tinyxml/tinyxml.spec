%define underscore_version 2_6_2

Name:           tinyxml
Version:        2.6.2
Release:        4%{?dist}
Summary:        A simple, small, C++ XML parser
Summary(zh_CN.UTF-8): C++ 编写的简单小巧的 XML 解析器
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        zlib
URL:            http://www.grinninglizard.com/tinyxml/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}_%{underscore_version}.tar.gz
Patch0:         tinyxml-2.5.3-stl.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
TinyXML is a simple, small, C++ XML parser that can be easily integrating
into other programs. Have you ever found yourself writing a text file parser
every time you needed to save human readable data or serialize objects?
TinyXML solves the text I/O file once and for all.
(Or, as a friend said, ends the Just Another Text File Parser problem.)
%description -l zh_CN.UTF-8
C++ 编写的简单小巧的 XML 解析器。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}
%patch0 -p1 -b .stl
touch -r tinyxml.h.stl tinyxml.h


%build
# Not really designed to be build as lib, DYI
for i in tinyxml.cpp tinystr.cpp tinyxmlerror.cpp tinyxmlparser.cpp; do
  g++ $RPM_OPT_FLAGS -fPIC -o $i.o -c $i
done
g++ $RPM_OPT_FLAGS -shared -o lib%{name}.so.0.%{version} \
   -Wl,-soname,lib%{name}.so.0 *.cpp.o


%install
rm -rf $RPM_BUILD_ROOT
# Not really designed to be build as lib, DYI
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
install -m 755 lib%{name}.so.0.%{version} $RPM_BUILD_ROOT%{_libdir}
ln -s lib%{name}.so.0.%{version} $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so.0
ln -s lib%{name}.so.0.%{version} $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so
install -p -m 644 %{name}.h $RPM_BUILD_ROOT%{_includedir}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc changes.txt readme.txt
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc docs/*
%{_includedir}/*
%{_libdir}/*.so


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.6.2-4
- 为 Magic 3.0 重建

* Sat Oct 03 2015 Liu Di <liudidi@gmail.com> - 2.6.2-3
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2.6.2-2
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon May 03 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 2.6.1-1
- Updated to 2.6.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.5.3-3
- Autorebuild for GCC 4.3

* Fri Dec 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.5.3-2
- Various improvements from review (bz 407571)

* Fri Nov 30 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.5.3-1
- Initial Fedora Package
