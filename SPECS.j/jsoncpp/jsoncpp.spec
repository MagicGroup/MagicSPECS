Name:       jsoncpp
Version:    0.10.5
Release:    1%{?dist}
Summary:    JSON library implemented in C++
Summary(zh_CN.UTF-8): C++ 实现的 JSON 库
Group:      System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:    Public Domain or MIT
URL:        https://github.com/open-source-parsers/jsoncpp
Source0:    https://github.com/open-source-parsers/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:    jsoncpp.pc

BuildRequires:  python scons doxygen
BuildRequires:  graphviz

%description
%{name} is an implementation of a JSON (http://json.org) reader and writer in
C++. JSON (JavaScript Object Notation) is a lightweight data-interchange format.
It is easy for humans to read and write. It is easy for machines to parse and
generate.

%description -l zh_CN.UTF-8
C++ 实现的 JSON 库。

%package devel
Summary:    Development headers and library for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:      Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development headers and library for %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary:    Documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
Group:      Documentation
Group(zh_CN.UTF-8): 文档
BuildArch:  noarch

%description doc
This package contains the documentation for %{name}

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q -n %{name}-%{version}
grep -e "-Wall" SConstruct
sed 's|CCFLAGS = "-Wall"|CCFLAGS = "%{optflags}"|' -i SConstruct

%build
scons platform=linux-gcc %{?_smp_mflags}
# Now, lets make a proper shared lib. :P
g++ -o libjsoncpp.so.0.0.0 -shared -Wl,-soname,libjsoncpp.so.0 buildscons/linux-gcc-*/src/lib_json/*.os -lpthread
# Build the doc
python doxybuild.py --with-dot --doxygen %{_bindir}/doxygen

%check
scons platform=linux-gcc check %{?_smp_mflags}

%install
install -p -D lib%{name}.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so.0.0.0
ln -s %{_libdir}/lib%{name}.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so
ln -s %{_libdir}/lib%{name}.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so.0

install -d $RPM_BUILD_ROOT%{_includedir}/%{name}/json
install -p -m 0644 include/json/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/json
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}/html
for f in AUTHORS LICENSE NEWS.txt README.md ; do
    install -p -m 0644 $f $RPM_BUILD_ROOT%{_docdir}/%{name}
done
install -p -m 0644 dist/doxygen/*/*.{html,png} $RPM_BUILD_ROOT%{_docdir}/%{name}/html
install -d $RPM_BUILD_ROOT%{_libdir}/pkgconfig
install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
sed -i 's|@@LIBDIR@@|%{_libdir}|g' $RPM_BUILD_ROOT%{_libdir}/pkgconfig/jsoncpp.pc

magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_docdir}/%{name}/
%exclude %{_docdir}/%{name}/html
%{_libdir}/lib%{name}.so.0
%{_libdir}/lib%{name}.so.0.0.0

%files devel
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/jsoncpp.pc

%files doc
%{_docdir}/%{name}/

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.6.0-0.14.rc2
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0.6.0-0.13.rc2
- 为 Magic 3.0 重建

* Wed Apr 23 2014 Liu Di <liudidi@gmail.com> - 0.6.0-0.12.rc2
- 为 Magic 3.0 重建

* Tue Sep 10 2013 Sébastien Willmann <sebastien.willmann@gmail.com> - 0.6.0-0.11.rc2
- https://bugzilla.redhat.com/show_bug.cgi?id=998149 : applied Michael Schwendt's
  patch to fix duplicated documentation

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-0.10.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Sébastien Willmann <sebastien.willmann@gmail.com> - 0.6.0-0.9.rc2
- Changed Summary
- Added %%doc files to the doc package
- Added python as an explicit BuildRequires

* Fri Feb 15 2013 Sebastien Willmann <sebastien.willmann@gmail.com> - 0.6.0-0.8.rc2
- Added documentation sub-package

* Sun Jan 20 2013 Sebastien Willmann <sebastien.willmann@gmail.com> - 0.6.0-0.7.rc2
- Added graphviz as a BuildRequire

* Sat Jan 19 2013 Sebastien Willmann <sebastien.willmann@gmail.com> - 0.6.0-0.6.rc2
- Install the corrected library

* Sat Dec 22 2012 Sebastien Willmann <sebastien.willmann@gmail.com> - 0.6.0-0.5.rc2
- Added libjsoncpp.so.0
- Moved the shared lib build to the correct section

* Fri Dec 21 2012 Sebastien Willmann <sebastien.willmann@gmail.com> - 0.6.0-0.4.rc2
- Removed doc subpackage
- Added .pc file
- Fixed shared lib

* Wed Dec 12 2012 Sebastien Willmann <sebastien.willmann@gmail.com> - 0.6.0-0.3.rc2
- Removed static package
- Preserving timestamp on installed files
- Added guard grep to the sed expression
- Removed duplicated doc files
- Removed dependency on pkgconfig
- Changed base package group

* Sun Dec 02 2012 Sébastien Willmann <sebastien.willmann@gmail.com> - 0.6.0-0.2.rc2
- Changed license field to Public Domain or MIT

* Tue Nov 27 2012 Sébastien Willmann <sebastien.willmann@gmail.com> 0.6.0-0.1.rc2
- Creation of the spec file

