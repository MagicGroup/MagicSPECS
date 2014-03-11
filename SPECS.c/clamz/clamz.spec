Name:           clamz
Version:        0.5
Release:        3%{?dist}
Summary:        Amazon Downloader
Group:          Applications/Internet
License:        GPLv3+
URL:            http://clamz.googlecode.com/
Source0:        http://clamz.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libcurl-devel, libgcrypt-devel, expat-devel
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description
Clamz is a little command-line program to download MP3 files from
Amazon.com's music store.  It is intended to serve as a substitute
for Amazon's official MP3 Downloader, which is not free software (and
therefore is only available in binary form for a limited set of
platforms.)  Clamz can be used to download either individual songs or
complete albums that you have purchased from Amazon.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} UPDATE_MIME_DATABASE=: UPDATE_DESKTOP_DATABASE=:

%post
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :

%postun
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README COPYING
%{_bindir}/%{name}
%{_mandir}/*/%{name}*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml

%changelog
* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 30 2011 Jim Radford <radford@blackbean.org> - 0.5-0
- Upgrade to 0.5 for support for the Amazon Cloud Player

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat May 22 2010 Jim Radford <radford@blackbean.org> - 0.4-3
- Remove obsolete build dependency on desktop-file-install
- Re-remove dependency on shared-mime-info as per
  https://fedoraproject.org/wiki/Packaging/ScriptletSnippets#mimeinfo

* Fri May 21 2010 Jim Radford <radford@blackbean.org> - 0.4-2
- Require shared-mime-info for update-mime-database and packages dir

* Tue May 18 2010 Jim Radford <radford@blackbean.org> - 0.4-1
- Upgrade to 0.4 (4 patches, desktop and mime-info file included upstream)

* Wed Sep 16 2009 Jim Radford <radford@blackbean.org> - 0.2-10
- Fixed desktop dependencies again (#473184)

* Fri Jul 17 2009 Jim Radford <radford@blackbean.org> - 0.2-9
- Add --sane-defaults for use by the .desktop file to default downloads into
      ~/Music/<artist>/<album>/<track> - <title>.<suffix>
  while still allowing previous config file and command line usage.

* Sat Apr 18 2009 Jim Radford <radford@blackbean.org> - 0.2-8
- fedora guidelines now explicitly allow including desktop files
  inline in the spec, so put them back.

* Sat Apr 18 2009 Jim Radford <radford@blackbean.org> - 0.2-7
- Fixed desktop dependencies (#473184).

* Wed Nov 26 2008 Jim Radford <radford@blackbean.org> 0.2-6
- Initial package (#473184).
