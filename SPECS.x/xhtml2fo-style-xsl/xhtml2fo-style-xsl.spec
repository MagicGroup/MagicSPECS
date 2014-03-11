Name: xhtml2fo-style-xsl
Version: 20051222
Release: 7%{?dist}
Group: Applications/Text

Summary: Antenna House, Inc. XHTML to XSL:FO stylesheets
License: Copyright only
URL: http://www.antennahouse.com/XSLsample/XSLsample.htm

Requires(pre): xhtml1-dtds
Requires(pre): xml-common >= 0.6.3-8
#Requires(post): libxml2
#Requires(postun): libxml2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch
Source0: http://www.antennahouse.com/XSLsample/sample-xsl-xhtml2fo.zip
Source1: AntennaHouse-COPYRIGHT

%description
These XSL stylesheets allow you to transform any XHTML document to FO.
With a XSL:FO processor you could create PDF versions of XHTML documents.


%prep
%setup -q -c -n %{name}-%{version} -T -b 0
%__cp %{SOURCE1} .
%build


%install
%__rm -Rf $RPM_BUILD_ROOT
%__mkdir -p $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT/usr/share/sgml/xhtml1/xhtml2fo-stylesheets
%__mkdir -p $DESTDIR
%__cp *xsl $DESTDIR/

%clean
%__rm -Rf $RPM_BUILD_ROOT


%files
%defattr (-,root,root)
%doc AntennaHouse-COPYRIGHT
/usr/share/sgml/xhtml1/xhtml2fo-stylesheets


%post
CATALOG=%{_sysconfdir}/xml/catalog
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://www.antennahouse.com/XSLsample/sample-xsl-xhtml2fo/xhtml2fo.xsl" \
 "file:///usr/share/sgml/xhtml1/xhtml2fo-stylesheets/xhtml2fo.xsl" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://www.antennahouse.com/XSLsample/sample-xsl-xhtml2fo/xhtml2fo.xsl" \
 "file:///usr/share/sgml/xhtml1/xhtml2fo-stylesheets/xhtml2fo.xsl" $CATALOG

%postun
# remove entries only on removal of package
if [ "$1" = 0 ]; then
  CATALOG=%{_sysconfdir}/xml/catalog
  %{_bindir}/xmlcatalog --noout --del \
  "file://%{_datadir}/sgml/xhtml1/xhtml2fo-stylesheets/xhtml2fo.xsl" $CATALOG
fi


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 20051222-7
- 为 Magic 3.0 重建

* Fri Feb 24 2012 Liu Di <liudidi@gmail.com> - 20051222-6
- 为 Magic 3.0 重建

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20051222-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20051222-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20051222-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild


* Sun Oct 12 2008 Ismael Olea <ismael@olea.org> 20051222-2
- adding the %{?dist} macro to the spec

* Thu Jan 17 2008 Ismael Olea <ismael@olea.org> 20051222-1
- updating to last version of sample-xsl-xhtml2fo.zip
- fixing spec for contributing to Fedora and rpmlinting with 0.82																																		

* Mon Jan 10 2005 Ismael Olea <ismael@olea.org> 20050106-1
- First version (based on docbook-xsl-stylesheets.spec by Tim Waugh.

