Name:           urlview
Version:        0.9
Release:        14%{?dist}
Summary:        URL extractor/launcher

Group:          Applications/Internet
License:        GPLv2+
URL:            ftp://ftp.mutt.org/pub/mutt/contrib/urlview-0.9.README
Source0:        ftp://ftp.mutt.org/pub/mutt/contrib/urlview-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ncurses-devel

# mutt packages before 5:1.5.16-2 included urlview
Conflicts:      mutt < 5:1.5.16-2

Patch1: urlview-0.9-build.diff
Patch2: urlview-0.9-default.patch

%description
urlview is a screen oriented program for extracting URLs from text
files and displaying a menu from which you may launch a command to
view a specific item.

%prep
%setup -q
%patch1 -p1 -b .build
%patch2 -p1 -b .default

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_sysconfdir},%{_bindir},%{_mandir}/man{1,5}}
install -p -m644 urlview.conf.suse $RPM_BUILD_ROOT%{_sysconfdir}/urlview.conf
install -p urlview url_handler.sh $RPM_BUILD_ROOT%{_bindir}
install -p -m644 urlview.man $RPM_BUILD_ROOT%{_mandir}/man1/urlview.1
echo '.so man1/urlview.1' > $RPM_BUILD_ROOT%{_mandir}/man5/urlview.conf.5

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README sample.urlview
%config(noreplace) %{_sysconfdir}/urlview.conf
%{_bindir}/urlview
%{_bindir}/url_handler.sh
%{_mandir}/man1/urlview.1*
%{_mandir}/man5/urlview.conf.5*

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 0.9-14
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 0.9-13
- 为 Magic 3.0 重建

* Sat Sep 19 2015 Liu Di <liudidi@gmail.com> - 0.9-12
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.9-11
- 为 Magic 3.0 重建

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 29 2009 Miroslav Lichvar <mlichvar@redhat.com> 0.9-7
- add man page link for urlview.conf (#526162)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9-4
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Miroslav Lichvar <mlichvar@redhat.com> 0.9-3
- update license tag

* Fri Jun 29 2007 Miroslav Lichvar <mlichvar@redhat.com> 0.9-2
- add conflict with mutt, fix URL (#245951)

* Wed Jun 27 2007 Miroslav Lichvar <mlichvar@redhat.com> 0.9-1
- split from mutt package
