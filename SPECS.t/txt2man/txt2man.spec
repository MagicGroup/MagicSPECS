Name:           txt2man
Version:        1.5.6
Release:        5%{?dist}
Summary:        Convert flat ASCII text to man page format

Group:          Applications/Text
License:        GPLv2+
URL:            http://mvertes.free.fr/txt2man/
Source0:        http://mvertes.free.fr/download/%{name}-%{version}.tar.gz
#Fixes bug with bashisms in /bin/sh script, see http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=473696
#Patch0:         txt2man-1.5.5-fixbashisms.patch

# Fixes same bug as above, but code was changed in new release so old patch
# no longer worked.
Patch1:         txt2man-1.5.6-fixbashisms.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       gawk

%description
tx2man is a shell script using gnu awk, that should run on any
Unix-like system. The syntax of the ASCII text is very straightforward
and looks very much like the output of the man(1) program. 

%prep
%setup -q
#%patch0 -p1
%patch1

%build
#no build needed

%install
rm -rf $RPM_BUILD_ROOT
#manual install
install -p -m 0755 -D bookman $RPM_BUILD_ROOT%{_bindir}/bookman
install -p -m 0755 -D src2man $RPM_BUILD_ROOT%{_bindir}/src2man
install -p -m 0755 -D txt2man $RPM_BUILD_ROOT%{_bindir}/txt2man

install -p -m 0644 -D bookman.1 $RPM_BUILD_ROOT%{_mandir}/man1/bookman.1
install -p -m 0644 -D src2man.1 $RPM_BUILD_ROOT%{_mandir}/man1/src2man.1
install -p -m 0644 -D txt2man.1 $RPM_BUILD_ROOT%{_mandir}/man1/txt2man.1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING Changelog README
%{_bindir}/*
%{_mandir}/man?/*


%changelog
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon May 09 2011 Adam Miller <maxamillion@fedoraproject.org> - 1.5.6-1
- New upstream release, fixes old bugs.
- Upstream release notes claim POSIX shell code, but bookman still relies on
  bash styled syntax so we continue to patch it out.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 04 2009 Sindre Pedersen Bjordal <sindrepb@fedoraproject.org> - 1.5.5-1
- Initial build
- Include debian patch to fix bashisms
