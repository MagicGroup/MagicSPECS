Name:           evas-generic-loaders
Version:	1.16.0
Release:        3%{?dist}
Summary:        Set of generic loaders for Evas
Summary(zh_CN.UTF-8): Evas 的通用载入器集合
License:        GPLv2+
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Url:            http://enlightenment.org/
Source:         https://download.enlightenment.org/rel/libs/evas_generic_loaders/evas_generic_loaders-%{version}.tar.xz
Requires:       evas
BuildRequires:  efl-devel >= %{version} gstreamer-plugins-base-devel 
BuildRequires:  poppler-devel LibRaw-devel librsvg2-devel 
BuildRequires:  libspectre-devel zlib-devel

%description
Extra loaders for GPL loaders and unstable libraries.

%description -l zh_CN.UTF-8
Evas 的通用载入器集合。

%prep
%setup -q -n evas_generic_loaders-%{version}

%build
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
%make_install
magic_rpm_clean.sh

%files
%doc ChangeLog README COPYING
%_libdir/evas/utils

%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com>
- 更新到 1.16.0

* Sun Sep 06 2015 Liu Di <liudidi@gmail.com> - 1.15.0-2
- 更新到 1.15.0

* Sun Sep 06 2015 Liu Di <liudidi@gmail.com> - 1.7.10-2
- 为 Magic 3.0 重建

* Wed Apr 30 2014 Liu Di <liudidi@gmail.com> - 1.7.10-1
- 更新到 1.7.10

* Wed Apr 30 2014 Liu Di <liudidi@gmail.com> - 1.7.9-4
- 为 Magic 3.0 重建

* Wed Apr 30 2014 Liu Di <liudidi@gmail.com> - 1.7.9-3
- 为 Magic 3.0 重建

* Tue Jan 21 2014 Jon Ciesla <limburgher@gmail.com> - 1.7.9-2
- Rebuild for new LibRaw.

* Tue Nov 12 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.9-1
- Update to 1.7.9

* Fri Sep 13 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.8-1
- Update to 1.7.8

* Mon Aug 19 2013 Marek Kasik <mkasik@redhat.com> - 1.7.7-4
- Rebuild (poppler-0.24.0)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Marek Kasik <mkasik@redhat.com> - 1.7.7-2
- Rebuild (poppler-0.22.5)

* Tue Jun  4 2013 Tom Callaway <spot@fedoraproject.org> - 1.7.7-1
- 1.7.7

* Fri May 31 2013 Jon Ciesla <limburgher@gmail.com> - 1.7.6-2
- Rebuild for new LibRaw.

* Fri Apr 19 2013 Tom Callaway <spot@fedoraproject.org> - 1.7.6-1
- update to 1.7.6

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Marek Kasik <mkasik@redhat.com> - 1.7.4-3
- Rebuild (poppler-0.22.0)

* Sun Dec 30 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.4-2
- fix directory ownership, configure option and requires as per review

* Fri Dec 28 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.4-1 
- initial spec
