%global git_date 20150305
%global git_commit_hash 2eeb03b
%global aname crypto-policies

Name:           crypto-policies
Version:        %{git_date}
Release:        3.git%{git_commit_hash}%{?dist}
Summary:        Crypto policies package for Fedora

License:        LGPLv2+
URL:            https://github.com/nmav/fedora-crypto-policies

# This is a tarball of the git repository without the .git/
# directory.
Source0:        crypto-policies-git%{git_commit_hash}.tar.gz
Source1:	config

BuildArch: noarch
BuildRequires: asciidoc
BuildRequires: libxslt
BuildRequires: openssl
BuildRequires: gnutls-utils

# for shell script
Requires(post): coreutils

%description
This package provides update-crypto-policies, which is a tool that sets
the policy applicable for the various cryptographic back-ends, such as
SSL/TLS libraries. The policy set by the tool will be the default policy
used by these back-ends unless the application user configures them otherwise.
https://fedoraproject.org/wiki/Changes/CryptoPolicy


%prep
%setup -q -n %{aname}

%build
make %{?_smp_mflags} update-crypto-policies.8

%install
mkdir -p -m 755 %{buildroot}%{_datadir}/crypto-policies/profiles
mkdir -p -m 755 %{buildroot}%{_sysconfdir}/crypto-policies/
mkdir -p -m 755 %{buildroot}%{_mandir}/man8
mkdir -p -m 755 %{buildroot}%{_bindir}
install -p -m 644 update-crypto-policies.8 %{buildroot}%{_mandir}/man8
install -p -m 755 update-crypto-policies %{buildroot}%{_bindir}/update-crypto-policies
install -p -m 644 profiles/* %{buildroot}%{_datadir}/crypto-policies/profiles
install -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/crypto-policies/config

%check
make check %{?_smp_mflags}

%post
%{_bindir}/update-crypto-policies --no-check


%files
%defattr(-,root,root,-)

%dir %{_sysconfdir}/crypto-policies/

%config(noreplace) %{_sysconfdir}/crypto-policies/config

%dir %{_datadir}/crypto-policies/
%{_bindir}/update-crypto-policies
%{_mandir}/man8/update-crypto-policies.8.gz
%{_datadir}/crypto-policies/profiles/

%{!?_licensedir:%global license %%doc}
%license COPYING.LESSER

%changelog
* Fri Mar  6 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150305-3-git2eeb03b
- Added make check

* Fri Mar  6 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150305-2-git44afaa1
- Removed support for SECLEVEL (#1199274)

* Thu Mar  5 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150305-1-git098a8a6
- Include AEAD ciphersuites in gnutls (#1198979)

* Sun Jan 25 2015 Peter Robinson <pbrobinson@fedoraproject.org> 20150115-3-git9ef7493
- Bump release so lastest git snapshot is newer NVR

* Thu Jan 15 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150115-2-git9ef7493
- Updated to newest upstream version.
- Includes bind policies (#1179925)

* Tue Dec 16 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20141124-2-gitd4aa178
- Corrected typo in gnutls' future policy (#1173886)

* Mon Nov 24 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20141124-1-gitd4aa178
- re-enable SSL 3.0 (until its removal is coordinated with a Fedora change request)

* Thu Nov 20 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20141120-1-git9a26a5b
- disable SSL 3.0 (doesn't work in openssl)

* Fri Sep 05 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140905-1-git4649b7d
- enforce the acceptable TLS versions in openssl

* Wed Aug 27 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140827-1-git4e06f1d
- fix issue with RC4 being disabled in DEFAULT settings for openssl

* Thu Aug 14 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140814-1-git80e1e98
- fix issue in post script run on upgrade (#1130074)

* Tue Aug 12 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140812-1-gitb914bfd
- updated crypto-policies from repository

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> - 20140708-2-git3a7ae3f
- fix license handling

* Tue Jul 08 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140708-1-git3a7ae3f
- updated crypto-policies from repository

* Fri Jun 20 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140620-1-gitdac1524
- updated crypto-policies from repository
- changed versioning

* Thu Jun 12 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-7-20140612gita2fa0c6
- updated crypto-policies from repository

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-7.20140522gita50bad2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-6-20140522gita50bad2
- Require(post) coreutils (#1100335).

* Tue May 27 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-5-20140522gita50bad2
- Require coreutils.

* Thu May 22 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-4-20140522gita50bad2
- Install the default configuration file.

* Wed May 21 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-3-20140520git81364e4
- Run update-crypto-policies after installation.

* Tue May 20 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-2-20140520git81364e4
- Updated spec based on comments by Petr Lautrbach.

* Mon May 19 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-1-20140519gitf15621a
- Initial package build

