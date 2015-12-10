Name:           yaml-cpp
Version:        0.5.1
Release:        10%{?dist}
Summary:        A YAML parser and emitter for C++
Summary(zh_CN.UTF-8): C++ 的 YAML 解析器
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        MIT 
URL:            http://code.google.com/p/yaml-cpp/
Source0:        http://yaml-cpp.googlecode.com/files/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  boost-devel

%description
yaml-cpp is a YAML parser and emitter in C++ written around the YAML 1.2 spec.

%description -l zh_CN.UTF-8
C++ 的 YAML 解析器。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       boost-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
# Fix eol 
sed -i 's/\r//' license.txt


%build
# ask cmake to not strip binaries
%cmake . -DYAML_CPP_BUILD_TOOLS=0
make VERBOSE=1 %{?_smp_mflags}


%install
%make_install


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc license.txt
%{_libdir}/*.so.*

%files devel
%{_includedir}/yaml-cpp/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 0.5.1-10
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 0.5.1-9
- 为 Magic 3.0 重建

* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 0.5.1-8
- 为 Magic 3.0 重建

* Thu Apr 16 2015 Liu Di <liudidi@gmail.com> - 0.5.1-7
- 为 Magic 3.0 重建

* Thu Feb 26 2015 Guido Grazioli <guido.grazioli@gmail.com> - 0.5.1-6
- Rebuild for gcc switching default to -std=gnu11

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 0.5.1-5
- Rebuild for boost 1.57.0

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.5.1-2
- Rebuild for boost 1.55.0

* Thu Nov 14 2013 Richard Shaw <hobbes1069@gmail.com> - 0.5.1-1
- Update to latest upstream release.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 10 2012 Richard Shaw <hobbes1069@gmail.com> - 0.3.0-1
- Update to latest release.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 30 2011 Guido Grazioli <guido.grazioli@gmail.com> - 0.2.7-1
- Update to 0.2.7
- Remove gcc 4.6 patch fixed upstream

* Mon May 09 2011 Guido Grazioli <guido.grazioli@gmail.com> - 0.2.6-1
- Upstream 0.2.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Apr 02 2010 Guido Grazioli <guido.grazioli@gmail.com> - 0.2.5-1
- Upstream 0.2.5

* Fri Jan 15 2010 Guido Grazioli <guido.grazioli@gmail.com> - 0.2.4-1
- Upstream 0.2.4

* Sat Oct 17 2009 Guido Grazioli <guido.grazioli@gmail.com> - 0.2.2-2
- Remove duplicate file

* Wed Oct 14 2009 Guido Grazioli <guido.grazioli@gmail.com> - 0.2.2-1
- Initial packaging 
