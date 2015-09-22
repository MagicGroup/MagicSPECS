# ghc has been bootstrapped on all Fedora archs except aarch64.
# The ghc interpreter ghci is only supported on a subset of archs.

%global macros_dir %{_rpmconfigdir}/macros.d

Name:           ghc-srpm-macros
Version:        1.4.2
Release:        4%{?dist}
Summary:        RPM macros for building Haskell source packages

License:        GPLv2+
Url:            http://pkgs.fedoraproject.org/cgit/ghc-srpm-macros.git
BuildArch:      noarch

Source0:        macros.ghc-srpm

%description
Macros used when generating Haskell source RPM packages.


%prep
%{nil}


%build
echo no build stage needed


%install
install -p -D -m 0644 %{SOURCE0} %{buildroot}/%{macros_dir}/macros.ghc-srpm


%files
%{macros_dir}/macros.ghc-srpm


%changelog
* Tue Sep 22 2015 Liu Di <liudidi@gmail.com> - 1.4.2-4
- 为 Magic 3.0 重建

* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.4.2-3
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 27 2015 Jens Petersen <petersen@redhat.com> - 1.4.2-1
- reenable ghci on aarch64 (#1203951)

* Thu Mar 19 2015 Jens Petersen <petersen@fedoraproject.org> - 1.4.1-1
- disable ghci on aarch64 due to dynlinked runtime problems (see #1195231)

* Tue Feb 17 2015 Jens Petersen <petersen@redhat.com> - 1.4-1
- ghc-7.8 shared libraries allow ghci to work on all arch's

* Fri Jun 27 2014 Jens Petersen <petersen@redhat.com> - 1.3-2
- add pkg git as URL (#1093541)
- downgrade license tag to GPLv2+ in line with rpm (redhat-rpm-config is GPL+)
- sync with current ghc-rpm-macros: add ghc_arches for backwards compatibility

* Fri May  2 2014 Jens Petersen <petersen@redhat.com> - 1.3-1
- separate from ghc-rpm-macros
