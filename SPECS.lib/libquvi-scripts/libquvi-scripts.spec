%define debug_package %{nil}

Name:           libquvi-scripts
Version:        0.4.9 
Release:        2%{?dist}
Summary:        Embedded lua scripts that libquvi uses for parsing the media details

Group:          Applications/Internet
License:        LGPLv2+
URL:            http://quvi.sourceforge.net/
Source0:        http://downloads.sourceforge.net/quvi/%{name}-%{version}.tar.xz

BuildArch:      noarch

%description
libquvi-scripts contains the embedded lua scripts that libquvi
uses for parsing the media details. Some additional utility
scripts are also included.


%prep
%setup -q

%build
%configure --with-nsfw --with-nlfy

%install
make install DESTDIR=$RPM_BUILD_ROOT pkgconfigdir=%{_datadir}/pkgconfig/

%files
%doc ChangeLog COPYING README AUTHORS NEWS 
%{_datadir}/%{name}/
%{_mandir}/man7/%{name}.7.*
%{_datadir}/pkgconfig/%{name}.pc

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.4.9-2
- 为 Magic 3.0 重建

* Sun Oct 28 2012 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.9-1
- Update to 0.4.9

* Fri Aug 10 2012 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.7-1
- Update to 0.4.7

* Sun Jul 15 2012 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.6-1
- Update to 0.4.6

* Thu Mar 29 2012 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.4-1
- Update to 0.4.4

* Sun Mar 11 2012 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.3-1
- Update to 0.4.3

* Fri Dec  2 2011 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.2-1
- Update to 0.4.2

* Thu Nov 10 2011 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.1-1
- Update to 0.4.1

* Tue Oct 11 2011 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.0-3
- Remove the devel subpackage
- The package is now noarch

* Sun Oct  9 2011 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.0-2
- Create the devel subpackage

* Sat Oct  8 2011 Nicoleau Fabien <nicoleau.fabien@gmail.com> 0.4.0-1
- Initial build
