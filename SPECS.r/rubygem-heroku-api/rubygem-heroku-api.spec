# Generated from heroku-api-0.2.6.gem by gem2rpm -*- rpm-spec -*-
%global gem_name heroku-api

Name: rubygem-%{gem_name}
Version: 0.3.23
Release: 2%{?dist}
Summary: Ruby Client for the Heroku API
Group: Development/Languages
License: MIT
URL: http://github.com/heroku/heroku.rb
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(excon)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(multi_json)
BuildArch: noarch

%description
Ruby Client for the Heroku API.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# https://github.com/heroku/heroku.rb/pull/92
chmod a-x %{buildroot}%{gem_instdir}/README.md

%check
pushd .%{gem_instdir}
ruby -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd


%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%doc %{gem_instdir}/README.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/changelog.txt
%{gem_instdir}/heroku-api.gemspec
%{gem_instdir}/test

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 27 2015 Vít Ondruch <vondruch@redhat.com> - 0.3.23-1
- Update to heroku-api 0.3.23.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Vít Ondruch <vondruch@redhat.com> - 0.3.18-2
- OkJson is not bundled anymore.

* Mon May 26 2014 Vít Ondruch <vondruch@redhat.com> - 0.3.18-1
- Update to heroku-api 0.3.18.

* Wed Oct 09 2013 Josef Stribny <jstribny@redhat.com> - 0.3.15-1
- Update to heroku-api 0.3.15.
- Patch the test suite to work with minitest 4.7.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 17 2013 Josef Stribny <jstribny@redhat.com> - 0.3.10-1
- Update to heroku-api 0.3.10

* Fri Mar 08 2013 Vít Ondruch <vondruch@redhat.com> - 0.3.6-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 12 2012 Vít Ondruch <vondruch@redhat.com> - 0.3.6-1
- Update to heroku-api 0.3.6.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Vít Ondruch <vondruch@redhat.com> - 0.2.6-2
- Provides for bundled OkJson.

* Fri Jun 22 2012 Vít Ondruch <vondruch@redhat.com> - 0.2.6-1
- Initial package
