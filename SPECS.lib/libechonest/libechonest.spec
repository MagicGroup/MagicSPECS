Name:		libechonest
Version: 2.2.0
Release:	2%{?dist}
Summary:	C++ wrapper for the Echo Nest API
Summary(zh_CN.UTF-8): Echo Nest APi 的 C++ 接口

Group:		System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:	GPLv2+
URL:		https://projects.kde.org/projects/playground/libs/libechonest
Source0:	http://files.lfranchi.com/libechonest-%{version}.tar.bz2
Patch0:		libechonest-2.0.1-Werror.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	cmake
BuildRequires:	pkgconfig(QJson)
BuildRequires:	pkgconfig(QtNetwork)

## upstream patches


%description
libechonest is a collection of C++/Qt classes designed to make a developer's
life easy when trying to use the APIs provided by The Echo Nest.

%description -l zh_CN.UTF-8
这是让开发人员更容易使用 Echo Nest 提供的 API 的 C++/Qt 类库。

%package	devel
Summary:	Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf $RPM_BUILD_ROOT
make install/fast DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion libechonest)" = "%{version}"
# The tests need active internet connection, which is not available in koji builds
# besides, there's several known-failures yet anyway -- rex
#make test -C %%{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README TODO
%{_libdir}/libechonest.so.2*

%files devel
%defattr(-,root,root,-)
%{_includedir}/echonest/
%{_libdir}/libechonest.so
%{_libdir}/pkgconfig/libechonest.pc


%changelog
* Tue Jul 15 2014 Liu Di <liudidi@gmail.com> - 2.2.0-2
- 更新到 2.2.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 09 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0.2-1
- 2.0.2

* Tue Nov 27 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0.1-3
- rebuild (qjson)

* Fri Nov 23 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0.1-2
- rebuild (qjson)

* Thu Jul 26 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0.1-1
- Update to 2.0.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 23 2011 Rex Dieter <rdieter@fedoraproject.org> 1.2.1-1
- Update to 1.2.1
- BR: pkgconfig(QtNetwork)

* Sat Oct 08 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.2.0-1
- Update to 1.2.0

* Fri Aug 19 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.9-1
- Update to 1.1.9

* Wed Jun 01 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.8-1
- 1.1.8
- track soname
- %%check: verify pkgconfig sanity

* Tue May 10 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.5-1
- Update to 1.1.5

* Sun Mar 27 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.4-1
- Update to 1.1.4

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.1-1
- Update to 1.1.1

* Mon Dec 20 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.0-1
- Initial Fedora package
