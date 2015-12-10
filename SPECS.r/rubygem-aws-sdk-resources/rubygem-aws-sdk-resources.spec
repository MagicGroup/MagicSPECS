%global gem_name aws-sdk-resources

# rspec 3 required
%if 0%{?fedora} && 0%{?fedora} <= 21 || 0%{?rhel} && 0%{?rhel} <= 7
%global use_tests 0
%else
%global use_tests 1
%endif

Name:           rubygem-%{gem_name}
Version:        2.1.13
Release:        4%{?dist}
Summary:        AWS SDK for Ruby - Resources

Group:          Development/Languages
License:        ASL 2.0
URL:            http://github.com/aws/aws-sdk-ruby
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
# gem_name='aws-sdk-resources'
# version='2.1.13'
# git clone https://github.com/aws/aws-sdk-ruby && cd aws-sdk-ruby/${gem_name}
# git checkout v${version}
# cp -p ../LICENSE.txt ../NOTICE.txt ../README.md .
# tar -czf rubygem-${gem_name}-${version}-repo.tgz features/ spec/ LICENSE.txt NOTICE.txt README.md
Source1:        rubygem-%{gem_name}-%{version}-repo.tgz

BuildArch:      noarch
BuildRequires:  rubygems-devel
%if 0%{?use_tests}
BuildRequires:  rubygem(aws-sdk-core) = %{version}
BuildRequires:  rubygem(rspec) >= 3
BuildRequires:  rubygem(simplecov)
BuildRequires:  rubygem(webmock)
%endif
%if 0%{?rhel} && 0%{?rhel} <= 7
Requires:       ruby(rubygems)
Requires:       rubygem(aws-sdk-core) = %{version}
Provides:       rubygem(%{gem_name}) = %{version}
%endif

%description
Provides resource oriented interfaces and other higher-level abstractions for
many AWS services. This gem is part of the official AWS SDK for Ruby.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for %{name}.


%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n %{gem_name}-%{version} -a 1

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec


%build
gem build %{gem_name}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

cp -a LICENSE.txt NOTICE.txt README.md %{buildroot}%{gem_instdir}/


%check
%if 0%{?use_tests}
cp -a features/ spec/ .%{gem_instdir}/
pushd .%{gem_instdir}
rspec -Ilib spec
rm -rf features/ spec/
popd
%endif


%files
%license %{gem_instdir}/LICENSE.txt
%license %{gem_instdir}/NOTICE.txt
%doc %{gem_instdir}/README.md
%dir %{gem_instdir}/
%{gem_libdir}/
%{gem_spec}
%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}/


%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 2.1.13-4
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.1.13-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.1.13-2
- 为 Magic 3.0 重建

* Mon Aug 10 2015 František Dvořák <valtri@civ.zcu.cz> - 2.1.13-1
- Initial package
