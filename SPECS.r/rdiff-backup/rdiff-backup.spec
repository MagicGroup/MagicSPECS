%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Version: 1.2.8
Summary: Convenient and transparent local/remote incremental mirror/backup
Name: rdiff-backup
Release: 9%{?dist}

URL: http://www.nongnu.org/rdiff-backup/
Source: http://savannah.nongnu.org/download/%{name}/%{name}-%{version}.tar.gz
#
# Upstream bug: https://savannah.nongnu.org/bugs/?26064
#
Patch0: http://dev.sgu.ru/rpm/rdiff-backup--popen2.patch
License: GPLv2+
Group: Applications/Archiving
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: python-devel >= 2.2, librsync-devel >= 0.9.6

#recommended runtime dependencies
Requires: pylibacl, pyxattr

%description
rdiff-backup is a script, written in Python, that backs up one
directory to another and is intended to be run periodically (nightly
from cron for instance). The target directory ends up a copy of the
source directory, but extra reverse diffs are stored in the target
directory, so you can still recover files lost some time ago. The idea
is to combine the best features of a mirror and an incremental
backup. rdiff-backup can also operate in a bandwidth efficient manner
over a pipe, like rsync. Thus you can use rdiff-backup and ssh to
securely back a hard drive up to a remote location, and only the
differences from the previous backup will be transmitted.

%prep
%setup -q

%patch0 -p1

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root $RPM_BUILD_ROOT
# Produce .pyo files for %ghost directive later
python -Oc 'from compileall import *; compile_dir("'$RPM_BUILD_ROOT/%{python_sitearch}/rdiff_backup'")'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CHANGELOG COPYING FAQ.html README
%{_bindir}/rdiff-backup
%{_bindir}/rdiff-backup-statistics
%{_mandir}/man1/rdiff-backup*
%dir %{python_sitearch}/rdiff_backup
%{python_sitearch}/rdiff_backup/*.py
%{python_sitearch}/rdiff_backup/*.pyc
%{python_sitearch}/rdiff_backup/*.so
%{python_sitearch}/rdiff_backup/*.pyo
%if 0%{?fedora} >= 9
%{python_sitearch}/rdiff_backup-%{version}-py?.?.egg-info
%endif

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Mar 20 2010 Kevin Fenzi <kevin@tummy.com> - 1.2.8-4
- Add patch for cosmetic popen warning. Fixes bug #528940

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 12 2009 Kevin Fenzi <kevin@tummy.com> - 1.2.8-2
- Add conditional for egg info file (bug 490341)

* Thu Mar 26 2009 Kevin Fenzi <kevin@tummy.com> - 1.2.8-1
- Update to 1.2.8

* Thu Mar 12 2009 Kevin Fenzi <kevin@tummy.com> - 1.2.7-1
- Update to 1.2.7 (bug 486426)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Kevin Fenzi <kevin@tummy.com> - 1.2.5-1
- Update to 1.2.5

* Thu Jan 01 2009 Kevin Fenzi <kevin@tummy.com> - 1.2.4-1
- Update to 1.2.4

* Mon Dec 29 2008 Kevin Fenzi <kevin@tummy.com> - 1.2.3-1
- Update to 1.2.3
- Also fixes bug 477507

* Mon Dec 15 2008 Kevin Fenzi <kevin@tummy.com> - 1.2.2-1
- Update to 1.2.2 (bug 476539)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.2.1-3
- Fix locations for Python 2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.2.1-2
- Rebuild for Python 2.6

* Mon Sep 08 2008 Kevin Fenzi <kevin@tummy.com> - 1.2.1-1
- Update to 1.2.1

* Mon Aug 11 2008 Kevin Fenzi <kevin@tummy.com> - 1.2.0-1
- Update to 1.2.0

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.5-7
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Kevin Fenzi <kevin@tummy.com> 1.0.5-6
- Add egginfo file.

* Mon Aug 13 2007 Kevin Fenzi <kevin@tummy.com> 1.0.5-5
- Remove python-abi Requires

* Mon Aug 13 2007 Kevin Fenzi <kevin@tummy.com> 1.0.5-4
- Update License

* Fri Jun 15 2007 Gavin Henry <ghenry@suretecsystems.com> 1.0.5-3
- Applied patch from Marcin Zajaczkowski <mszpak ATT wp DOTT pl>
  for addition of pylibacl, pyxattr in Requires section

* Sun Dec 17 2006 Kevin Fenzi <kevin@tummy.com> - 1.0.5-2
- Rebuild for python 2.5

* Tue Dec 5  2006 Gavin Henry <ghenry@suretecsystems.com> - 0:1.0.5-1 
- Update to latest version

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1.0.4-3
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Kevin Fenzi <kevin@tummy.com> - 1.0.4-2
- Build for fc6
- No longer need to ghost pyo files (bug 205431)

* Fri Dec 9  2005 Gavin Henry <ghenry@suretecsystems.com> - 0:1.0.4-1 
- Update to latest version

* Fri Dec 9  2005 Gavin Henry <ghenry@suretecsystems.com> - 0:1.0.3-1 
- Update to latest version

* Wed Sep 14 2005 Gavin Henry <ghenry@suretecsystems.com> - 0:1.0.1-1
- New version

* Thu Aug 15 2005 Gavin Henry <ghenry@suretecsystems.com> - 0:1.0.0-1
- Latest version

* Wed May 11 2005 Bill Nottingham <notting@redhat.com> - 0:0.12.7-3
- rebuilt

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Jan 22 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.12.7-1
- Update to 0.12.7 which was released May 31st, 2004.
- Enhance spec with python-abi and arch-dependent sitelib paths.
- Update URL and Source.

* Sun Oct 05 2003 Ben Escoto <bescoto@stanford.edu> - 0:0.12.5-0.fdr.1
- Added epochs to python versions, more concise %%defines, %%ghost files

* Thu Aug 16 2003 Ben Escoto <bescoto@stanford.edu> - 0:0.12.3-0.fdr.4
- Implemented various suggestions of Fedora QA

* Sun Nov 4 2001 Ben Escoto <bescoto@stanford.edu>
- Initial RPM
