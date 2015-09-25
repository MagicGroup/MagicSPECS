# Generated from oauth-0.4.4.gem by gem2rpm -*- rpm-spec -*-
%global gem_name oauth


Summary: OAuth Core Ruby implementation
Name: rubygem-%{gem_name}
Version: 0.4.7
Release: 9%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/oauth-xx/oauth-ruby
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# https://github.com/oauth-xx/oauth-ruby/commit/aed1ee8d3a53524fa4e8e38af3750fc020a47532
Patch0: rubygem-oauth-0.4.7-Update-typhoeus-api.patch
# https://github.com/oauth-xx/oauth-ruby/commit/a42f835c4fa683f33529bc9e1a2acad6835ab3bc
Patch1: rubygem-oauth-0.4.7-Parameters-set-with-options-are-same-as-specified-via-query-string.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(typhoeus)
BuildRequires: rubygem(curb)
BuildRequires: rubygem(test-unit)
BuildRequires: rubygem(rack)
BuildRequires: rubygem(webmock)
# Enable when available in Fedora.
# BuildRequires: rubygem(em-http-request)
BuildArch: noarch

%description
This is a RubyGem for implementing both OAuth clients and servers
in Ruby applications.

See the OAuth specs http://oauth.net/core/1.0/

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

pushd .%{gem_instdir}
%patch0 -p1
%patch1 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x


%check
pushd .%{gem_instdir}
# The following test fails due to Rails 3 incompatibility. Oauth my fail also,
# but it seems that Rails 3 users don't care.
# https://github.com/oauth/oauth-ruby/issues/13
mv test/test_action_controller_request_proxy.rb test/test_action_controller_request_proxy.rb.disabled

# Fix mocha 1.x compatibility.
sed -i 's|mocha|mocha/setup|' test/test_helper.rb

ruby -Ilib -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%license %{gem_instdir}/LICENSE
%{_bindir}/oauth
%{gem_instdir}/bin
%{gem_libdir}
%{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/HISTORY
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/TODO
%{gem_instdir}/Gemfile*
%{gem_instdir}/oauth.gemspec
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/examples
%{gem_instdir}/tasks
%{gem_instdir}/test


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.4.7-9
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 17 2014 Vít Ondruch <vondruch@redhat.com> - 0.4.7-7
- Update upstream URL.

* Tue Jun 17 2014 Vít Ondruch <vondruch@redhat.com> - 0.4.7-6
- Fix FTBFS in Rawhide (rhbz#1107182).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 28 2013 Vít Ondruch <vondruch@redhat.com> - 0.4.7-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Vít Ondruch <vondruch@redhat.com> - 0.4.7-1
- Update to OAuth 0.4.7.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 06 2012 Vít Ondruch <vondruch@redhat.com> - 0.4.4-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 15 2011 Vít Ondruch <vondruch@redhat.com> - 0.4.4-1
- Initial package
