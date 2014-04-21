
%define apidocs 1 

Name:    grantlee
Summary: Qt string template engine based on the Django template system
Version: 0.4.0
Release: 4%{?dist}

License: LGPLv2+
URL:     http://www.gitorious.org/grantlee/pages/Home
Source0: http://downloads.grantlee.org/grantlee-%{version}%{?pre:-%{pre}}.tar.gz

BuildRequires: cmake >= 2.8.9
BuildRequires: pkgconfig(QtGui) pkgconfig(QtScript) 
%if 0%{?apidocs}
BuildRequires: doxygen
BuildRequires: graphviz
%endif
## for %%check
BuildRequires: xorg-x11-server-Xvfb

%description
Grantlee is a plug-in based String Template system written 
using the Qt framework. The goals of the project are to make it easier for
application developers to separate the structure of documents from the 
data they contain, opening the door for theming.

The syntax is intended to follow the syntax of the Django template system, 
and the design of Django is reused in Grantlee. 
Django is covered by a BSD style license.

Part of the design of both is that application developers can extend 
the syntax by implementing their own tags and filters. For details of 
how to do that, see the API documentation.

For template authors, different applications using Grantlee will present 
the same interface and core syntax for creating new themes. For details of 
how to write templates, see the documentation.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package apidocs
Summary: Grantlee API documentation
BuildArch: noarch
%description apidocs
This package includes the Grantlee API documentation in HTML
format for easy browsing.


%prep
%setup -q -n grantlee-%{version}%{?pre:-%{pre}}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DCMAKE_BUILD_TYPE=release \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%if 0%{?apidocs}
make docs -C %{_target_platform}
%endif


%install
make install/fast -C %{_target_platform} DESTDIR=%{buildroot}

%if 0%{?apidocs}
mkdir -p %{buildroot}%{_docdir}/HTML/en/grantlee-apidocs
cp -prf %{_target_platform}/apidox/* %{buildroot}%{_docdir}/HTML/en/grantlee-apidocs
%endif


%check
export CTEST_OUTPUT_ON_FAILURE=1
xvfb-run -a make test -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc AUTHORS CHANGELOG COPYING.LIB README GOALS
%{_libdir}/libgrantlee_core.so.0*
%{_libdir}/libgrantlee_gui.so.0*
%{_libdir}/grantlee/

%files devel
%{_includedir}/grantlee/
%{_includedir}/grantlee_core.h
%{_includedir}/grantlee_templates.h
%{_includedir}/grantlee_textdocument.h
%{_libdir}/libgrantlee_core.so
%{_libdir}/libgrantlee_gui.so
%dir %{_libdir}/cmake
%{_libdir}/cmake/grantlee/

%if 0%{?apidocs}
%files apidocs
%{_docdir}/HTML/en/grantlee-apidocs/
%endif

%changelog
* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 0.4.0-4
- 为 Magic 3.0 重建

* Tue Dec 03 2013 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-3
- %%check: use xvfb-run

* Tue Dec 03 2013 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-2
- %%check: make test

* Fri Nov 29 2013 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-1
- 0.4.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 02 2012 Rex Dieter <rdieter@fedoraproject.org>  0.3.0-1
- 0.3.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 04 2011 Rex Dieter <rdieter@fedoraproject.org>  0.2.0 -1
- 2.0.0
- pkgconfig-style deps

* Tue Oct 18 2011 Rex Dieter <rdieter@fedoraproject.org>  0.2.0 -0.2.rc2
- 2.0.0-rc2

* Tue Aug 09 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-0.1.rc1
- 2.0.0-rc1

* Tue Jul 12 2011 Rex Dieter <rdieter@fedoraproject.org> 0.1.9-1
- 0.1.9

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Sep 27 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.1.6-1
- grantlee 0.1.6

* Fri Aug 27 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.1.5-1
- grantlee 0.1.5

* Sun Jul 04 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.1.2-1
- grantlee 0.1.2

* Tue May 18 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.1.1-3
- disabled apidocs until we find a standard path

* Tue May 11 2010 Jaroslav Reznik <jreznik@redhat.com> 0.1.1-2
- added -apidocs subpackage

* Sun May 09 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.1.1-1
- grantlee 0.1.1
- fixed Group

* Thu Apr 15 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.1.0-1
- initial fedora release
