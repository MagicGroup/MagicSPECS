Name:           vbetool
Version:        1.2.2
Release:        3%{?dist}
Summary:        Run real-mode video BIOS code to alter hardware state

Group:          System Environment/Base
License:        GPLv2
URL:            http://www.codon.org.uk/~mjg59/vbetool/
Source0:        http://www.codon.org.uk/~mjg59/vbetool/download/vbetool-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: libpciaccess > 0.10.6-4 libx86
BuildRequires:  zlib-devel libx86-devel
BuildRequires:  libpciaccess-devel >= 0.10.6-4 libx86-devel
BuildRequires: autoconf automake libtool pkgconfig
# does not build on ppc, ppc64 and sparc arches, see #285361 (RedHat Bugzilla)
# on ppc sys/io.h is missing, on ppc64 there are more complaints
# build.logs are attached in the bug report
ExcludeArch:    ppc ppc64 %{sparc} s390 s390x mips64el
# vbetool is included in (some of) these pm-utils releases
Conflicts:      pm-utils <= 0.99.3-11

%description
vbetool uses lrmi in order to run code from the video BIOS. Currently, it is
able to alter DPMS states, save/restore video card state and attempt to
initialize the video card from scratch.


%prep
%setup -q

%build
autoreconf -v --install
%configure --with-x86emu
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -m 0644 -D udev-video-post-example.rules $RPM_BUILD_ROOT/etc/udev/rules.d/92-video-post.rules

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING
%{_sbindir}/vbetool
%{_mandir}/man1/vbetool.1.gz
%{_sysconfdir}/udev/rules.d/92-video-post.rules

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.2.2-3
- 为 Magic 3.0 重建

* Tue Feb 21 2012 Liu Di <liudidi@gmail.com> - 1.2.2-2
- 为 Magic 3.0 重建

* Fri Oct 02 2009 Dave Airlie <airlied@redhat.com> 1.2.2-1
- update to 1.2.2 - fixes infinte loops on s/r (#516694)

* Wed Aug 05 2009 Dave Airlie <airlied@redhat.com> 1.2.1-1
- rebase to 1.2.1 and install the udev rules

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 1.2.0-1
- rebase to vbetool 1.2.0

* Fri Jul 31 2009 Dave Airlie <airlied@redhat.com> 1.1-5.1
- pciacccess.patch: post to use libpciaccess
- vgaarbpost.patch: use vga arb to post secondaries

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 07 2009 Karsten Hopp <karsten@redhat.com> 1.1-3.1
- ExcludeArch s390, s390x

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 14 2009 Dennis Gilmore <dennis@ausil.us> - 1.1-2
- exclude sparc arches missing sys/io.h

* Mon May 19 2008 Matthew Garrett <mjg@redhat.com> - 1.1-1
- update to version 1.1

* Tue Mar 25 2008 Till Maas <opensource till name> - 0.7-6
- remove overriding of CFLAGS for x86emu

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.7-5
- Autorebuild for GCC 4.3

* Sun Dec 02 2007 Till Maas <opensource till name> - 0.7-4
- libz.a is now in a -static subpackage, add to BR

* Tue Nov 13 2007 Adam Jackson <ajax@redhat.com> 0.7-3
- Build with x86emu everywhere for uniformity of bugs and consistency with X.

* Fri Sep 07 2007 Till Maas <opensource till name> 0.7-2
- ExcludeArch: ppc and ppc64 (does not build there)
- add Conflicts with old pm-utils package

* Fri Aug 31 2007 Till Maas <opensource till name> - 0.7-1
- initial release for Fedora with patches from the pm-utils package
