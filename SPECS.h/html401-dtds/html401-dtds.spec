# Note to self: like is with the HTML 2.0 and 3.2 DTDs, HTML 4.0 and 4.01
# have the same public id to their ENTITIES files.  They are not exactly the
# same in 4.0 and 4.01, but the changes are in comments only, so no need
# use a hardcoded system id.  Well, until something installs another, and
# incompatible set of entities using the same public id anyway...

%define date    19991224

Name:           html401-dtds
Version:        4.01
Release:        %{date}.12%{?dist}.3
Summary:        HTML 4.01 document type definitions

# W3C Software License for DTDs etc:
# http://www.w3.org/Consortium/Legal/IPR-FAQ-20000620#DTD
License:        W3C
URL:            http://www.w3.org/TR/1999/REC-html401-%{date}/
# Source0 generated with Source99, see comments in the script
Source0:        %{name}-%{date}.tar.bz2
Source99:       %{name}-prepare-tarball.sh
Patch0:         %{name}-catalog.patch

BuildArch:      noarch
Requires:       sgml-common
Requires(post): /usr/bin/install-catalog
Requires(preun): /usr/bin/install-catalog

%description
This package provides the three HTML 4.01 DTDs (strict, frameset, and
transitional).  The DTDs are required for processing HTML 4.01
document instances using SGML tools such as OpenSP, OpenJade, or
SGMLSpm.


%prep
%setup -q -n %{name}
%patch0 -p1


%build


%install

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/sgml/html/4.01
install -pm 644 *.dtd *.cat *.ent *.decl \
    $RPM_BUILD_ROOT%{_datadir}/sgml/html/4.01

install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/sgml
cd $RPM_BUILD_ROOT%{_sysconfdir}/sgml
touch %{name}-%{version}-%{release}.soc
ln -s %{name}-%{version}-%{release}.soc %{name}.soc
cd -


%post
/usr/bin/install-catalog --add \
  %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.soc \
  %{_datadir}/sgml/html/4.01/HTML4.cat >/dev/null

%preun
/usr/bin/install-catalog --remove \
  %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.soc \
  %{_datadir}/sgml/html/4.01/HTML4.cat >/dev/null || :


%files
%ghost %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.soc
%{_sysconfdir}/sgml/%{name}.soc
%{_datadir}/sgml/html/


%changelog
* Tue Apr 15 2014 Liu Di <liudidi@gmail.com> - 4.01-19991224.12.3
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.01-19991224.12.2
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.01-19991224.12.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec  1 2011 Ville Skyttä <ville.skytta@iki.fi> - 4.01-19991224.12
- Add system entries to catalog.
- Drop specfile constructs no longer needed with Fedora or EL6+.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.01-19991224.11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.01-19991224.10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.01-19991224.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Ville Skyttä <ville.skytta@iki.fi> - 4.01-19991224.8
- Prune nondistributable content from source tarball.

* Mon Aug 13 2007 Ville Skyttä <ville.skytta@iki.fi> - 4.01-19991224.5
- Don't use %%{dist}.

* Mon Aug 13 2007 Ville Skyttä <ville.skytta@iki.fi> - 4.01-19991224.4
- Don't ship the docs, the W3C Documentation License is not an acceptable
  one per Fedora licensing guidelines.
- License: W3C

* Fri Sep 15 2006 Ville Skyttä <ville.skytta@iki.fi> - 4.01-19991224.3
- Rebuild.

* Tue Jun 20 2006 Ville Skyttä <ville.skytta@iki.fi> - 4.01-19991224.2
- Require install-catalog at post-install and pre-uninstall time (#181068).

* Sun Jun 18 2006 Ville Skyttä <ville.skytta@iki.fi> - 4.01-19991224.1
- Include specification date in release field (#181068).
- Make doc symlinks relative.

* Sat Feb 25 2006 Ville Skyttä <ville.skytta@iki.fi> - 4.01-0.3
- Improve description (#181068).
- Fold specification into main package as %%doc (#181068).

* Wed Jun 15 2005 Ville Skyttä <ville.skytta@iki.fi> - 4.01-0.2
- Rebuild for FC4.

* Sat Apr 16 2005 Ville Skyttä <ville.skytta@iki.fi> - 4.01-0.1
- Use -maxdepth before other options to find(1).

* Tue Jun 22 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:4.01-0.fdr.6
- Move files below %%{_datadir}/sgml/html/4.01, remove alternatives.
- Add non-versioned %%{_sysconfdir}/sgml/%%{name}.soc symlink.

* Sun Jun 20 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:4.01-0.fdr.5
- Add additional public id "aliases" for entities to SGML catalog as defined
  in ISO-HTML Annex B, http://purl.org/NET/ISO+IEC.15445/Users-Guide.html#DTD

* Sat Jun 19 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:4.01-0.fdr.4
- Add DTDDECLs to SGML catalog.

* Sun Dec  7 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:4.01-0.fdr.3
- Use alternatives to install preferred HTML DTD location.

* Sat Dec  6 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:4.01-0.fdr.2
- Install dir directly under %%{_datadir}/sgml.
- Spec cleanups.

* Tue Dec  2 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:4.01-0.fdr.1
- First build.
