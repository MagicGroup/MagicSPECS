Name:           qmmp-plugin-pack
Version:        0.7.1
Release:        1%{?dist}
Summary:        A set of extra plugins for Qmmp

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://qmmp.ylsoftware.com/plugins.php
Source0:        http://qmmp.ylsoftware.com/files/plugins/%{name}-%{version}.tar.bz2

BuildRequires:  qmmp >= %{version}
BuildRequires:  cmake
BuildRequires:  qt4-devel
BuildRequires:  taglib-devel
BuildRequires:  yasm

%description
Plugin pack is a set of extra plugins for Qmmp.

 * FFap - enhanced Monkey's Audio (APE) decoder
   (24-bit samples and embedded cue support)
 * Simple Ui - simple user interface based on standard widgets set

%prep
%setup -q


%build
%cmake \
    -D USE_MPG123:BOOL=TRUE \
    .
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%doc AUTHORS COPYING ChangeLog.rus README README.RUS
%{_libdir}/qmmp/Input/*.so
%{_libdir}/qmmp/Ui/*.so


%changelog
* Thu Jun 20 2013 Karel Volný <kvolny@redhat.com> 0.7.1-1
- new version
- see upstream changelog at http://qmmp.ylsoftware.com/

* Sun Apr 28 2013 Karel Volný <kvolny@redhat.com> 0.7.0-1
- new version
- see upstream changelog at http://qmmp.ylsoftware.com/
- project URLs changes

* Tue Apr 02 2013 Karel Volný <kvolny@redhat.com> 0.6.6-1
- new version
- see upstream changelog at http://qmmp.ylsoftware.com/index_en.php

* Tue Jan 29 2013 Karel Volný <kvolny@redhat.com> 0.6.4-1
- new version
- see upstream changelog at http://qmmp.ylsoftware.com/index_en.php

* Tue Dec 11 2012 Karel Volný <kvolny@redhat.com> 0.6.3-1
- new version
- see upstream changelog at http://qmmp.ylsoftware.com/index_en.php

* Fri Aug 24 2012 Karel Volný <kvolny@redhat.com> 0.6.2-2
- update spec to newer style as suggested in package review
- removed %%buildroot actions
- removed %%clean section which got empty
- removed %%defattr

* Fri Aug 17 2012 Karel Volný <kvolny@redhat.com> 0.6.2-1
- new version
- fixes FSF address and execstack issues found by rpmlint
- see upstream changelog at http://qmmp.ylsoftware.com/index_en.php

* Tue Jul 31 2012 Karel Volný <kvolny@redhat.com> 0.6.1-1
- initial Fedora release
