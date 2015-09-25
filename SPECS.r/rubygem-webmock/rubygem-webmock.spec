# Generated from webmock-1.7.6.gem by gem2rpm -*- rpm-spec -*-
%global gem_name webmock

Name: rubygem-%{gem_name}
Version: 1.21.0
Release: 2%{?dist}
Summary: Library for stubbing HTTP requests in Ruby
Group: Development/Languages
License: MIT
URL: http://github.com/bblimke/webmock
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(addressable)
BuildRequires: rubygem(crack)
BuildRequires: rubygem(curb)
BuildRequires: rubygem(excon)
BuildRequires: rubygem(httpclient)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(rack)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(test-unit)
BuildRequires: rubygem(typhoeus)
BuildArch: noarch

%description
WebMock allows stubbing HTTP requests and setting expectations on HTTP
requests.


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

pushd %{buildroot}%{gem_instdir}
sed -i s-/usr/bin/env\ rake-/usr/bin/rake- Rakefile
rm  .travis.yml .rspec-tm .gitignore .gemtest
popd



# Run the test suite
%check
pushd .%{gem_instdir}
ruby -e 'Dir.glob "./minitest/**/*.rb", &method(:require)'
ruby -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'

# rubygem-{patron,em-http-request,http} are not in Fedora yet.
sed -i '/patron/ s/^/#/' spec/spec_helper.rb
sed -i '/em-http/ s/^/#/' spec/spec_helper.rb

# and we don't care about code quality, that's upstream business.
rspec spec --exclude-pattern 'spec/{quality_spec.rb,acceptance/{patron,http_rb,em_http_request}/*}'

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
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/minitest
%{gem_instdir}/spec
%{gem_instdir}/test
%{gem_instdir}/webmock.gemspec

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.21.0-2
- 为 Magic 3.0 重建

* Tue Sep 01 2015 Vít Ondruch <vondruch@redhat.com> - 1.21.0-1
- Updated to webmock 1.21.0.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 21 2014 Mo Morsi <mmorsi@redhat.com> - 1.17.1-1
- Update to version 1.17.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 1.9.0-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Mo Morsi <mmorsi@redhat.com> - 1.9.0-1
- Updated to webmock 1.9.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 02 2012 Vít Ondruch <vondruch@redhat.com> - 1.8.7-1
- Updated to webmock 1.8.7.

* Mon Feb 13 2012 Mo Morsi <mmorsi@redhat.com> - 1.7.10-1
- Update to latest upstream release
- Build against ruby 1.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 03 2011 Mo Morsi <mmorsi@redhat.com> - 1.7.6-2
- Update to conform to guidelines

* Wed Sep 28 2011 Mo Morsi <mmorsi@redhat.com> - 1.7.6-1
- Initial package
