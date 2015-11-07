Name:          yelp-tools
Version:       3.11.3
Release:       2%{?dist}
Summary:       Create, manage, and publish documentation for Yelp

Group:         Applications/Publishing
License:       GPLv2+
URL:           http://projects.gnome.org/yelp/
Source0:       http://download.gnome.org/sources/yelp-tools/3.11/yelp-tools-%{version}.tar.xz
BuildArch:     noarch

BuildRequires: yelp-xsl-devel
BuildRequires: itstool
BuildRequires: libxslt

Requires: /usr/bin/itstool
Requires: /usr/bin/xmllint
Requires: yelp-xsl

%description
yelp-tools is a collection of scripts and build utilities to help create,
manage, and publish documentation for Yelp and the web. Most of the heavy
lifting is done by packages like yelp-xsl and itstool. This package just
wraps things up in a developer-friendly way.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%doc AUTHORS COPYING COPYING.GPL README
%{_bindir}/yelp-build
%{_bindir}/yelp-check
%{_bindir}/yelp-new
%{_datadir}/yelp-tools
%{_datadir}/aclocal/yelp.m4

%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 3.11.3-2
- 为 Magic 3.0 重建

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Mon Nov 25 2013 Richard Hughes <rhughes@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Tue Nov 19 2013 Richard Hughes <rhughes@redhat.com> - 3.11.1-1
- Update to 3.11.1

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.1-1
- Update to 3.9.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Tue Sep 18 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.92-1
- Update to 3.5.92

* Tue Sep 04 2012 Richard Hughes <hughsient@gmail.com> - 3.5.91-1
- Update to 3.5.91

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-2
- Depend on itstool and xmllint, which are required by yelp.m4

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.4-1
- Update to 3.3.4

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.1-1
- Update to 3.3.1

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> 3.1.7-1
- Update to 3.1.7

* Wed Sep 07 2011 Kalev Lember <kalevlember@gmail.com> 3.1.6-1
- Update to 3.1.6

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> 3.1.5-1
- Update to 3.1.5

* Mon Jun 16 2011 Zeeshan Ali <zeenix@redhat.com> 3.1.4-1
- Initial release.
