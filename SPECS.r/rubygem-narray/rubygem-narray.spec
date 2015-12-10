# For compatibility with RHEL <= 6
%{!?ruby_vendorlibdir:	%global ruby_vendorlibdir	%(ruby -rrbconfig -W0 -e "puts Config::CONFIG['sitelibdir']")}
%{!?ruby_vendorarchdir:	%global ruby_vendorarchdir	%(ruby -rrbconfig -W0 -e "puts Config::CONFIG['sitearchdir']")}
%{!?gem_dir:		%global gem_dir			%(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)}
%{!?gem_instdir:	%global gem_instdir		%{gem_dir}/gems/%{gem_name}-%{version}}
%{!?gem_libdir:		%global gem_libdir		%{gem_instdir}/lib}
%{!?gem_cache:		%global gem_cache		%{gem_dir}/cache/%{gem_name}-%{version}.gem}
%{!?gem_spec:		%global gem_spec		%{gem_dir}/specifications/%{gem_name}-%{version}.gemspec}
%{!?gem_docdir:		%global gem_docdir		%{gem_dir}/doc/%{gem_name}-%{version}}
%{!?gem_extdir_mri:	%global gem_extdir_mri		%{ruby_vendorarchdir}}

%global gem_name narray

Name:			rubygem-%{gem_name}
Version:		0.6.1.1
Release:		5%{?dist}
Summary:		N-dimensional Numerical Array class for Ruby
%{?el5:Group:		System Environment/Libraries}

License:		BSD and Ruby
URL:			http://%{gem_name}.rubyforge.org
Source0:		http://rubygems.org/downloads/%{gem_name}-%{version}.gem

%{?el5:BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)}
BuildRequires:		ruby-devel
BuildRequires:		rubygems%{!?el5:-devel}

%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
Requires:		ruby(release)
%else #0%{?fedora} >= 19 || 0%{?rhel} >= 7
%{?rhel:Requires:	ruby(abi)			== 1.8}
%{!?rhel:Requires:	ruby(abi)			== 1.9.1}
%endif #0%{?fedora} >= 19 || 0%{?rhel} >= 7
Requires:		rubygems

%if 0%{?fedora} && 0%{?fedora} <= 22
Obsoletes:		%{name}-common			<  %{version}-%{release}
%endif #0%{?fedora} && 0%{?fedora} <= 22

Provides:		rubygem(%{gem_name})		== %{version}
Provides:		rubygem(%{gem_name})%{?_isa}	== %{version}

%description
NArray is a Numerical N-dimensional Array class.  Supported element types are
1/2/4-byte Integer, single/double-precision, Real/Complex and Ruby Object.
This extension library incorporates fast calculation and easy manipulation of
large numerical arrays into the Ruby language.  NArray has features similar to
NumPy, but NArray has vector and matrix sub-classes.


%package devel
Summary:		Development files and developer's docs for %{name}
%{?el5:Group:		Development/Libraries}

%if (0%{?fedora} && 0%{?fedora} <= 20) || 0%{?rhel} == 7
BuildArch:		noarch
Requires:		%{name}				== %{version}-%{release}
%else #(0%{?fedora} && 0%{?fedora} <= 20) || 0%{?rhel} == 7
Requires:		%{name}%{?_isa}			== %{version}-%{release}
%endif #(0%{?fedora} && 0%{?fedora} <= 20) || 0%{?rhel} == 7

%if 0%{?fedora} && 0%{?fedora} <= 22
Obsoletes:		%{name}-devel			<  %{version}-%{release}
Obsoletes:		%{name}-common-devel		<  %{version}-%{release}
Obsoletes:		%{name}-doc			<  %{version}-%{release}
%endif #0%{?fedora} && 0%{?fedora} <= 22

%description devel
This package contains the development files and the developer's documentation
for %{name}.


%prep
%setup -qcT
%if 0%{?fedora} || 0%{?rhel} >= 6
%gem_install -n %{SOURCE0}
%else #0%{?fedora} || 0%{?rhel} >= 6
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
mkdir -p .%{gem_dir}
gem install									\
	-V --local --install-dir .%{gem_dir} --bindir .%{_bindir}		\
	--force --backtrace %{SOURCE0}
%endif #0%{?fedora} || 0%{?rhel} >= 6


%build
# noop


%install
%{?el5:rm -rf %{buildroot}}
mkdir -p %{buildroot}%{_prefix}

# Install the gem to final location
cp -a ./%{_prefix}/* %{buildroot}%{_prefix}
%if (0%{?fedora} && 0%{?fedora} <= 20) || (0%{?rhel} && 0%{?rhel} <= 7)
mkdir -p %{buildroot}%{gem_extdir_mri}
mv -f %{buildroot}%{gem_instdir}/%{gem_name}.so					\
	%{buildroot}%{gem_extdir_mri}
%endif #(0%{?fedora} && 0%{?fedora} <= 20) || (0%{?rhel} && 0%{?rhel} <= 7)

# Clean-up
pushd %{buildroot}
find .%{gem_instdir} -depth -type f -name '*.so' -print0 | xargs -0 rm -rf
find . -depth -type f -name '.*' -print0 | xargs -0 rm -rf
find . -depth -type f -name '*.log' -print0 | xargs -0 rm -rf
find . -depth -type f -name '*.o' -print0 | xargs -0 rm -rf
find . -depth -type f -name '*.out' -print0 | xargs -0 rm -rf
find . -depth -size 0 -type f -print0 | xargs -0 rm -rf
rm -rf .%{gem_cache} .%{gem_instdir}/src .%{gem_instdir}/%{gem_name}.gemspec
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 8
touch %{buildroot}%{gem_extdir_mri}/gem.build_complete
%endif #0%{?fedora} >= 21 || 0%{?rhel} >= 8
popd

# On <= el6 there needs to be a symlink for %%{gem_name}_ext.rb
# in %%{ruby_vendorarchdir}.  Otherwise the so-plugin can't be loaded.
%if 0%{?rhel} && 0%{?rhel} <= 6
ln -fs	%{gem_instdir}/%{gem_name}_ext.rb %{buildroot}%{gem_extdir_mri}
%endif #0%{?rhel} && 0%{?rhel} <= 6


%clean
%{?el5:rm -rf %{buildroot}}


%files
%doc %{gem_instdir}/ChangeLog
%doc %{gem_instdir}/README.*
%dir %{gem_instdir}
%exclude %{gem_instdir}/MANIFEST
%exclude %{gem_instdir}/SPEC.*
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 8
%exclude %{gem_extdir_mri}/*.h
%else #0%{?fedora} >= 21 || 0%{?rhel} >= 8
%exclude %{gem_instdir}/*.h
%{gem_instdir}/*.rb
%endif #0%{?fedora} >= 21 || 0%{?rhel} >= 8
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%{gem_extdir_mri}
%else #0%{?fedora} >= 19 || 0%{?rhel} >= 7
%{gem_extdir_mri}/%{gem_name}*
%endif #0%{?fedora} >= 19 || 0%{?rhel} >= 7
%{gem_spec}

%files devel
%doc %{gem_docdir}
%doc %{gem_instdir}/MANIFEST
%doc %{gem_instdir}/SPEC.*
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 8
%{gem_extdir_mri}/*.h
%else #0%{?fedora} >= 21 || 0%{?rhel} >= 8
%{gem_instdir}/*.h
%endif #0%{?fedora} >= 21 || 0%{?rhel} >= 8

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.6.1.1-5
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.6.1.1-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.6.1.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Feb 01 2015 Björn Esser <bjoern.esser@gmail.com> - 0.6.1.1-1
- new upstream release (#1178432)

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 0.6.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Björn Esser <bjoern.esser@gmail.com> - 0.6.0.9-1
- new upstream release (#1103230)

* Mon May 26 2014 Björn Esser <bjoern.esser@gmail.com> - 0.6.0.8-14
- preserve `%%{gem_extdir_mri}/gem.build_complete` on Fedora >= 21
- no need to modify gemspec

* Sat May 17 2014 Björn Esser <bjoern.esser@gmail.com> - 0.6.0.8-13
- fix gemspec on Fedora >= 21
- remove `%%{gem_extdir_mri}/gem_make.out` again

* Sat May 17 2014 Björn Esser <bjoern.esser@gmail.com> - 0.6.0.8-12
- one must NOT delete `%%{gem_extdir_mri}/gem_make.out`

* Thu May 01 2014 Björn Esser <bjoern.esser@gmail.com> - 0.6.0.8-11
- rebuilt for libruby.so.2.0() so-name bump

* Sun Dec 22 2013 Björn Esser <bjoern.esser@gmail.com> - 0.6.0.8-10
- package must not obsolete itself
- improved indention

* Fri Dec 13 2013 Björn Esser <bjoern.esser@gmail.com> - 0.6.0.8-9
- fixed the way ruby(abi) is required
- dropped the symlinks in %%{ruby_vendorarchdir}, except for <= el6
- fixed directory ownerships on <= el6
- use BuildRequires: rubygems-devel on el6, too

* Tue Dec 10 2013 Björn Esser <bjoern.esser@gmail.com> - 0.6.0.8-8
- fixed symlinks in %%{ruby_vendorarchdir}

* Tue Dec 10 2013 Björn Esser <bjoern.esser@gmail.com> - 0.6.0.8-7
- adapted Requires: ruby(abi) = 1.9.1 for Fedora 18, only

* Tue Dec 10 2013 Björn Esser <bjoern.esser@gmail.com> - 0.6.0.8-6
- several improvements for RHEL <= 6 and added needed bits for RHEL <= 5
- added needed Provides

* Mon Nov 25 2013 Björn Esser <bjoern.esser@gmail.com> - 0.6.0.8-5
- Fedora <= 18 && RHEL <= 6 need Requires: ruby(abi)

* Mon Nov 25 2013 Björn Esser <bjoern.esser@gmail.com> - 0.6.0.8-4
- added conditional for Requires: ruby(release) or ruby(abi) on older dists

* Mon Oct 28 2013 Björn Esser <bjoern.esser@gmail.com> - 0.6.0.8-3
- added symlink to %%{gem_name}_ext.rb in %%{ruby_vendorarchdir}

* Sun Sep 15 2013 Björn Esser <bjoern.esser@gmail.com> - 0.6.0.8-2
- obsoleted common, common-devel and doc pkg
- moved some development-related files from main to devel pkg
- removed some unneeded files, e.g. the copy of sources inside %%{gem_instdir}

* Sat Sep 07 2013 Björn Esser <bjoern.esser@gmail.com> - 0.6.0.8-1
- Initial rpm release (#1005463)
