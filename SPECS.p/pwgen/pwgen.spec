Name:           pwgen
Version:        2.07
Release:        2%{?dist}
Summary:        Automatic password generation

Group:          Applications/System
License:        GPL+
URL:            http://sf.net/projects/pwgen
Source0:        http://download.sf.net/pwgen/pwgen-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pwgen generates random, meaningless but pronounceable passwords. These
passwords contain either only lowercase letters, or upper and lower case, or
upper case, lower case and numeric digits. Upper case letters and numeric
digits are placed in a way that eases memorizing the password.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%doc debian/changelog debian/copyright
%{_bindir}/pwgen
%{_mandir}/man1/pwgen.1*


%changelog
* Sun Mar 01 2015 Liu Di <liudidi@gmail.com> - 2.07-2
- 为 Magic 3.0 重建

* Fri Dec 5 2014 Orion Poplawski <orion@cora.nwra.com> - 2.07-1
- Update to 2.07 (bug 1159526) fixes:
  CVE-2013-4440 (bug 1020222, 1020223)
  CVE-2013-4442 (bug 1020259, 1020261)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.06-3
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 James Bowes <jbowes@redhat.com> - 2.06-2
- Mark license as GPL+

* Sun Aug 05 2007 James Bowes <jbowes@redhat.com> - 2.06-1
- Update to 2.06

* Mon Sep 11 2006 James Bowes <jbowes@redhat.com> - 2.05-4
- EVR bumped for mass rebuild.

* Sat Mar 25 2006 James Bowes <jbowes@redhat.com> - 2.05-3
- Add dist tag to release.
- Don't strip binary, since rpmbuild will do it.

* Fri Mar 24 2006 James Bowes <jbowes@redhat.com> - 2.05-2
- Use url for Source0 in spec file.
- Use glob for man page extension.

* Sun Mar 12 2006 James Bowes <jbowes@redhat.com> - 2.05-1
- Initial Fedora packaging.
