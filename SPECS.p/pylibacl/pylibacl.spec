Name:		pylibacl
Summary:	POSIX.1e ACLs library wrapper for python
Summary(zh_CN.UTF-8): POSIX.1e ACL 库的 Python 接口
Version:	0.5.3
Release:	2%{?dist}
#license version is precised on a website
License:	LGPLv2+
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:		http://pylibacl.sourceforge.net/
Source:		https://github.com/iustin/pylibacl/archive/pylibacl-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides:	python-libacl = %{version}-%{release}
Obsoletes:	python-libacl <= %{version}-%{release}
#libacl package is already forced by RPM
Requires:	python >= 2.4
BuildRequires:	python-devel, libacl-devel, python-setuptools

%description
Python extension module for POSIX ACLs. It allows to query, list,
add and remove ACLs from files and directories.

%description -l zh_CN.UTF-8
POSIX.1e ACL 库的 Python 接口。

%prep
%setup -q

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --root="%{buildroot}"
magic_rpm_clean.sh

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc COPYING README NEWS
%{python_sitearch}/posix1e.so
%{python_sitearch}/*egg-info

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.5.3-2
- 为 Magic 3.0 重建

* Fri Aug 14 2015 Liu Di <liudidi@gmail.com> - 0.5.3-1
- 更新到 0.5.3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.5.1-2
- fix wrong licence tag - starting from 0.4 it should be LGPLv2+ instead of GPLv2+

* Tue Jun 26 2012 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.5.1-1
- updated to 0.5.1
- fix bugs found with cpycheck (bug 800126)
- adjust minimal required Python version to 2.4

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul 06 2010 Kevin Fenzi <kevin@tummy.com> - 0.5.0-1
- Update to 0.5.0
- Fix egg-info

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2.2-5
- Rebuild for Python 2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2.2-4
- Rebuild for Python 2.6

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.2-3
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.2-2
- added compatibility with Python Eggs forced in F9

* Mon Aug 27 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.2-1
- upgraded to 0.2.2

* Sun Aug 26 2007 Kevin Fenzi <kevin@tummy.com> - 0.2.1-7
 - Updated License tag

* Wed Apr 25 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.1-6
 - added Provides/Obsoletes tags

* Sat Apr 21 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.1-5
 - removed redundant after name change "exclude" tag
 - comments cleanup

* Wed Apr 18 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.1-4
 - applied suggestions from Kevin Fenzi
 - name changed from python-libacl to pylibacl
 - corrected path to the source file

* Fri Apr 6 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.1-3
 - fixed path to a source package

* Thu Apr 5 2007 Marcin Zajaczkowski <mszpak ATT wp DOTT pl> - 0.2.1-2
 - added python-devel in BuildRequires
 - added Provides section
 - modified to Fedora Extras requirements

* Sun Sep 11 2005 Dag Wieers <dag@wieers.com> - 0.2.1-1
- Initial package. (using DAR)
