
%global scintilla_ver 2.25 

# bootstrapping -python
%global python 1

Name:    qscintilla
Version: 2.6.2
Release: 4%{?dist}
Summary: A Scintilla port to Qt

# matches up (pretty much) with qt4
License: GPLv3 or GPLv2 with exceptions
Group:   Development/Tools
Url:     http://www.riverbankcomputing.com/software/qscintilla/
Source0: http://www.riverbankcomputing.com/static/Downloads/QScintilla2/QScintilla-gpl-%{version}.tar.gz  
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

## Upstreamable patches
# posted to upstream ml, not in archive yet
Patch50: QScintilla-gpl-2.6.2-qt4qt5_designer_incpath.patch

Obsoletes: qscintilla-designer < 2.4-3
Provides:  qscintilla-designer = %{version}-%{release}
%{?_isa:Provides: qscintilla-designer%{_isa} = %{version}-%{release}}

BuildRequires: pkgconfig(QtDesigner) pkgconfig(QtGui) pkgconfig(QtScript) pkgconfig(QtXml)

# for -python
%if 0%{?python}
%{!?python_sitearch:%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%global pyqt4_version 4.7 
BuildRequires:  PyQt4-devel >= %{pyqt4_version} 
BuildRequires:  sip-devel 
%endif


%description
QScintilla is a port of Scintilla to the Qt GUI toolkit.

%{?scintilla_ver:This version of QScintilla is based on Scintilla v%{scintilla_ver}.}

%package devel
Summary:  QScintilla Development Files
Group:    Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt4-devel 
%description devel
%{summary}.

%package python
Summary:  QScintilla PyQt4 bindings
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: PyQt4 >= %{pyqt4_version}
%{?_sip_api:Requires: sip-api(%{_sip_api_major}) >= %{_sip_api}}
%description python
%{summary}.

%package python-devel
Summary:  Development files for QScintilla PyQt4 bindings 
Group:    Development/Libraries
Requires: PyQt4-devel
Requires: sip-devel
%if 0%{?fedora} > 9 || 0%{?rhel} > 5
BuildArch: noarch
# when noarch landed
Obsoletes: qscintilla-python-devel < 2.4-4
%endif

%description python-devel
%{summary}.


%prep
%setup -q -n QScintilla-gpl-%{version}

%patch50 -p1 -b .qt4_designer_incpath

# fix line endings in license file(s)
sed -i 's/\r//' LICENSE.GPL2 GPL_EXCEPTION_ADDENDUM.TXT


%build
pushd Qt4Qt5
%{_qt4_qmake} qscintilla.pro
make %{?_smp_mflags}
popd

pushd designer-Qt4
%{_qt4_qmake} designer.pro
make %{?_smp_mflags}
popd

%if 0%{?python}
pushd Python
%{__python} \
  configure.py \
    -c -j 3 \
    -n ../Qt4Qt5 \
    -o ../Qt4Qt5
make %{?_smp_mflags}
popd
%endif


%install
rm -rf %{buildroot}

make -C Qt4Qt5 install INSTALL_ROOT=%{buildroot} 
make -C designer-Qt4 install INSTALL_ROOT=%{buildroot}
%if 0%{?python}
make -C Python install DESTDIR=%{buildroot}
%endif
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc NEWS README
%doc LICENSE.GPL3 LICENSE.GPL2
%doc GPL_EXCEPTION.TXT GPL_EXCEPTION_ADDENDUM.TXT
%{_qt4_libdir}/libqscintilla2.so.8*
%{_qt4_plugindir}/designer/libqscintillaplugin.so
%{_qt4_translationdir}/*
%{_qt4_prefix}/qsci/

%files devel
%defattr(-,root,root,-)
%doc doc/html-Qt4Qt5 doc/Scintilla example-Qt4Qt5
%{_qt4_headerdir}/Qsci/
%{_qt4_libdir}/libqscintilla2.so

%if 0%{?python}
%files python
%defattr(-,root,root,-)
%{python_sitearch}/PyQt4/Qsci.so

%files python-devel
%defattr(-,root,root,-)
%{_datadir}/sip/PyQt4/Qsci/
%endif


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.6.2-4
- 为 Magic 3.0 重建

* Mon Oct 01 2012 Rex Dieter <rdieter@fedoraproject.org> 2.6.2-3
- rebuild (sip)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Rex Dieter <rdieter@fedoraproject.org> 2.6.2-1
- 2.6.2

* Sat Feb 11 2012 Rex Dieter <rdieter@fedoraproject.org> 2.6.1-1
- 2.6.1
- pkgconfig-style deps

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 23 2011 Rex Dieter <rdieter@fedoraproject.org> 2.6-2
- rebuild (sip/PyQt4)

* Sat Dec 03 2011 Rex Dieter <rdieter@fedoraproject.org> 2.6-1
- 2.6

* Fri Nov 11 2011 Rex Dieter <rdieter@fedoraproject.org> 2.5.1-2
- rebuild (sip)

* Fri May 06 2011 Rex Dieter <rdieter@fedoraproject.org> 2.5.1-1
- 2.5.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4.6-1
- 2.4.6

* Thu Sep 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4.5-1
- 2.4.5

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 14 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4.4-1
- 2.4.4

* Thu Mar 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4.3-1
- 2.4.3

* Thu Jan 21 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4.2-1
- 2.4.2

* Fri Jan 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4.1-1
- 2.4.1 
- pyqt4_version 4.7

* Thu Jan 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4-10 
- rebuild (sip)

* Fri Nov 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-9
- -python: Requires: sip-api(%%_sip_api_major) >= %%_sip_api
- -python-devel: Requires: sip-devel

* Mon Nov 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-8 
- rebuild (for qt-4.6.0-rc1, f13+)

* Wed Nov 11 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-7
- pyqt4_version 4.6.1

* Wed Oct 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-6
- autocomplete_popup patch

* Fri Oct 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-5
- rebuild (PyQt4)

* Tue Aug 11 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-4
- -python-devel: make noarch, drop dep on -python

* Sat Aug 08 2009 Rex Dieter <rdieter@fedoraproject.org - 2.4-3
- include designer plugin in main pkg, Obsoletes: qscintilla-designer

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-1
- QScintilla-gpl-2.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.3.2-2
- Rebuild for Python 2.6

* Mon Nov 17 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.3.2-1
- Qscintilla-gpl-2.3.2
- soname bump 4->5

* Mon Nov 10 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.3.1-1
- Qscintilla-gpl-2.3.1

* Mon Sep 22 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.3-1
- Qscintilla-gpl-2.3
- scintilla_ver is missing (#461777)

* Fri Jul 18 2008 Dennis Gilmore <dennis@ausil.us> - 2.2-3
- rebuild for newer PyQT4
- fix #449423 properly

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.2-2
- fix build (#449423)

* Mon May 05 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.2-1
- Qscintilla-gpl-2.2
- License: GPLv3 or GPLv2 with exceptions

* Thu Feb 14 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.1-4
- use %%_qt4_* macros (preparing for qt4 possibly moving %%_qt4_datadir)
- -python: fix Requires
- -python-devel: new pkg
- omit Obsoletes: PyQt-qscintilla 
  (leave that to PyQt, that can get the versioning right)

* Mon Jan 28 2008 Dennis Gilmore <dennis@ausil.us> - 2.1-3
- fix typo in Obsoletes: on python package

* Mon Jan 28 2008 Dennis Gilmore <dennis@ausil.us> - 2.1-2
- remove dumb require on di from qscintilla-python

* Mon Jan 28 2008 Dennis Gilmore <dennis@ausil.us> - 2.1-1
- update to 2.1 branch

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.7.1-3
- respin (BuildID)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.7.1-2
- License: GPLv2+

* Mon Dec 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 1.7.1-1
- QScintilla-1.71-gpl-1.7.1

* Thu Nov 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 1.7-1
- QScintilla1-1.71-gpl-1.7 (#214192)

* Sun Sep 03 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.6-3.3
- FC6 rebuild.
- Export flags.

* Mon Feb 13 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.6-3.2
- FC5 Rebuild.

* Tue Jan 31 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.6-3.1
- Rebuild for FC5.

* Wed Sep 14 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 1.6-3
- Fix permissions in prep, not in install.

* Tue Sep 13 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 1.6-2
- Fix permissions on doc files to be 0644.

* Sun Sep 11 2005 Konstantin Ryabitsev <icon@linux.duke.edu> 1.6-1
- Update to 1.65-gpl-1.6
- Use the patch from Aurelien Bompard to build sanely in buildroot
- Include docs and examples for the -devel package

* Sat Aug 27 2005 Konstantin Ryabitsev <icon@linux.duke.edu> 1.5.1-1
- Adapt for Fedora Extras
- Drop 0-Epoch
- Make specfile simpler
- Move .so to devel

* Mon Mar 09 2005 Rex Dieter 0:1.5.1-0.0.kde
- 1.5.1

* Thu Sep 16 2004 Rex Dieter <rexdieter at sf.net> 0:1.4-0.1.kde
- updated designer-incpath patch: don't require an already installed
  qscintilla-devel
- BuildConflicts: qscintilla-devel != %%version

* Thu Sep 16 2004 Rex Dieter <rexdieter at sf.net> 0:1.4-0.0.kde
- 1.4
- include designer plugin
- Prereq: %%qtdir

* Fri May 28 2004 Rex Dieter <rexdieter at sf.net> 0:1.3-0.fdr.0
- 1.3

* Thu Mar 11 2004 Rex Dieter <rexdieter at sf.net> 0:1.2-0.fdr.6
- dynamically determine version for qt dependancy.

* Wed Mar 10 2004 Rex Dieter <rexdieter at sf.net> 0:1.2-0.fdr.5
- (re)build against qt-3.3.1

* Wed Dec 03 2003 Rex Dieter <rexdieter at sf.net> 0:1.2-0.fdr.4
- remove extraneous macros
- (re)build against qt-3.2.3

* Mon Nov 10 2003 Rex Dieter <rexdieter at sf.net> 0:1.2-0.fdr.3
- (re)build against qt-3.2.2

* Wed Sep 17 2003 Rex Dieter <rexdieter at sf.net> 0:1.2-0.fdr.2
- use Epoch's in Requires

* Tue Aug 19 2003 Rex Dieter <rexdieter at sf.net> 0:1.2-0.fdr.1
- 1.2

