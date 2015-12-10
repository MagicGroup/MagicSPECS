%global gem_name rspec-longrun

# For compatibility with RHEL <= 6
%{!?ruby_vendorlibdir:	%global ruby_vendorlibdir	%(ruby -rrbconfig -e "puts RbConfig::CONFIG['sitelibdir']")}
%{!?ruby_vendorarchdir:	%global ruby_vendorarchdir	%(ruby -rrbconfig -e "puts RbConfig::CONFIG['sitearchdir']")}
%{!?gem_dir:		%global gem_dir			%(ruby -rubygems -e "puts Gem::dir" 2>/dev/null)}
%{!?gem_instdir:	%global gem_instdir		%{gem_dir}/gems/%{gem_name}-%{version}}
%{!?gem_libdir:		%global gem_libdir		%{gem_instdir}/lib}
%{!?gem_cache:		%global gem_cache		%{gem_dir}/cache/%{gem_name}-%{version}.gem}
%{!?gem_spec:		%global gem_spec		%{gem_dir}/specifications/%{gem_name}-%{version}.gemspec}
%{!?gem_docdir:		%global gem_docdir		%{gem_dir}/doc/%{gem_name}-%{version}}
%{!?gem_extdir_mri:	%global gem_extdir_mri		%{ruby_vendorarchdir}}

Name:		rubygem-%{gem_name}
Version:	0.1.2
Release:	7%{?dist}
Summary:	RSpec formatter for long-running specs
%{?el5:Group:	System Environment/Libraries}

License:	MIT
URL:		http://github.com/mdub/%{gem_name}
Source0:	https://rubygems.org/downloads/%{gem_name}-%{version}.gem

BuildArch:	noarch
%{?el5:BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)}

BuildRequires:	ruby-devel
BuildRequires:	rubygem(rspec)			>= 2.10.0

%if 0%{?fedora} >=19 || 0%{?rhel} >= 7
BuildRequires:	rubygem(rdoc)
BuildRequires:	rubygems-devel

Requires:	ruby(release)
%else
BuildRequires:	rubygems%{!?el5:-devel}

%{?rhel:Requires:	ruby(abi)		=  1.8}
%{!?rhel:Requires:	ruby(abi)		=  1.9.1}
%endif

Requires:	rubygem(rspec)			>= 2.10.0
Requires:	rubygems

Provides:	rubygem(%{gem_name})		=  %{version}

%description
RSpec is a fine unit-testing framework, but is also handy for acceptance
and integration tests.  But the default report formatters make it difficult
to track progress of such long-running tests.

The RSpec::Longrun::Formatter outputs the name of each test as it starts,
rather than waiting until it passes or fails.  It also provides a mechanism
for reporting on progress of a test while it is still executing.


%package doc
Summary:	Documentation files for %{name}
Requires:	%{name}				=  %{version}-%{release}

%description doc
This package contains the documentation files
for %{name}.


%prep
%setup -qcT
%if 0%{?fedora} || 0%{?rhel} >= 6
%gem_install -n %{SOURCE0}
%else
export CONFIGURE_ARGS="--with-cflags='%{optflags}'"
mkdir -p .%{gem_dir}
gem install								\
	-V --local --install-dir .%{gem_dir} --bindir .%{_bindir}	\
	--force --backtrace %{SOURCE0}
%endif


%build
# noop


%install
%{?el5:rm -rf %{buildroot}}
mkdir -p %{buildroot}%{gem_dir}

# Remove hashbang from Rakefile
_file=".%{gem_instdir}/Rakefile" &&					\
sed -i.orig -e '1{/^#!.*/d}' ${_file} &&				\
touch -r ${_file}.orig ${_file} &&					\
rm -f ${_file}.orig

# Clean-up
find .%{gem_dir} -depth -type f -name '.*' -print0 | xargs -0 rm -rf
find .%{gem_dir} -depth -size 0 -type f -print0 | xargs -0 rm -rf
rm -rf .%{gem_cache} .%{gem_instdir}/%{gem_name}.gemspec

# Install the gem to final location
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}


%check
pushd .%{gem_instdir}
rspec spec
popd


%{?el5:%clean}
%{?el5:rm -rf %{buildroot}}


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md
%{gem_libdir}
%{gem_spec}

%files doc
%doc %{gem_instdir}/examples
%doc %{gem_docdir}
%{gem_instdir}/spec
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.1.2-7
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.1.2-6
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.1.2-5
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Dec 12 2013 Björn Esser <bjoern.esser@gmail.com> - 0.1.2-3
- improvements as recommended in review by Vít Ondruch (vondruch)
  from comments #7 and #8 (#1040453)

* Wed Dec 11 2013 Björn Esser <bjoern.esser@gmail.com> - 0.1.2-2
- improvements as recommended in review by Vít Ondruch (vondruch)
  from comments #2 and #3 (#1040453)

* Sun Dec 08 2013 Björn Esser <bjoern.esser@gmail.com> - 0.1.2-1
- Initial rpm release (#1040453)
