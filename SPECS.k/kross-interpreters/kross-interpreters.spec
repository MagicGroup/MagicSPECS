
## falcon (still) not functional
#define kross_falcon 0
## java needs love
#define kross_java 1

# http://bugs.kde.org/243565
# define kross_ruby 1

Name:    kross-interpreters 
Version: 4.14.2
Release: 1%{?dist}
Summary: Kross interpreters 

License: LGPLv2+
URL:     http://developer.kde.org/language-bindings/
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/%{version}/src/%{name}-%{version}.tar.xz

BuildRequires: kdelibs4-devel >= %{version} 
%if 0%{?kross_falcon}
BuildRequires: Falcon-devel
%endif
%if 0%{?kross_java}
BuildRequires: java-devel
%endif
%if 0%{?kross_ruby}
BuildRequires: ruby-devel ruby
%endif
BuildRequires: python-devel

%description
%{summary}.

%package -n kross-python
Summary:  Kross plugin for python
Requires: kdelibs4 >= %{version}
Provides: kross(python) = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
%description -n kross-python
Python plugin for the Kross archtecture in KDE.

%package -n kross-falcon
Summary:  Kross plugin for falcon
Requires: Falcon
Requires: kdelibs4 >= %{version}
Provides: kross(falcon) = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
%description -n kross-falcon
Falcon plugin for the Kross archtecture in KDE.

%package -n kross-java
Summary:  Kross plugin for java 
Requires: kdelibs4 >= %{version}
Provides: kross(java) = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
AutoReq:  no
Requires: jdk
%description -n kross-java
Java plugin for the Kross archtecture in KDE.

%package -n kross-ruby
Summary:  Kross plugin for ruby
%{?ruby_abi:Requires: ruby(abi) = %{ruby_abi}}
Requires: kdelibs4 >= %{version}
Provides: kross(ruby) = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
%description -n kross-ruby
Ruby plugin for the Kross architecture in KDE.


%prep
%setup -q
%if ! 0%{?kross_ruby}
rm -rf ruby
%endif

%if ! 0%{?kross_java}
rm -rf java
%endif

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} \
	..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%clean
rm -rf %{buildroot}


%files
# intentionally left blank (for now)

%files -n kross-python
%{_kde4_libdir}/kde4/krosspython.so

%if 0%{?kross_falcon}
%files -n kross-falcon
%{_kde4_libdir}/kde4/krossfalcon.so
%endif

%if 0%{?kross_java}
%files -n kross-java
%{kde4_plugindir}/kross/kross.jar
%{kde4_plugindir}/krossjava.so
%endif

%if 0%{?kross_ruby}
%files -n kross-ruby
%{_kde4_libdir}/kde4/krossruby.so
%endif


%changelog
* Thu Oct 30 2014 Liu Di <liudidi@gmail.com> - 4.14.2-1
- 更新到 4.14.2

* Fri Jul 18 2014 Liu Di <liudidi@gmail.com> - 4.13.3-1
- 更新到 4.13.3

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 4.13.2-1
- 更新到 4.13.2

* Sun Jun 01 2014 Liu Di <liudidi@gmail.com> - 4.13.1-1
- 更新到 4.13.1

* Mon May 06 2013 Than Ngo <than@redhat.com> - 4.10.3-1
- 4.10.3

* Mon Apr 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.2-1
- 4.10.2

* Sat Mar 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.1-1
- 4.10.1

* Fri Feb 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.0-1
- 4.10.0

* Tue Jan 22 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.98-1
- 4.9.98

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.97-1
- 4.9.97

* Thu Dec 20 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.95-1
- 4.9.95

* Tue Dec 04 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.90-1
- 4.9.90

* Mon Dec 03 2012 Than Ngo <than@redhat.com> - 4.9.4-1
- 4.9.4

* Sat Nov 03 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.3-1
- 4.9.3

* Sat Sep 29 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.2-1
- 4.9.2

* Wed Sep 05 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.1-1
- 4.9.1

* Thu Jul 26 2012 Lukas Tinkl <ltinkl@redhat.com> - 4.9.0-1
- 4.9.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.97-1
- 4.8.97

* Thu Jun 28 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.95-1
- 4.8.95

* Sun Jun 10 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.90-1
- 4.8.90

* Wed May 23 2012 Than Ngo <than@redhat.com> - 4.8.3-2
- rhel/fedora condition

* Mon Apr 30 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.3-1
- 4.8.3

* Fri Mar 30 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.2-1
- 4.8.2

* Mon Mar 05 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.1-1
- 4.8.1

* Sat Feb 11 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-2
- omit kross-ruby on f17+, ftbfs against ruby (#794742, kde#243565)

* Sun Jan 22 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.0-1
- 4.8.0

* Wed Jan 04 2012 Radek Novacek <rnovacek@redhat.com> - 4.7.97-1
- 4.7.97

* Thu Dec 22 2011 Radek Novacek <rnovacek@redhat.com> - 4.7.95-1
- 4.7.95

* Sun Dec 04 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.7.90-1
- 4.7.90

* Fri Nov 25 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.80-1
- 4.7.80

* Sat Oct 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.3-1
- 4.7.3

* Tue Oct 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-1
- 4.7.2

* Wed Sep 14 2011 Radek Novacek <rnovacek@redhat.com> 4.7.1-1
- 4.7.1

* Tue Jul 26 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7.0-1
- 4.7.0

* Fri Jul 15 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.95-1
- 4.6.95

* Wed Jul 06 2011 Than Ngo <than@redhat.com> - 4.6.90-1
- first Fedora RPM
