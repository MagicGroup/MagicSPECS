%define real_name libkgapi
#%%global		git_commit f18d699
Name:		kde4-libkgapi
Version:	5.0.0
#Release:	1.20120530git%%{git_commit}%%{?dist}
Release:	4%{?dist}
Summary:	Library to access to Google services
Summary(zh_CN.UTF-8): 访问谷歌服务的库
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库

License:	GPLv2+
URL:		https://projects.kde.org/projects/extragear/libs/%{real_name}

# Package from git snapshots, create example:
# git clone git://anongit.kde.org/%%{name}
# cd libkgoogle
# git archive \\
#	--format=tar.gz \\
#	--prefix=%%{name}/ \\
#	-o ../%%{name}-%%{version}-git%%{git_commit}.tar.gz \\
#	master
#Source0:	%%{name}-%%{version}-git%%{git_commit}.tar.gz
Source0:	http://download.kde.org/stable/%{real_name}/%{version}/src/%{real_name}-%{version}.tar.bz2

BuildRequires:	kdepimlibs4-devel 
BuildRequires:	kdelibs4-devel 
BuildRequires:	pkgconfig(QJson)

Obsoletes:	libkgoogle < 0.3.2
Provides:	libkgoogle = %{version}-%{release}

%{?_kde4_version:Requires: kdepimlibs%{?_isa} >= %{_kde4_version}}

%description
Library to access to Google services, this package is needed by kdepim-runtime
to build akonadi-google resources.

%description -l zh_CN.UTF-8
访问谷欲服务的库，这个包是 kdepim-runtime 编译 akonadi-google 资源需要的。

%package devel
Summary: Development files for %{real_name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: kdepimlibs4-devel
Obsoletes: libkgoogle-devel < 0.3.2
Provides: libkgoogle-devel = %{version}-%{release}
%description devel
Libraries and header files for developing applications that use akonadi-google
resources.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{real_name}-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc README 
%{_libdir}/libkgapi*.so.*

%files devel
%{_kde4_includedir}/libkgapi*/
%{_kde4_includedir}/LibKGAPI2/
#%{_libdir}/pkgconfig/libkgapi*.pc
%{_libdir}/libkgapi*.so
%{_libdir}/cmake/LibKGAPI*/


%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 5.0.0-4
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 5.0.0-3
- 更新到 5.0.0

* Wed Jun 04 2014 Liu Di <liudidi@gmail.com> - 2.1.1-2
- 更新到 2.1.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 16 2012 Dan Vrátil <dvratil@redhat.com> 0.4.4-1
- 0.4.4

* Tue Nov 27 2012 Dan Vrátil <dvratil@redhat.com> 0.4.3-3
- Rebuild against qjson 0.8.1

* Fri Nov 23 2012 Dan Vrátil <dvratil@redhat.com> 0.4.3-2
- Rebuild against qjson 0.8.0

* Sun Nov 11 2012 Mario Santagiuliana <fedora@marionline.it> 0.4.3-1
- Update to new version 0.4.3

* Sun Aug 26 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.2-1
- 0.4.2

* Sat Aug 11 2012 Mario Santagiuliana <fedora@marionline.it> 0.4.1-1
- Update to new version 0.4.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Rex Dieter <rdieter@fedoraproject.org> 
- 0.4.0-5
- -devel: tighten subpkg dep via %%_isa, Req: kdepimlibs-devel
- Parsing token page failed (kde#301240)

* Sun Jun 10 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-4
- -devel: track files closer
- pkgconfig-style deps

* Thu Jun 07 2012 Mario Santagiuliana <fedora@marionline.it> 0.4.0-3
- Update spec file following Gregor Tätzner request:
https://bugzilla.redhat.com/show_bug.cgi?id=817622#c8

* Thu May 31 2012 Mario Santagiuliana <fedora@marionline.it> 0.4.0-2
- Update spec file following Rex Dieter and Kevin Kofler suggestion
- Add obsolete and provide for devel subpkg

* Thu May 31 2012 Mario Santagiuliana <fedora@marionline.it> 0.4.0-1
- Update to new version 0.4.0
- Update to new licence GPLv2+
- Update to new name libkgapi
- Add obsolete and provide libkgoogle

* Wed May 30 2012 Mario Santagiuliana <fedora@marionline.it> 0.3.2-1.20120530gitf18d699
- Update spec comment to new git repository
- Update to new version 0.3.2
- Snapshot f18d699d9ef7ceceff06c2bb72fc00f34811c503

* Mon Apr 30 2012 Mario Santagiuliana <fedora@marionline.it> 0.3.1-1.20120430gitefb3215
- Rename package from akonadi-google to libkgoogle
- Update spec file
- Snapshot efb32159c283168cc2ab1a39e6fa3c8a30fbc941

* Mon Apr 30 2012 Mario Santagiuliana <fedora@marionline.it> 0.3.1-1
- New version 0.3.1

* Thu Apr 01 2012 Mario Santagiuliana <fedora@marionline.it> 0.3-1.20120402git3e0a93e
- New version 0.3
- Update to git snapshot 3e0a93e1b24cd7b6e394cf76d153c428246f9fa9
- Obsolete akonadi-google-tasks
- Fix error in changelog

* Thu Mar 01 2012 Mario Santagiuliana <fedora@marionline.it> 0.2-12.20120301git41cd7c5
- Update to git snapshot 41cd7c5d6e9cfb62875fd21f8a920a235b7a7d9c

* Wed Jan 20 2012 Mario Santagiuliana <fedora@marionline.it> 0.2-11.20120121gitbe021c6
- Update to git snapshot be021c6f12e6804976dcac203a1864686a219c26

* Wed Jan 20 2012 Mario Santagiuliana <fedora@marionline.it> 0.2-10.20120120git11bf6ad
- Update spec file follow comment 1:
https://bugzilla.redhat.com/show_bug.cgi?id=783317#c1
- Update to git snapshot 11bf6ad40dd93eda1f880a99d592009ea3ff47ac
- Include LICENSE

* Thu Jan 19 2012 Mario Santagiuliana <fedora@marionline.it> 0.2-9.20120119git754771b
- Create spec file for Fedora Review
- Source package create from git snapshot 754771b6081b194aedf750fac76a9af2709a5de3

* Wed Nov 16 2011 Dan Vratil <dan@progdan.cz> 0.2-8.1
- Initial SPEC
