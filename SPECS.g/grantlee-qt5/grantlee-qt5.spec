
%define apidocs 1

Name:    grantlee-qt5
Summary: Qt5 string template engine based on the Django template system
Version: 5.0.0
Release: 3%{?dist}

License: LGPLv2+
URL:     https://github.com/steveire/grantlee
Source0: http://downloads.grantlee.org/grantlee-%{version}%{?pre:-%{pre}}.tar.gz

## upstreamable patches
# Install headers into a versioned directory to be parallel-installable
# https://github.com/steveire/grantlee/pull/1
Patch1: Install-headers-into-a-versioned-directory.patch

BuildRequires: cmake >= 2.8.12
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Script)
BuildRequires: pkgconfig(Qt5Test)
# qt5-linguist, when ready
BuildRequires: qt5-linguist
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

Part of the design of both is that application developers can extend
the syntax by implementing their own tags and filters. For details of
how to do that, see the API documentation.

For template authors, different applications using Grantlee will present
the same interface and core syntax for creating new themes. For details of
how to write templates, see the documentation.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: cmake
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
%autosetup -p1 -n grantlee-%{version}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake} .. \
  -DCMAKE_BUILD_TYPE=release
popd

make %{?_smp_mflags} -C %{_target_platform}

%if 0%{?apidocs}
make docs -C %{_target_platform}
%endif


%install
make install/fast -C %{_target_platform} DESTDIR=%{buildroot}

%if 0%{?apidocs}
mkdir -p %{buildroot}%{_docdir}/HTML/en/Grantlee5/
cp -prf %{_target_platform}/apidox/* %{buildroot}%{_docdir}/HTML/en/Grantlee5/
%endif


%check
export CTEST_OUTPUT_ON_FAILURE=1
xvfb-run -a make test -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING.LIB
%doc AUTHORS CHANGELOG README
%{_libdir}/libGrantlee_Templates.so.5*
%{_libdir}/libGrantlee_TextDocument.so.5*
%dir %{_libdir}/grantlee/
%{_libdir}/grantlee/5.0/

%files devel
%{_includedir}/Grantlee5/
%{_libdir}/libGrantlee_Templates.so
%{_libdir}/libGrantlee_TextDocument.so
%{_libdir}/cmake/Grantlee5/

%if 0%{?apidocs}
%files apidocs
%{_docdir}/HTML/en/Grantlee5/
%endif


%changelog
* Fri Dec 18 2015 Liu Di <liudidi@gmail.com> - 5.0.0-3
- 为 Magic 3.0 重建

* Sat Aug 08 2015 Rex Dieter <rdieter@fedoraproject.org>  5.0.0-2
- update URL

* Thu May 28 2015 Rex Dieter <rdieter@fedoraproject.org>  5.0.0-1
- grantlee-5.0.0
