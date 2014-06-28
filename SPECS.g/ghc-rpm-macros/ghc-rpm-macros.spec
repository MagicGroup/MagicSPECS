%global debug_package %{nil}

%global macros_dir %{_rpmconfigdir}/macros.d

# uncomment to bootstrap without hscolour
#%%global without_hscolour 1

Name:           ghc-rpm-macros
Version:        1.2.13
Release:        3%{?dist}
Summary:        RPM macros for building packages for GHC

License:        GPLv3+
URL:            https://fedoraproject.org/wiki/Packaging:Haskell

# This is a Fedora maintained package, originally made for
# the distribution.  Hence the source is currently only available
# from this package.  But it could be hosted on fedorahosted.org
# for example if other rpm distros would prefer that.
Source0:        macros.ghc
Source1:        COPYING
Source2:        AUTHORS
Source3:        ghc-deps.sh
Source4:        cabal-tweak-dep-ver
Source5:        cabal-tweak-flag
Source6:        macros.ghc-extra
Source7:        macros.ghc-srpm
Requires:       ghc-srpm-macros = %{version}-%{release}
# macros.ghc-srpm moved out from magic-rpm-config
Requires:       magic-rpm-config >= 3.0
%if %{undefined without_hscolour}
%ifarch %{ix86} %{ix86} x86_64 ppc ppc64 alpha sparcv9 armv7hl armv5tel s390 s390x ppc64le aarch64
Requires:       hscolour
%endif
%endif
# for execstack (hack not needed for ghc-7.8)
%ifnarch ppc64le aarch64
Requires:       prelink
%endif

%description
A set of macros for building GHC packages following the Haskell Guidelines
of the Fedora Haskell SIG.  ghc needs to be installed in order to make use of
these macros.


%package extra
Summary:        Extra RPM macros for building Haskell library subpackages
Requires:       %{name} = %{version}-%{release}

%description extra
Extra macros used for subpackaging of Haskell libraries,
for example in ghc and haskell-platform.


%package -n ghc-srpm-macros
Summary:        RPM macros for building Haskell source packages
BuildArch:      noarch


%description -n ghc-srpm-macros
Macros used when generating source Haskell rpm packages.


%prep
%setup -c -T
cp %{SOURCE1} %{SOURCE2} .


%build
echo no build stage needed


%install
install -p -D -m 0644 %{SOURCE0} %{buildroot}/%{macros_dir}/macros.ghc
install -p -D -m 0644 %{SOURCE6} %{buildroot}/%{macros_dir}/macros.ghc-extra
install -p -D -m 0644 %{SOURCE7} %{buildroot}/%{macros_dir}/macros.ghc-srpm

install -p -D -m 0755 %{SOURCE3} %{buildroot}/%{_prefix}/lib/rpm/ghc-deps.sh

install -p -D -m 0755 %{SOURCE4} %{buildroot}/%{_bindir}/cabal-tweak-dep-ver
install -p -D -m 0755 %{SOURCE5} %{buildroot}/%{_bindir}/cabal-tweak-flag

# this is why this package is now arch-dependent:
# turn off shared libs and dynamic linking on secondary archs
%ifnarch %{ix86} x86_64
cat >> %{buildroot}/%{macros_dir}/macros.ghc <<EOF

# shared libraries are only supported on primary intel archs
%%ghc_without_dynamic 1
%%ghc_without_shared 1
EOF
%endif


%files
%doc COPYING AUTHORS
%{macros_dir}/macros.ghc
%{_prefix}/lib/rpm/ghc-deps.sh
%{_bindir}/cabal-tweak-dep-ver
%{_bindir}/cabal-tweak-flag


%files extra
%{macros_dir}/macros.ghc-extra


%files -n ghc-srpm-macros
%{macros_dir}/macros.ghc-srpm


%changelog
* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 1.2.13-3
- 为 Magic 3.0 重建

* Wed Jun 18 2014 Liu Di <liudidi@gmail.com> - 1.2.13-2
- 为 Magic 3.0 重建


