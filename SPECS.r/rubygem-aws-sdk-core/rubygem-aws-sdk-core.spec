%global gem_name aws-sdk-core

# rspec 3 required
%if 0%{?fedora} && 0%{?fedora} <= 21 || 0%{?rhel} && 0%{?rhel} <= 7
%global use_tests 0
%else
%global use_tests 1
%endif

Name:           rubygem-%{gem_name}
Version:        2.1.13
Release:        4%{?dist}
Summary:        AWS SDK for Ruby - Core

Group:          Development/Languages
License:        ASL 2.0
URL:            http://github.com/aws/aws-sdk-ruby
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem
# gem_name='aws-sdk-core'
# version='2.1.13'
# git clone https://github.com/aws/aws-sdk-ruby && cd aws-sdk-ruby/${gem_name}
# git checkout v${version}
# cp -p ../LICENSE.txt ../NOTICE.txt ../README.md .
# tar -czf rubygem-${gem_name}-${version}-repo.tgz features/ spec/ LICENSE.txt NOTICE.txt README.md
Source1:        rubygem-%{gem_name}-%{version}-repo.tgz
# https://github.com/aws/aws-sdk-core-ruby/pull/116
# (rejected by upstream)
Source2:        awsv2.rb.1
Patch0:         %{name}-test-plugin.diff
Patch1:         %{name}-help.diff

BuildArch:      noarch
BuildRequires:  rubygems-devel
%if 0%{?use_tests}
BuildRequires:  rubygem(builder) => 3.0
BuildRequires:  rubygem(builder) < 4
BuildRequires:  rubygem(jmespath) >= 1.0
BuildRequires:  rubygem(jmespath) < 2
BuildRequires:  rubygem(rspec) >= 3
BuildRequires:  rubygem(simplecov)
BuildRequires:  rubygem(webmock)
%endif
Requires:       ca-certificates
%if 0%{?rhel} && 0%{?rhel} <= 7
Requires:       ruby(rubygems)
Requires:       rubygem(builder) => 3.0
Requires:       rubygem(builder) < 4
Requires:       rubygem(jmespath) >= 1.0
Requires:       rubygem(jmespath) < 2
Provides:       rubygem(%{gem_name}) = %{version}
%endif

%description
Provides API clients for AWS. This gem is part of the official AWS SDK for
Ruby.


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
%patch0 -p2
%patch1 -p2

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec


%build
gem build %{gem_name}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

mv %{buildroot}%{_bindir}/aws.rb %{buildroot}%{_bindir}/awsv2.rb

cp -a LICENSE.txt NOTICE.txt README.md %{buildroot}%{gem_instdir}/

mkdir -p %{buildroot}%{_mandir}/man1
install -p -m 0644 %{SOURCE2} %{buildroot}%{_mandir}/man1/

# no bundled CAs (even it is not used by default)
rm -f %{buildroot}%{gem_instdir}/ca-bundle.crt
ln -s /etc/ssl/certs/ca-bundle.crt %{buildroot}%{gem_instdir}/


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
%{_bindir}/awsv2.rb
%{_mandir}/man1/awsv2.rb.1*
%{gem_instdir}/apis/
%{gem_instdir}/bin/
%{gem_libdir}/
%{gem_spec}
%{gem_instdir}/ca-bundle.crt
%{gem_instdir}/endpoints.json
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
- Update to 2.1.13
- Add NOTICE.txt file
- Minor packaging updates

* Sun Aug 02 2015 František Dvořák <valtri@civ.zcu.cz> - 2.1.11-1
- Update to 2.1.11
- Use CA certificates bundle from the system
- Remove multi_xml, multi_json dependencies

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 17 2015 František Dvořák <valtri@civ.zcu.cz> - 2.0.24-1
- Update to 2.0.24

* Wed Feb 11 2015 František Dvořák <valtri@civ.zcu.cz> - 2.0.23-1
- Update to 2.0.23

* Fri Feb 06 2015 František Dvořák <valtri@civ.zcu.cz> - 2.0.22-1
- Update to 2.0.22

* Thu Feb 05 2015 František Dvořák <valtri@civ.zcu.cz> - 2.0.21-1
- Update to 2.0.21

* Fri Dec 05 2014 František Dvořák <valtri@civ.zcu.cz> - 2.0.12-1
- Initial package
