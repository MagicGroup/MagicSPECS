Name:           elementary
Version:	1.16.0-beta3
Release:        2%{?dist}
Summary:        Basic widget set that is easy to use based on EFL
Summary(zh_CN.UTF-8): 易于使用基于 EFL 系统的基本部件集
License:        LGPLv2+
URL:            http://www.enlightenment.org
Source0:        https://download.enlightenment.org/rel/libs/elementary/%{name}-%{version}.tar.xz

BuildRequires: desktop-file-utils
BuildRequires: doxygen
BuildRequires: efl-devel
BuildRequires: evas-generic-loaders
BuildRequires: gettext
BuildRequires: libeina-devel

%description
Elementary is a widget set. It is a new-style of widget set much more canvas
object based than anything else.

%description -l zh_CN.UTF-8
易于使用基于 EFL 系统的基本部件集.

%package devel
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}
Summary:        Stuff
Summary(zh_CN.UTF-8): %{name} 的开发包

%description devel
Devel packages

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-rpath --disable-doc --disable-static --disable-elementary-test
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete
find %{buildroot} -name 'elementary_testql.so' -delete
find %{buildroot} -name 'elementary_test.desktop' -delete
find %{buildroot} -name 'elementary_testql' -delete


desktop-file-install                                                                    \
        --delete-original                                                               \
        --dir=%{buildroot}%{_datadir}/applications                                      \
%{buildroot}%{_datadir}/applications/*.desktop
magic_rpm_clean.sh
%find_lang %{name}

%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons &>/dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_bindir}/elementary_config
%{_bindir}/elementary_quicklaunch
%{_bindir}/elementary_run
%{_bindir}/elementary_codegen
%{_bindir}/elm_prefs_cc
%{_libdir}/libelementary.so.1*
%{_datadir}/applications/elementary_config.desktop
%{_datadir}/elementary
%{_datadir}/icons/elementary.png
%{_libdir}/edje/modules/elm
%{_libdir}/elementary
%{_datadir}/eolian/include/elementary-1/

%files devel
%{_includedir}/elementary-1
%{_libdir}/libelementary.so
%{_libdir}/pkgconfig/elementary.pc
%{_libdir}/cmake/Elementary/ElementaryConfig.cmake
%{_libdir}/cmake/Elementary/ElementaryConfigVersion.cmake
%{_libdir}/pkgconfig/elementary-cxx.pc


%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com>
- 更新到 1.16.0-beta3

* Sun Sep 06 2015 Liu Di <liudidi@gmail.com> - 1.15.1-1
- 更新到 1.15.1

* Sun Mar 30 2014 Liu Di <liudidi@gmail.com> - 1.7.10-1
- 更新到 1.7.10

* Thu Nov 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.9-1
- Update to 1.7.9

* Mon Oct 07 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-5
- Add ethumb support and others.

* Fri Sep 27 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-4
- Fix licensing
- Add icon scriptlets
- Remove elementary_test desktop and binary files
- Fix directory ownership
- Fix unused direct shlib dependency

* Thu Sep 26 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-3
- Fix build errors

* Tue Sep 24 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-2
- Remove useless shared object.

* Fri Sep 06 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.7.8-1
- Update to 1.7.8
- Pretty up spec file.

* Wed Jan 02 2013 Rahul Sundaram <sundaram@fedoraproject.org> 1.7.4-1
- Initial spec
