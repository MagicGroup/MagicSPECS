# Generated from ethon-0.5.10.gem by gem2rpm -*- rpm-spec -*-
%global gem_name ethon

Name: rubygem-%{gem_name}
Version: 0.7.4
Release: 3%{?dist}
Summary: Libcurl wrapper
Group: Development/Languages
License: MIT
URL: https://github.com/typhoeus/ethon
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel >= 1.3.6
BuildRequires: ruby
BuildRequires: rubygem(rspec) < 3
BuildRequires: rubygem(ffi) => 1.3.0
BuildRequires: rubygem(mime-types) => 1.18
BuildRequires: rubygem(rack)
BuildRequires: rubygem(sinatra)
BuildArch: noarch

%description
Very lightweight libcurl wrapper.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

sed -i "/#!\/usr\/bin\/env/d" %{buildroot}/%{gem_instdir}/spec/support/server.rb

%check
pushd .%{gem_instdir}
# Don't use Bundler.
sed -i -e "/require 'bundler'/ s/^/#/" \
       -e "/Bundler.setup/ s/^/#/" \
       spec/spec_helper.rb

# Not sure why this triggers NoMethodError, but it does nothing usefull anyway.
sed -i '/skip/ s/^/#/' spec/ethon/multi/operations_spec.rb

rspec2 spec
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Guardfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/ethon.gemspec
%{gem_instdir}/profile
%{gem_instdir}/spec

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.7.4-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.7.4-2
- 为 Magic 3.0 重建

* Wed Jun 24 2015 Vít Ondruch <vondruch@redhat.com> - 0.7.4-1
- Update to Ethon 0.7.4.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Vít Ondruch <vondruch@redhat.com> - 0.7.0-1
- Update to Ethon 0.7.0.

* Wed Aug 14 2013 Vít Ondruch <vondruch@redhat.com> - 0.5.10-3
- Fix test suite failure when running against curl 7.30.0.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Vít Ondruch <vondruch@redhat.com> - 0.5.10-1
- Initial package
