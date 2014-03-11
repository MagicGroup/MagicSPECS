# We need to regenerate the HMAC values after the buildroot policies have
# mucked around with binaries.  This overrides the default which was in place
# at least from Red Hat Linux 9 through Fedora 11's development cycle.
%define __spec_install_post \
	%{?__debug_package:%{__debug_install_post}} \
	%{__arch_install_post} \
	%{__os_install_post} \
	for length in 1 256 384 512 ; do \
		$RPM_BUILD_ROOT/%{_bindir}/sha${length}hmac -S > \\\
		$RPM_BUILD_ROOT/%{_libdir}/%{name}/sha${length}hmac.hmac \
	done \
	%{nil}

Name:		hmaccalc
Version:	0.9.12
Release:	5%{?dist}
Summary:	Tools for computing and checking HMAC values for files

Group:		System Environment/Base
License:	MIT
URL:		https://fedorahosted.org/hmaccalc/
Source0:	https://fedorahosted.org/released/hmaccalc/hmaccalc-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	nss-devel, prelink

%description
The hmaccalc package contains tools which can calculate HMAC (hash-based
message authentication code) values for files.  The names and interfaces are
meant to mimic the sha*sum tools provided by the coreutils package.

%prep
%setup -q

%build
%ifarch mips64el
export CFLAGS="$RPM_OPT_FLAGS -DNON_FIPS=1"
%endif
%configure --enable-sum-directory=%{_libdir}/%{name}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%check
make check

%files
%defattr(-,root,root,-)
%doc README LICENSE
%{_bindir}/sha1hmac
%{_bindir}/sha256hmac
%{_bindir}/sha384hmac
%{_bindir}/sha512hmac
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/sha1hmac.hmac
%{_libdir}/%{name}/sha256hmac.hmac
%{_libdir}/%{name}/sha384hmac.hmac
%{_libdir}/%{name}/sha512hmac.hmac
%{_mandir}/*/*

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.9.12-5
- 为 Magic 3.0 重建

* Thu Jul 26 2012 Liu Di <liudidi@gmail.com> - 0.9.12-4
- 为 Magic 3.0 重建

* Mon Dec 12 2011 Liu Di <liudidi@gmail.com> - 0.9.12-3
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 15 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9.12-1
- fix regression of #512275 -- we looked for prelink, but didn't record
  its location properly (#559458)

* Tue Sep  8 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9.11-1
- error out when we previously skipped a check entry because the value to be
  checked is the wrong size
- fix estimation of the expected length for truncated values

* Thu Sep  3 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9.10-1
- refuse to truncate output below half the size of the hash length, or 80
  bits, whichever is higher, in case we get used in a situation where
  not doing so would make us vulnerable to CVE-2009-0217, in which an
  attacker manages to convince a party doing verification to truncate
  both the just-computed value and the value to be checked before
  comparing them, as comparing just 1 bit would make detecting forgeries
  close to impossible

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 11 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9.9-1
- look for prelink at compile-time, and if we find it try to invoke it
  using a full pathname before trying with $PATH (#512275)
- buildrequires: prelink so that it will be found at compile-time

* Tue Jun  9 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9.8-1
- when checking, skip input lines which don't look like valid input lines

* Tue Jun  9 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9.7-1
- add a binary (-b) mode when summing

* Wed Apr  8 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9.6-1
- fix 'make check' by using binaries built with a different path for their
  own check files
- add a non-fips compile-time option, which we don't use

* Mon Mar 30 2009 Nalin Dahyabhai <nalin@redhat.com>
- handle '-' as indicating that stdin should be used for the input file

* Fri Mar 27 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9.5-1
- add a -t option, for truncating HMAC outputs

* Wed Mar 25 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9.4-1
- use a longer default key, when we use the default key

* Tue Mar 24 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9.3-1
- fix the -k option
- move self-check files to %%{_libdir}/%{name}

* Tue Mar 24 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9.2-1
- provide a way to override the directory which will be searched for self-check
  values (part of #491719)

* Tue Mar 24 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9.1-1
- store self-check values in hex rather than in binary form (part of #491719)

* Tue Mar 24 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9-2
- add URL to fedorahosted home page, and mention it in the man page as a means
  to report bugs and whatnot (part of #491719)
- correct the license tag: "X11" -> "MIT" (part of #491719)
- expand the acronym HMAC in the description (part of #491719)
- disable the sumfile prefix (part of #491719)

* Fri Mar 20 2009 Nalin Dahyabhai <nalin@redhat.com>
- initial .spec file
