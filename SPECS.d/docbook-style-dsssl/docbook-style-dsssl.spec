Name: docbook-style-dsssl
Version: 1.79
Release: 14%{?dist}
Group: Applications/Text

Summary: Norman Walsh's modular stylesheets for DocBook

License: Copyright only
URL: http://docbook.sourceforge.net/

Requires: docbook-dtds
Requires: openjade
Requires: sgml-common
Requires(post): sgml-common
Requires(preun): sgml-common

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch: noarch
Source0: http://prdownloads.sourceforge.net/docbook/docbook-dsssl-%{version}.tar.gz
Source1: %{name}.Makefile


%description
These DSSSL stylesheets allow to convert any DocBook document to another
printed (for example, RTF or PostScript) or online (for example, HTML) format.
They are highly customizable.

%prep
%setup -q -n docbook-dsssl-%{version}
cp %{SOURCE1} Makefile


%build


%install
DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
make install BINDIR=$DESTDIR/usr/bin DESTDIR=$DESTDIR/usr/share/sgml/docbook/dsssl-stylesheets-%{version} MANDIR=$DESTDIR%{_mandir}
cd ..
ln -s dsssl-stylesheets-%{version} $DESTDIR/usr/share/sgml/docbook/dsssl-stylesheets


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-,root,root,-)
%doc BUGS README ChangeLog WhatsNew
/usr/bin/collateindex.pl
%{_mandir}/man1/collateindex.pl.1*
/usr/share/sgml/docbook/dsssl-stylesheets-%{version}
/usr/share/sgml/docbook/dsssl-stylesheets


%post
for centralized in /etc/sgml/*-docbook-*.cat
do
  /usr/bin/install-catalog --add $centralized \
    /usr/share/sgml/docbook/dsssl-stylesheets-%{version}/catalog \
    > /dev/null 2>/dev/null
done


%preun
if [ "$1" = "0" ]; then
  for centralized in /etc/sgml/*-docbook-*.cat
  do
    /usr/bin/install-catalog --remove $centralized /usr/share/sgml/docbook/dsssl-stylesheets-%{version}/catalog > /dev/null 2>/dev/null
  done
fi
exit 0

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1.79-14
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.79-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jun 07 2010 Ondrej Vasik <ovasik@redhat.com> - 1.79-11
- do not touch openjade catalogs by this package - it's
  done in docbook-dtds (#600878)

* Tue Feb 02 2010 Ondrej Vasik <ovasik@redhat.com> - 1.79-10
- fix merge review issues(#225703)

* Fri Dec 18 2009 Ondrej Vasik <ovasik@redhat.com> - 1.79-9
- License Copyright only

* Fri Aug 28 2009 Ondrej Vasik <ovasik@redhat.com> - 1.79-8
- ship manpage for collateindex.pl
- preserve attributes and timestamps in Makefile

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.79-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.79-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 05 2007 Ondrej Vasik <ovasik@redhat.com> - 1.79-5
- rpmlint cleanup
- fixed summary, dist tag, license tag, cosmetic spec cleanup

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.79-4.1
- rebuild

* Tue Dec 20 2005 Tim Waugh <twaugh@redhat.com> 1.79-4
- Rebuilt again.

* Mon Dec 19 2005 Tim Waugh <twaugh@redhat.com> 1.79-3
- Rebuilt.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 10 2005 Tim Waugh <twaugh@redhat.com> 1.79-2
- Ship olink.dsl (bug #172523).

* Mon Nov  8 2004 Tim Waugh <twaugh@redhat.com> 1.79-1
- 1.79.
- No longer need articleinfo patch.

* Wed Sep 22 2004 Than Ngo <than@redhat.com> 1.78-4
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Mar 28 2003 Tim Waugh <twaugh@redhat.com> 1.78-2
- Require new docbook-dtds.
- Fix %%post scriptlet.

* Fri Mar 14 2003 Tim Waugh <twaugh@redhat.com> 1.78-1
- Require openjade 1.3.2.
- 1.78, incorporating seealso, aname patches.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Nov 20 2002 Tim Powers <timp@redhat.com>
- rebuild in current collinst

* Fri Jul 26 2002 Tim Waugh <twaugh@redhat.com> 1.76-6
- In HTML output always close anchor tags (bug #69737).

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 1.76-5
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com> 1.76-4
- automated rebuild

* Fri May  3 2002 Tim Waugh <twaugh@redhat.com> 1.76-3
- Another go at fixing seealso handling (bug #64111).

* Thu May  2 2002 Tim Waugh <twaugh@redhat.com> 1.76-2
- Fix collateindex.pl's seealso handling (bug #64111).

* Fri Feb 22 2002 Tim Waugh <twaugh@redhat.com> 1.76-1
- 1.76 (fixes bug #58883).
- Fix HTML generation for articleinfo elements (bug #58837).

* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 1.75-1
- 1.75.
- Rebuild in new environment.

* Mon Jan 28 2002 Tim Waugh <twaugh@redhat.com> 1.74b-3
- Prepare for openjade 1.3.1.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 1.74b-2
- automated rebuild

* Mon Dec  3 2001 Tim Waugh <twaugh@redhat.com> 1.74b-1
- 1.74b.

* Fri Nov  2 2001 Tim Waugh <twaugh@redhat.com> 1.73-3
- Conflict with docbook-utils if its custom stylesheet hasn't been
  updated to work with version 1.72 or later of this package.

* Fri Oct 19 2001 Tim Waugh <twaugh@redhat.com> 1.73-2
- Shut the scripts up.

* Mon Oct  1 2001 Tim Waugh <twaugh@redhat.com> 1.73-1
- 1.73.

* Fri Sep 28 2001 Tim Waugh <twaugh@redhat.com> 1.72-1
- 1.72.

* Wed Jul 25 2001 Bill Nottingham <notting@redhat.com> 1.64-3
- bump release 

* Thu May  9 2001 Tim Waugh <twaugh@redhat.com> 1.64-2
- Make an unversioned dsssl-stylesheets symbolic link.

* Wed May  2 2001 Tim Waugh <twaugh@redhat.com> 1.64-1
- 1.64 (fixes #38095).
- Fix up post/preun scripts so that we don't get duplicate entries with
  different versions on upgrade.

* Sun Mar 25 2001 Tim Waugh <twaugh@redhat.com> 1.59-10
- Fix up Makefile (patch from SATO Satoru).
- Change postun to preun.
- Make preun conditional on remove rather than upgrade.

* Tue Mar  6 2001 Tim Waugh <twaugh@redhat.com>
- PreReq docbook-dtd-sgml (it was a requirement before), so that the
  scripts work right.

* Tue Feb 20 2001 Tim Waugh <twaugh@redhat.com>
- Change Requires(...) to PreReq at Preston's request.
- PreReq at least openjade-1.3-12, so that its catalogs get installed.

* Wed Jan 24 2001 Tim Waugh <twaugh@redhat.com>
- Make scripts quieter.

* Tue Jan 23 2001 Tim Waugh <twaugh@redhat.com>
- Last fix was wrong; corrected (require openjade 1.3).

* Fri Jan 19 2001 Tim Waugh <twaugh@redhat.com>
- Require jade not openjade (bug #24306).

* Mon Jan 15 2001 Tim Waugh <twaugh@redhat.com>
- Don't play so many macro games.
- Change requirement on /usr/bin/install-catalog to sgml-common.
- Be sure to own dsssl-stylesheets-1.59 directory.

* Mon Jan 08 2001 Tim Waugh <twaugh@redhat.com>
- Change group.
- openjade not jade.
- %%{_tmppath}.
- rm before install.
- Change Copyright: to License:.
- Remove Packager: line.

* Mon Jan 08 2001 Tim Waugh <twaugh@redhat.com>
- Based on Eric Bischoff's new-trials packages.
