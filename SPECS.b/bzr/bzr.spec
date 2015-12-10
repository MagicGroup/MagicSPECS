# It's not strictly necessary to conditionalize this but it's a reminder of
# when it can go away
%if 0%{?rhel} && 0%{?rhel} < 6
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

# Fedora 20 introduced unversioned docdirs.  In F20 and beyond, _pkgdocdir is
# already defined as %%{_docdir}/%%{name}.  This macro defines a suitable
# %%_pkgdocdir for previous releases and EPEL
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

# All package versioning is found here:
# the actual version is composed from these below, including leading 0 for release candidates
#   bzrmajor:  main bzr version
#   Version: bzr version, add subrelease version here
#   bzrrc: release candidate version, if any, line starts with % for rc, # for stable releas (no %).
#   release: rpm subrelease (0.N for rc candidates, N for stable releases)
%global bzrmajor 2.6
%global bzrminor .0
#global bzrrc b6
%global release 4

Name:           bzr
Version:        %{bzrmajor}%{?bzrminor}
Release:        %{release}%{?bzrrc:.}%{?bzrrc}%{?dist}
Summary:        Friendly distributed version control system
Summary(zh_CN.UTF-8): 一个版本控制系统

Group:          Development/Tools
Group(zh_CN.UTF-8): 开发/工具
License:        GPLv2+
URL:            http://www.bazaar-vcs.org/
Source0:        https://launchpad.net/%{name}/%{bzrmajor}/%{version}%{?bzrrc}/+download/%{name}-%{version}%{?bzrrc}.tar.gz
Source1:        https://launchpad.net/%{name}/%{bzrmajor}/%{version}%{?bzrrc}/+download/%{name}-%{version}%{?bzrrc}.tar.gz.sig
Source2:        bzr-icon-64.png
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python2-devel zlib-devel
# For building documents
BuildRequires:  python-sphinx
BuildRequires:  gettext
BuildRequires: Cython
%if 0%{?fedora} || (0%{?rhel} && 0%{?rhel} <= 6)
Requires:   python-paramiko
%endif
# Workaround Bug #230223 otherwise this would be a soft dependency
Requires:   python-pycurl
# ElementTree is part of python2.5 so only needed for EL-5
%if 0%{?rhel} && 0%{?rhel} <= 5
BuildRequires:   python-elementtree
Requires:   python-elementtree
%endif

%description
Bazaar is a distributed revision control system that is powerful, friendly,
and scalable.  It is the successor of Baz-1.x which, in turn, was
a user-friendly reimplementation of GNU Arch.

%description -l zh_CN.UTF-8
这一个版本控制工具。

%package doc
Summary:        Documentation for Bazaar
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档
%if 0%{?fedora} > 9
BuildArch:      noarch
%endif
Requires:       %{name} = %{version}-%{release}

%description doc
This package contains the documentation for the Bazaar version control system.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q -n %{name}-%{version}%{?bzrrc}

sed -i '1{/#![[:space:]]*\/usr\/bin\/\(python\|env\)/d}' bzrlib/_patiencediff_py.py
sed -i '1{/#![[:space:]]*\/usr\/bin\/\(python\|env\)/d}' bzrlib/weave.py

# Remove Cython generated .c files
find . -name '*_pyx.c' -exec rm \{\} \;

%build
# RHEL and Fedora < 19 have a distutils bug that doesn't add this
# automatically: https://bugzilla.redhat.com/show_bug.cgi?id=849994
%if (0%{?fedora} && 0%{?fedora} < 19) || (0%{?rhel} && 0%{?rhel} < 8)
export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%endif
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

chmod a-x contrib/bash/bzrbashprompt.sh

# Build documents
make docs-sphinx

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --install-data %{_datadir} --root $RPM_BUILD_ROOT
chmod -R a+rX contrib
chmod 0644 contrib/debian/init.d
chmod 0644 contrib/bzr_ssh_path_limiter
chmod 0644 contrib/bzr_access
chmod 0755 $RPM_BUILD_ROOT%{python_sitearch}/bzrlib/*.so

install -d $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/
install -m 0644 contrib/bash/bzr $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/
rm contrib/bash/bzr

# This is included in %doc, remove redundancy here
#rm -rf $RPM_BUILD_ROOT%{python_sitearch}/bzrlib/doc/

# Use independently packaged python-elementtree instead
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/bzrlib/util/elementtree/

# Install documents
install -d $RPM_BUILD_ROOT/%{_pkgdocdir}/pdf
cp -pr NEWS README TODO COPYING.txt contrib/ $RPM_BUILD_ROOT/%{_pkgdocdir}/
cd doc
for dir in *; do
    if [ -d $dir/_build/html ]; then
        cp -R $dir/_build/html $RPM_BUILD_ROOT%{_pkgdocdir}/$dir
        rm -f $RPM_BUILD_ROOT%{_pkgdocdir}/$dir/.buildinfo 
        rm -f $RPM_BUILD_ROOT%{_pkgdocdir}/$dir/_static/$dir/Makefile
        find $RPM_BUILD_ROOT%{_pkgdocdir}/$dir -name '*.pdf' | while read pdf; do
            ln $pdf $RPM_BUILD_ROOT%{_pkgdocdir}/pdf/
        done
    fi
done
cd ..

install -d $RPM_BUILD_ROOT%{_datadir}/pixmaps
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/pixmaps/bzr.png

%find_lang bzr

%clean
rm -rf $RPM_BUILD_ROOT


%files -f bzr.lang
%defattr(-,root,root,-)
%doc %{_pkgdocdir}/NEWS
%doc %{_pkgdocdir}/README
%doc %{_pkgdocdir}/TODO
%doc %{_pkgdocdir}/COPYING.txt
%doc %{_pkgdocdir}/contrib/
%{_bindir}/bzr
%{_mandir}/man1/*
%{python_sitearch}/bzrlib/
%{_sysconfdir}/bash_completion.d/
%{_datadir}/pixmaps/bzr.png
%if 0%{?fedora} || 0%{?rhel} > 5
%{python_sitearch}/*.egg-info
%endif

%files doc
%defattr(-,root,root,-)
%doc %{_pkgdocdir}/*
%exclude %{_pkgdocdir}/NEWS
%exclude %{_pkgdocdir}/README
%exclude %{_pkgdocdir}/TODO
%exclude %{_pkgdocdir}/COPYING.txt
%exclude %{_pkgdocdir}/contrib/

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 2.6.0-4
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 2.6.0-3
- 为 Magic 3.0 重建

* Tue Aug  6 2013 Toshio Kuratomi <toshio@fedoraproject.org> - -
- Move the documentation in the bzr-doc subpackage into _pkgdocdir.  This is
  a cleanup prompted by
  https://fedoraproject.org/wiki/Changes/UnversionedDocdirs but in addition to
  that feature also puts the documentation into the documentation directory for
  the main package.

* Sat Jul 27 2013 Henrik Nordstrom <henirk@henriknordstrom.net> - 2.6.0-1
- Upstream 2.6.0 release

* Fri Jun 28 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 2.5.1-13
- Fix for unicode traceback when doing bzr version
  https://bugzilla.redhat.com/show_bug.cgi?id=979399

* Tue May 28 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 2.5.1-12
- Patch for failure to gpg sign commits with no gpg-agent 
  https://bugzilla.redhat.com/show_bug.cgi?id=905087

* Tue May 28 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 2.5.1-11
- BuildRequires Cython so that the C extensions are built from their original sources.

* Tue May 28 2013 Ondrej Oprala <ooprala@redhat.com 2.5.1-10
- Conditionally add -fno-strict-aliasing to CFLAGS

* Tue May 28 2013 Ondrej Oprala <ooprala@redhat.com 2.5.1-9
- Add gettext to BuildRequires

* Mon May 27 2013 Ondrej Oprala <ooprala@redhat.com> 2.5.1-8
- Fix conditional include of python-paramiko

* Fri May 24 2013 Ondrej Oprala <ooprala@redhat.com> - 2.5.1-7
- Turn off strict aliasing in CFLAGS

* Fri May 24 2013 Ondrej Oprala <ooprala@redhat.com> - 2.5.1-6
- Add condition not to include python-paramiko in RHEL7 and above

* Fri May 24 2013 Ondrej Oprala <ooprala@redhat.com> - 2.5.1-5
- Fix unpackaged files error

* Thu May 23 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 2.5.1-4
- Patch for CVE-2013-2099
- Trim changelog

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 30 2012 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.5.1-1
- Upstream 2.5.1 bugfix release

* Fri Feb 24 2012 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.5.0-1
- Upstream 2.5.0 stable release

* Thu Feb 23 2012 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.5-0.3.b5
- Upstream 2.5b6 release

* Sun Feb  5 2012 Michel Salim <salimma@fedoraproject.org> - 2.5-0.2.b5
- Fix problem in generating documentation

* Tue Jan 17 2012 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.5-0.1.b5
- 2.5b5 final beta release of bzr 2.5

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 03 2011 Henrik Nordstrom <henrik@henriknordstorm.net> - 2.4.2-1
- Upstream 2.4.2 bugfix release

* Fri Sep 09 2011 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.4.1-1
- Upstream 2.4.1 bugfix release

* Fri Aug 12 2011 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.4.0-1
- Upstream 2.4.0 release

* Sun Jul 31 2011 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.4-0.5.b5
- Rebuilt for dependency changes

* Tue Jul 12 2011 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.4-0.4.b5
- Upstream 2.4b5 release

* Tue May 31 2011 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.4-0.3.b3
- Upstream 2.4b3 release

* Thu Apr 28 2011 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.4-0.2.b2
- Upstream 2.4b2 release

* Sun Mar 20 2011 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.4-0.1.b1
- Upstream 2.4b1 release

* Sun Mar 20 2011 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.3.1-1
- Upstream 2.3.1 bugfix release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.3.0-1
- Upstream 2.3.0 stable release

* Wed Jan 26 2011 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.3-0.4.b5
- Upstream 2.3b5 release

* Thu Dec 02 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.3-0.3.b4
- Upstream 2.3b4 release

* Sat Nov 06 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.3-0.2.b3
- Upstream 2.3b3 release

* Fri Oct 29 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.3-0.1.b2
- Upstream 2.3b2 release

* Wed Sep 29 2010 jkeating - 2.2.1-3
- Rebuilt for gcc bug 634757

* Sun Sep 21 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.2.1-2
- Backport bzr.dev rev 5439 change fixing lp: branch references
  (Toshio Kuratomi)

* Sun Sep 21 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.2.1-1
- Upstream 2.2.1 bugfix release

* Sat Aug 21 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.2.0-1
- Upstream 2.2.0 release

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.2-0.10.b4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 16 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.2-0.9.b4
- Upstream 2.2b4 release

* Mon May 31 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.2-0.8.b3
- Upstream 2.2b3 release

* Mon May 31 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 2.2-0.6.b1
- Add an icon for bzr.  This lets the gtk and qbzr plugins share the same icon
  for things like associating an image with a file type.

* Tue Apr 13 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 2.2-0.5.b1
- Clean up rhel/fedora conditionals bz#537254

* Mon Apr 12 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 2.2-0.4.b1
- Clean up some rpmlint warnings

* Mon Apr 12 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 2.2-0.3.b1
- Fixes so this spec file will also build on EL-5
- define => global

* Thu Apr 01 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.2-0.1.b1
- Upstream 2.2b1 beta release

* Tue Mar 30 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.1.1-1
- Upstream 2.1.1 bugfix release

* Wed Mar 03 2010 Henrik Nordstrom <henrik@henriknordstrom.net> -  2.1.0-1
- Update to 2.1.0

* Sat Feb 06 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.1.0-0.6.rc2
- Build HTML documentation and package in separate bzr-doc package
  (Bug #562392, Patch by Cheese Lee)

* Fri Feb 05 2010 Henrik Nordstrom <henrik@henriknordstrom.net> -  2.1.0-0.5.rc2
- Update to 2.1.0rc2

* Thu Dec 17 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.1.0-0.4.b4
- Update to 2.1.0b4

* Wed Oct 28 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.1.0-0.1.b1
- Highlights for this release include support for `bzr+ssh://host/~/homedir`
  style urls, finer control over the plugin search path via extended
  BZR_PLUGIN_PATH syntax, visible warnings when extension modules fail to
  load, and improved error handling during unlocking.

* Fri Sep 25 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.0.0-1
- Update to 2.0.0

* Thu Sep 10 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 2.0-0.1rc2
- Update to 2.0rc2 with new default repository format 2a

* Wed Aug 26 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.18-1
- Update to 1.18

* Thu Aug 20 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.18-0.1.rc1
- Update to 1.18rc1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.17-1
- Update to 1.17

* Mon Jul 13 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.17-0.1.rc1
- Update to 1.17rc1

* Fri Jun 26 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.16.1-1
- Update to 1.16.1

* Thu Jun 18 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.16-1
- Update to 1.16

* Wed Jun 10 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.15.1-1
- Update to 1.15.1

* Sat May 23 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.15-2
- Update to 1.15final

* Sat May 16 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.15-0.1.rc1
- Update to 1.15rc1

* Sat May 02 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.14.1-1
- Update to 1.14.1

* Wed Apr 29 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.14-1
- Update to 1.14

* Mon Apr 20 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.14-0.3.rc2
- Update to 1.14rc2

* Sat Apr 11 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.14-0.2.rc1
- Correct build dependencies

* Thu Apr 09 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.14-0.1.rc1
- Update to 1.14rc1

* Tue Mar 24 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.13.1-1
- Update to 1.13.1

* Mon Mar 16 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.13-1
- Update to 1.13

* Tue Mar 10 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.13-0.1.rc1
- Update to 1.13rc1

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.12-1
- Update to 1.12

* Tue Feb 10 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.12-0.1.rc1
- Update to 1.12rc1

* Mon Jan 19 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 1.11-1
- Update to 1.11

* Wed Dec 10 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 1.10-1
- Update to 1.10

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.9-2
- Rebuild for Python 2.6

* Thu Nov 13 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 1.9-1
- Update to 1.9

* Thu Sep 25 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 1.7-1
- 1.7 Final

* Wed Sep 3 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 1.7-0.1.rc2
- 1.7rc2
- Remove executable permission from a %%doc file

* Wed Sep 3 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 1.6.1-0.1.rc2
- New upstream bugfix release.

* Thu May 21 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5-2
- Upload tarball.

* Wed May 21 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5-1
- Update to 1.5.

* Thu May 15 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 1.4-2
- Workaround upstream Bug# 230223 by Requiring python-pycurl.

* Mon May 5 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 1.4-1
- Update to 1.4.

* Sun Apr 27 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.1-1
- Paramiko/sftp backport from 1.4.0. bz#444325
- Update to 1.3.1 final.

* Sat Apr 4 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.1-0.1.rc1
- Update to 1.3.1rc1 to fix a bug when you have a pack based remote repo and
  knit based local branch.

* Wed Mar 26 2008 Warren Togami <wtogami@redhat.com> - 1.3-1
- Update to 1.3.

* Mon Feb 25 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 1.2-1
- Update to 1.2.

* Fri Feb 8 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 1.1-2
- Rebuild for new gcc.

* Mon Jan 21 2008 Toshio Kuratomi <a.badger@gmail.com> - 1.1-1
- Upstream 1.1 bugfix and performance enhancement release.
- Enable bash completion script from the contrib directory.

* Thu Dec 13 2007 Toshio Kuratomi <a.badger@gmail.com> - 1.0-1
- Update to 1.0 final.

* Tue Dec 11 2007 Toshio Kuratomi <a.badger@gmail.com> - 1.0-0.1.rc3
- Update to 1.0rc3
- The new rawhide python package generates egg-info files.

* Fri Nov 30 2007 Toshio Kuratomi <a.badger@gmail.com> - 1.0-0.1.rc2
- Update to 1.0rc2

* Tue Aug 28 2007 Toshio Kuratomi <a.badger@gmail.com> - 0.91-1
- Update to 0.91.
  + Fixes some issues with using tag-enabled branches.

* Tue Aug 28 2007 Toshio Kuratomi <a.badger@gmail.com> - 0.90-1
- Update to 0.90

* Mon Aug 27 2007 Toshio Kuratomi <a.badger@gmail.com> - 0.90-0.1.rc1
- Update to 0.90rc1.
- 0.90 contains some pyrex code to speed things up.  bzr is now arch specific.
- Update license tag.

* Wed Jul 25 2007 Warren Togami <wtogami@redhat.com> - 0.18-1
- Update to 0.18.

* Tue Jun 26 2007 Warren Togami <wtogami@redhat.com>  - 0.17-2
- Update to 0.17.

* Tue May 08 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.16-1
- Update to 0.16.

* Thu Mar 22 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.15-1
- Update to 0.15.
- Simplify the %%files list.

* Tue Jan 23 2007 Toshio Kuratomi <toshio@tiki-lounge.com> - 0.14-1
- Update to 0.14
