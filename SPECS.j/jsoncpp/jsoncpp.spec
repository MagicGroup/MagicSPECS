%global src_release 0.6.0
%global src_prerelease rc2
%global src_version %{src_release}-%{src_prerelease}

Name:       jsoncpp
Version:    %{src_release}
Release:    0.11.%{src_prerelease}%{?dist}
Summary:    JSON library implemented in C++
Group:      System Environment/Libraries
License:    Public Domain or MIT
URL:        http://sourceforge.net/projects/%{name}/
Source0:    http://downloads.sourceforge.net/project/%{name}/%{name}/%{src_version}/%{name}-src-%{src_version}.tar.gz
Source1:    jsoncpp.pc

BuildRequires:  python scons doxygen
BuildRequires:  graphviz

%description
%{name} is an implementation of a JSON (http://json.org) reader and writer in
C++. JSON (JavaScript Object Notation) is a lightweight data-interchange format.
It is easy for humans to read and write. It is easy for machines to parse and
generate.


%package devel
Summary:    Development headers and library for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development headers and library for %{name}.


%package doc
Summary:    Documentation for %{name}
Group:      Documentation
BuildArch:  noarch

%description doc
This package contains the documentation for %{name}


%prep
%setup -q -n %{name}-src-%{src_version}
grep -e "-Wall" SConstruct
sed 's/CCFLAGS = "-Wall"/CCFLAGS = "%{optflags}"/' -i SConstruct

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
for f in AUTHORS LICENSE NEWS.txt README.txt ; do
    install -p -m 0644 $f $RPM_BUILD_ROOT%{_docdir}/%{name}
done
install -p -m 0644 dist/doxygen/*/*.{html,png} $RPM_BUILD_ROOT%{_docdir}/%{name}/html
install -d $RPM_BUILD_ROOT%{_libdir}/pkgconfig
install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
sed -i 's|@@LIBDIR@@|%{_libdir}|g' $RPM_BUILD_ROOT%{_libdir}/pkgconfig/jsoncpp.pc

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

