%global gem_name ruby-rc4
%if 0%{?rhel} == 6
%global gem_dir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{version}
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{version}.gem
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}
%endif

Summary: Pure Ruby implementation of the RC4 algorithm
Name: rubygem-%{gem_name}
Version: 0.1.5
Release: 10%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/caiges/Ruby-RC4
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: rubygems
%if 0%{?rhel} == 6
Requires: ruby(abi) = 1.8
%else
Requires: ruby(release)
%endif
%if 0%{?fedora}
BuildRequires: rubygems-devel
%endif
BuildRequires: rubygems
%if 0%{?fedora} > 16
BuildRequires: rubygem-rspec
%endif
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
RC4 is a pure Ruby implementation of the RC4 algorithm.

%package doc
BuildArch:  noarch
Requires:   %{name} = %{version}-%{release}
Summary:    Documentation for rubygem-%{gem_name}

%description doc
This package contains documentation for rubygem-%{gem_name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build

# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install
rm -rf ./%{gem_dir}/gems/%{gem_name}-%{version}/.yardoc

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/
rm %{buildroot}%{gem_instdir}/{README.md,LICENSE}

%check
%if 0%{?fedora} > 16
pushd .%{gem_instdir}
rspec spec/
popd
%endif

%files
%dir %{gem_instdir}
%{gem_instdir}/lib
%{gem_cache}
%{gem_spec}
%doc LICENSE

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%doc README.md
%{gem_instdir}/spec

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.1.5-10
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Miroslav Suchý <msuchy@redhat.com> - 0.1.5-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 15 2012 Miroslav Suchý <msuchy@redhat.com> 0.1.5-4
- do not run test on Fedora 16 and el6 (msuchy@redhat.com)

* Wed Aug 15 2012 Miroslav Suchý <msuchy@redhat.com> 0.1.5-3
- 845819 - run test suite in instdir (msuchy@redhat.com)

* Thu Aug 09 2012 Miroslav Suchý <msuchy@redhat.com> 0.1.5-2
- use test suite (msuchy@redhat.com)
- edit spec for Fedora review (msuchy@redhat.com)

* Sun Aug 05 2012 Miroslav Suchý <msuchy@redhat.com> 0.1.5-1
- new package built with tito


