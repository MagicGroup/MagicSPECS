Name: docbook5-style-xsl
Version: 1.78.0
Release: 2%{?dist}
Group: Applications/Text

Summary: Norman Walsh's XSL stylesheets for DocBook 5.X

# Package is licensed as MIT/X (http://wiki.docbook.org/topic/DocBookLicense),
# some .js files under ./slides/browser/ are licensed MPLv1.1
License: MIT and MPLv1.1
URL: http://wiki.docbook.org/DocBookXslStylesheets

Provides: docbook-xsl-ns = %{version}
# xml-common was using /usr/share/xml until 0.6.3-8.
Requires: xml-common >= 0.6.3-8
# libxml2 required because of usage of /usr/bin/xmlcatalog
Requires(post): libxml2 >= 2.4.8
Requires(postun): libxml2 >= 2.4.8
Conflicts: passivetex < 1.21

BuildArch: noarch
Source0: http://downloads.sourceforge.net/docbook/docbook-xsl-ns-%{version}.tar.bz2

%description
These XSL namespace aware stylesheets allow you to transform any
DocBook 5 document to other formats, such as HTML, manpages, FO,
XHMTL and other formats. They are highly customizable. For more
information see W3C page about XSL.

%prep
%setup -q -n docbook-xsl-ns-%{version}
#remove .gitignore files
rm -rf $(find -name '.gitignore' -type f)
#make ruby scripts executable
chmod +x epub/bin/dbtoepub

%build

%install
DESTDIR=$RPM_BUILD_ROOT
mkdir -p $DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%version
cp -a [[:lower:]]* $DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%version/
cp -a VERSION $DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%version/VERSION.xsl
ln -s VERSION.xsl \
$DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%version/VERSION
ln -s xsl-ns-stylesheets-%{version} \
 $DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets

# Don't ship the extensions.
rm -rf $DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets/extensions
# Don't ship install shell script.
rm -rf $DESTDIR%{_datadir}/sgml/docbook/xsl-ns-stylesheets/install.sh

%files
%defattr (-,root,root,-)
%doc BUGS
%doc README COPYING
%doc TODO NEWS
%doc RELEASE-NOTES.*
%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}
%{_datadir}/sgml/docbook/xsl-ns-stylesheets

%post
CATALOG=%{_sysconfdir}/xml/catalog
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://docbook.sourceforge.net/release/xsl-ns/%{version}" \
 "file://%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://docbook.sourceforge.net/release/xsl-ns/%{version}" \
 "file://%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://docbook.sourceforge.net/release/xsl-ns/current" \
 "file://%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://docbook.sourceforge.net/release/xsl-ns/current" \
 "file://%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}" $CATALOG


%postun
# remove entries only on removal of package
if [ "$1" = 0 ]; then
  CATALOG=%{_sysconfdir}/xml/catalog
  %{_bindir}/xmlcatalog --noout --del \
   "file://%{_datadir}/sgml/docbook/xsl-ns-stylesheets-%{version}" $CATALOG
fi

%changelog
* Thu Jan 03 2013 Ondrej Vasik <ovasik@redhat.com> 1.78.0-2
- resolve missing VERSION.xsl (#891459)

* Thu Dec 20 2012 Ondrej Vasik <ovasik@redhat.com> 1.78.0-1
- new upstream release 1.78.0

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.77.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 05 2012 Ondrej Vasik <ovasik@redhat.com> 1.77.1-1
- new upstream release 1.77.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.76.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 02 2010 Ondrej Vasik <ovasik@redhat.com> 1.76.1-1
- new upstream release 1.76.1

* Mon Sep 06 2010 Ondrej Vasik <ovasik@redhat.com> 1.76.0-1
- new upstream release 1.76.0

* Tue Feb 23 2010 Ondrej Vasik <ovasik@redhat.com> 1.75.2-4
- fix the licenses, use better URL

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.75.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Ondrej Vasik <ovasik@redhat.com> 1.75.2-2
- upstream changed tarballs after release

* Tue Jul 21 2009 Ondrej Vasik <ovasik@redhat.com> 1.75.2-1
- new upstream release 1.75.2

* Thu May 28 2009 Ondrej Vasik <ovasik@redhat.com> 1.75.1-1
- new upstream release 1.75.1

* Mon May 11 2009 Ondrej Vasik <ovasik@redhat.com> 1.75.0-1
- new upstream release 1.75.0

* Wed Mar 11 2009 Ondrej Vasik <ovasik@redhat.com> 1.74.3-1
- new upstream release 1.74.3

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.74.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Ondrej Vasik <ovasik@redhat.com> 1.74.2-1
- new upstream release 1.74.2

* Wed Feb 18 2009 Ondrej Vasik <ovasik@redhat.com> 1.74.1-1
- new upstream release 1.74.1

* Fri Feb 13 2009 Ondrej Vasik <ovasik@redhat.com> 1.74.0-2
- Ship VERSION file (#485297) , ship RELEASE-NOTES

* Mon Nov 10 2008 Ondrej Vasik <ovasik@redhat.com> 1.74.0-1
- Initial Fedora release
